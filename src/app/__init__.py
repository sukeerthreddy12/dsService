from flask import Flask
from flask import request, jsonify
from service.messageService import MessageService
from kafka import KafkaProducer
import json

app = Flask(__name__)
app.config.from_pyfile('config.py')
kafka_broker = app.config['KAFKA_BROKER']
kafka_topic = app.config['KAFKA_TOPIC']

messageService = None
producer = KafkaProducer(bootstrap_servers=kafka_broker,value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def getMessageService():
    global messageService
    if messageService is None:
        messageService = MessageService()
    return messageService

@app.route('/v1/ds/message' , methods=['POST'])
def handle_message():
    message = request.json.get('message')
    user_id = request.json.get('user_id')
    result = getMessageService().processMessage(message)

    if result is None:
        return jsonify({'error': 'Invalid message format'}), 400

    serialized_result = result.model_dump()
    serialized_result['user_id'] = user_id
    producer.send(kafka_topic, serialized_result)
    producer.flush()

    return jsonify({"message": "Message processed successfully"})

@app.route('/' , methods=['GET'])
def handle_get(): 
    return jsonify({"message": "Hello, World!"})


if __name__ == "__main__" : 
    app.run(host = "localhost" , port = 8010 , debug = True)

