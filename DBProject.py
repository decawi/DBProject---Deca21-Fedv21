from datetime import date
import os
import project
from tabulate import tabulate 

def firstPage():
    #os.system('cls')

    print("1 New User")
    print("2 Login")
    while True:
        try:
            userInput = int(input("(1|2):"))
            break
        except ValueError:
            continue
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
    memberType = input("Membertype (Student|Senior|Guld): ")
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
    print("1 Products\n2 Discounts\n3 Cart\n4 Favorites\n5 Logout")
    
    if id == "1":
        print("6 Admin")
        adminMenu(id)
    else:
        while True:
            while True:
                try:
                    choice = int(input("(1|2|3|4|5): "))
                    break 
                except ValueError:
                    pass
            
            if str(choice) in "12345":
                break
            else:
                continue

        if choice == 1:
            products(id)
        elif choice == 2:
            discounts(id)
        elif choice == 3:
            cart(id)
        elif choice == 4:
            favorites(id)
        elif choice == 5:
            firstPage()
        else:
            print("Invalid input!")
            mainPage(id)

def adminMenu(id):
    while True:
        try:
            choice = int(input("(1|2|3|4|5|6): "))
        except ValueError:
            continue
        if str(choice) not in ("(1|2|3|4|5|6)"):
            print("not valid input")
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
    elif choice == 6:
        adminPage(id)
    elif choice == 5:
        firstPage()
    else:
        print("Invalid input!")
        
        mainPage(id)

def adminPage(id):
    os.system('cls')

    print("Admin Page")
    print("1 Change inventory\n2 Change discount\n3 Check mailinglist\n4 Check Customers\n5 Check all carts")
    print("Type Exit to go back")
    while True:
        cartFav = input("1|2|3|4|5: ")
        if str(cartFav) in "1|2|3|4|5 Exit":
            break
        continue


    if cartFav == "Exit":
        mainPage(id)
    elif cartFav == "1":
        adminInventory(id)
    elif cartFav == "2":
        adminDiscounts(id)
    elif cartFav == "3":
        adminMailinglist(id)
    elif cartFav == "4":
        adminCustomers(id)
    elif cartFav == "5":
        adminCart(id)

def adminCart(id):
    os.system('cls')

    cart = project.session.sql("select * from cart").execute()

    tabulateList = []
    for item in cart.fetch_all():
        tabulateList.append(item)

    print (tabulate(tabulateList, headers=["Customer ID", "Product List"]))
    
    print("Type Exit to go back")

    remove = input("Input: ")
    if remove == "Exit":
        adminPage(id)
    else:
        adminCart(id)

def adminCustomers(id):
    os.system('cls')

    customers = project.session.sql("select * from customers").execute()

    tabulateList = []
    for item in customers.fetch_all():
        tabulateList.append(item)

    print (tabulate(tabulateList, headers=["Customer ID", "Name", "Email","Member Type","Favorite Products", "Favorite Category", "Join Date"]))

    print("1 Remove Customer")
    print("Type Exit to go back")

    while True:
        remove = input("Input: ")
        if str(remove) not in "1 Exit":
            continue
        else:
            break
    
    if remove == "Exit":
        adminPage(id)
    elif remove == "1":
        print("Remove Customer")
        print("Write ID for customer you want removed")
        
        while True:
            try:
                remove = int(input("ID: "))
                break 
            except ValueError:
                pass
            
        project.session.sql(f"delete from customers where uniqueID = {remove}").execute()
        print("removed", remove)
        adminCustomers(id)
    
def adminInventory(id):
    os.system('cls')

    inventory = project.session.sql("select * from inventory").execute()
    tabulateList = []
    for item in inventory.fetch_all():
        tabulateList.append(item)

    print (tabulate(tabulateList, headers=["Product ID", "Name", "Price","Category","quantity"]))

    categories = project.session.sql("select category, sum(available) as total from inventory group by category").execute()
    tabulateCategories = []
    for item in categories.fetch_all():
        tabulateCategories.append(item)

    print (tabulate(tabulateCategories, headers=["Category","Total quantity"]))

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
            try:
                remove = int(input("ID: "))
                break
            except ValueError:
                continue
           
        project.session.sql(f"delete from inventory where prodID = '{remove}';").execute()
        adminInventory(id)

    elif addremove == "2":
        print("Add item")
        while True:
            try:
                prodID = int(input("Product ID: ")) 
                break 
            except ValueError:
                continue
        
        prodName = input("Product Name: ") # varchar
        category = input("Product Category: ") #varchar
        while True:
            try:
                price = float(input("Product Price: ")) #Decimal -> int
                break 
            except ValueError:
                continue
        while True:
            try:
                available = int(input("Products available: "))
                break
            except ValueError:
                continue
        project.session.sql(f"insert into inventory (prodID, prodName, category, price, available) "\
        f"values ({prodID},'{prodName}', '{category}', {price}, {available});").execute()
        adminInventory(id)

    elif addremove == "3":
        print("Update item")
        while True:
            try:
                itemID = input("ID for item: ")
                break
            except ValueError:
                continue
        column = input("What column should be updated: ")
        update = input("Update: ")
        project.session.sql(f"UPDATE inventory SET {column} = '{update}' WHERE prodID = {itemID}").execute()
        adminInventory(id)

