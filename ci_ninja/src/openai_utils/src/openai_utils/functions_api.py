from collections import namedtuple
import functools
import inspect
import json
import traceback
import typing
import openai
from rich import print
from difflib import SequenceMatcher

def parse_doc(doc: str):
    param_docs = {}
    return_doc = None
    real_doc = ''

    if not doc:
        return param_docs, return_doc, real_doc

    for line in doc.split('\n'):
        line = line.strip()
        if line.startswith(':param'):
            line = line[6:].strip()
            param_name, param_doc = line.split(':', maxsplit=1)
            param_docs[param_name.strip()] = param_doc.strip()
        elif line.startswith(':return:'):
            line = line[8:].strip()
            return_doc = line.strip()
        else:
            real_doc += line + '\n'

    return param_docs, return_doc, real_doc.strip()

def type_annotation_to_json_schema(type_annotation):
    if type_annotation is str:
        return {"type": "string"}
    elif type_annotation is int:
        return {"type": "integer"}
    elif type_annotation is float:
        return {"type": "number"}
    elif type_annotation is bool:
        return {"type": "boolean"}
    elif type_annotation is None:
        return {"type": "null"}

    # now handle the types from `typing`
    origin_type = typing.get_origin(type_annotation)
    if origin_type is None:
        raise ValueError(f"unsupported type annotation: {type_annotation}")

    if origin_type is dict:
        key_type, value_type = typing.get_args(type_annotation)
        assert key_type is str, f"unsupported type annotation for a JSON schema: {type_annotation}"
        return {
            "type": "object",
            "additionalProperties": type_annotation_to_json_schema(value_type),
        }
    elif origin_type is list:
        value_type, = typing.get_args(type_annotation)
        return {
            "type": "array",
            "items": type_annotation_to_json_schema(value_type),
        }
    else:
        raise ValueError(f"unsupported type annotation: {type_annotation}")


ChatGPTFunctionMetadata = namedtuple('ChatGPTFunctionMetadata', ['name', 'arg_names', 'kwarg_names'])
ChatGPTFunction = namedtuple('ChatGPTFunction', ['schema', 'metadata', 'function'])
__CHATGPT_FUNCTIONS = []
def chatgpt_function(function):
    '''
    A decorator that takes a python function and exposes it to the chatgpt engine.

    An example of such a translation is that a function like this:
    ```
    def get_function_source(name=None):
        """
        Returns the C source code for the function named `name`. Returns None if the function is unknown or a builtin with known semantics.

        :param name: The name of the function to return the source code for.
        :return: source code for `name` or None if not found.
        """
        return FUNCTIONS.get(name, None)
    ```

    would be translated to this:
    ```
    functions.append({
        "name": "get_function_source",
        "description": "Returns the C source code for the function named `name`. Returns None if the function is unknown or a builtin with known semantics.\n# RETURN VALUE: source code for `name` or None if not found.",

        # json schema for parameters
        "parameters": {
            "type": "object",
            "required": ["name"],
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the function to return the source code for.",
                },
            },
        },
    })
    ```
    '''

    if type(function) is functools.partial:
        # code = function.func.__code__
        fname = function.func.__name__
        argcount = function.func.__code__.co_argcount
        varnames = function.func.__code__.co_varnames[:argcount][len(function.args):]
        code_flags = function.func.__code__.co_flags
        annotations = function.func.__annotations__
        defaults = function.func.__defaults__ # strip the partial'ed args
        func_doc = function.func.__doc__
    else:
        # code = function.__code__
        fname = function.__name__
        argcount = function.__code__.co_argcount
        varnames = function.__code__.co_varnames[:argcount]
        code_flags = function.__code__.co_flags
        annotations = function.__annotations__
        defaults = function.__defaults__
        func_doc = function.__doc__

    args = varnames
    if args and args[0] == 'self':
        args = args[1:]
    # we don't support *args or **kwargs
    assert code_flags & (inspect.CO_VARARGS) == 0, f"unsupported function signature: *args in {fname}"
    # assert code_flags & inspect.CO_VARKEYWORDS != 0, f"must handle **kwargs in {fname}"
    arg_types = annotations
    defaults = defaults or []
    if len(defaults) > 0:
        args, kwargs = args[:-len(defaults)], args[-len(defaults):]
    else:
        args = args
        kwargs = []

    param_docs, return_doc, function_doc = parse_doc(func_doc)
    required_args = args

    properties = {}

    for arg in args:
        arg_type = arg_types.get(arg, str)
        arg_doc = param_docs.get(arg, '')
        property = type_annotation_to_json_schema(arg_type)
        property['description'] = arg_doc
        properties[arg] = property

    for kwarg, default in zip(kwargs, defaults):
        kwarg_type = arg_types.get(kwarg, str)
        kwarg_doc = param_docs.get(kwarg, '')
        property = type_annotation_to_json_schema(kwarg_type)
        property['description'] = kwarg_doc + f"\n\n# DEFAULT: {default!r}"
        properties[kwarg] = property

    func_schema = {
        "name": fname,
        "description": f"{function_doc}\n\n# RETURN VALUE: {return_doc}",
        "parameters": {
            "type": "object",
            "required": args,
            "properties": properties,
        },
    }

    chatgpt_function_metadata = ChatGPTFunctionMetadata(fname, args, kwargs)
    chatgpt_function = ChatGPTFunction(func_schema, chatgpt_function_metadata, function)
    __CHATGPT_FUNCTIONS.append(chatgpt_function)

    function.__chatgpt_metadata__ = chatgpt_function_metadata
    function.__chatgpt_schema__ = func_schema
    function.__chatgpt_function__ = chatgpt_function

    return function

