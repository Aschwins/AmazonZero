from flask import Flask, request, json
app = Flask(__name__)
@app.route('/', methods=['POST', 'GET'])
def index():    
    # Parse request body for model input
    return json.dumps("hello")
if __name__ == '__main__':    
    # listen on all IPs 
    app.run(host='0.0.0.0')