import conn
import random


class BankFunctions:
    def random(n):
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return int(random.random() * (range_end - range_start + 1)) + range_start

class Bank(BankFunctions):
    balance = 0
    def __init__(self):
        sql = "CREATE TABLE IF NOT EXISTS `users` (name VARCHAR(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,phone VARCHAR(20) NOT NULL,accNo BIGINT NOT NULL PRIMARY KEY,pass VARCHAR(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,securityQue VARCHAR(5000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,securityAns VARCHAR(5000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,balance BIGINT NOT NULL DEFAULT 0)"

        conn.cursor.execute(sql)
        conn.cursor.fetchall()
        conn.mydb.commit()

    def createAcc(self):
        print("____Welcome to the bank of Dhruv____")
        name = input("Enter your full name: ")
        while True:
            phone = input("Enter your phone number: ")
            if len(str(phone))<11:
                break
            else:
                print("-----Enter valid number!-----")

        accNo = BankFunctions.random(12)
        sql = "SELECT * FROM `users` WHERE accNo = %s"
        conn.cursor.execute(sql,(accNo,))
        conn.cursor.fetchall()
        conn.mydb.commit()
        if conn.cursor.rowcount != 0:
            accNo = BankFunctions.random(12)

        password = input("Enter your password: ")
        if password == "":
            print("Password should not be blank!")
            return
        cpassword = input("Re-enter your password: ")
        if password == cpassword:
            print("----Plz remember the security question and answer---")
            secQue = input("Enter security question: ")
            secAns = input("Enter security answer: ")
            sql_insert = "INSERT INTO `users` (name, phone, accNo, pass, securityQue, securityAns) VALUES (%s,%s,%s,%s,%s,%s)"
            val = (name, phone, accNo, password, secQue, secAns)
            conn.cursor.execute(sql_insert, val)
            conn.mydb.commit()
            print("----Account created successfully!----")
            print(f"Your account number is: {accNo}")
        else:
            print("----Your Password Does Not Match----")

    def login(self):
        accEnter = input("Enter Account number: ")
        passEnter = input("Enter password: ")
        sql = "SELECT * FROM `users` WHERE accNo = %s AND pass = %s"
        conn.cursor.execute(sql,(accEnter,passEnter))
        fetchBal = conn.cursor.fetchall()
        conn.mydb.commit()
        if conn.cursor.rowcount != 0:
            self.balance = fetchBal[0][-1]
            self.acc = accEnter
            return True

    def withdraw(self):
        if self.login():
            sql = f"CREATE TABLE IF NOT EXISTS `bank`.`{'s' + self.acc}` (`id` INT NOT NULL AUTO_INCREMENT , `amount` VARCHAR(10000) NOT NULL , `time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP , `fees` INT NOT NULL , PRIMARY KEY (`id`))"

            conn.cursor.execute(sql)
            conn.cursor.fetchall()
            conn.mydb.commit()


            withdrawAmount = int(input("Enter the amount want to withdraw: "))
            if withdrawAmount > 50000:
                print("Withdrawal amount is 50,000 which is exceeds!")
            else:
                if withdrawAmount > self.balance:
                    print("Insufficient balance.")
                    print(f"Available balance Rs.{self.balance}")
                else:
                    sql = f"UPDATE `users` SET balance = {self.balance-withdrawAmount} WHERE accNo = {self.acc}"
                    conn.cursor.execute(sql)
                    conn.cursor.fetchall()
                    conn.mydb.commit()
                    print("Withdrawal successful.")
                    print(f"Available balance Rs.{self.balance-withdrawAmount}")


                    sql = f"INSERT INTO `s{self.acc}` (amount, time, fees) VALUES (%s,current_timestamp(),%s)"
                    vals = (str("-"+str(withdrawAmount)),20)
                    conn.cursor.execute(sql,vals)
                    conn.cursor.fetchall()
                    conn.mydb.commit()
        else:
            print("----Invalid account number or password!----")

    def deposit(self):
        if self.login():
            sql = f"CREATE TABLE IF NOT EXISTS `bank`.`{'s' + self.acc}` (`id` INT NOT NULL AUTO_INCREMENT , `amount` VARCHAR(10000) NOT NULL , `time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP , `fees` INT NOT NULL , PRIMARY KEY (`id`))"
            conn.cursor.execute(sql)
            conn.cursor.fetchall()
            conn.mydb.commit()


            depositAmount = int(input("Enter the amount want to deposit: "))
            if depositAmount > 50000:
                print("Deposit amount is 50,000 which is exceeds!")
            else:
                if depositAmount < 0:
                    print("Deposit Amount Cannot Be Negative!")
                else:
                    sql = f"UPDATE `users` SET balance = {self.balance+depositAmount} WHERE accNo = {self.acc}"
                    conn.cursor.execute(sql)
                    conn.cursor.fetchall()
                    conn.mydb.commit()
                    print("Deposit successful.")
                    print(f"Available balance Rs.{self.balance+depositAmount}")


                    sql = f"INSERT INTO `s{self.acc}` (amount, time, fees) VALUES (%s,current_timestamp(),%s)"
                    vals = (str("+"+str(depositAmount)),20)
                    conn.cursor.execute(sql,vals)
                    conn.cursor.fetchall()
                    conn.mydb.commit()
        else:
            print("----Invalid account number or password!----")
    def statement(self):
        if self.login():
            sql = f"SELECT * FROM `s{self.acc}`"
            conn.cursor.execute(sql)
            data = conn.cursor.fetchall()
            conn.mydb.commit()

            print(f"{'ID':<5} {'Amount':<10} {'Time':<20} {'Fees':<5}")
            print("="*44)

            for row in data:
                id_, value, timestamp, count = row
                timestamp_str = str(timestamp)[:20]
                print(f"{id_:<5} {value:<10} {timestamp_str:<20} {count:<5}")

        else:
            print("----Invalid account number or password!----")

    def forgetPass(self):
        fAccName = int(input("Enter your account number: "))
        sql = "SELECT * FROM `users` WHERE accNo = %s"
        conn.cursor.execute(sql,(fAccName,))
        fetchBal = conn.cursor.fetchall()
        print(fetchBal[0][-3])
        ans = fetchBal[0][-2]
        getAns = input("Enter security answer: ")
        if ans == getAns:
            password = input("Enter your new password: ")
            cpassword = input("Re-Enter your new password: ")
            if password == cpassword:
                sql = "UPDATE `users` SET pass = %s WHERE accNo = %s"
                conn.cursor.execute(sql, (password, fAccName))
                # conn.cursor.execute(sql)
                conn.cursor.fetchall()
                conn.mydb.commit()

        else:
            print("---Answer is wrong!---")

        conn.mydb.commit()
#Main
dhruv = Bank()
print("----Features Offered By Bank Of Dhruv----")
print("1 for create account\n2 for withdraw\n3 for deposit\n4 for statement\n5 for Forget password")
choice = int(input("Enter Your Choice: "))
if choice == 1:
    dhruv.createAcc()
elif choice == 2:
    dhruv.withdraw() 
elif choice == 3:
    dhruv.deposit() 
elif choice == 4:
    dhruv.statement() 
elif choice == 5:
    dhruv.forgetPass() 
else:
    print("Invalid Input!") 
# dhruv.forgetPass()

