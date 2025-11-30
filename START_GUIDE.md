📁 1. Folder Structure

Your project folder should look like this:

sales_kafka_project/
│
├── sales_producer.py
├── sales_consumer.py
├── dashboard.py
├── config.env
├── requirements.txt
├── START_GUIDE.md   ← (this file)
└── README.md




🛠️ 2. Install Required Dependencies

Run this inside the project folder:

pip install -r requirements.txt


If you don’t have a requirements.txt yet, use:

kafka-python
psycopg2-binary
pandas
streamlit
python-dotenv
plotly

🐘 3. Start PostgreSQL

Start PostgreSQL service:

brew services start postgresql


Then check database:

psql -U YOUR_USERNAME -d salesdb


Create table if not created:

CREATE TABLE sales_data (
    id SERIAL PRIMARY KEY,
    product_name VARCHAR(50),
    quantity INT,
    price FLOAT,
    timestamp TIMESTAMP
);

🦁 4. Start Apache Kafka

Go to your Kafka folder:

cd ~/Kafka

Start Zookeeper
bin/zookeeper-server-start.sh config/zookeeper.properties


(keep this terminal open)

Start Kafka Broker

Open a new terminal:

cd ~/Kafka
bin/kafka-server-start.sh config/server.properties


(keep this terminal open)

🧵 5. Start the Kafka Producer

Open a new terminal:

cd ~/sales_kafka_project
python3 sales_producer.py


This will start generating live sales data.

You can stop it anytime using:

CTRL + C

📥 6. Start the Kafka Consumer (Database Loader)

Open a new terminal:

cd ~/sales_kafka_project
python3 sales_consumer.py


This will continuously insert data into PostgreSQL.

📊 7. Start the Real-Time Dashboard

Run:

cd ~/sales_kafka_project
streamlit run dashboard.py


It will open your dashboard in browser.

Dashboard refreshes live every 30 seconds.

✔️ 8. Complete Data Pipeline (Summary)
sales_producer.py 
      → Kafka Topic (sales-topic) 
            → sales_consumer.py 
                  → PostgreSQL (salesdb.sales_data)
                         → dashboard.py (Streamlit)


This is a full real-time ETL pipeline using Kafka.

🛑 9. How to Stop Everything

Stop producer → CTRL + C
Stop consumer → CTRL + C
Stop dashboard → CTRL + C

Stop Kafka:

CTRL + C   (in both terminals)


Stop PostgreSQL:

brew services stop postgresql
