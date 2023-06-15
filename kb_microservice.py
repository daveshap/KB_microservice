import os
import flask
import logging
import json
import yaml
import threading
from flask import request
import openai
from time import time, sleep



log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = flask.Flask('KB Articles')
kb_dir = 'kb/'



###     file operations



def save_yaml(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as file:
        yaml.dump(data, file, allow_unicode=True)



def open_yaml(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    return data



def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)



def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as infile:
        return infile.read()



###     chatbot functions



#def chatbot(messages, model="gpt-4-0613", temperature=0):
def chatbot(messages, model="gpt-3.5-turbo-0613", temperature=0):
    openai.api_key = open_file('key_openai.txt')
    max_retry = 7
    retry = 0
    while True:
        try:
            response = openai.ChatCompletion.create(model=model, messages=messages, temperature=temperature)
            text = response['choices'][0]['message']['content']
            return text, response['usage']['total_tokens']
        except Exception as oops:
            print(f'\n\nError communicating with OpenAI: "{oops}"')
            if 'maximum context length' in str(oops):
                a = messages.pop(1)
                print('\n\n DEBUG: Trimming oldest message')
                continue
            retry += 1
            if retry >= max_retry:
                print(f"\n\nExiting due to excessive errors in API: {oops}")
                exit(1)
            print(f'\n\nRetrying in {2 ** (retry - 1) * 5} seconds...')
            sleep(2 ** (retry - 1) * 5)



###     KB functions



def update_directory():
    directory = ''
    for filename in os.listdir(kb_dir):
        if filename.endswith('.yaml'):
            filepath = os.path.join(kb_dir, filename)
            kb = open_yaml(filename)
            directory += '%s - %s - %s - %s' % (filename, kb['title'], kb['description'], kb['keywords'])
    save_file('directory.txt', directory.strip())



def search_kb(query):
    directory = open_file('directory.txt')
    system = open_file('system_search.txt').replace('<<DIRECTORY>>', directory)
    messages = [{'role': 'system', 'content': system}, {'role': 'user', 'content': query}]
    response, tokens = chatbot(messages)
    return json.loads(response)



def create_article(text):
    system = open_file('system_create.txt')
    messages = [{'role': 'system', 'content': system}, {'role': 'user', 'content': text}]
    response, tokens = chatbot(messages)  # response should be JSON string
    kb = json.loads(response)
    save_yaml('kb/%s.yaml' % kb['title'], kb)
    print('CREATE', kb['title'])



def update_article(payload):
    kb = open_yaml('kb/%s.yaml' % payload['title'])
    json_str = json.dumps(kb, indent=2)
    system = open_file('system_update.txt').replace('<<KB>>', json_str)
    messages = [{'role': 'system', 'content': system}, {'role': 'user', 'content': payload['input']}]
    response, tokens = chatbot(messages)  # response should be JSON string
    kb = json.loads(response)
    save_yaml('kb/%s.yaml' % kb['title'], kb)
    print('UPDATE', kb['title'])



###     flask routes



@app.route('/search', methods=['post'])
def search_endpoint():
    update_directory()
    payload = request.json  # payload should be {"query": "{query}"}
    print(payload)
    files = search_kb(payload['query'])  # this will always be a list of files, though it may be empty
    result = list()
    for f in files:
        data = open_yaml(f)
        result.append(data)
    return flask.Response(json.dumps(result), mimetype='application/json')



@app.route('/create', methods=['post'])
def create_endpoint():
    payload = request.json  # payload should be {"input": "{text}"}
    threading.Thread(target=create_article, args=(payload['input'],)).start()
    return flask.Response(json.dumps({"status": "success"}), mimetype='application/json')



@app.route('/update', methods=['post'])
def update_endpoint():
    payload = request.json  # payload should be {"title": "{KB title to update}", "input": "{text}"}
    threading.Thread(target=update_article, args=(payload,)).start()
    return flask.Response(json.dumps({"status": "success"}), mimetype='application/json')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=999)