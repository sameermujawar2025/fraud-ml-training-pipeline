# fraud-ml-training-pipeline
Type: Batch / Scheduler
Role: Process client CSV → train → export models
Train models from client CSV (offline), Python (Scheduler + boto3 + XGBoost)

Responsibilities:
Function	Description
-Fetch CSV from client (S3 / FTP / API)	Scheduler runs daily (00:00) or on trigger
-Data cleaning & feature engineering	Handle missing values, normalization, categorical encoding
-Train ML models	XGBoost, AutoEncoder, Isolation Forest
-Save model artifacts	fraud_xgb.json, fraud_autoencoder.pt, iforest.pkl
-Generate manifest.json	Tracks model version, metrics, timestamp
-Upload models to S3/minio	Centralized model store
-Notify fraud-ml-model-service	via Kafka / webhook / Redis pub-sub
-Optional: store training logs	in PostgreSQL / S3
