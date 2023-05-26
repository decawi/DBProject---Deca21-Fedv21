from datetime import date
import os
import project
from tabulate import tabulate 

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
        firstPage()

def newUser():
    os.system('cls')

    print("Create new user")

    name = input("Name: ")
    email = input("Email: ")
    memberType = input("Membertype (Student|Senior|None): ")
    joined = date.today()

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
    while True:
        try:
            email = input("Email: ")
            id_fetch = project.session.sql(f"select uniqueID from customers where mail = '{email}';").execute()
            for i in id_fetch.fetch_one():
                id = str(i)
            break
        except:
            print("Wrong email or email is not in database")
            continue
    mainPage(id)

def mainPage(id):
    os.system('cls')

    print("Menu")
    print("____")
    print("1 Products\n2 Discounts\n3 Cart\n4 Favorites")
    
    if id == "1":
        print("5 Admin")
        adminMenu(id)
    else:
        choice = int(input("(1|2|3|4): "))

        if choice == 1:
            products(id)
        elif choice == 2:
            discounts(id)
        elif choice == 3:
            cart(id)
        elif choice == 4:
            favorites(id)
        else:
            print("Invalid input!")
            mainPage(id)

def adminMenu(id):
    while True:
        choice = int(input("(1|2|3|4|5): "))
        if str(choice) not in ("(1|2|3|4|5)"):
            print("not valid inpuT")
            continue
        else:
            break

    if choice == 1:
        products(id)
    elif choice == 2:
        discounts(id)
    elif choice == 3:
        cart(id)
    elif choice == 4:
        favorites(id)
    elif choice == 5:
        adminPage(id)
    else:
        print("Invalid input!")
        
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
    while True:
        addremove = input("(1|2|3): ")
        if str(addremove) not in "123 Exit":
            continue
        else:
            break

    if addremove == "Exit":
        adminPage(id)

    elif addremove == "1":
        print("Remove item")
        print("Write ID for item you want removed")
        while True:
            remove = input("ID: ")
            if remove != int:
                continue
            else:
                break
        project.session.sql(f"delete from inventory where prodID = '{remove}';").execute()

    elif addremove == "2":
        print("Add item")
        prodID = input("Product ID: ")
        prodName = input("Product Name: ")
        category = input("Product Category: ")
        price = input("Product Price: ")
        available = input("Products available: ")
        project.session.sql(f"insert into inventory (prodID, prodName, category, price, available) "\
        f"values ({prodID},'{prodName}', '{category}', {price}, {available});").execute()

    elif addremove == "3":
        print("Update item")
        itemID = input("ID for item: ")
        column = input("What column should be updated: ")
        update = input("Update: ")
        project.session.sql(f"UPDATE inventory SET {column} = '{update}' WHERE prodID = {itemID}").execute()

    adminInventory(id)

def adminDiscounts(id):
    os.system('cls')

    discount_fetch =  project.session.sql("select * from discounts").execute()

    for item in discount_fetch.fetch_all():
        output = ' | '.join(map(str, item))
        output = output.replace("(", "").replace(")", "").replace("Decimal", "")
        print(output)

    print("1 Remove discount\n2 Add discount\n3 Update discount")
    print("Type Exit to go back")
    while True:
        addremove = (input("(1|2|3): "))
        if addremove not in "123 Exit":
            continue
        else:
            break
    if addremove == "Exit":
        adminPage(id)

    elif addremove == "1":
        print("Remove discount")
        print("Write ID for the discount you want removed")
        remove = input("ID: ")
        project.session.sql(f"delete from discounts where discountID = '{remove}';").execute()

    elif addremove == "2":
        print("Add discount")
        prodID = input("Product ID: ")
        prodName = input("Product Name: ")
        category = input("Product Category: ")
        discount = input("Discount : ")
        memberType = input("Membertype: ")
        project.session.sql(f"insert into discounts (prodID, prodName, category, discount, memberType) "\
        f"values ({prodID},'{prodName}', '{category}', {discount}, '{memberType}');").execute()

    elif addremove == "3":
        print("Update item")
        discountID = input("ID for discount ")
        column = input("What column should be updated: ")
        update = input("Update: ")
        project.session.sql(f"UPDATE discounts SET {column} = '{update}' WHERE discountID = {discountID}").execute()

    adminDiscounts(id)

