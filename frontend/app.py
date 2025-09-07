import streamlit as st
import pandas as pd
import sqlite3

st.title("HR Analytics & Reporting Dashboard")

# Connect to SQLite
conn = sqlite3.connect("hr_data.db")

# Fetch Departments
departments = pd.read_sql("SELECT DISTINCT department FROM employees", conn)
dept_list = ["All"] + departments["department"].tolist()

# Dropdown for Department Filter
choice = st.selectbox("Select Department", dept_list)

# SQL Query
query = """
SELECT e.emp_id, e.name, e.department, e.salary, e.status, 
       p.rating, a.present_days
FROM employees e
LEFT JOIN performance p ON e.emp_id = p.emp_id
LEFT JOIN attendance a ON e.emp_id = a.emp_id
"""

df = pd.read_sql(query, conn)

if choice != "All":
    df = df[df["department"] == choice]

st.write("### Employee Report")
st.dataframe(df)

# Summary Metrics
st.write("### Summary Stats")
st.write(df.groupby("department").agg({
    "emp_id": "count",
    "rating": "mean",
    "present_days": "mean"
}).rename(columns={"emp_id": "Total Employees", "rating": "Avg Rating", "present_days": "Avg Attendance"}))
