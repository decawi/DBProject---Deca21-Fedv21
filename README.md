# DBProject---Deca21-Fedv21
---
The *basequeries.sql* file contains the initial setup for the database.
the *checkcart.sql* file contains source code for the procedure to check the cart.

The base users in the database are:
**Admin**: The email is **admin** and have the admin privliges in the python implementation
**Felix**: The email is **felix@mail.com** and it already have a cart with products in it.

The project.py file contains the initial conneection to the database and all bigger sql queries
And imports **mysqlx**

The DBProject.py is the main python implementation. It uses the library datetime the get the date
the customer joined. It also uses the os library to clear the terminal for a easier user experience.
Lastly it uses the tabulate library for nicer table outputs.

Youtube link for the demonstation video: [Here](https://youtu.be/ASfNCbWmsYk)
