import os

config = {}

if os.getenv('DEBUG', "true").lower() == "true":
    config['DEBUG'] = True
    config['HOST'] = 'localhost'
    config['PORT'] = 5000
    config['ACLIMATE_API_BASE_URL'] = 'https://webapi.aclimate.org/api/'
    config['OLLAMA_MODEL'] = 'llama3.3'
    config['OLLAMA_API_URL'] = "http://192.168.199.91:11434/api/generate"
else:
    config['DEBUG'] = False
    config['HOST'] = '0.0.0.0'
    config['PORT'] = os.getenv('PORT')
    config['ACLIMATE_API_BASE_URL'] = os.getenv('ACLIMATE_API_BASE_URL')
    config['OLLAMA_MODEL'] = os.getenv('OLLAMA_MODEL')
    config['OLLAMA_API_URL'] =  os.getenv('OLLAMA_API_URL')



