import dbcreds
import mariadb

def login_check(alias, password):
    cursor.execute("SELECT * FROM hackers WHERE alias=? AND password=?", [alias, password])
    hackers = cursor.fetchall()
    for hacker in hackers:
        if alias == hacker[0] and password == hacker[1]:
            return True
    return False

def exit_check():
    check = input("would you like to continue? y/n: ")
    if check == "n":
        return True
    elif check == "y":
        return False

def insert_hacker():
    alias = input("Please type your username: ")
    password = input("Please type your password: ")
    cursor.execute("INSERT INTO hackers(alias, password) VALUES(?, ?)", [alias, password])
    conn.commit()

conn = None
cursor = None
try:
    conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
    cursor = conn.cursor()
    while True:
        print("Have you registered? y/n")
        registration = input()
        if registration == "n":
            insert_hacker()
        elif registration == "y":
            alias = input("Please type your alias: ")
            password = input("Please type your password: ")
            if(len(password) < 6):
                print("Password too short!")
            elif login_check(alias, password) == False:
                print("Sorry, your alias/password is not correct, please try it again.")
            elif login_check(alias, password):
                while True:
                    print("Hi " + alias + ", please select from the following options: ")
                    print("1: Write a new exploit")
                    print("2: See all of your exploits")
                    print("3: see other hackers' exploits")
                    print("4: modify your exploit")
                    userSelection = input()
                    if userSelection == "1":
                        content = input("Please write a new exploit: ")
                        cursor.execute("SELECT * FROM hackers WHERE alias =? AND password =?", [alias, password])
                        row = cursor.fetchone()
                        id = row[2]
                        cursor.execute("INSERT INTO exploits(content, user_id) VALUES (?, ?)", [content, id])
                        conn.commit()
                        if(cursor.rowcount == 1):
                            print("Congrats, exploit has been created!")
                        else:
                            print("Shame, exploit has not been created!")

                    elif userSelection == "2":
                        cursor.execute("SELECT * FROM exploits INNER JOIN hackers ON alias=? AND exploits.user_id = hackers.id", [alias,])
                        contents = cursor.fetchall()
                        for content in contents:
                            print(content[1])
            
                    elif userSelection == "3":
                        cursor.execute("SELECT * FROM exploits INNER JOIN hackers ON exploits.user_id = hackers.id")
                        rows = cursor.fetchall()
                        for row in rows:
                            if alias != row[3]:
                                print(row[1])
                            # else:
                            #     print("Sorry, results don't match!")
                    elif userSelection == "4":
                        cursor.execute("SELECT * FROM hackers WHERE alias =? AND password =?", [alias, password])
                        row = cursor.fetchone()
                        id = row[2]
                        pick_content = ""
                        cursor.execute("SELECT * FROM exploits WHERE user_id=?", [id])
                        contents = cursor.fetchall()
                        print(contents)
                        new_content = input("Please type your new exploit: ")
                        pick_id = input("Please type id of exploits you would like to modify: ")
                        for content in contents:
                            if int(pick_id) == content[0]:
                                pick_content = content[1]                             
                                # print(pick_content)
                                cursor.execute("UPDATE exploits SET content=? WHERE content=? AND user_id=?", [new_content, pick_content, id])
                                conn.commit()
                            else:
                                pass
                        if(cursor.rowcount == 1):
                            print("Congrats, exploit has been updated!")
                        else:
                            print("Shame, exploit has not been updated!")
                        print(row[0])
                        cursor.execute("SELECT * FROM exploits WHERE user_id=?", [id])
                        updated_contents = cursor.fetchall()
                        for updated_content in updated_contents:
                            print(updated_content[1])

                        if exit_check():
                            print("Goodbye!")
                            break
                break

except mariadb.ProgrammingError:
    print("You need lessons.")
except mariadb.OperationalError:
    print("There seems to be something wrong with the connection.")
# except:
#     print("This is lazy. Bad error catching.")
finally:
    if(cursor != None):
        cursor.close()
    if(conn != None):
        conn.rollback()
        conn.close()

print("Woah, that was dangerous! Stay frosty.")