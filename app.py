import functions


while True:
        print("Have you registered? y/n")
        registration = input()
        if registration == "n":
            functions.insert_hacker()
        elif registration == "y":
            alias = input("Please type your alias: ")
            password = input("Please type your password: ")
            if(len(password) < 6):
                print("Password too short!")
            elif functions.login_check(alias, password) == False:
                print("Sorry, your alias/password is not correct, please try it again.")
            elif functions.login_check(alias, password):
                while True:
                    print("Hi " + alias + ", please select from the following options: ")
                    print("1: Write a new exploit")
                    print("2: See all of your exploits")
                    print("3: see other hackers' exploits")
                    print("4: modify your exploit")
                    print("5: log out")
                    userSelection = input()
                    if userSelection == "1":
                        print("Please write a new exploit:")
                        content = input()
                        functions.create_exploit(alias, password, content)

                    elif userSelection == "2":
                        functions.get_hacker_exploits(alias, password)

                    elif userSelection == "3":
                        functions.get_other_hackers_exploits(alias)

                    elif userSelection == "4":
                        functions.modify_hacker_exploits(alias, password)
                        
                    if functions.exit_check():
                        print("Goodbye!")
                        break
                    elif userSelection == "5":
                        functions.exit_check()
                        print("Goodbye!")
                        break
                break