# 💰 Expense Management System

A command-line Expense Management System built with **Python** and **SQLite**.

This project helps users manage their income and expenses, organize spending into categories, generate reports, and perform financial analysis using SQL queries.

---

## 📌 Features

### 💵 Income Management
- Add Income
- View Income
- Update Income
- Delete Income

### 💸 Expense Management
- Add Expense
- View Expense
- Update Expense
- Delete Expense
- Balance Alert

### 📂 Category Management
- Add Category
- View Category
- Update Category
- Delete Category

### 📊 Reports
- Total Income
- Total Expense
- Remaining Balance
- Highest Expense Category
- Monthly Report
- Yearly Report

### 🔍 Search
- Search by Date
- Search by Category
- Search by Amount

### 📈 Analytics
- Month with Highest Expense
- Month with Lowest Expense
- Average Monthly Spending

---

## 🛠 Technologies Used

- Python 3
- SQLite3
- SQL
- Command Line Interface (CLI)

---

## 🗄 Database Structure

### Income Table

| Column | Type |
|---------|------|
| income_id | INTEGER (Primary Key) |
| source | TEXT |
| amount | REAL |
| description | TEXT |
| date | DATETIME |

---

### Expense Table

| Column | Type |
|---------|------|
| expense_id | INTEGER (Primary Key) |
| category_id | INTEGER |
| amount | REAL |
| description | TEXT |
| date | DATETIME |

---

### Category Table

| Column | Type |
|---------|------|
| category_id | INTEGER (Primary Key) |
| category_name | TEXT |

---

## 📂 Project Structure

```
expense_management.py
expense.db
README.md
```

---

## ▶️ How to Run

1. Clone the repository

```
git clone https://github.com/your-username/Expense-Management-System.git
```

2. Open the project folder

```
cd Expense-Management-System
```

3. Run the program

```
python expense_management.py
```

The SQLite database (`expense.db`) will be created automatically if it does not already exist.

---

## 📚 SQL Concepts Used

- CREATE TABLE
- INSERT
- UPDATE
- DELETE
- SELECT
- WHERE
- LIKE
- GROUP BY
- ORDER BY
- SUM()
- AVG()
- JOIN
- LIMIT
- CURRENT_TIMESTAMP
- STRFTIME()

---

## 📷 Main Menu

```
1. Income
2. Expense
3. Category
4. Report
5. Search
6. Analytics
7. Exit
```

---

## 🚀 Future Improvements (Version 2)

- Foreign Key Constraints
- Automatic ID Generation
- Better Input Validation
- Search by Amount Range
- Category Validation Before Adding Expense
- Prevent Deleting Categories Used by Expenses
- Export Reports to CSV
- Multiple Python Files
- Graphical User Interface (Tkinter or CustomTkinter)

---

## 🎯 What I Learned

While building this project I learned:

- Database design
- CRUD operations
- SQLite integration with Python
- SQL JOIN operations
- Aggregate functions
- Monthly and yearly financial reports
- Menu-driven application design
- Python functions and modular programming
- Error handling using try/except

---

## 👨‍💻 Author

Developed by **Souma**

This project was created as part of my Python and SQL learning journey to improve backend development and database management skills.
