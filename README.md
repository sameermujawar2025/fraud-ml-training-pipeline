# Transaction Data Pipeline Service — TAO Fraud Platform
This service is part of the TAO Real-Time Fraud Detection Platform.
Its primary purpose is to pre-process historical transaction data and build fast lookup datasets used by the real-time fraud engine.

Instead of querying large historical tables during real-time transaction scoring,
this service prepares optimized MongoDB collections, updated periodically.

This allows the fraud engine to deliver real-time decisions in milliseconds, even with large datasets.

# What this service does
-Every time the pipeline runs: 10 min of duration  

# Load & Clean Historical Data
*Reads CSV containing 90+ days of transactions  
*Normalizes fields (card number, timestamps, geo, IP)  
*Converts each row into a validated Pydantic model  

# Build “Last 1 Hour Transactions” Dataset
*Used for R1 (Velocity), R2 (IP Clustering), R3 (Decline Spike)  
*Filters only last 60 minutes of data  
*Writes to MongoDB **transactions_last_1_hour**  
*TTL index auto-removes old records  
*Fast lookups for real-time scoring  

# Build “User Behavior (Last 60 Days)” Dataset
*Used for R4–R6 (Impossible Travel, Amount Spike, Cross-Border)  
*For each user/card pair, stores:  
*Last known location  
*Avg / min / max transaction amount  
*Decline count  
*Total 60-day transaction count  
*Last country / last geo coordinates  
*Stored in MongoDB: **user_behavior_60_days**  

# Load Blacklist (Optional)
Used for R9 Blacklist Rule
Loads a simple blacklist CSV (users, cards, IPs)
Writes to MongoDB: **blacklist**

# Store All Datasets in MongoDB
Real-time Fraud Engine uses these optimized collections to:
Run rules instantly (R1–R9)
Build ML feature vectors
Score transactions in milliseconds

# Why this is useful
This pipeline prepares all historical context needed for real-time fraud decisions, 
so the online scoring engine never queries large historical datasets.
This gives very fast, scalable, low-latency fraud detection.
