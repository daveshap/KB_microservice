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
            kb_articles.append(kb_article)
            directory += '%s - %s - %s' % (filename, kb_article['title'], kb_article['description'])
    save_file('directory.txt', directory.strip())



def search_kb(query):
    directory = open_file('directory.txt')
    system = open_file('system_search.txt').replace('<<DIRECTORY>>', directory)
    messages = [{'role': 'system', 'content': system}, {'role': 'user', 'content': query}]
    response, tokens = chatbot(messages, model='gpt-3.5-turbo-0613')
    return json.loads(response)



def create_article(payload):
    # TODO: Implement the logic to create a new KB article based on the payload
    pass



def update_article(payload):
    # TODO: Implement the logic to update a KB article based on the payload
    pass



###     flask routes



@app.route('/search', methods=['post'])
def search_endpoint():
    update_directory()
    payload = request.json  # payload should just be string
    print(payload)
    files = search_kb(payload)  # this will always be a list, though it may be empty
    result = list()
    for f in files
        data = open_yaml(f)
        result.append(data)
    return flask.Response(json.dumps(result), mimetype='application/json')



@app.route('/create', methods=['post'])
def create_endpoint():
    payload = request.json
    threading.Thread(target=create_article, args=(payload,)).start()
    return flask.Response(json.dumps({"status": "success"}), mimetype='application/json')



@app.route('/update', methods=['post'])
def update_endpoint():
    payload = request.json
    threading.Thread(target=update_article, args=(payload,)).start()
    return flask.Response(json.dumps({"status": "success"}), mimetype='application/json')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=999)