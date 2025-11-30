from kafka import KafkaProducer
from faker import Faker
import json
import time
import random

fake = Faker()

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

products = ["Laptop", "Mobile", "Headphones", "Keyboard", "Mouse"]

while True:
    data = {
        "product_name": random.choice(products),
        "quantity": random.randint(1, 5),
        "price": round(random.uniform(500, 50000), 2),
        "timestamp": fake.date_time_this_year().isoformat()
    }

    producer.send("sales-topic", data)
    print("Sent:", data)

    time.sleep(1)
