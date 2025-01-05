# U-BirdEat API Documentation

## Table of Contents
- [U-BirdEat API Documentation](#u-birdeat-api-documentation)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Authentication](#authentication)
  - [Endpoints](#endpoints)
    - [User Authentication](#user-authentication)
      - [Login](#login)
      - [Token Refresh](#token-refresh)
      - [Logout](#logout)
    - [Provider APIs](#provider-apis)
      - [Provider Registration](#provider-registration)
      - [Provider Profile Management](#provider-profile-management)
      - [Provider Products Management](#provider-products-management)
      - [Provider Orders Management](#provider-orders-management)
      - [Provider Income Information](#provider-income-information)
    - [Delivery APIs](#delivery-apis)
      - [Deliver Registration](#deliver-registration)
      - [Deliver Profile Management](#deliver-profile-management)
      - [Deliver Orders Management](#deliver-orders-management)
      - [Deliver Income Information](#deliver-income-information)
    - [Customer APIs](#customer-apis)
      - [Customer Registration](#customer-registration)
      - [Customer Profile Management](#customer-profile-management)
      - [Customer Provider Interaction](#customer-provider-interaction)
      - [Customer Order Management](#customer-order-management)
      - [Customer Special Features](#customer-special-features)
      - [Customer Chatbot](#customer-chatbot)

## Introduction
This document describes the API endpoints for U-BirdEat, a food delivery platform that connects customers with providers and delivery persons. The API is built using Django REST framework.

## Authentication
The API uses JWT (JSON Web Token) for authentication. Most endpoints require a valid access token to be included in the request header:
```
Authorization: Bearer <access_token>
```

## Endpoints

### User Authentication

#### Login
- **URL**: `/token/`
- **Method**: `POST`
- **Auth Required**: No
- **Body** (JSON):
  ```json
  {
      "username": string,
      "password": string
  }
  ```
- **Success Response**: 
  - Returns access and refresh tokens
  ```json
  {
      "access": string,
      "refresh": string
  }
  ```
- **Error Response**:
  - **Status Code**: 401 Unauthorized
    ```json
    {
        "detail": "No active account found with the given credentials"
    }
    ```

#### Token Refresh
- **URL**: `/token/refresh/`
- **Method**: `POST`
- **Auth Required**: Yes
- **Body** (JSON):
  ```json
  {
      "refresh": string
  }
  ```
- **Success Response**: 
  - Returns new access token and refresh token
  ```json
  {
      "access": string,
      "refresh": string
  }
  ```
- **Error Response**:
- **Status Code**: 401 Unauthorized
  ```json
  {
      "detail": "Token is invalid or expired",
      "code": "token_not_valid"
  }
  ```

#### Logout
- **URL**: `/token/blacklist/`
- **Method**: `POST`
- **Auth Required**: Yes
- **Body** (JSON):
  ```json
  {
      "refresh": string
  }
  ```
- **Success Response**: 
  - **Status Code**: 200 OK
    ```json
    {}
    ```

### Provider APIs
- **Note**: All provider APIs require the user to be authenticated as a provider.

#### Provider Registration
- **URL**: `/provider/`
- **Method**: `POST`
- **Auth Required**: No
- **Body** (JSON):
    ```json
    {
        "username": string,
        "password": string,
        "password2": string,
        "shop_name": string,
        "phone": string,
        "address": string,
        "image_url": string,
        "category": string
    }
    ```
- **Success Response**:
  - **Status Code**: 201 Created

#### Provider Profile Management
- **Get Profile**
  - **URL**: `/provider/profile/`
  - **Method**: `GET`
  - **Auth Required**: Yes
  - **success response**:
    ```json
    {
      "shop_name": string,
      "phone": string,
      "address": string,
      "image_url": string,
      "category": string
    }
    ```

- **Update Profile**
  - **URL**: `/provider/profile/`
  - **Method**: `PUT`
  - **Auth Required**: Yes
  - **Body** (JSON):
    ```json
    {
        "shop_name": string,
        "phone": string,
        "address": string,
        "image_url": string,
        "category": string
    }
    ```
  - **success response**:
    ```json
    {
      "shop_name": string,
      "phone": string,
      "address": string,
      "image_url": string,
      "category": string
    }
    ```


#### Provider Products Management
- **List Products**
  - **URL**: `/provider/products/`
  - **Method**: `GET`
  - **Auth Required**: Yes
  - **Success Response**: 
    ```json
    [
      {
        "id": number,
        "name": string,
        "price": number,
        "description": string,
        "created_at": string,
        "update_at": string
      },
      ...
    ]
    ```

- **Get Product**
  - **URL**: `/provider/products/{id}/`
  - **Method**: `GET`
  - **Auth Required**: Yes
  - **Success Response**:
    ```json
    {
        "id": number,
        "name": string,
        "price": number,
        "description": string,
        "created_at": string,
        "update_at": string
    }
    ```

- **Add Product**
  - **URL**: `/provider/products/`
  - **Method**: `POST`
  - **Auth Required**: Yes
  - **Body** (JSON):
    ```json
    {
        "name": string,
        "price": number,
        "description": string
    }
    ```
  - **Success Response**:
    ```json
    {
        "id": number,
        "name": string,
        "price": number,
        "description": string,
        "created_at": string,
        "update_at": string
    }
    ```

- **Update Product**
  - **URL**: `/provider/products/{id}/`
  - **Method**: `PUT`
  - **Auth Required**: Yes
  - **Body** (JSON):
    ```json
    {
        "name": string,
        "price": number,
        "description": string
    }
    ```
  - **Success Response**:
    ```json
    {
        "id": number,
        "name": string,
        "price": number,
        "description": string,
        "created_at": string,
        "update_at": string
    }
    ```

- **Delete Product**
  - **URL**: `/provider/products/{id}/`
  - **Method**: `DELETE`
  - **Auth Required**: Yes
  - **Success Response**:
    - **Status code**: 204 No Content

#### Provider Orders Management
- **List Orders**
  - **URL**: `/provider/orders/`
  - **Method**: `GET`
  - **Auth Required**: Yes
  - **Success Response**:
    ```json
    [
      {
        "id": number,
        "total_price": number,
        "provider_fee": number,
        "status": number,
        "created_at": string,
        "memo": string
      },
      ...
    ]
    ```

- **Get Order**
  - **URL**: `/provider/orders/{id}/`
  - **Method**: `GET`
  - **Auth Required**: Yes
  - **Success Response**:
    ```json
    {
      "order_info": {
        "id": number,
        "total_price": number,
        "provider_fee": number,
        "status": number,
        "created_at": string,
        "memo": string
      },
      "product_info": [
        {
          "product": {
            "name": string,
            "price": number
          },
          "count": number
        },
        ...
      ]
    }
    ```

- **Update Order**
  - **URL**: `/provider/orders/{id}/`
  - **Method**: `PUT`
  - **Auth Required**: Yes
  - **Body** (JSON):
    ```json
    {
      "status": number
    }
    ```
  - **Success Response**:
    ```json
    {
      "id": number,
      "total_price": number,
      "provider_fee": number,
      "status": number,
      "created_at": string,
      "memo": string
    }
    ```

- **Delete Order**
  - **URL**: `/provider/orders/{id}/`
  - **Method**: `DELETE`
  - **Auth Required**: Yes
  - **Success Response**:
    - **Status code**: 204 No Content

#### Provider Income Information
- **List Income Information**
  - **URL**: `/provider/income/`
  - **Method**: `GET`
  - **Auth Required**: Yes
  - **Success Response**:
    ```json
    {
      "total_income": number,
      "orders": [
        {
          "id": number,
          "provider_fee": number,
          "created_at": string
        },
        ...
      ]
    }
    ```

### Delivery APIs
- **Note**: All delivery APIs require the user to be authenticated as a delivery person.

#### Deliver Registration
- **URL**: `/deliver/`
- **Method**: `POST`
- **Auth Required**: No
- **Body** (JSON):
  ```json
  {
      "username": string,
      "password": string,
      "password2": string,
      "real_name": string,
      "phone": string
  }
  ```
- **Success Response**:
  - **Status Code**: 201 Created

#### Deliver Profile Management
- **Get Profile**
  - **URL**: `/deliver/profile/`
  - **Method**: `GET`
  - **Auth Required**: Yes
  - **Success Response**:
    ```json
    {
      "real_name": string,
      "phone": string
    }
    ```

- **Update Profile**
  - **URL**: `/deliver/profile/`
  - **Method**: `PUT`
  - **Auth Required**: Yes
  - **Body** (JSON):
    ```json
    {
        "real_name": string,
        "phone": string
    }
    ```
  - **Success Response**:
    ```json
    {
      "real_name": string,
      "phone": string
    }
    ```

#### Deliver Orders Management
- **List Orders**
  - **URL**: `/deliver/orders/`
  - **Method**: `GET`
  - **Auth Required**: Yes
  - **Success Response**:
    ```json
    [
        {
            "id": number,
            "delivery_fee": number,
            "status": number,
            "created_at": string,
            "delivery_address": string,
        },
        ...
    ]
    ```

- **Get Order**
  - **URL**: `/deliver/orders/{id}/`
  - **Method**: `GET`
  - **Auth Required**: Yes
  - **Success Response**:
    ```json
    {
        "id": number,
        "status": number,
        "customer": {
            "real_name": string,
            "phone": string
        },
        "provider": {
            "shop_name": string,
            "address": string,
        },
        "total_price": number,
        "delivery_fee": number,
        "delivery_address": string,
    }
    ```

- **Update Order**
  - **URL**: `/deliver/orders/{id}/`
  - **Method**: `PUT`
  - **Auth Required**: Yes
  - **Success Response**:
    ```json
    {
        "id": number,
        "status": number,
        "customer": {
            "real_name": string,
            "phone": string
        },
        "provider": {
            "shop_name": string,
            "address": string,
        },
        "total_price": number,
        "delivery_fee": number,
        "delivery_address": string,
    }
    ```

#### Deliver Income Information
- **List Income Information**
  - **URL**: `/deliver/income/`
  - **Method**: `GET`
  - **Auth Required**: Yes
  - **Success Response**:
    ```json
    {
      "total_income": number,
      "orders": [
        {
          "id": number,
          "delivery_fee": number,
          "created_at": string
        },
        ...
      ]
    }
    ```

### Customer APIs
- **Note**: All customer APIs require the user to be authenticated as a customer.

#### Customer Registration
- **URL**: `/customer/`
- **Method**: `POST`
- **Auth Required**: No
- **Body** (JSON):
  ```json
  {
      "username": string,
      "password": string,
      "password2": string,
      "real_name": string,
      "phone": string
  }
  ```
- **Success Response**:
  - **Status Code**: 201 Created

#### Customer Profile Management
- **Get Profile**
  - **URL**: `/customer/profile/`
  - **Method**: `GET`
  - **Auth Required**: Yes
  - **Success Response**:
    ```json
    {
      "real_name": string,
      "phone": string
    }
    ```

- **Update Profile**
  - **URL**: `/customer/profile/`
  - **Method**: `PUT`
  - **Auth Required**: Yes
  - **Body** (JSON):
    ```json
    {
        "real_name": string,
        "phone": string
    }
    ```
  - **Success Response**:
    ```json
    {
      "real_name": string,
      "phone": string
    }
    ```

#### Customer Provider Interaction
- **List Providers**
  - **URL**: `/customer/providers/`
  - **Method**: `GET`
  - **Auth Required**: Yes
  - **Success Response**:
    ```json
    [
      {
        "id": number,
        "shop_name": string,
        "image_url": string,
        "category": string
      },
      ...
    ]
    ```

- **Search Provider**
  - **URL**: `/customer/providers?search={query}`
  - **Method**: `GET`
  - **Auth Required**: Yes
  - **Success Response**:
    ```json
    [
      {
        "id": number,
        "shop_name": string,
        "image_url": string,
        "category": string
      },
      ...
    ]
    ```

- **Get Provider Detail**
  - **URL**: `/customer/providers/{id}/`
  - **Method**: `GET`
  - **Auth Required**: Yes
  - **Success Response**:
    ```json
    {
      "provider": {
        "id": number,
        "shop_name": string,
        "image_url": string,
        "category": string
      },
      "products": [
        {
          "id": number,
          "name": string,
          "price": number,
          "description": string
        },
        ...
      ]
    }
    ```

#### Customer Order Management
- **Place Order**
  - **URL**: `/customer/order/`
  - **Method**: `POST`
  - **Auth Required**: Yes
  - **Body** (JSON):
    ```json
    {
        "products": [
            {
                "id": number,
                "count": number
            },
            ...
        ],
        "order_detail": {
            "provider": number,
            "delivery_address": string,
            "memo": string
        }
    }
    ```

- **List Orders**
  - **URL**: `/customer/order/`
  - **Method**: `GET`
  - **Auth Required**: Yes
  - **Success Response**:
    ```json
    [
      {
        "id": number,
        "shop_name": string,
        "deliver_name": string,
        "status": number,
        "total_price": number,
        "created_at": string,
      },
      ...
    ]
    ```
  
- **Get Order**
  - **URL**: `/customer/order/{id}/`
  - **Method**: `GET`
  - **Auth Required**: Yes
  - **Success Response**:
    ```json
    {
      "id": number,
      "shop_name": string,
      "deliver_name": string,
      "status": number,
      "total_price": number,
      "created_at": string,
      "memo": string,
      "products": [
        {
          "name": string,
          "price": number,
          "count": number
        },
        ...
      ]
    }
    ```

#### Customer Special Features
- **Place Random Order**
  - **URL**: `/customer/random_choice/`
  - **Method**: `POST`
  - **Auth Required**: Yes
  - **Body** (JSON):
    ```json
    {
        "budget": number,
        "delivery_address": string
    }
    ```
  - **Success Response**:
    ```json
    {
      "id": number,
      "shop_name": string,
      "deliver_name": string,
      "status": number,
      "total_price": number,
      "created_at": string,
      "memo": string,
      "products": [
        {
          "name": string,
          "price": number,
          "count": number
        },
        ...
      ]
    }
    ```
  - **Error Response**:
    - **Status Code**: 404 Not Found
    - Cannot find a provider that fits the budget
      ```json
      {
      "error": "無法找到符合預算的供應商"
      }
      ```

#### Customer Chatbot
- **Chat with ChatBot**
  - **URL**: `/customer/chatbot/`
  - **Method**: `POST`
  - **Auth Required**: Yes
  - **Body** (JSON):
    ```json
    {
        "prompt": string
    }
    ```
  - **Success Response**:
    ```json
    {
      "response": string
    }
    ```

- **Get Chat History**
  - **URL**: `/customer/chatbot/`
  - **Method**: `GET`
  - **Auth Required**: Yes
  - **Success Response**:
    ```json
    {
      "history": [
      {
        "role": string,
        "content": string,
        "created_at": string
      },
      ...
      ]
    } 
    ```

- **Delete Chat History**
  - **URL**: `/customer/chatbot/`
  - **Method**: `DELETE`
  - **Auth Required**: Yes
  - **Success Response**:
    - **Status code**: 204 No Content