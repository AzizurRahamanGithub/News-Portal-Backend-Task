import psycopg2

connection = None  # Define connection here to avoid NameError

try:
    connection = psycopg2.connect(
        host="grativid.cx86qs4wcg48.us-east-2.rds.amazonaws.com",
        database="grativid",
        user="postgres",
        password="gratividpostgres",  # Make sure to put your actual password here
        port="5432",
        connect_timeout=30  # Set connection timeout to 30 seconds
    )
    print("Connection successful")
except Exception as e:
    print("Error connecting to database:", e)
finally:
    if connection:
        connection.close()
