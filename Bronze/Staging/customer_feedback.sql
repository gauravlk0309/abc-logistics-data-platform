CREATE TABLE customer_feedback(
    feedback_id VARCHAR(20),
    shipment_id VARCHAR(20),
    customer_id VARCHAR(20),
    rating INTEGER,
    on_time_delivery VARCHAR(20),
    comments TEXT,
    feedback_date DATE,
    channel VARCHAR(50)
);

SELECT * FROM customer_feedback