import os,json
import time,subprocess
from openai import OpenAI

keyy = str(input('Api key: '))
prompt = os.path.join(os.getcwd(),'prompt','Prompt_v1.txt')


def Json_cleaning(Your_json):
    a = Your_json.replace("\n"," ")
    b = json.loads(a)
    c = str(b["To customer"]).replace("\n"," ")
    return c

def extract_server_command(Your_json):
    try:
        a = Your_json.replace("\n"," ")
        b = json.loads(a)
        if "To server" in b:
            return str(b["To server"]).strip()
        return ""
    except:
        return ""

def execute_server_command(command):
    if not command:
        return
    
    if command.startswith("+add") or command.startswith("+Remove") or command.startswith("+finish") or command.startswith("+clear"):
        order_file = os.path.join("Server", "AI_order_command.txt")
        
        if not os.path.exists("Server"):
            os.makedirs("Server")
        
        command = command.replace('/','\n')
            
        with open(order_file, 'w') as f:
            f.write(f'{command}')
        
        print(f"Server command received: {command}")
    


class OpenAICLI:
    def __init__(self):
        self.client = OpenAI(api_key=keyy, base_url="https://api.deepseek.com")
        if not self.client.api_key:
            raise ValueError("Please set OPENAI_API_KEY environment variable")

        # Customizable settings
        self.system_prompt = prompt
        self.user_prompt = "Customer: "
        self.ai_prompt = "Assistant: "
        self.temperature = 0.4
        self.model = "deepseek-chat"

        # Initialize conversation history
        self.conversation_history = []
        if self.system_prompt:
            self.conversation_history.append({
                "role": "system",
                "content": self.system_prompt
            })

    def chat(self):
        print("OpenAI CLI - Type 'exit' to end the conversation")
        
        while True:
                user_input = input(f"\n{self.user_prompt}")
                if user_input.lower() in ['exit', 'quit']:
                    break
                
                self.conversation_history.append({"role": "user", "content": user_input})
                
                # Time the API response
                start_time = time.time()
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.conversation_history,
                    temperature=self.temperature,
                )

                elapsed_time = time.time() - start_time
                
                ai_response = response.choices[0].message.content
                print(f"\n{self.ai_prompt} ({elapsed_time:.2f}s): {ai_response}")
                y = Json_cleaning(ai_response)
                
                server_command = extract_server_command(ai_response)
                execute_server_command(server_command)
                
                self.conversation_history.append({
                    "role": "assistant",
                    "content": ai_response
                })
                

if __name__ == "__main__":
    try:
        subprocess.Popen(['start', 'python', 'Cashier.py'], shell=True)

        cli = OpenAICLI()
        cli.chat()
    except ValueError as e:
        print(e)