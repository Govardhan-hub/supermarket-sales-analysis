#  Supermarket Sales Analysis

 **[Click here to visit Live Dashboard](https://supermarket-sales-analysis-jrqksuoe7aygid2srcbbjh.streamlit.app/)**

A beginner-friendly data analysis project based on supermarket sales data.

The goal of this project is to clean the data, analyze sales patterns, visualize the results, and extract useful business insights using Python.

The project also includes an interactive Streamlit dashboard to make the analysis easier to explore.

---

##  Project Overview

This project follows a simple data analysis workflow:

**Raw Data → Data Cleaning → Analysis → Visualization → Business Insights → Dashboard**

The analysis focuses on areas such as:

- Revenue and gross income
- Product category performance
- Branch performance
- Customer types
- Payment methods
- Sales by month, day, and hour
- Quantity sold
- Transaction values
- Relationships between different numerical variables

---

##  Dataset

The dataset contains supermarket transaction records with information such as:

- Invoice ID
- Date and Time
- Branch
- City
- Customer Type
- Gender
- Product Line
- Unit Price
- Quantity
- Tax
- Total
- Payment Method
- COGS
- Gross Income
- Rating

The dataset contains missing values and duplicate records, which were intentionally handled as part of the data-cleaning process.

---

##  Data Cleaning

The following cleaning steps were performed using Pandas:

- Filled missing `Payment_Method` values with `"Unknown"`
- Filled missing `Customer_Type` values with `"Unknown"`
- Converted the `Rating` column into numeric values
- Handled invalid rating values using `NaN`
- Removed duplicate rows
- Saved the cleaned dataset as `supermarket_cleaned.csv`

---

##  Data Analysis

Several business questions were explored using Pandas.

Some of the questions included:

- Which branch generates the most revenue?
- Which product category generates the most revenue?
- Which customer type generates the most revenue?
- Which payment method generates the most revenue?
- Which month has the highest revenue?
- Which product category sells the most units?
- Which branch has the most transactions?
- Which day generates the most revenue?
- What time of the day has the highest revenue?
- Which product category generates the most gross income?
- How are quantity and transaction value related?
- How are unit price and transaction value related?

---

##  Data Visualization

Matplotlib was used to visualize the results of the analysis.

The project includes visualizations for:

- Revenue by branch
- Revenue by product category
- Revenue by customer type
- Revenue share by payment method
- Monthly revenue
- Average transaction by customer type
- Revenue by gender
- Quantity sold by product category
- Average rating by product category
- Average unit price by product category
- Gross income by product category
- Gross income by branch
- Number of transactions by branch
- Average transaction by branch
- Revenue by day of the week
- Revenue by hour
- COGS by product category
- Gross income by payment method
- Quantity vs Total
- Unit Price vs Total

---

##  Key Business Insights

Some of the main findings from the analysis were:

### Branch Performance
Branch A generated the highest revenue with approximately **₹430,953.90**.

### Product Category Performance
**Sports and Travel** generated the highest revenue with approximately **₹267,916.93**.

### Customer Type
**Members** generated the highest total revenue among the customer types.

### Payment Method
**Credit Card** generated the highest total revenue among the payment methods.

### Monthly Performance
**December** recorded the highest monthly revenue at approximately **₹118,216.74**.

### Product Quantity
**Health and Beauty** had the highest quantity sold with **4,928 units**.

### Gross Income
**Sports and Travel** generated the highest gross income at approximately **₹76,547.69**.

### Branch Transactions
Branch A had the highest number of transactions with **1,736 transactions**.

### Day Performance
**Saturday** generated the highest daily revenue at approximately **₹190,524.08**.

### Hourly Performance
The highest hourly revenue was recorded at **7 PM**, with approximately **₹136,965.30**.

### Overall Gross Income
The supermarket generated approximately **₹353,386.86** in total gross income.

### Gross Income Percentage
Gross income represented approximately **28.57%** of total revenue.

### Correlation

The correlation between:

- **Quantity and Total:** approximately **0.65**
- **Unit Price and Total:** approximately **0.69**

These indicate moderate positive relationships in this dataset.

> Correlation shows a relationship between variables, but it does not mean that one variable directly causes the other.

### Customer Type Observation

Customers with an unknown customer type had the highest average transaction value at approximately **₹258.72**.

However, there were only **74 Unknown customer transactions**, compared with thousands of Member and Normal transactions, so this result should be interpreted carefully.

---

##  Streamlit Dashboard

The project also includes an interactive dashboard built using **Streamlit**.

The dashboard displays important KPIs such as:

- Total Revenue
- Gross Income
- Number of Transactions
- Average Transaction Value

### Run the Dashboard

Install the required libraries:

```bash
pip install pandas matplotlib streamlit
