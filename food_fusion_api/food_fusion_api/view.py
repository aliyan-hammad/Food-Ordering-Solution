
# Sure! A database schema for a service like Foodpanda (which is an online food delivery platform) would typically involve several entities like users, restaurants, food items, orders, payments, and reviews.

# Below is a simplified schema of what the database could look like:

# 1. Users Table
# This stores information about the users (both customers and admin).

# sql
# Copy code
# CREATE TABLE Users (
#     user_id INT AUTO_INCREMENT PRIMARY KEY,
#     username VARCHAR(100) NOT NULL UNIQUE,
#     password_hash VARCHAR(255) NOT NULL,
#     email VARCHAR(100) NOT NULL,
#     phone_number VARCHAR(15),
#     role ENUM('customer', 'admin') DEFAULT 'customer',
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
# );
# 2. Restaurants Table
# Stores details about restaurants available on the platform.

# sql
# Copy code
# CREATE TABLE Restaurants (
#     restaurant_id INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(255) NOT NULL,
#     description TEXT,
#     location VARCHAR(255),
#     rating DECIMAL(3, 2) DEFAULT 0,
#     phone_number VARCHAR(15),
#     user_id INT,  -- Linking to the admin user who manages this restaurant
#     FOREIGN KEY (user_id) REFERENCES Users(user_id),
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
# );
# 3. Menu Items Table
# Contains details about food items in a restaurant's menu.

# sql
# Copy code
# CREATE TABLE MenuItems (
#     item_id INT AUTO_INCREMENT PRIMARY KEY,
#     restaurant_id INT,
#     name VARCHAR(255) NOT NULL,
#     description TEXT,
#     price DECIMAL(10, 2) NOT NULL,
#     category VARCHAR(100),
#     available BOOLEAN DEFAULT TRUE,  -- Whether the item is currently available
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#     FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id)
# );
# 4. Orders Table
# Stores information about customer orders.

# sql
# Copy code
# CREATE TABLE Orders (
#     order_id INT AUTO_INCREMENT PRIMARY KEY,
#     user_id INT,  -- Customer who placed the order
#     restaurant_id INT,  -- The restaurant from which the order was placed
#     total_price DECIMAL(10, 2),
#     status ENUM('pending', 'confirmed', 'in_progress', 'delivered', 'cancelled') DEFAULT 'pending',
#     delivery_address VARCHAR(255),
#     delivery_time TIMESTAMP,
#     payment_status ENUM('pending', 'completed', 'failed') DEFAULT 'pending',
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#     FOREIGN KEY (user_id) REFERENCES Users(user_id),
#     FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id)
# );
# 5. Order Items Table
# Links orders to the specific food items that were ordered.

# sql
# Copy code
# CREATE TABLE OrderItems (
#     order_item_id INT AUTO_INCREMENT PRIMARY KEY,
#     order_id INT,
#     item_id INT,
#     quantity INT DEFAULT 1,
#     price DECIMAL(10, 2),  -- The price at the time of the order (to handle price changes)
#     FOREIGN KEY (order_id) REFERENCES Orders(order_id),
#     FOREIGN KEY (item_id) REFERENCES MenuItems(item_id)
# );
# 6. Payments Table
# Handles the payment details related to each order.

# sql
# Copy code
# CREATE TABLE Payments (
#     payment_id INT AUTO_INCREMENT PRIMARY KEY,
#     order_id INT,
#     payment_method ENUM('credit_card', 'debit_card', 'paypal', 'cod') NOT NULL,
#     payment_status ENUM('pending', 'completed', 'failed') DEFAULT 'pending',
#     payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY (order_id) REFERENCES Orders(order_id)
# );
# 7. Reviews Table
# Allows customers to leave reviews for restaurants and food items.

# sql
# Copy code
# CREATE TABLE Reviews (
#     review_id INT AUTO_INCREMENT PRIMARY KEY,
#     user_id INT,  -- Customer who left the review
#     restaurant_id INT,
#     item_id INT,
#     rating INT CHECK (rating BETWEEN 1 AND 5),
#     review_text TEXT,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY (user_id) REFERENCES Users(user_id),
#     FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id),
#     FOREIGN KEY (item_id) REFERENCES MenuItems(item_id)
# );
# 8. Delivery Partners Table
# Stores information about delivery drivers who deliver orders.

# sql
# Copy code
# CREATE TABLE DeliveryPartners (
#     partner_id INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(255) NOT NULL,
#     phone_number VARCHAR(15),
#     email VARCHAR(100),
#     vehicle_type ENUM('car', 'bike', 'scooter'),
#     status ENUM('available', 'on_delivery', 'busy', 'offline') DEFAULT 'available',
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
# );
# 9. Deliveries Table
# Links delivery partners to specific orders they are responsible for delivering.

# sql
# Copy code
# CREATE TABLE Deliveries (
#     delivery_id INT AUTO_INCREMENT PRIMARY KEY,
#     order_id INT,
#     partner_id INT,
#     delivery_status ENUM('picked_up', 'in_transit', 'delivered', 'failed') DEFAULT 'picked_up',
#     delivery_time TIMESTAMP,
#     FOREIGN KEY (order_id) REFERENCES Orders(order_id),
#     FOREIGN KEY (partner_id) REFERENCES DeliveryPartners(partner_id)
# );
# Key Relationships:
# Users can place Orders.
# Orders consist of multiple MenuItems (via OrderItems).
# Restaurants have MenuItems and Reviews.
# Orders are paid via Payments.
# Reviews link Users to MenuItems and Restaurants.
# DeliveryPartners deliver Orders, and this is tracked by Deliveries.
# This schema is just a foundational structure and can be expanded with more complex features like loyalty programs, coupons, promotional offers, delivery tracking, etc. It can also be optimized depending on the specific use case, scalability requirements, and database type you're using (MySQL, PostgreSQL, etc.).