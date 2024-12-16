# fC.py
import os
import time
import boto3

sqs_client = boto3.client('sqs', region_name=os.environ.get("AWS_REGION", "us-east-1"))

QUEUE_B_TO_C_URL = os.environ.get("QUEUE_B_TO_C_URL")

def process_message_c(dataC):
    print("[fC] Procesando:", dataC)
    time.sleep(4)
    return dataC + "C"

def main_loop():
    """ Bucle infinito que hace polling de la cola B->C """
    while True:
        messages = sqs_client.receive_message(
            QueueUrl=QUEUE_B_TO_C_URL,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10  # Long Polling
        )
        if "Messages" in messages:
            for msg in messages["Messages"]:
                body = msg["Body"]
                output_data = process_message_c(body)
                
                # Aquí podríamos almacenar el resultado en una base de datos
                print("[fC] Resultado final:", output_data)
                
                # Borrar el mensaje de la cola B->C
                sqs_client.delete_message(
                    QueueUrl=QUEUE_B_TO_C_URL,
                    ReceiptHandle=msg["ReceiptHandle"]
                )
        time.sleep(2)

if __name__ == "__main__":
    main_loop()