def adminDiscounts(id):
    os.system('cls')

    discount_fetch =  project.session.sql("select * from discounts").execute()

    tabulateList = []
    for item in discount_fetch.fetch_all():
        tabulateList.append(item)

    print (tabulate(tabulateList, headers=["Discount ID", "Product ID", "Product Name", "Category","Discount","Tier"]))

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
        while True:
            
            try:
                remove = int(input("ID: "))
                break
            except ValueError:
                continue

        project.session.sql(f"delete from discounts where discountID = {remove}").execute()
        print("removed", remove )
        adminDiscounts(id)

    elif addremove == "2":
        print("Add discount")
        prodID = input("Product ID: ")
        prodName = input("Product Name: ")
        category = input("Product Category: ")
        discount = input("Discount : ")
        memberType = input("Membertype: ")
        project.session.sql(f"insert into discounts (prodID, prodName, category, discount, memberType) "\
        f"values ({prodID},'{prodName}', '{category}', {discount}, '{memberType}');").execute()
        adminDiscounts(id)

    elif addremove == "3":
        print("Update item")
        while True:
            try:
                discountID = int(input("ID for discount: "))
                break 
            except ValueError:
                pass
        column = input("What column should be updated: ")
        update = input("Update: ")
        project.session.sql(f"UPDATE discounts SET {column} = '{update}' WHERE discountID = {discountID}").execute()
        adminDiscounts(id)

def adminMailinglist(id):
    os.system('cls')
    mailing_list_result = project.session.sql(project.mailing_list).execute()
    tabulateList = []
    for item in mailing_list_result.fetch_all():
        tabulateList.append(item)

    print (tabulate(tabulateList, headers=["customer ID", "Mail", "Product name","Discount"]))
    back = input("Type Exit to go back: ")

    if back == "Exit":
        adminPage(id)
    else:
        adminMailinglist(id)

def products(id):
    os.system('cls')
    
    product_fetch =  project.session.sql("select prodName, category, price, available from inventory").execute()
    tabulateList = []
    for item in product_fetch.fetch_all():
        tabulateList.append(item)

    print (tabulate(tabulateList, headers=["Product Name", "Category","Price","available"]))
    print("Products")
    print("Type Item name and 1(itemname 1) to add to cart")
    print("Type Item name and 2(itemname 2) to add to favorites")
    
    print("Type Exit to go back")
    cartFav = input("Input: ")
    if cartFav == "Exit":
        mainPage(id)
    else:
        x = cartFav.split()
        itemName = x[0] # finns i inventory
        while True:
            try:
                test = x[1]
                break
            except IndexError:
                products(id)
        
        if x[1] == "1":

            cartList = project.session.sql(f"select prodList from cart where uniqueID = {id}").execute()
            for item in cartList.fetch_one():
                cartList = item

            while True:
                try:
                    itemID = project.session.sql(f"select prodID from inventory where prodName = '{itemName}'").execute()
                    item = itemID.fetch_one()
                    if item is None:
                        products(id)
                    else:
                        itemID = str(item[0])
                        

                    break
                except ValueError:
                    products(id)

            temp = [cartList, str(itemID)]
            newCart = ", ".join(temp)
            project.session.sql(f"UPDATE cart SET prodList = '{newCart}' WHERE uniqueID = {id}").execute()

        elif x[1] == "2":
            favList = project.session.sql(f"select favoriteProd from customers where uniqueID = {id}").execute()
            for item in favList.fetch_one():
                favList = item

            while True:
                try:
                    itemID = project.session.sql(f"select prodID from inventory where prodName = '{itemName}'").execute()
                    item = itemID.fetch_one()
                    if item is None:
                        products(id)
                    else:
                        itemID = str(item[0])
                        

                    break
                except ValueError:
                    products(id)

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
    if back == "Exit":
        mainPage(id)
    else:
        discounts(id)

def cart(id):
    os.system('cls')

    cartList = project.session.sql(f"select prodList from cart where uniqueID = {id}").execute()
    for item in cartList.fetch_one():
        cartList = item

    check_price = project.session.sql(f"call CheckCart({id})").execute()
    tabulateList = []

    for row in check_price.fetch_all():
        tabulateList.append(row)

    print (tabulate(tabulateList, headers=["Product", "Price", "Quantity"]))
    print("Cart")
    x = cartList.replace(",", "").split()
    remove = input("Remove product(Name of product) Exit to go back: ")

    if remove == "Exit":
        mainPage(id)

    while True:
        try:
            removeID = project.session.sql(f"SELECT prodID FROM inventory WHERE prodName = '{remove}'").execute()
            item = removeID.fetch_one()
            if item is None:
                cart(id)
            else:
                removeID = str(item[0])
                

            break
        except ValueError:
            cart(id)

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
        tabulateList.append(row)

    print (tabulate(tabulateList, headers=["Product", "Price"]))

    print("favorites")

    x = itemList.replace(",", "").split()
    remove = input("Remove product(Name of product) Exit to go back: ")
    
    if remove == "Exit":
        mainPage(id)

    while True:
        try:
            removeID = project.session.sql(f"select prodID from inventory where prodName = '{remove}'").execute()
            item = removeID.fetch_one()
            if item is None:
                favorites(id)
            else:
                removeID = str(item[0])
                

            break
        except ValueError:
            favorites(id)
    
    print("removeID", removeID)

    if removeID in x:
        tempstring = itemList.replace(f"{removeID}", "", 1).replace(" ,", "")
        tempstring = tempstring.replace(',', '', 1) if tempstring.startswith(',') else tempstring
        
        project.session.sql(f"UPDATE customers SET favoriteProd = '{tempstring}' WHERE uniqueID = {id}").execute()
        favorites(id)



firstPage()