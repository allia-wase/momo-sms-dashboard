CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    transaction_id VARCHAR(255) UNIQUE,
    type VARCHAR(255),
    amount INT,
    sender VARCHAR(255),
    recipient VARCHAR(255),
    date TIMESTAMP,
    description TEXT
);
