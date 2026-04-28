# 🍔 Food Mamy App

A full-featured restaurant ordering web application built using **Streamlit** and designed with **Object-Oriented Programming (OOP)** principles.
The app provides a complete food ordering experience with a modern UI, smooth navigation, and interactive features.

---

## 🚀 Live Demo

https://foodmamyproject-wcicqzanpqrq7ia4wgpyyr.streamlit.app/

---

## 🧠 Project Overview

Food Mamy is an interactive web app that simulates a real restaurant system.
Users can browse the menu, add items to their cart, apply promo codes, and complete orders through a multi-step checkout process.

---

## ✨ Features

### 🍽️ Menu System

* Categorized menu (Main Dishes, Sandwiches, Breakfast, Drinks, Desserts)
* Each item includes:

  * Name, price, description
  * Preparation time
  * Extra details (size, portion, etc.)
* Dynamic filtering by category

---

### 🛒 Cart System

* Add items to cart
* Remove items from cart
* Real-time subtotal calculation
* Dynamic cart updates

---

### 🏷️ Promo Code System

* Apply discount codes:

  * `WELCOME10` → 10% for first order
  * `BIG500` → 15% for orders above 500 EGP
* Validation based on:

  * First order condition
  * Minimum order value
* Automatic discount calculation

---

### 💳 Order Calculation

* Subtotal calculation
* Tax calculation (14%)
* Delivery fee:

  * 20 EGP standard
  * Free delivery for orders above 1000 EGP
* Final total after promo discount

---

### 🧾 Multi-Step Checkout

1. Review Cart
2. Enter Delivery Information
3. Confirm Order

* Input validation (name, address, phone number)
* Clean and guided user experience

---

### 📦 Order Management

* Order confirmation page
* Animated success screen 🎉
* Order history tracking
* Each order includes:

  * Items
  * Total price
  * Date & time
  * Status

---

### 🎨 UI / UX Design

* Modern and responsive interface
* Dark / Light mode toggle
* Custom CSS styling
* Animated components (confetti, delivery animation)
* Clean layout with sections and cards

---

## 🧠 OOP Concepts Used

This project is fully structured using Object-Oriented Programming:

* **Classes & Objects**

  * `MenuItem`, `Order`, `RestaurantSystem`

* **Encapsulation**

  * Private price attribute with getter & setter methods

* **Inheritance**

  * Specialized classes:

    * `MainDish`
    * `Sandwich`
    * `Breakfast`
    * `Drink`
    * `Dessert`

* **Polymorphism**

  * Different item types handled using a unified interface

---

## 🛠️ Technologies Used

* Python
* Streamlit
* OOP Design Principles

---

## 📂 Project Structure

```id="x1"
food-mamy-app/
│
├── app.py
├── requirements.txt
└── README.md
```

---

## ▶️ Run Locally

```bash id="x2"
pip install -r requirements.txt
streamlit run app.py
```

---

## 💡 Future Improvements

* Add user authentication system
* Connect to real database (Firebase / PostgreSQL)
* Online payment integration
* Admin dashboard for managing menu & orders

---

## 👩‍💻 Author

**Menna Akram**

---

## ❤️ Final Note

This project demonstrates building a complete real-world application using Python, OOP, and Streamlit with a focus on user experience and clean code structure.
