-- schema.sql
CREATE DATABASE IF NOT EXISTS ecom;
USE ecom;

CREATE TABLE users (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE items (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  sku VARCHAR(128) UNIQUE,
  title VARCHAR(255),
  category VARCHAR(128),
  price DECIMAL(10,2),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE transactions (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT NOT NULL,
  item_id BIGINT NOT NULL,
  action ENUM('view','click','cart','purchase') NOT NULL,
  price DECIMAL(10,2) NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (item_id) REFERENCES items(id)
);

-- Performance indexes
CREATE INDEX idx_transactions_user_time ON transactions (user_id, created_at);
CREATE INDEX idx_transactions_item_time ON transactions (item_id, created_at);
CREATE INDEX idx_transactions_action ON transactions (action);
