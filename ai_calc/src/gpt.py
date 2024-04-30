import openai
import os

class GPT:
    def __init__(
            self,
            system_content="You are a helpful assistant"):
        
        self.model = "gpt-3.5-turbo"
        self.api_key = os.environ["API_KEY"]

        self.system_content = system_content

    def get_response(self, prompt):
        response = openai.ChatCompletion.create(
            api_key=self.api_key,
            model=self.model,
            messages=[{"role": "system", "content": self.system_content},
                    {"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response["choices"][0]["message"]["content"]
