import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Load CSV Data
employees = pd.read_csv("data/employees.csv")
performance = pd.read_csv("data/performance.csv")
attendance = pd.read_csv("data/attendance.csv")

# Store into SQLite
conn = sqlite3.connect("hr_data.db")
employees.to_sql("employees", conn, if_exists="replace", index=False)
performance.to_sql("performance", conn, if_exists="replace", index=False)
attendance.to_sql("attendance", conn, if_exists="replace", index=False)

# SQL Report
query = """
SELECT e.department, COUNT(e.emp_id) as total_employees,
       AVG(p.rating) as avg_rating,
       AVG(a.present_days) as avg_attendance
FROM employees e
LEFT JOIN performance p ON e.emp_id = p.emp_id
LEFT JOIN attendance a ON e.emp_id = a.emp_id
WHERE e.status = 'Active'
GROUP BY e.department;
"""

report_df = pd.read_sql(query, conn)
print(report_df)

# Save Excel Report
report_df.to_excel("reports/summary_report.xlsx", index=False)

# Visualization
plt.bar(report_df["department"], report_df["avg_rating"])
plt.title("Average Performance Rating by Department")
plt.xlabel("Department")
plt.ylabel("Avg Rating")
plt.savefig("reports/performance_chart.png")
plt.close()
