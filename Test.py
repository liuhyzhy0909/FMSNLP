from flask import Flask, jsonify, abort, request
from NLPForFMS import SelectForFMS
app = Flask(__name__)
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

@app.route('/NLP',methods=['POST'])
def NLP():
    #ValueList = Aol.getTestValueList();
    if not request.json: #or not 'title' in request.json:
        abort(400)
    rq = SelectForFMS.fenci(SelectForFMS,request.json)

    task = rq
    #tasks.append(task)
    return jsonify({'task': task}), 201

@app.route('/<string:name>', methods=['GET'])
def hello(name):
    return "hello " + name + " !"

if __name__ == '__main__':
    #app.run()
    app.run(host='0.0.0.0',port=5000)