def adminMailinglist(id):
    os.system('cls')

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

            itemID = project.session.sql(f"select prodID from inventory where prodName = '{itemName}'").execute()
            for k in itemID.fetch_one():
                itemID = k

            temp = [cartList, str(itemID)]
            newCart = ", ".join(temp)
            project.session.sql(f"UPDATE cart SET prodList = '{newCart}' WHERE uniqueID = {id}").execute()

        elif x[1] == "2":
            favList = project.session.sql(f"select favoriteProd from customers where uniqueID = {id}").execute()
            for item in favList.fetch_one():
                favList = item

            itemID = project.session.sql(f"select prodID from inventory where prodName = '{itemName}'").execute()
            for k in itemID.fetch_one():
                itemID = k

            temp = [favList, str(itemID)]
            newFav = ", ".join(temp)

            project.session.sql(f"UPDATE customers SET favoriteProd = '{newFav}' WHERE uniqueID = {id}").execute()

        products(id)

def discounts(id):
    os.system('cls')

    discount_query = "SELECT discounts.prodName, discounts.discount "\
    "FROM customers "\
    "LEFT JOIN discounts "\
    "    ON discounts.memberType LIKE CONCAT('%', customers.memberType, '%') "\
    "    or discounts.memberType = 'none'"\
    f"WHERE uniqueID = {id};"
    
    print("Discounts")
    discount_fetch =  project.session.sql(discount_query).execute()
    for item in discount_fetch.fetch_all():
        output = ' | '.join(map(str, item))
        output = output.replace("(", "").replace(")", "").replace("Decimal", "")
        print(output)

    back = input("Exit to go back: ")
    if back == "Exit" or back == "exit":
        mainPage(id)

def cart(id):
    os.system('cls')

    cartList = project.session.sql(f"select prodList from cart where uniqueID = {id}").execute()
    for item in cartList.fetch_one():
        cartList = item

    check_price = project.session.sql(f"call CheckCart({id})").execute()
    tabulateList = []

    for row in check_price.fetch_all():
        output = ' '.join(map(str, row))
        output = output.replace("(", "").replace(")", "").replace("Decimal", "")
        tabulateList.append(output.split())

    print (tabulate(tabulateList, headers=["Product", "Price", "Quantity"]))
    print("Cart")
    x = cartList.replace(",", "").split()
    remove = input("Remove product(Name of product) exit to go back: ")

    if remove == "Exit":
        mainPage(id)

    removeID = project.session.sql(f"select prodID from inventory where prodName = '{remove}'").execute()
    for item in removeID.fetch_one():
        removeID = str(item)

    if removeID in x:
        tempstring = cartList.replace(f"{removeID}", "", 1).replace(" ,", "")
        tempstring = tempstring.replace(',', '', 1) if tempstring.startswith(',') else tempstring

        project.session.sql(f"UPDATE cart SET prodList = '{tempstring}' WHERE uniqueID = {id}").execute()
        cart(id)

def favorites(id):
    os.system('cls')

    itemList = project.session.sql(f"select favoriteProd from customers where uniqueID = {id}").execute()
    for item in itemList.fetch_one():
        itemList = item

    check_fav = project.session.sql(f"call CheckFav({id})").execute()
    tabulateList = []
    for row in check_fav.fetch_all():
        output = ' '.join(map(str, row))
        output = output.replace("(", "").replace(")", "").replace("Decimal", "")
        tabulateList.append(output.split())

    print (tabulate(tabulateList, headers=["Product", "Price", "Quantity"]))

    print("favorites")

    x = itemList.replace(",", "").split()
    remove = input("Remove product(Name of product) exit to go back: ")
    
    if remove == "Exit":
        mainPage(id)
    
    removeID = project.session.sql(f"select prodID from inventory where prodName = '{remove}'").execute()
    for item in removeID.fetch_one():
        removeID = str(item)

    print("removeID", removeID)

    if removeID in x:
        tempstring = itemList.replace(f"{removeID}", "", 1).replace(" ,", "")
        tempstring = tempstring.replace(',', '', 1) if tempstring.startswith(',') else tempstring
        
        project.session.sql(f"UPDATE customers SET favoriteProd = '{tempstring}' WHERE uniqueID = {id}").execute()
        favorites(id)

firstPage()