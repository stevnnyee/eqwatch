-- EQWatch Common Queries
-- Format: each query is preceded by "-- name: <query_name>" to allow loading by name.

-- =============================================================================
-- CRUD Queries
-- =============================================================================

-- name: get_all_users
-- services/users.py, get_all_users()
SELECT user_id, first_name, last_name, email, created_at
FROM users;

-- name: get_user
-- services/users.py, get_user()
SELECT user_id, first_name, last_name, email, created_at
FROM users
WHERE user_id = %s;

-- name: create_user
-- services/users.py, create_user()
INSERT INTO users (first_name, last_name, email, password)
VALUES (%s, %s, %s, %s);

-- name: delete_user
-- services/users.py, delete_user()
DELETE FROM users
WHERE user_id = %s;

-- name: get_regions_for_user
-- services/user_regions.py, get_regions_for_user()
SELECT r.region_id, r.name, r.min_lat, r.max_lat, r.min_lon, r.max_lon
FROM regions r
JOIN user_regions ur ON r.region_id = ur.region_id
WHERE ur.user_id = %s;

-- name: add_user_region
-- services/user_regions.py, add_user_region()
INSERT INTO user_regions (user_id, region_id)
VALUES (%s, %s);

-- name: remove_user_region
-- services/user_regions.py, remove_user_region()
DELETE FROM user_regions
WHERE user_id = %s AND region_id = %s;

-- name: get_all_regions
-- services/regions.py, get_all_regions()
SELECT region_id, name, min_lat, max_lat, min_lon, max_lon
FROM regions;

-- name: get_region
-- services/regions.py, get_region()
SELECT region_id, name, min_lat, max_lat, min_lon, max_lon
FROM regions
WHERE region_id = %s;

-- name: create_region
-- services/regions.py, create_region()
INSERT INTO regions (name, min_lat, max_lat, min_lon, max_lon)
VALUES (%s, %s, %s, %s, %s);

-- name: delete_region
-- services/regions.py, delete_region()
DELETE FROM regions
WHERE region_id = %s;

-- name: get_all_earthquakes
-- services/earthquakes.py, get_all_earthquakes()
SELECT eq_id, magnitude, depth, latitude, longitude, location_name, occurred_at
FROM earthquakes;

-- name: get_earthquake
-- services/earthquakes.py, get_earthquake()
SELECT eq_id, magnitude, depth, latitude, longitude, location_name, occurred_at
FROM earthquakes
WHERE eq_id = %s;

-- name: insert_earthquake
-- services/earthquakes.py, insert_earthquake()
INSERT INTO earthquakes (magnitude, depth, latitude, longitude, location_name, occurred_at)
VALUES (%s, %s, %s, %s, %s, %s);

-- name: get_all_alerts
-- services/alerts.py, get_all_alerts()
SELECT alert_id, user_id, eq_id, sent_at
FROM alerts;

-- name: create_alert
-- services/alerts.py, create_alert()
INSERT INTO alerts (user_id, eq_id)
VALUES (%s, %s);

-- name: delete_alert
-- services/alerts.py, delete_alert()
DELETE FROM alerts
WHERE alert_id = %s;

-- name: get_preferences_for_user
-- services/notification_preferences.py, get_preferences_for_user()
SELECT pref_id, user_id, min_magnitude, notify_email
FROM notification_preferences
WHERE user_id = %s;

-- name: create_preference
-- services/notification_preferences.py, create_preference()
INSERT INTO notification_preferences (user_id, min_magnitude, notify_email)
VALUES (%s, %s, %s);

-- name: delete_preference
-- services/notification_preferences.py, delete_preference()
DELETE FROM notification_preferences
WHERE pref_id = %s;

-- =============================================================================
-- Analytical Queries
-- =============================================================================

-- name: get_earthquakes_in_region
-- All earthquakes whose coordinates fall within a region's bounding box.
-- Params: region_id
SELECT e.eq_id, e.magnitude, e.depth, e.latitude, e.longitude, e.location_name, e.occurred_at,
       r.name AS region_name
FROM earthquakes e
JOIN regions r
  ON e.latitude  BETWEEN r.min_lat AND r.max_lat
 AND e.longitude BETWEEN r.min_lon AND r.max_lon
WHERE r.region_id = %s
ORDER BY e.occurred_at DESC;

-- name: get_users_to_alert
-- Users who watch a region containing the given earthquake AND have a
-- min_magnitude preference at or below the earthquake's magnitude.
-- Params: eq_id
SELECT DISTINCT u.user_id, u.email, u.first_name, u.last_name,
       np.min_magnitude, np.notify_email, r.name AS region_name
FROM earthquakes e
JOIN regions r
  ON e.latitude  BETWEEN r.min_lat AND r.max_lat
 AND e.longitude BETWEEN r.min_lon AND r.max_lon
JOIN user_regions ur ON r.region_id = ur.region_id
JOIN users u         ON ur.user_id = u.user_id
JOIN notification_preferences np ON u.user_id = np.user_id
WHERE e.eq_id = %s
  AND np.min_magnitude <= e.magnitude;

-- name: get_alert_history_for_user
-- Full alert history for a user, with earthquake details.
-- Params: user_id
SELECT a.alert_id, a.sent_at,
       e.eq_id, e.magnitude, e.depth, e.location_name, e.occurred_at
FROM alerts a
JOIN earthquakes e ON a.eq_id = e.eq_id
WHERE a.user_id = %s
ORDER BY a.sent_at DESC;

-- name: get_magnitude_distribution
-- Count of earthquakes grouped into 1-unit magnitude buckets.
SELECT FLOOR(magnitude) AS magnitude_bucket,
       COUNT(*) AS earthquake_count
FROM earthquakes
GROUP BY FLOOR(magnitude)
ORDER BY magnitude_bucket;

-- name: get_top_regions_by_activity
-- Regions ranked by how many earthquakes fall within their bounding box.
SELECT r.region_id, r.name,
       COUNT(e.eq_id) AS earthquake_count
FROM regions r
LEFT JOIN earthquakes e
  ON e.latitude  BETWEEN r.min_lat AND r.max_lat
 AND e.longitude BETWEEN r.min_lon AND r.max_lon
GROUP BY r.region_id, r.name
ORDER BY earthquake_count DESC;

-- name: get_user_activity_summary
-- Per-user count of watched regions and alerts received.
SELECT u.user_id, u.first_name, u.last_name, u.email,
       COUNT(DISTINCT ur.region_id) AS watched_regions,
       COUNT(DISTINCT a.alert_id)   AS alerts_received
FROM users u
LEFT JOIN user_regions ur ON u.user_id = ur.user_id
LEFT JOIN alerts a        ON u.user_id = a.user_id
GROUP BY u.user_id, u.first_name, u.last_name, u.email
ORDER BY alerts_received DESC;
