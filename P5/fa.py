# fA.py
import os
import time
import boto3
from flask import Flask, request

app = Flask(__name__)
sqs_client = boto3.client('sqs', region_name=os.environ.get("AWS_REGION", "us-east-1"))

QUEUE_A_TO_B_URL = os.environ.get("QUEUE_A_TO_B_URL")

@app.route("/start", methods=["POST"])
def start_flow():
    """ Recibe un input (por ejemplo en JSON) y lo envía a la cola A->B """
    input_data = request.json.get("data", "Inicio:")
    print("[fA] Recibiendo:", input_data)
    
    # Simula un proceso pesado
    time.sleep(5)
    
    # Genera la salida
    output_data = input_data + "A"
    print("[fA] Enviando a SQS (QueueAtoB):", output_data)
    
    # Envía el resultado a la cola A->B
    sqs_client.send_message(
        QueueUrl=QUEUE_A_TO_B_URL,
        MessageBody=output_data
    )
    return {"status": "ok", "fA_output": output_data}, 200

if __name__ == "__main__":
    # Ejemplo: flask run -h 0.0.0.0 -p 5001
    app.run(host="0.0.0.0", port=5001)
