from flask import Flask
from proj import app  
#app = Flask(__name__) #creating the Flask class object   
 
# @app.route('/') #decorator drfines the   
# def index():  
#     return "hello, this is our first flask website";  
  
if __name__ =="__main__":  
    app.run(debug = True)  