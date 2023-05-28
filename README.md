# DBProject---Deca21-Fedv21
---
The *setup.sql* file contains the initial setup for the database.<br/>
The *checkcart.sql* file contains source code for the procedure to check the cart.<br />

The base users in the database are:<br />
**Admin**: The email is **admin** and have the admin privliges in the python implementation<br />
**Felix**: The email is **felix@mail.com** and it already have a cart with products in it.<br />

The project.py file contains the initial connection to the database and all bigger sql queries<br />
And imports **mysqlx**<br />

The DBProject.py is the main python implementation. It uses the library **datetime** the get the date<br />
the customer joined. It also uses the **os** library to clear the terminal for a easier user experience.<br />
Lastly it uses the **tabulate** library for nicer table outputs.<br />

Youtube link for the demonstation video: [Here](https://youtu.be/ASfNCbWmsYk)
