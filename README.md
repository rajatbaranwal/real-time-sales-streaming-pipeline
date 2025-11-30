📊 Real-Time Sales Data Pipeline using Kafka, PostgreSQL & Python

This project demonstrates a real-time data engineering pipeline using industry-standard tools.

It continuously generates sales events, streams them via Kafka, consumes them, stores them in PostgreSQL, and updates a real-time dashboard every 30 seconds automatically.

🚀 What this project demonstrates

✔ Real-time data streaming
✔ Live ingestion + processing
✔ ETL pipeline (Extract → Transform → Load)
✔ Database storage
✔ Automated dashboards (refresh every 30 sec)
✔ Scalable system used by companies like Netflix, Uber, Amazon, Flipkart, Swiggy, Paytm

🧩 Pipeline Components
Layer	Technology	Purpose
Real-Time Streaming	Apache Kafka	Moves live data
Data Generator	Python (Faker)	Creates new sales every second
Processing Layer	Python Kafka Consumer	Reads Kafka messages & inserts into DB
Storage Layer	PostgreSQL	Stores structured sales data
Analytics Layer	Pandas + Matplotlib	Generates insights & graphs
UI Layer	Streamlit	Auto-refresh dashboard (every 30 sec)
🔥 Architecture Diagram
┌────────────────────┐       ┌─────────────────────────┐
│  Python Producer   │ ----> │   Kafka Topic: sales     │
└────────────────────┘       └─────────────────────────┘
                                  │
                                  ▼
┌────────────────────┐       ┌─────────────────────────┐
│  Python Consumer   │ ----> │      PostgreSQL          │
└────────────────────┘       └─────────────────────────┘
                                  │
                                  ▼
        ┌───────────────────────────────────────────────────┐
        │ Streamlit Dashboard (Auto-refresh every 30 sec)   │
        │ Pandas + Matplotlib Visualizations                │
        └───────────────────────────────────────────────────┘

🛠 Technologies Used
Component	Technology
Streaming	Apache Kafka
Data Generation	Python + Faker
Consumer	Python Kafka Client
Database	PostgreSQL
Visualizations	Pandas, Matplotlib, Streamlit
Language	Python 3.13
📁 Project Structure
sales_kafka_project/
│── sales_producer.py        # Real-time data generator
│── sales_consumer.py        # Kafka → PostgreSQL consumer
│── dashboard.py             # Auto-updating real-time dashboard
│── sales.csv                # Sample dataset (optional)
│── requirements.txt         # Dependencies
│── README.md                # Documentation

🔥 1. Python Producer — Real-Time Data Generator

sales_producer.py generates new sales every second:

product_name

quantity

price

timestamp

Sends each as JSON to:

➡️ Kafka Topic: sales-topic

Example:

Sent: {"product_name": "Mobile", "quantity": 3, "price": 24999, ...}

🔄 2. Python Consumer — Ingestion Layer

sales_consumer.py listens to Kafka and inserts records into PostgreSQL table:

CREATE TABLE sales_data (
    sale_id SERIAL PRIMARY KEY,
    product_name VARCHAR(50),
    quantity INT,
    price NUMERIC(10,2),
    timestamp TIMESTAMP
);


Example:

Inserted: {"product_name": "Laptop", "quantity": 2, ...}

🗄 3. PostgreSQL Storage

Data stored in:

Database: salesdb

Table: sales_data

This stores clean structured data for analysis.

📊 4. Real-Time Analytics Dashboard

Auto-refresh every 30 seconds

dashboard.py displays:

Total revenue

Total sales

Top products

Revenue over time

Quantity trends

Price distribution

Auto-refresh code:
st_autorefresh(interval=30 * 1000, key="refresh")


✔ Fetches NEW rows from PostgreSQL
✔ Updates all charts & KPIs automatically
✔ No need to reload manually

🛠 How to Run the Project
✔ Step 1 — Start Zookeeper
cd ~/Kafka
bin/zookeeper-server-start.sh config/zookeeper.properties

✔ Step 2 — Start Kafka Server
bin/kafka-server-start.sh config/server.properties

✔ Step 3 — Create Kafka Topic
bin/kafka-topics.sh --create --topic sales-topic --bootstrap-server localhost:9092

✔ Step 4 — Start Producer
python3 sales_producer.py

✔ Step 5 — Start Consumer
python3 sales_consumer.py

✔ Step 6 — Start Dashboard
streamlit run dashboard.py

🔁 Complete Flow (Simple Explanation)
Python Producer → Kafka → Python Consumer → PostgreSQL → Streamlit Dashboard


Producer: Creates fake real-time sales

Kafka: Streams the data

Consumer: Inserts into PostgreSQL

DB: Stores all sales

Dashboard: Auto-refreshes every 30 sec to show new data
