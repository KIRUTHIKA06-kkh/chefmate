import mysql.connector
from dotenv import load_dotenv
import os
print('starting')
load_dotenv()
try:
    mydb = mysql.connector.connect(
       host = 'chefmatedb.cvwcymg00994.ap-south-1.rds.amazonaws.com',
       port = 3306,
       user = 'admin',
       password = os.getenv('passworddb'))

    print("connected")
    
except:
    print('not connected')

print('end')

