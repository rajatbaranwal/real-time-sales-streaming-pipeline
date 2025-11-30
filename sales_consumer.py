from kafka import KafkaConsumer
import psycopg2
import json

consumer = KafkaConsumer(
    'sales-topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

conn = psycopg2.connect(
    host="localhost",
    database="salesdb",
    user="rajatbaranwal",
    password=""    
)

cursor = conn.cursor()

insert_query = """
INSERT INTO sales_data (product_name, quantity, price, timestamp)
VALUES (%s, %s, %s, %s)
"""

for message in consumer:
    data = message.value

    cursor.execute(insert_query, (
        data["product_name"],
        data["quantity"],
        data["price"],
        data["timestamp"]
    ))

    conn.commit()
    print("Inserted:", data)
