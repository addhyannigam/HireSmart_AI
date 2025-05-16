import pymysql

# Database connection parameters (must match Workbench)
config = {
    'host': 'localhost',
    'port': 3306,  # Explicitly add port
    'user': 'root',
    'password': 'Addy@123',  # Must match what you set in Workbench
    'database': 'cv',
    'charset': 'utf8mb4'
}

connection = None

try:
    # Establish connection
    connection = pymysql.connect(**config)
    cursor = connection.cursor()
    
    # Test connection
    cursor.execute("SELECT DATABASE()")
    db_name = cursor.fetchone()[0]
    print(f"✅ Successfully connected to database: {db_name}")
    
    # Your application code here...
    
except pymysql.Error as e:
    print(f"❌ Connection failed: {e}")
finally:
    if connection:
        connection.close()

"""
mysql --version
sudo apt update sudo apt install mysql-server
sudo systemctl status mysql
sudo mysql_secure_installation
"""
