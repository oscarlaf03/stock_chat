import pika

class Publisher:
    def __init__(self,data, address='localhost'):
        self.data = data
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(address))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='main_queue', durable=True)

    def publish(self):
        self.channel.basic_publish(exchange='',routing_key='main_queue', body=str(self.data))
