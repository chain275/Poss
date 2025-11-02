import deepseek,subprocess,threading,deepseek_ui,real_ui
from openai import OpenAI
import tkinter as tk 

key1 = str(input('LLM Api key: '))
key2 = str(input('ASR Api key: '))


deepseek_api = OpenAI(api_key=key1, base_url="https://api.deepseek.com")
asr_api = OpenAI(api_key=key2,base_url="https://api.opentyphoon.ai/v1")

subprocess.Popen(['start', 'python', 'Cashier.py'], shell=True)

def tran_ui():
    root = tk.Tk()
    app = real_ui.OrderDisplayApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

def realui():
    root = tk.Tk()
    app = deepseek_ui.OrderDisplayApp(root)
    root.mainloop()

thread1 = threading.Thread(target=tran_ui)
thread2 = threading.Thread(target=realui)

thread1.start()
thread2.start()

cli = deepseek.OpenAICLI(deepseek_api=deepseek_api,asr_api=asr_api)   
cli.chat()