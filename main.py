import socketserver,os,random,string,threading
from http.server import BaseHTTPRequestHandler
import shutil
connectedusers = 0
miners = []
buxrate = 5
cwd = os.getcwd()


def startxmr():
    exec(open('balupdate.py').read())
def starteth():
    exec(open('ethearn.py').read())
def updatebals():
    print("Updating balances")
    

def getbal(self):
    user = self.headers["username"]
    print( f"User requested balance: {user}")

    self.send_response(200,message="Yes")
    with open(f'{cwd}/users/{user}/balance.txt') as f:
        bal = f.read()
        bal = int((float(bal)/buxrate) * 1000) 
        print(bal)
    self.send_header("balance",bal)
    self.end_headers()
def connect(self):
    try:
        global connectedusers
        user = self.headers["username"].lower()
    
        addressi = self.client_address
        connectedusers += 1
        print(f"{user} connected from {addressi}! Connected users: {connectedusers}")
        files = os.listdir(f"{cwd}/users")
        exists = False
        for userlist in files:
            if userlist.lower() == user.lower():
                exists = True
        if exists == False:
            self.send_response(200,message="Yes")
            source_dir = rf"{cwd}/users/userbase"
            destination_dir = f"{cwd}/users/{user}"
            shutil.copytree(source_dir, destination_dir)
            token = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits + '_', k=random.randint(8, 9)))
            self.send_header("pw",token)
            self.end_headers()
            print("Sent token " + token)
            f = open(f'{cwd}/users/{user}/pw.txt', "w")
            f.write(token)
            f.close()
        else:
            self.end_headers()
        print(miners)
    except:
        print("Connection error")
def disconnect(self):
    global connectedusers
    user = self.headers["username"]
    addressi = self.client_address
    self.send_response(200)
    self.end_headers()
    connectedusers -= 1
    #miners.remove(user)
    #print(miners)
    print(f"{user} disconnected from {addressi}! Connected users: {connectedusers}")
def payout(self):
    global connectedusers
    user = self.headers["username"]
    passid = self.headers["id"]
    f = open(f'passid.txt', "w")
    f.write(passid)
    f.close()
    f = open(f'robloxuser.txt', "w")
    f.write(user)
    f.close()
    token = ""
    with open(f"{cwd}/users/{user}/pw.txt") as m:
        token = m.read()
    reqtoken = self.headers["token"]
    print(reqtoken + " " + token)
    if reqtoken == token:

        exec(open("payout.py").read())
        self.send_response(200)
    else:
        self.send_response(403)

    
    self.end_headers()
    
    
class MyHandler(BaseHTTPRequestHandler):
    print("Got req")
    def do_GET(self):
        try:
            self.headers["username"] = self.headers["username"].lower()
        except:
            x = 0
        if self.path == '/balance':
            # Insert your code here
            getbal(self)
        if self.path == '/connect':
            # Insert your code here
            connect(self)
    def do_POST(self):
        try:
            self.headers["username"] = self.headers["username"].lower()
        except:
            x = 0
        if self.path == '/connect':
            # Insert your code here
            connect(self)
        if self.path == '/disconnect':
            # Insert your code here
            disconnect(self)
        
        if self.path == '/payout':
            # Insert your code here
            payout(self)
print("Server running " )      
t1 = threading.Thread(target=startxmr)
t1.start()
t2 = threading.Thread(target=starteth)
t2.start()
httpd = socketserver.TCPServer(("0.0.0.0",1003), MyHandler)
print(httpd)
httpd.serve_forever()