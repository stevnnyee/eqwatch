-- EQWatch Database Schema

CREATE TABLE Users (
    user_id     INT AUTO_INCREMENT PRIMARY KEY,
    first_name  VARCHAR(100) NOT NULL,
    last_name   VARCHAR(100) NOT NULL,
    email       VARCHAR(100) NOT NULL UNIQUE,
    password    VARCHAR(255) NOT NULL,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Earthquakes (
    eq_id           INT AUTO_INCREMENT PRIMARY KEY,
    magnitude       DECIMAL(4, 2) NOT NULL CHECK (magnitude BETWEEN -2 AND 10),
    depth           DECIMAL(7, 3) NOT NULL CHECK (depth >= 0),
    latitude        DECIMAL(9, 6) NOT NULL CHECK (latitude BETWEEN -90 AND 90),
    longitude       DECIMAL(9, 6) NOT NULL CHECK (longitude BETWEEN -180 AND 180),
    location_name   VARCHAR(255),
    occurred_at     DATETIME NOT NULL,
    INDEX idx_magnitude (magnitude),
    INDEX idx_occurred_at (occurred_at)
);

CREATE TABLE Regions (
    region_id   INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    min_lat     DECIMAL(9, 6) NOT NULL,
    max_lat     DECIMAL(9, 6) NOT NULL,
    min_lon     DECIMAL(9, 6) NOT NULL,
    max_lon     DECIMAL(9, 6) NOT NULL,
    CHECK (min_lat < max_lat),
    CHECK (min_lon < max_lon)
);

CREATE TABLE UserRegions (
    user_id     INT NOT NULL,
    region_id   INT NOT NULL,
    PRIMARY KEY (user_id, region_id),
    FOREIGN KEY (user_id)   REFERENCES Users(user_id)   ON DELETE CASCADE,
    FOREIGN KEY (region_id) REFERENCES Regions(region_id) ON DELETE CASCADE
);

CREATE TABLE NotificationPreferences (
    pref_id         INT AUTO_INCREMENT PRIMARY KEY,
    user_id         INT NOT NULL,
    min_magnitude   DECIMAL(4, 2) NOT NULL CHECK (min_magnitude BETWEEN -2 AND 10),
    notify_email    BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE Alerts (
    alert_id    INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL,
    eq_id       INT NOT NULL,
    sent_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (eq_id)   REFERENCES Earthquakes(eq_id) ON DELETE CASCADE
);
