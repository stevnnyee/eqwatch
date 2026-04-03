-- EQWatch Database Schema

CREATE TABLE users (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  first_name VARCHAR(100),
  last_name VARCHAR(100),
  email VARCHAR(100) NOT NULL UNIQUE,
  password VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE earthquakes (
  eq_id INT AUTO_INCREMENT PRIMARY KEY,
  magnitude DECIMAL(10, 2),
  depth DECIMAL(12, 4),
  latitude DECIMAL(10, 7),
  longitude DECIMAL(10, 7),
  location_name VARCHAR(255),
  `timestamp` DATETIME NOT NULL
);

CREATE TABLE regions (
  region_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  min_lat DECIMAL(10, 7) NOT NULL,
  max_lat DECIMAL(10, 7) NOT NULL,
  min_lon DECIMAL(10, 7) NOT NULL,
  max_lon DECIMAL(10, 7) NOT NULL
);

CREATE TABLE user_regions (
  user_id INT NOT NULL,
  region_id INT NOT NULL,
  PRIMARY KEY (user_id, region_id),
  FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
  FOREIGN KEY (region_id) REFERENCES regions (region_id) ON DELETE CASCADE
);

CREATE TABLE notification_preferences (
  pref_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  min_magnitude DECIMAL(10, 2),
  notify_email BOOLEAN DEFAULT TRUE,
  FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
);

CREATE TABLE alerts (
  alert_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  eq_id INT NOT NULL,
  sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
  FOREIGN KEY (eq_id) REFERENCES earthquakes (eq_id) ON DELETE CASCADE
);
