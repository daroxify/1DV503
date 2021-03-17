### Installation
The GUI used in the application is ``PySimpleGUI`` and is needed to run the application.

Use ``pip install PySimleGUI`` to install the GUI.  

### How to use the application
If you are using the provided .csv files, change the path in the ``database.py`` files.

If you are using the provided database dump, import it to your server environment and choose ``utf-8`` as character set of the file.

Also make sure that the information in code below, in the file database, is correct
````
cnx = mysql.connector.connect(user = 'root',
                                    password = 'root',
                                    unix_socket = '/Applications/MAMP/tmp/mysql/mysql.sock')
````
Run the file ``database.py``. If the database exists or is successfully created, a window should appear and you should be able to use the application.