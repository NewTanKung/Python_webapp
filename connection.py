import pyodbc

connect = pyodbc.connect("DRIVER={SQL Server}; SERVER=NEWTAN\SQLEXPRESS; DATABASE=iStockCoop;")

def connection_database():
    code = 0
    if connect:
        print("Connection Successful!")
        code = 1
        return code
    else:
        print("Connection failed")
        code = 0
        return code

def execute_data(query):
    
    corsur = connect.cursor()
    corsur.execute(query)
    row = corsur.fetchall()
    connect.commit()

    return row


def execute_data_insert(query):
    cursor = connect.cursor()
    cursor.execute(query)
    connect.commit()

    cursor.close()
    return 1