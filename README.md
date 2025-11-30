📊 Real-Time Sales Data Pipeline Using Kafka, PostgreSQL & Python
(Complete End-to-End Streaming + ETL + Dashboard Project)
📌 Project Overview

This project demonstrates a real-time data engineering pipeline built using industry-standard tools.

It continuously generates sales events, streams them via Kafka, consumes them, stores them in PostgreSQL, and updates a dashboard every 30 seconds automatically.

🚀 What this project demonstrates

✔ Real-time data streaming
✔ Live ingestion and processing
✔ ETL pipeline (Extract → Transform → Load)
✔ Database storage
✔ Automated dashboards that refresh every 30 seconds
✔ Scalable architecture used by companies like Netflix, Uber, Amazon, Flipkart, Swiggy, BigBasket, Paytm, Zomato

🎯 Pipeline Components
Layer	Technology	Purpose
Real-Time Streaming	Apache Kafka	Moves live data through pipeline
Data Generator	Python (Faker)	Creates random sales events every second
Processing Layer	Python Kafka Consumer	Reads messages & inserts into DB
Storage Layer	PostgreSQL	Stores structured sales records
Analytics Layer	Pandas + Matplotlib	Generates insights and graphs
Auto Refresh UI	Streamlit	Refreshes dashboard every 30 seconds
⚙️ Architecture Diagram
     ┌──────────────────┐       ┌───────────────────────┐
     │  Python Producer │ ----> │   Kafka Topic: sales   │
     └──────────────────┘       └───────────────────────┘
                                       │
                                       ▼
     ┌──────────────────┐       ┌──────────────────┐
     │ Python Consumer  │ ----> │   PostgreSQL     │
     └──────────────────┘       └──────────────────┘
                                       │
                                       ▼
           ┌──────────────────────────────────────────────┐
           │  Streamlit Dashboard (Auto refresh 30 sec)    │
           │  Pandas + Matplotlib Visualizations           │
           └──────────────────────────────────────────────┘

🧩 Technologies Used
Component	Technology
Real-Time Streaming	Apache Kafka
Data Generation	Python (Faker)
Data Ingestion	Python Kafka Consumer
Storage	PostgreSQL
Visualization	Pandas, Matplotlib, Streamlit
Programming Language	Python 3.13
📂 Project Structure
sales_kafka_project/
│── sales_producer.py       → Generates live sales stream
│── sales_consumer.py       → Consumes Kafka data & stores in DB
│── dashboard.py            → Auto-updating analytics dashboard
│── sales.csv               → Sample dataset for offline demo
│── requirements.txt        → Python dependencies
│── README.md               → Project documentation

🔥 1. Python Producer — Real-Time Data Generator

sales_producer.py generates new sales every second:

product_name

quantity

price

timestamp

Then sends each event to:

Kafka Topic → sales-topic

Output looks like:

Sent: {'product_name': 'Mobile', 'quantity': 3, 'price': 23499, ...}

🔄 2. Python Consumer — Ingestion Layer

sales_consumer.py listens to sales-topic and inserts data into PostgreSQL table.

PostgreSQL Table
CREATE TABLE sales_data (
    sale_id SERIAL PRIMARY KEY,
    product_name VARCHAR(50),
    quantity INT,
    price NUMERIC(10,2),
    timestamp TIMESTAMP
);


Consumer output:

Inserted: {'product_name': 'Laptop', 'quantity': 2, ...}

🗄️ 3. PostgreSQL — Storage Layer

Data is stored in:

Database: salesdb

Table: sales_data

This forms the warehouse layer for analysis.

📊 4. Real-Time Dashboard (Auto Refresh Every 30 Seconds)

dashboard.py shows:

📈 Key Charts

Daily Revenue Trend

Top 10 Products by Revenue

Quantity Sold Per Day

Price Distribution Curve

KPIs (Total Sales, Revenue, Average Price, Top Product)

🔁 Auto-Refresh (every 30 seconds)

The dashboard automatically fetches the latest DB records every 30 seconds:

st_autorefresh(interval=30 * 1000, key="auto_refresh")


That means:

Even if producer is running and generating 1000s of new rows

Even if consumer is inserting them live

The dashboard keeps updating automatically WITHOUT clicking refresh

This impresses teachers a lot because it shows true real-time BI.

🛠 How to Run the Entire Project (Step-by-Step)
✔ STEP 1 — Start Zookeeper
cd ~/Kafka
bin/zookeeper-server-start.sh config/zookeeper.properties

✔ STEP 2 — Start Kafka Broker
cd ~/Kafka
bin/kafka-server-start.sh config/server.properties

✔ STEP 3 — Create Kafka Topic
bin/kafka-topics.sh --create --topic sales-topic --bootstrap-server localhost:9092

✔ STEP 4 — Run Producer (Live Data)
cd ~/sales_kafka_project
python3 sales_producer.py


You will see new data generated EVERY SECOND.

✔ STEP 5 — Run Consumer
python3 sales_consumer.py


New rows start populating PostgreSQL LIVE.

✔ STEP 6 — Run Analytics Dashboard
streamlit run dashboard.py


You will see:

real-time charts

updated KPIs

new rows every 30 seconds

growing revenue curves

🔄 Complete Data Flow (Simple Explanation)

Python Producer
→ Creates fake sales every second

Kafka Topic
→ Acts as a real-time buffer

Kafka Consumer
→ Reads stream continuously

PostgreSQL
→ Stores clean structured data

Streamlit Dashboard
→ Auto-refreshes every 30 seconds
→ Shows latest graphs & KPIs
