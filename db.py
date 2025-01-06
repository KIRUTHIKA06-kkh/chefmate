import mysql.connector

print('starting')
try:
    mydb = mysql.connector.connect(
       host = 'finaldb.c3i8ggm6665z.ap-south-1.rds.amazonaws.com',
       port = 3306,
       user = 'admin',
       password = '')
    print("connected")
    
except:
    print('not connected')

print('end')