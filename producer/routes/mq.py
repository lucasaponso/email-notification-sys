from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from fastapi import HTTPException, Depends
from pydantic import BaseModel
import pika
from constants import QUEUE_NAME, RABBITMQ_HOST

router = APIRouter(prefix="/mq")

"""
The following class relates to 
the content being sent to the rabbit_mq.
"""
class mq_msg(BaseModel):
    msg: str

def get_rabbitmq_channel():
    """
    The following function returns a valid channel connection.
    For the send message to use.
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    return connection, channel

@router.post("/send")
def send_message(msg: mq_msg, channel_dep = Depends(get_rabbitmq_channel)):
    """
    The following function sends a message to the 
    MQ_RABBIT server.
    """
    connection, channel = channel_dep

    try:
        channel.basic_publish(
            exchange='',
            routing_key=QUEUE_NAME,
            body=msg.msg,
            properties=pika.BasicProperties(delivery_mode=2)
        )

        connection.close()
        return {"status": "Message sent"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))