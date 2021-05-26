from flask import Flask, request, json
from amazonzero.test import hello_world
app = Flask(__name__)
@app.route('/', methods=['POST', 'GET'])
def index():
    a = hello_world()
    return json.dumps(a)
if __name__ == '__main__':    
    # listen on all IPs 
    app.run(host='0.0.0.0')