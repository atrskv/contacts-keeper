CREATE TABLE contacts (
    id VARCHAR(36) PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    gender VARCHAR(20),
    phone VARCHAR(20),
    email VARCHAR(100),
    date_of_birth DATE,
    priority VARCHAR(20),
    category VARCHAR(50),
    channels TEXT[],  -- массив текстов
    current_address TEXT
);
