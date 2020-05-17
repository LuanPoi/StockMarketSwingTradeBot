import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="toor"
)

print(mydb)

mycursor = mydb.cursor()

sql = "INSERT INTO stock (ticker, date, open, high, low, close, adj_close, volume) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
val = ("John", "Highway 21")
mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")


#print("Indice ["+str(index)+"]: ", end="")
        #print(dayStockValue['Open'], dayStockValue['High'], dayStockValue['Low'], dayStockValue['Close'], dayStockValue['Adj Close'], dayStockValue['Volume'], sep="\t")