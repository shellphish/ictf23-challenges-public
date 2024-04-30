from gpt import GPT
from safe_eval import safe_eval

def print_banner():
    print("*********************")
    print("*  Welcome to iCTF  *")
    print("*********************")
    print("\nTry out our novel AI-powered calculator!\n")
    print("You can describe your problem in natural language and we will do the math for you!")
    print("For example, you can ask: `If I have 100 apples and consume 2 apples daily, how long will my supply of apples last?`\n\n")

def unwrap(response):
    print(f"Got this expression from the AI: {response}")
    response = response.strip("` \n")
    if response.startswith('eval("') and response.endswith('")'):
        return response[6:-2]
    return None

def calculate(expr):
    return safe_eval(expr)

def main():
    print_banner()

    problem = input("Input your problem description: ")

    if len(problem) > 100:
        print("Your problem description is too long!")
        return
    

    system = """Use python's `eval` to solve the calculation problem.
Give me the `eval` function call without explanation.
Be careful, replace % with / instead. You should never use % in any situation.

For example, when asked "What is one plus one?", respond `eval("1+1")`.
When asked "what is 5 mod 2", respond `eval("5/2")`.
"""

    model = GPT(system)
    
    response = model.get_response(problem)

    to_eval = unwrap(response)
    if to_eval:
        ans = calculate(to_eval)
        if ans is None:
            print(f"The answer: {ans}")
            print("\nHave a great day!")
        else:
            print("The AI returned something unexpected. Please try again..")
    else:
        print("The AI returned something unexpected. Please try again.")

if __name__=="__main__":
    main()