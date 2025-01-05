# U-Bird Eats Platform Database Design Documentation

## Overview
This database design supports a food delivery platform system, encompassing user management, order processing, and product management functionalities. The system includes three main roles: customers, delivery personnel, and merchants, along with order and product management.

## Table
- All tables are 3rd normal form (3NF) to minimize data redundancy and ensure data integrity

### Customer
| Field Name | Type           | Description                   |
| ---------- | -------------- | ----------------------------- |
| id         | AutoField      | Primary key                   |
| user       | OneToOneField  | Relation to Django User model |
| real_name  | CharField(100) | Customer's real name          |
| phone      | CharField(20)  | Contact phone number          |

### ChatRecord
| Field Name | Type          | Description          |
| ---------- | ------------- | -------------------- |
| id         | AutoField     | Primary key          |
| customer   | ForeignKey    | Relation to Customer |
| role       | CharField(10) | Conversation role    |
| content    | TextField     | Conversation content |
| created_at | DateTimeField | Creation timestamp   |

### Deliver
| Field Name | Type           | Description                   |
| ---------- | -------------- | ----------------------------- |
| id         | AutoField      | Primary key                   |
| user       | OneToOneField  | Relation to Django User model |
| real_name  | CharField(100) | Delivery person's real name   |
| phone      | CharField(20)  | Contact phone number          |

### Provider
| Field Name | Type           | Description                   |
| ---------- | -------------- | ----------------------------- |
| id         | AutoField      | Primary key                   |
| user       | OneToOneField  | Relation to Django User model |
| shop_name  | CharField(100) | Store name                    |
| phone      | CharField(20)  | Contact phone number          |
| address    | CharField(100) | Store address                 |
| image_url  | CharField(200) | Store image URL               |
| category   | CharField(50)  | Store category                |

### Product
| Field Name  | Type                 | Description          |
| ----------- | -------------------- | -------------------- |
| id          | AutoField            | Primary key          |
| name        | CharField(100)       | Product name         |
| provider    | ForeignKey           | Relation to Provider |
| price       | PositiveIntegerField | Product price        |
| description | TextField            | Product description  |
| created_at  | DateTimeField        | Creation timestamp   |
| update_at   | DateTimeField        | Update timestamp     |

### Order
| Field Name       | Type                 | Description                    |
| ---------------- | -------------------- | ------------------------------ |
| id               | AutoField            | Primary key                    |
| customer         | ForeignKey           | Relation to Customer           |
| provider         | ForeignKey           | Relation to Provider           |
| deliver          | ForeignKey           | Relation to Deliver (nullable) |
| delivery_address | CharField(100)       | Delivery address               |
| total_price      | PositiveIntegerField | Total order amount             |
| delivery_fee     | PositiveIntegerField | Delivery fee                   |
| provider_fee     | PositiveIntegerField | Provider earnings              |
| status           | IntegerField         | Order status                   |
| created_at       | DateTimeField        | Creation timestamp             |
| memo             | TextField            | Order notes                    |

- Order Status Description:
  - PROVIDER_PREPARING (0): Provider is preparing the order
  - WAITING_FOR_DELIVERY (1): Waiting for delivery
  - DELIVERING (2): Order is being delivered
  - COMPLETED (3): Order completed

*Note: System automatically calculates provider_fee as 80% of total amount and delivery_fee as 20% of total amount*

### OrderDetail
| Field Name | Type                 | Description         |
| ---------- | -------------------- | ------------------- |
| order      | ForeignKey           | Relation to Order   |
| product    | ForeignKey           | Relation to Product |
| count      | PositiveIntegerField | Product quantity    |

*Note: order and product fields are set as unique_together to prevent duplicate product entries in the same order*

## Data Relationships
1. User Relationships
   - Each Customer, Deliver, and Provider has a one-to-one relationship with a Django User
   - This ensures each role has an independent login account
2. Order Relationships
   - Order has many-to-one relationships with Customer, Provider, and Deliver
   - Order has many-to-many relationship with Product through OrderDetail
   - OrderDetail maintains quantity relationships between orders and products
3. Product Relationships
   - Product has many-to-one relationship with Provider, indicating each product belongs to a specific merchant

## Important Notes
1. Amount Calculations
   - All amount-related fields use PositiveIntegerField to ensure non-negative values
   - System automatically calculates provider earnings and delivery fees
   - Provider earnings ratio: 80%
   - Delivery fee ratio: 20%
2. Order Status Flow
   - Order status transitions follow the sequence: PROVIDER_PREPARING → WAITING_FOR_DELIVERY → DELIVERING → COMPLETED
   - Each status change should be timestamped
3. Data Integrity
   - Uses CASCADE deletion for relationships to ensure data consistency
   - OrderDetail uses unique_together to prevent duplicate entries