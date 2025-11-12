# fraud-cache-service
Central Redis cache for storing blacklists, device data, and transaction context.Hybrid caching model: - Direct Redis access by rule-engine for low-latency operations. - Thin gRPC façade cache-service for non-critical lookups. Namespaces include velocity, geo, avg_amount, ml_feature, decision_audit.
