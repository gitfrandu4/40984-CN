import os
import time
import boto3

sqs_client = boto3.client('sqs', region_name=os.environ.get("AWS_REGION", "us-east-1"))

QUEUE_A_TO_B_URL = os.environ.get("QUEUE_A_TO_B_URL")
QUEUE_B_TO_C_URL = os.environ.get("QUEUE_B_TO_C_URL")

def process_message_b(dataB):
    print("[fB] Procesando:", dataB)
    time.sleep(3)
    return dataB + "B"

def main_loop():
    """ Bucle infinito que hace polling de la cola A->B """
    while True:
        messages = sqs_client.receive_message(
            QueueUrl=QUEUE_A_TO_B_URL,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10  # Long Polling
        )
        if "Messages" in messages:
            for msg in messages["Messages"]:
                body = msg["Body"]
                output_data = process_message_b(body)
                
                # Enviar el resultado a la cola B->C
                print("[fB] Enviando a SQS (QueueBtoC):", output_data)
                sqs_client.send_message(
                    QueueUrl=QUEUE_B_TO_C_URL,
                    MessageBody=output_data
                )
                
                # Borrar el mensaje de la cola A->B
                sqs_client.delete_message(
                    QueueUrl=QUEUE_A_TO_B_URL,
                    ReceiptHandle=msg["ReceiptHandle"]
        )
        time.sleep(2)  # Espera antes de seguir el polling

if __name__ == "__main__":
    main_loop()
