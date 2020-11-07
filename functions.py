import dbcreds
import mariadb

def insert_hacker():
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
        cursor = conn.cursor()
        alias = input("Please type your username: ")
        password = input("Please type your password: ")
        if(len(password) < 6):
            print("Password too short!")
        else:
            cursor.execute("INSERT INTO hackers(alias, password) VALUES(?, ?)", [alias, password])
            conn.commit()
        if(cursor.rowcount == 1):
            print("Congrats, hacker created!")
        else:
            print("Shame, hacker not created!")
    except mariadb.ProgrammingError:
        print("You need lessons.")
    except mariadb.OperationalError:
        print("There seems to be something wrong with the connection.")
    finally:
        if(cursor != None):
            cursor.close()
        if(conn != None):
            conn.rollback()
            conn.close()

def login_check(alias, password):
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM hackers WHERE alias=? AND password=?", [alias, password])
        hackers = cursor.fetchall()
        for hacker in hackers:
            if alias == hacker[0] and password == hacker[1]:
                return True
        return False
    except mariadb.ProgrammingError:
        print("You need lessons.")
    except mariadb.OperationalError:
        print("There seems to be something wrong with the connection.")
    finally:
        if(cursor != None):
            cursor.close()
        if(conn != None):
            conn.rollback()
            conn.close()

def create_exploit(alias, password, content):
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM hackers WHERE alias =? AND password =?", [alias, password])
        row = cursor.fetchone()
        id = row[2]
        cursor.execute("INSERT INTO exploits(content, user_id) VALUES (?, ?)", [content, id])
        conn.commit()
        if(cursor.rowcount == 1):
            print("Congrats, exploit has been created!")
        else:
            print("Shame, exploit has not been created!")
    except mariadb.ProgrammingError:
        print("You need lessons.")
    except mariadb.OperationalError:
        print("There seems to be something wrong with the connection.")
    finally:
        if(cursor != None):
            cursor.close()
        if(conn != None):
            conn.rollback()
            conn.close()

def get_hacker_exploits(alias, password):
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM exploits INNER JOIN hackers ON alias=? AND password=? AND exploits.user_id = hackers.id", [alias, password])
        contents = cursor.fetchall()
        for content in contents:
            print(content[1])

    except mariadb.ProgrammingError:
        print("You need lessons.")
    except mariadb.OperationalError:
        print("There seems to be something wrong with the connection.")
    finally:
        if(cursor != None):
            cursor.close()
        if(conn != None):
            conn.rollback()
            conn.close()

def get_other_hackers_exploits(alias):
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM exploits INNER JOIN hackers ON exploits.user_id = hackers.id")
        rows = cursor.fetchall()
        for row in rows:
            if alias != row[3]:
                print(row[3])
                print(row[1])
            else:
                pass
    except mariadb.ProgrammingError:
        print("You need lessons.")
    except mariadb.OperationalError:
        print("There seems to be something wrong with the connection.")
    finally:
        if(cursor != None):
            cursor.close()
        if(conn != None):
            conn.rollback()
            conn.close()

def modify_hacker_exploits(alias, password):
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM hackers WHERE alias =? AND password =?", [alias, password])
        row = cursor.fetchone()
        id = row[2]
        cursor.execute("SELECT * FROM exploits WHERE user_id=?", [id])
        old_contents = cursor.fetchall()
        for old_content in old_contents:
            print(old_content[0])
            print(old_content[1])              
        pick_id = input("Please type id of exploits you would like to modify: ")
        print("Please type your new exploit:")
        new_content = input()                           
        cursor.execute("UPDATE exploits SET content=? WHERE id=?", [new_content, pick_id])
        conn.commit()
        if(cursor.rowcount == 1):
            print("Congrats, exploit has been updated!")
        else:
            print("Shame, exploit has not been updated!")
        print(row[0])
        cursor.execute("SELECT * FROM exploits WHERE user_id=?", [id])
        updated_contents = cursor.fetchall()
        for updated_content in updated_contents:
            print(updated_content[1])
    except mariadb.ProgrammingError:
        print("You need lessons.")
    except mariadb.OperationalError:
        print("There seems to be something wrong with the connection.")
    finally:
        if(cursor != None):
            cursor.close()
        if(conn != None):
            conn.rollback()
            conn.close()
    
def exit_check():
    check = input("would you like to continue? y/n: ")
    if check == "n":
        return True
    elif check == "y":
        return False

    
        