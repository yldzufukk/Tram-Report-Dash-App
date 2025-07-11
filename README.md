# 🚋 TRAMS Daily, Weekly, Monthly Kilometers and Power Reports

This project is designed to generate **daily**, **weekly**, and **monthly** reports for trams, including **distance traveled (in kilometers)** and **power consumption** metrics. It's ideal for transportation analytics, energy monitoring, and performance insights.

---

## 🔧 Setup Instructions

### 1. Database Configuration

Open the `reportDaily.py`, `reportWeekly.py`, `reportMonthly.py` file and locate the database connection block. Replace the placeholders with your actual database credentials:

```python
conn = mysql.connector.connect(
    host="your_database_host",
    port=your_database_port,        
    user="your_database_user",    
    password="your_database_password",       
    database=self.database
)
```

### 2. Run the Script
Once you've saved your database details, run the script via terminal:
```python
python main.py
```
The script will automatically generate the reports and output the results.

### 📁 Output
Daily Kilometer & Power Report

Weekly Kilometer & Power Report

Monthly Kilometer & Power Report

All reports are structured and can be exported to CSV, Excel, or any desired format with minor modifications.

### 🧱 Requirements
Python 3.x

mysql-connector-python

You can install the required library using:
```python
pip install mysql-connector-python
```


## 📸 Screenshots
### 🖼️ Main Dashboard
<img width="1920" height="1080" alt="Main Dashboard" src="https://github.com/user-attachments/assets/7798f9d4-8c6c-48bb-90ad-e0369a2b0140" />

### 📊 Weekly Report Sample
<img width="1908" height="903" alt="1" src="https://github.com/user-attachments/assets/67d1b208-36f7-460c-96f6-03ed7fbe5b03" />


### ⚡ Monthly Power Report
<img width="1920" height="1080" alt="Monthly Power Report" src="https://github.com/user-attachments/assets/68e3b404-3a40-4553-b94b-47388c43c26f" />

### DEMO


https://github.com/user-attachments/assets/2d5e89d4-c995-4738-94dd-52fa536c20c7





📬 Contact
For any questions or improvements, feel free to open an issue or submit a pull request.

