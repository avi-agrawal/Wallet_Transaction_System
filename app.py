#imports
from flask import Flask, render_template, request, flash, redirect
# from flask.helpers import flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

#global
min_amount = 100
#dictionary of user wallet- {unique no. : {balance: value, transactions: [(liste)]} }
user_dict = {}


#configuring
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///wallets.db"
db = SQLAlchemy(app)
app.config["SECRET_KEY"]= "Wallet"
login_manager = LoginManager()
login_manager.init_app(app)


#creating flask models or databses
class wallet_class(UserMixin, db.Model):
    name = db.Column("Name",db.String(50), nullable=False)
    ID = db.Column("ID",db.Integer, primary_key=True)
    balance = db.Column("Balance",db.Float,nullable=False, default=0)

    def get_id(self):
           return (self.ID)

    # def __repr__(self):
    #     return "Wallet created for: " + str(self.id)

#creating transaction db
class transactions_class(db.Model):
    transaction_id = db.Column("Transaction ID",db.Text,primary_key=True)
    ID = db.Column("Wallet ID",db.Integer)
    timestamp = db.Column("Timestamp",db.DateTime, nullable=False, default=datetime.utcnow)
    log = db.Column("Log",db.Text,nullable=False)
    balance = db.Column("Amount",db.Float,nullable=False)

    # def __repr__(self):
    #     return "Transaction: " + str(self.log) + " for " + str(self.id)


@login_manager.user_loader
def load_user(user_id):
    return wallet_class.query.get(int(user_id))


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Api for login user
@app.route("/")
@app.route("/login", methods=["GET","POST"])
def login_user_func():

    if(request.method == "POST"):
        id = request.form["id"]

        #if no entry in the form
        if(not id):
            err_msg = "Give input"
            flash(err_msg,"error")
            return redirect("/login")

        #check whether phone_no/id is 10 digits
        if(len(id)!=10):
            err_msg = "Enter 10 digits Phone no."
            flash(err_msg,"error")
            return redirect("/login")

        id = int(id)

        print("fetch:",wallet_class.query.get(id))
        if(wallet_class.query.get(id) == None):
            err_msg = "Wallet for phone_no: " + str(id) + " doesn't exist, First Create new user"

            # return redirect("/error/"+err_msg)
            # print("inside if")
            flash(err_msg,"error")
            # print("after flash")
            print("Id not there")
            # return redirect("/create_wallet")
            return redirect("/login")

        else:
            user = wallet_class.query.filter_by(ID=id).first()
            print("User",user)
            login_user(user)
            flash("You are logged in","success")
            return redirect("/home")

    return render_template("login_page.html")


#logout API
@app.route("/logout")
@login_required
def logout():
    id = current_user.ID
    user = wallet_class.query.filter_by(ID=id).first()
    # print(user)
    logout_user()
    flash("You are logged out","success")
    return redirect("/login")



#home 
@app.route("/home")
@login_required
def index():
    id = current_user.ID
    return render_template("index.html",id=id)



#create_wallet API
@app.route("/create_wallet", methods=["GET","POST"])
def create_wallet():
    # return render_template("createwallet.html")
    global user_dict, min_amount
    # try:
    # print("inside try")
    if(request.method == "POST"):
        print("inside post")
        name = request.form["name"]
        id = request.form["id"]
        opening_balance = request.form["opening_balance"]
        print(id)

        #if no entry in the form
        if(not name or not id or not opening_balance):
            err_msg = "Give all the inputs"
            flash(err_msg,"error")
            return redirect("/create_wallet")

        #check whether phone_no/id is 10 digits
        if(len(id)!=10):
            err_msg = "Enter 10 digits Phone no."
            flash(err_msg,"error")
            return redirect("/create_wallet")


        id = int(id)
        opening_balance = float(opening_balance)
        #check id already exist or not
        # if(id in user_dict):
        if(wallet_class.query.get(id) != None):
            err_msg = "Wallet for phone_no: " + str(id) + " already exist"

            # return redirect("/error/"+err_msg)
            # print("inside if")
            flash(err_msg,"error")
            # print("after flash")
            print("Id already there")
            # return redirect("/create_wallet")
            return redirect("/create_wallet")

        #check whether opening balance is greater than minimum allowed balance
        if(opening_balance < min_amount):
            err_msg = "Open wallet with at least " +  str(min_amount) + " Rs. of balance"
            flash(err_msg,"error")
            return redirect("/create_wallet")


        else:
            log_msg = "Wallet Created with opening balance " + str(opening_balance)

            # user_dict[id] = {"balance":opening_balance,"transactions":[log_msg]}
            # print("user_dict:",user_dict)

            #db working
            new_wallet_entry = wallet_class(name=name, ID=id, balance=opening_balance)
            db.session.add(new_wallet_entry)
            db.session.commit()
            
            # print("before")
            curr_transaction_id = str(id) + " :-: " + str(datetime.utcnow())
            new_transaction_entry = transactions_class(transaction_id=curr_transaction_id ,ID=id, log=log_msg, balance=float(opening_balance))
            db.session.add(new_transaction_entry)
            db.session.commit() 
            # print("after")           

            print(wallet_class.query.all())
            print(transactions_class.query.all())

            flash("Wallet created successfully","success")
            return redirect("/create_wallet")

    return render_template("createwallet.html")

    # except Exception as e:
    #     print(e)
    #     print("Error in creating wallet")
    #     return "Error in creating wallet"



# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------


@app.route("/error/<string:msg>")
def error_msg(msg):
    return render_template("error.html",err_msg = msg)
    # redirect("/create_wallet")

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------


#check balance
@app.route("/check_balance",methods=["GET","POST"])
@login_required
def check_balance():
    global user_dict, min_amount
    try:
        if(request.method=="POST"):
            # id = request.form["id"]
            id = current_user.ID
            print("Id:",id)
            print(type(id))

            #if fields not enter
            if(not id):
                err_msg = "No Id given"
                flash(err_msg,"error")
                return redirect("/check_balance")
            
            #check whether phone_no/id is 10 digits
            if(len(str(id))!=10):
                err_msg = "Give 10 digits Phone no."
                flash(err_msg,"error")
                return redirect("/check_balance")

            id = int(id)
            #if phone no doesn't exist
            # if(id not in user_dict):
            if(wallet_class.query.get(id) == None):
                err_msg = "User: " + str(id) + " doesn't exist"
                flash(err_msg,"error")

                return redirect("/check_balance")
            
            else:
                # balance = user_dict[id]["balance"]
                record_obj = wallet_class.query.filter_by(ID=id).first()
                balance = record_obj.balance

                msg = "Balance: " + str(balance)
                flash(msg,"success")
                return redirect("/check_balance")
        
        return render_template("checkbalance.html")


    except Exception as e:
        print(e)
        print("Error in checking balance")
        return "Error in checking balance"

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------


#credit money to wallet
@app.route("/credit",methods=["GET","POST"])
@login_required
def credit_money():
    global user_dict, min_amount
    
    # try:

    if(request.method=="POST"):
        # id = request.form["id"]
        # print("type:",type(id))
        id = current_user.ID
        amount = request.form["amount"]

        #if fields not enter
        if(not id or not amount):
            err_msg = "Give all the input"
            flash(err_msg,"error")
            return redirect("/credit")
        
        #check whether phone_no/id is 10 digits
        if(len(str(id))!=10):
            err_msg = "Enter 10 digits Phone no."
            flash(err_msg,"error")
            return redirect("/credit")

        id = int(id)
        amount = float(amount)

        # checking whether phone no. exist or not
        # if(id not in user_dict):
        if(wallet_class.query.get(id) == None):
            err_msg = "User: " + str(id) + " doesn't exist"
            flash(err_msg,"error")
            return redirect("/credit")

        #check whether amount entered is positive value
        if(amount <= 0):
            err_msg = "Credit amount should be greater than 0"
            flash(err_msg,"error")
            return redirect("/credit")
                
        else:
            #updating balance
            # balance = user_dict[id]["balance"] + amount
            # user_dict[id]["balance"] = balance

            record_obj = wallet_class.query.filter_by(ID=id).first()
            credit_balance = float(record_obj.balance) + float(amount)
            record_obj.balance = float(credit_balance)
            db.session.commit()
            
            print("Success till credit")
            print(type(credit_balance))
            print(credit_balance)
            print(type(record_obj.balance))

            #adding transaction to account
            log_msg = "Amount credited: " + str(amount)
            # user_dict[id]["transactions"].append(log)
            print(log_msg)
            
            print("id:",type(id))
            curr_transaction_id = str(id) + " :-: " + str(datetime.utcnow())
            new_transaction_entry = transactions_class(transaction_id=curr_transaction_id, ID=id, log=log_msg, balance=float(credit_balance))
            db.session.add(new_transaction_entry)
            db.session.commit() 

            print("after new transac")

            msg = "Money credited successfully, Curr. Balance: " + str(credit_balance)
            flash(msg,"success")

            return redirect("/credit")
    
    return render_template("creditbalance.html")
        

    # except Exception as e:
    #     print(e)
    #     print("Error in crediting balance")
    #     return "Error in crediting balance"

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------


