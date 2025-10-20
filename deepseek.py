import os,json
import time,subprocess
from openai import OpenAI
from ASR import Recorder,Asr

location = os.path.join(os.getcwd(),'prompt','Prompt_v1.txt')   
recorder = Recorder.SentenceRecorder(silence_threshold=1000,pause_duration=1.75,sample_rate=44100,output_dir="recordings")

with open(location, 'r',encoding='utf-8') as file:
    prompt = file.read()

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

        command_cleaning = ''

        for i in command.split('\n'):
            command_cleaning += f'{i.strip()}\n'


            
        with open(order_file, 'w') as f:
            f.write(f'{command_cleaning}')
        
        print(f"Server command received: {command}")
    



class OpenAICLI:
    def __init__(self,deepseek_api,asr_api):
        if not os.path.exists("Server"):
            os.makedirs("Server")
        self.client = deepseek_api
        if not self.client.api_key:
            raise ValueError("Please set OPENAI_API_KEY environment variable")

        self.system_prompt = prompt
        self.user_prompt = "Customer: "
        self.ai_prompt = "Assistant: "
        self.temperature = 0.4
        self.model = "deepseek-chat"
        self.asr = asr_api
        self.response_format={
        'type': 'json_object'
        }


        self.conversation_history = []
        if self.system_prompt:
            self.conversation_history.append({
                "role": "system",
                "content": self.system_prompt
            })

    def reset(self):
        self.conversation_history = []
        if self.system_prompt:
            self.conversation_history.append({
                "role": "system",
                "content": self.system_prompt
            })

    def chat(self):
        print("OpenAI CLI - Type 'exit' to end the conversation")
        
        while True:
                transcription = Asr.transcribe_audio_file(recorder.record_continuously(),client=self.asr)
                user_input = str(transcription.text)
                if user_input == '':
                    continue
                print(f"\n{self.user_prompt}: {user_input}")
                if user_input.lower() in ['exit', 'quit']:
                    break
                
                self.conversation_history.append({"role": "user", "content": user_input})
                
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

                if server_command.startswith('+finish'):
                    self.conversation_history = []
                    if self.system_prompt:
                        self.conversation_history.append({
                            "role": "system",
                            "content": self.system_prompt
                        }) 
                else:  
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