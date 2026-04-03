-- EQWatch Common Queries
-- Format: each query is preceded by "-- name: <query_name>" to allow loading by name.

-- name: get_all_users
-- services/users.py, get_all_users()
SELECT user_id, first_name, last_name, email, created_at
FROM Users;

-- name: get_user
-- services/users.py, get_user()
SELECT user_id, first_name, last_name, email, created_at
FROM Users
WHERE user_id = %s;

-- name: create_user
-- services/users.py, create_user()
INSERT INTO Users (first_name, last_name, email, password)
VALUES (%s, %s, %s, %s);

-- name: delete_user
-- services/users.py, delete_user()
DELETE FROM Users
WHERE user_id = %s;

-- name: get_regions_for_user
-- services/user_regions.py, get_regions_for_user()
SELECT r.region_id, r.name, r.min_lat, r.max_lat, r.min_lon, r.max_lon
FROM Regions r
JOIN UserRegions ur ON r.region_id = ur.region_id
WHERE ur.user_id = %s;

-- name: add_user_region
-- services/user_regions.py, add_user_region()
INSERT INTO UserRegions (user_id, region_id)
VALUES (%s, %s);

-- name: remove_user_region
-- services/user_regions.py, remove_user_region()
DELETE FROM UserRegions
WHERE user_id = %s AND region_id = %s;

-- name: get_all_regions
-- services/regions.py, get_all_regions()
SELECT region_id, name, min_lat, max_lat, min_lon, max_lon
FROM Regions;

-- name: get_region
-- services/regions.py, get_region()
SELECT region_id, name, min_lat, max_lat, min_lon, max_lon
FROM Regions
WHERE region_id = %s;

-- name: create_region
-- services/regions.py, create_region()
INSERT INTO Regions (name, min_lat, max_lat, min_lon, max_lon)
VALUES (%s, %s, %s, %s, %s);

-- name: delete_region
-- services/regions.py, delete_region()
DELETE FROM Regions
WHERE region_id = %s;

-- name: get_all_earthquakes
-- services/earthquakes.py, get_all_earthquakes()
SELECT eq_id, magnitude, depth, latitude, longitude, location_name, occurred_at
FROM Earthquakes;

-- name: get_earthquake
-- services/earthquakes.py, get_earthquake()
SELECT eq_id, magnitude, depth, latitude, longitude, location_name, occurred_at
FROM Earthquakes
WHERE eq_id = %s;

-- name: insert_earthquake
-- services/earthquakes.py, insert_earthquake()
INSERT INTO Earthquakes (magnitude, depth, latitude, longitude, location_name, occurred_at)
VALUES (%s, %s, %s, %s, %s, %s);

-- name: get_all_alerts
-- services/alerts.py, get_all_alerts()
SELECT alert_id, user_id, eq_id, sent_at
FROM Alerts;

-- name: create_alert
-- services/alerts.py, create_alert()
INSERT INTO Alerts (user_id, eq_id)
VALUES (%s, %s);

-- name: delete_alert
-- services/alerts.py, delete_alert()
DELETE FROM Alerts
WHERE alert_id = %s;

-- name: get_preferences_for_user
-- services/notification_preferences.py, get_preferences_for_user()
SELECT pref_id, user_id, min_magnitude, notify_email
FROM NotificationPreferences
WHERE user_id = %s;

-- name: create_preference
-- services/notification_preferences.py, create_preference()
INSERT INTO NotificationPreferences (user_id, min_magnitude, notify_email)
VALUES (%s, %s, %s);

-- name: delete_preference
-- services/notification_preferences.py, delete_preference()
DELETE FROM NotificationPreferences
WHERE pref_id = %s;
