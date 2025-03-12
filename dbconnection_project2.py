import mysql.connector

host = 'localhost'  
user = 'root'      
password = '12345'  # Your MySQL password
database = 'project2'  # Name of the database you want to connect to

# Connect to MySQL

def dbwrite(query,data):
    conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
    )

    cursor = conn.cursor()
    print(query)
    cursor.executemany(query, data)
    conn.commit()
    cursor.close()
    conn.close()
    return

def dbread(query):
    conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
    )

    cursor = conn.cursor()
    print("query from dbread ::::"+query)
    cursor.execute(query)
    rows = cursor.fetchall()
    # column_names = [desc[0] for desc in cursor.description]
    # print(column_names)
    
    cursor.close()
    conn.close()
    return rows


def dbreadWithColumnNames(query):
    conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
    )

    cursor = conn.cursor()
    print("query from dbread ::::"+query)
    cursor.execute(query)
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    print(column_names)
    
    cursor.close()
    conn.close()
    return rows,column_names
