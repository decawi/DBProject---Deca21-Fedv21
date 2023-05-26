from datetime import date
import os
import project 
# Connect to server on localhost

def firstPage():
    os.system('cls')
    print("1 New User")
    print("2 Login")
    userInput = int(input("(1|2):"))
    if userInput == 1:
        newUser()
    elif userInput == 2:
        login()
    else:
        print("Invalid input!")
        testing = input("Press enter to return")
        firstPage()

def newUser():
    os.system('cls')
    id = 1 #testing
    print("Create new user")
    name = input("Name: ")
    email = input("Email: ")
    memberType = input("Membertype (Student|Senior|None): ")
    joined = date.today()
    #add to database with sql get id
    insert_a_customer = f"insert into customers (customerName, mail, memberType, joindate) "\
    f"values ('{name}', '{email}', '{memberType}', '{joined}');"
    project.session.sql(insert_a_customer).execute()
    id_fetch = project.session.sql(f"select uniqueID from customers where mail = '{email}';").execute()
    for i in id_fetch.fetch_one():
            id = str(i)
    mainPage(id)

def login():
    os.system('cls')
    print("Login")
    try:
        email = input("Email: ")
        id_fetch = project.session.sql(f"select uniqueID from customers where mail = '{email}';").execute()
        for i in id_fetch.fetch_one():
            id = str(i)
    except:
        print("Wrong email or email is not in database")
    
    #getid
    #check email against database!
    #try get id if not print invalid user
    #if ok mainPage(id)
    mainPage(id)

def mainPage(id):
    os.system('cls')
    print("Menu")
    print("____")
    print("1 Products\n2 Discounts\n3 Cart")
    
    if id == "1":
        print("4 Admin")
        adminMenu(id)
    else:
        choice = int(input("(1|2|3): "))
        if choice == 1:
            products(id)
        elif choice == 2:
            discounts(id)
        elif choice == 3:
            cart(id)
        else:
            print("Invalid input!")
            testing = input("Press enter to return")
            mainPage(id)

def adminMenu(id):
    choice = int(input("(1|2|3|4): "))
    if choice == 1:
        products(id)
    elif choice == 2:
        discounts(id)
    elif choice == 3:
        cart(id)
    elif choice == 4:
        adminPage(id)
    else:
        print("Invalid input!")
        testing = input("Press enter to return")
        mainPage(id)

def adminPage(id):
    os.system('cls')
    print("Admin Page")
    print("1 Change inventory\n2 Change discount\n3 Check mailinglist")
    print("Type Exit to go back")
    cartFav = input("Input: ")
    if cartFav == "Exit":
        mainPage(id)
    elif cartFav == "1":
        adminInventory(id)
    elif cartFav == "2":
        adminDiscounts(id)
    elif cartFav == "3":
        adminMailinglist(id)
    
def adminInventory(id):
    os.system('cls')
    inventory = project.session.sql("select * from inventory").execute()
    for item in inventory.fetch_all():
        output = ' | '.join(map(str, item))
        output = output.replace("(", "").replace(")", "").replace("Decimal", "")
        print(output)
    print("1 Remove items\n2 Add item\n3 Update item")
    print("Type Exit to go back")
    addremove = input("(1|2|3): ")
    if addremove == "Exit":
        adminPage(id)
    elif addremove == "1":
        print("Remove item")
        print("Write ID for item you want removed")
        remove = input("ID: ")
        #sql
        project.session.sql(f"delete from inventory where prodID = '{remove}';").execute()
    elif addremove == "2":
        print("Add item")
        prodID = input("Product ID: ")
        prodName = input("Product Name: ")
        category = input("Product Category: ")
        price = input("Product Price: ")
        available = input("Products available: ")
        #sql insert
        project.session.sql(f"insert into inventory (prodID, prodName, category, price, available) "\
        f"values ({prodID},'{prodName}', '{category}', {price}, {available});").execute()
    elif addremove == "3":
        print("Update item")
        itemID = input("ID for item: ")
        column = input("What column should be updated: ")
        update = input("Update: ")
        #Update sql
        project.session.sql(f"UPDATE inventory SET {column} = '{update}' WHERE prodID = {itemID}").execute()
    adminInventory(id)