#debit money from wallet
@app.route("/debit",methods=["GET","POST"])
@login_required
def debit_money():
    global user_dict, min_amount
    
    try:
        if(request.method=="POST"):

            # id = request.form["id"]
            id = current_user.ID
            amount = request.form["amount"]

            #if fields not enter
            if(not id or not amount):
                err_msg = "Give all the input"
                flash(err_msg,"error")
                return redirect("/debit")
            
            #check whether phone_no/id is 10 digits
            if(len(str(id))!=10):
                err_msg = "Enter 10 digits Phone no."
                flash(err_msg,"error")
                return redirect("/debit")

            id = int(id)
            amount = float(amount)

            # checking whether phone no. exist or not
            # if(id not in user_dict):
            if(wallet_class.query.get(id) == None):
                    err_msg = "User: " + str(id) + " doesn't exist"
                    flash(err_msg,"error")
                    return redirect("/debit")
            
            #check whether amount entered is positive value
            if(amount <= 0):
                err_msg = "Debit amount should be greater than 0"
                flash(err_msg,"error")
                return redirect("/debit")
                    
            else:
                #updating balance
                # balance = user_dict[id]["balance"] - amount

                record_obj = wallet_class.query.filter_by(ID=id).first()
                debit_balance = record_obj.balance - amount

                #check whether after debiting balance is less than minimum allowed amount or not
                if(debit_balance < min_amount):
                    err_msg = "Amount: " + str(amount) + " cannot be debited, it will lower down the avl. balance lesser than minimum allowed balance for your wallet, Avl: Balance: " +  str(record_obj.balance) + ", \n minimum allowed: " + str(min_amount)
                    flash(err_msg,"error")
                    return redirect("/debit")

                record_obj.balance = debit_balance
                db.session.commit()

                # user_dict[id]["balance"] = balance
                
                #adding transaction to account
                log_msg = "Amount Debited: " + str(amount)
                # user_dict[id]["transactions"].append(log)

                curr_transaction_id = str(id) + " :-: " + str(datetime.utcnow())
                new_transaction_entry = transactions_class(transaction_id=curr_transaction_id, ID=id, log=log_msg, balance=float(debit_balance))
                db.session.add(new_transaction_entry)
                db.session.commit()

                msg = "Money debit successfully, Curr. Avl Balance: " + str(debit_balance)
                flash(msg,"success")

                return redirect("/debit")
        
        return render_template("debitbalance.html")


    except Exception as e:
        print(e)
        print("Error in debiting balance")
        return "Error in debiting balance"

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# #check users
# @app.route("/all_users")
# def all_users():
#     global user_dict

#     return render_template("alluser.html",user_dict=user_dict)


@app.route("/show_transactions", methods= ["GET","POST"])
@login_required
def show_transactions():
    try:
        if(request.method=="POST"):
            # id = (request.form["id"])
            id = current_user.ID
            
            #check for inputs
            if(not id):
                err_msg = "Give input"
                flash(err_msg,"error")
                return redirect("/show_transactions")

            #check whether phone_no/id is 10 digits
            if(len(str(id))!=10):
                err_msg = "Enter 10 digits Phone no."
                flash(err_msg,"error")
                return redirect("/show_transactions")

            id = int(id)

            # checking whether phone no. exist or not
            # if(id not in user_dict):
            if(wallet_class.query.get(id) == None):
                    err_msg = "User: " + str(id) + " doesn't exist"
                    flash(err_msg,"error")
                    return redirect("/show_transactions")
            
            else:
                all_transactions = transactions_class.query.filter_by(ID=id).all()
                
                return render_template("show_transactions.html",all_transactions=all_transactions)

        return render_template("show_transactions.html",all_transactions=[])

    except Exception as e:
        print(e)
        print("Error in all_transactions")
        return "Error in all_transactions"



if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=5000)

