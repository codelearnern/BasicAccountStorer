import sqlite3
import hashlib
import binascii
import os
 
def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')
 
def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

accountYesNo = input("Do you already have a master password? ")

if accountYesNo.lower() == "no":
    print("Alright then, what do you want your master password to be?")
    newMasterpwd = input()
    with open("masterpwd.txt", "w") as f:
        f.write(hash_password(newMasterpwd))
        f.close()
    print("Your done, run the program again to start storing accounts.")

elif accountYesNo.lower() == "yes":
    print("Then type in your master password")
    masterpwd = input()
    masterPwdFile = open("masterpwd.txt", "r") 
    if verify_password(masterPwdFile.readline(), masterpwd):
        print("loading...")
        conn = sqlite3.connect("account.db")

        c = conn.cursor()
        try:
            c.execute("""CREATE TABLE accounts (
                product text,
                uname text,
                pwd text
            )""")
            conn.commit()

            conn.close()
            print("Run the program again to start storing accounts.")
        except:
            InsertAccount = input("Ok, do you want to insert a new account? ")
            if InsertAccount.lower() == "yes":
                print("Type in your account info.")
                productName = input("What is the name of the product? ")
                uname = input("What is the username? ")
                pwd = input("What is the password? ")

                c.execute("INSERT INTO accounts VALUES (?, ?, ?)", (productName, uname, pwd))
                conn.commit()
                print("Ok, your account has been stored")

                c.execute("SELECT * FROM accounts")

                print("Here is all the accounts you have stored.")

                print("Product, Username, Password")
                for i in c.fetchall():
                    print(i[0], i[1], i[2], sep=", ")
                    
                conn.commit()

                conn.close()
            else:
                print("Here is all the accounts you have stored.")
                c.execute("SELECT * FROM accounts")
                print("Product, Username, Password")
                for i in c.fetchall():
                    print(i[0], i[1], i[2], sep=", ")

                conn.commit()

                conn.close()
        
    else:
        print("You entered the wrong master password, run the program again and enter the right password.")
    masterPwdFile.close()