## Zolve
# Wallet Transaction System
***

### About the Project
A simple web app to perform various operations for wallet transactions using Python and Flask web framework.

### Pre-requisites
1. Python3 should be installed on the machine.

### Libraries Used
Below are the libraries that are in the project and some are need to be installed first on the system before running the program:-(see requirements.txt)
1. Flask
2. flask-sqlalchemy
3. flask-login
3. datetime

### How to run the application
1. Go inside the folder where the `app.py` and `requirements.txt` is stored.
2. Open terminal here and Run `pip3 install -r requirements.txt` to install all dependencies.
3. Now, Run `python3 app.py`
4. Now a server is started on `IP: 127.0.0.1` and `PORT: 5000`, open browser and on URL write `127.0.0.1:5000`
5. The login page appears, now you can start working with Wallet system

### Functionalities provided
1. Create New Wallet/User
2. Login and Logout from the Wallet (Cannot perform any Wallet operations without login in)
3. Check Currently available Balance
4. Credit Money to the Wallet
5. Debit Money from the Wallet
6. See Wallet's All Transactions performed
7. Error Handling:
    * Input Validation: Cannot Leave any empty inputs/fields
    * User Validation: Cannot login if user dont exist
    * Balance Validation: Enter amount in any positive number
    * Opening Balance has to be greater than minimum amount set by company, in app it is Rs. 100 (can be changed among the top of the code in global variables)

### Application Flow
1. <p align="center"><img src="https://github.com/avi-agrawal/Wallet_Transaction_System/blob/main/screenshots/server_starting.png" width="75%"></p>
2. 