def adminDiscounts(id):
    #sql select * from discounts
    discount_fetch =  project.session.sql("select * from discounts").execute()
    for item in discount_fetch.fetch_all():
        output = ' | '.join(map(str, item))
        output = output.replace("(", "").replace(")", "").replace("Decimal", "")
        print(output)

    print("1 Remove discount\n2 Add discount\n3 Update discount")
    print("Type Exit to go back")
    addremove = (input("(1|2|3): "))
    if addremove == "Exit":
        adminPage(id)
    elif addremove == "1":
        print("Remove discount")
        print("Write ID for the discount you want removed")
        remove = input("ID: ")
        #sql
        project.session.sql(f"delete from discounts where discountID = '{remove}';").execute()
    elif addremove == "2":
        print("Add discount")
        prodID = input("Product ID: ")
        prodName = input("Product Name: ")
        category = input("Product Category: ")
        discount = input("Discount : ")
        memberType = input("Membertype: ")
        #sql insert
        project.session.sql(f"insert into discounts (prodID, prodName, category, discount, memberType) "\
        f"values ({prodID},'{prodName}', '{category}', {discount}, '{memberType}');").execute()
    elif addremove == "3":
        print("Update item")
        discountID = input("ID for discount ")
        column = input("What column should be updated: ")
        update = input("Update: ")
        #Update sql
        project.session.sql(f"UPDATE discounts SET {column} = '{update}' WHERE discountID = {discountID}").execute()
    adminDiscounts(id)

def adminMailinglist(id):
    #sql mailing list
    for item in project.mailing_list_result.fetch_all():
        output = ' | '.join(map(str, item))
        output = output.replace("(", "").replace(")", "").replace("Decimal", "")
        print(output)
    back = input("Type Exit to go back: ")
    if back == "Exit":
        adminPage(id)

def products(id):
    os.system('cls')
    
    product_fetch =  project.session.sql("select prodName, category, price, available from inventory").execute()
    for item in product_fetch.fetch_all():
        output = ' | '.join(map(str, item))
        output = output.replace("(", "").replace(")", "").replace("Decimal", "")
        print(output)
    print("Products")
    print("Type Item name and 1(itemname 1) to add to cart")
    print("Type Item name and 2(itemname 2) to add to favorites")
    print("Type Exit to go back")
    cartFav = input("Input: ")
    if cartFav == "Exit":
         mainPage(id)
    else:
        x = cartFav.split()
        itemName = x[0]
        if x[1] == "1":

            cartList = project.session.sql(f"select prodList from cart where uniqueID = {id}").execute()
            for item in cartList.fetch_one():
                cartList = item

            itemID = project.session.sql(f"select prodID from inventory where prodName = '{itemName}'").execute
            for k in itemID.fetch_one():
                itemID = k

            temp = [cartList, itemID]
            newCart = ", ".join(temp)



            project.session.sql(f"UPDATE cart SET prodList = '{newCart}' WHERE uniqueID = {id}").execute()

        elif x[1] == "2":
            favList = project.session.sql(f"select favoriteProd from customers where uniqueID = {id}").execute()
            for item in favList.fetch_one():
                favList = item

            itemID = project.session.sql(f"select prodID from inventory where prodName = '{itemName}'").execute
            for k in itemID.fetch_one():
                itemID = k

            temp = [favList, itemID]
            newFav = ", ".join(temp)

            project.session.sql(f"UPDATE cart SET favoriteProd = '{newFav}' WHERE uniqueID = {id}").execute()
        #category ------------------------
        products(id)

def discounts(id):
    os.system('cls')
    print("Discounts")
    discount_fetch =  project.session.sql("select * from discounts").execute()#ändra till funktionen byggd av felix
    for item in discount_fetch.fetch_all():
        output = ' | '.join(map(str, item))
        output = output.replace("(", "").replace(")", "").replace("Decimal", "")
        print(output)
    back = input("Exit to go back: ")
    if back == "Exit":
        mainPage(id)

def cart(id):
    os.system('cls')
    cartList = project.session.sql(f"select prodList from cart where uniqueID = {id}").execute()
    for item in cartList.fetch_one():
        cartList = item
    #check cart
    #project.session("call checkcart({id})").execute
    print("Cart")
    remove = input("Remove product(Name of product) exit to go back: ")
    if remove == "Exit":
        mainPage(id)

    elif remove in cartList:
        #cartList = sträng hantering kolla output remove "remove"
        project.session.sql(f"UPDATE cart SET prodList = '{cartList}' WHERE uniqueID = {id}").execute()
        testing = input("...")
        cart(id)

products(1)
#firstPage()