def get_chatgpt_function_schema(decorated_funcs_to_use):
    return [func.__chatgpt_schema__ for func in decorated_funcs_to_use]

def call_chatgpt_function(function_name, arguments, prompt_for_confirmation=True, available_functions=None):
    if available_functions is None:
        available_functions = [cgptf.function for cgptf in __CHATGPT_FUNCTIONS]
    for func in available_functions:
        if func.__chatgpt_metadata__.name == function_name:
            break
    else:
        return dict(role='system', content=f"ERROR: Unknown function {function_name}")

    # check if the arguments are valid
    try:
        arguments = json.loads(arguments)
    except json.JSONDecodeError as e:
        bt = traceback.format_exc()
        return dict(role='system', content=f"ERROR: Invalid JSON in the arguments: {e}\n" + bt)

    schema = func.__chatgpt_schema__
    func_name, arg_names, kwarg_names = func.__chatgpt_metadata__

    # check if the arguments are valid
    for arg in arg_names:
        if arg not in arguments:
            return dict(role='system', content=f"ERROR: Missing required argument {arg!r} for function {func_name!r}")

    for arg in arguments:
        if arg not in arg_names and arg not in kwarg_names:
            return dict(role='system', content=f"ERROR: Unknown argument {arg!r} for function {func_name!r}")

    try:
        args = [arguments[arg] for arg in arg_names]
        kwargs = {arg: arguments[arg] for arg in kwarg_names}
        if prompt_for_confirmation:
            # ask the user if this function call should be allowed
            prompt = f"Call function [bold]{func_name}[/bold] with arguments [bold]{args}[/bold] and keyword arguments [bold]{kwargs}[/bold]"
            print(prompt)

            while input("[y/n]? ").lower() != 'y':
                pass
        result = func(*args, **kwargs)
    except KeyboardInterrupt:
        return dict(role='system', content=f"ERROR: User cancelled the function call.")
    except Exception as e:
        bt = traceback.format_exc()
        return dict(role='system', content=f"ERROR while calling {func_name!r}: {e}\n" + bt)

    # do the json encoding out here, because JSON encoding errors are an application bug and SHOULD propagate out to the user
    return dict(role='function', name=func_name, content=json.dumps(result, indent=2))
