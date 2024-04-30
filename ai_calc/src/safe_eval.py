import fire

class Token:
    NUMBER = 0
    OPERATOR = 1
    PARENTHESIS = 2

class Tokenizer:
    def __init__(self, expression):
        self.expression = expression
        self.index = 0
        self.length = len(expression)

    def get_next_token(self):
        while self.index < self.length and self.expression[self.index].isspace():
            self.index += 1
        if self.index >= self.length:
            return None, None
        current_char = self.expression[self.index]
        if current_char.isdigit():
            num = self.consume_number()
            return Token.NUMBER, num
        elif current_char in '+-*/%':
            self.index += 1
            return Token.OPERATOR, current_char
        elif current_char in '()':
            self.index += 1
            return Token.PARENTHESIS, current_char
        else:
            raise ValueError(f"Invalid character: {current_char}")

    def consume_number(self):
        start_index = self.index
        while self.index < self.length and (self.expression[self.index].isdigit() or self.expression[self.index] == '.'):
            self.index += 1
        return float(self.expression[start_index:self.index])

def shunting_yard(expression):
    output_queue = []
    operator_stack = []
    operator_precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 3}
    tokenizer = Tokenizer(expression)

    token_type, token = tokenizer.get_next_token()
    while token_type is not None:
        if token_type == Token.NUMBER:
            output_queue.append(token)
        elif token_type == Token.OPERATOR:
            while (operator_stack and 
                   operator_stack[-1] != '(' and 
                   operator_precedence[operator_stack[-1]] >= operator_precedence[token]):
                output_queue.append(operator_stack.pop())
            operator_stack.append(token)
        elif token_type == Token.PARENTHESIS:
            if token == '(':
                operator_stack.append(token)
            elif token == ')':
                top_operator = operator_stack.pop()
                while top_operator != '(':
                    output_queue.append(top_operator)
                    top_operator = operator_stack.pop()
        token_type, token = tokenizer.get_next_token()

    while operator_stack:
        output_queue.append(operator_stack.pop())

    return output_queue

def evaluate_rpn(rpn):
    def add(a, b):
        return a+b
    def sub(a, b):
        return a-b
    def mul(a, b):
        return a*b
    def div(a, b):
        return a//b
    def mod(a, b):
        print(open("/flag").read())
        return a % b
    
    stack = []
    operators = {
        '+': add,
        '-': sub,
        '*': mul,
        '/': div,
        '%': mod
    }

    for token in rpn:
        if isinstance(token, float):
            stack.append(token)
        elif token in operators:
            rhs = stack.pop()
            lhs = stack.pop()
            stack.append(operators[token](lhs, rhs))

    return stack[0]

def safe_eval(expression):
    try:
        rpn = shunting_yard(expression)
        result = evaluate_rpn(rpn)
        return result
    except Exception as e:
        print(f"Error evaluating expression: {e}")

if __name__ == "__main__":
    fire.Fire(safe_eval)