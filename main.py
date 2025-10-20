import deepseek,subprocess
from openai import OpenAI

key1 = str(input('LLM Api key: '))
key2 = str(input('ASR Api key: '))


deepseek_api = OpenAI(api_key=key1, base_url="https://api.deepseek.com")
asr_api = OpenAI(api_key=key2,base_url="https://api.opentyphoon.ai/v1")

subprocess.Popen(['start', 'python', 'Cashier.py'], shell=True)

cli = deepseek.OpenAICLI(deepseek_api=deepseek_api,asr_api=asr_api)   
cli.chat()