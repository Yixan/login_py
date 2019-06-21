from kafka import KafkaProducer

def connect(msg):
    producer = KafkaProducer(bootstrap_servers=['118.24.76.130:9092', '118.24.184.203:9092', '132.232.250.82:9092'])
    future = producer.send('my-first-topic', key=b'my_key', value=bytes(msg, encoding = "utf8"))
    result = future.get(timeout=10)
    print(result)

if __name__ == '__main__':
    connect("你好")