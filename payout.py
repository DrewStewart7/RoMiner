from logging import exception
import requests,os
cwd = os.getcwd()
passid = ""
user = ""
userbal = ""
buxrate = 5
geturl = "https://www.roblox.com/catalog/"
baseurl = "https://economy.roblox.com/v1/purchases/products/"
with open(f'passid.txt') as f:
    passid = f.read()
with open(f'robloxuser.txt') as f:
    user = f.read()
try:
    with open(f'{cwd}/users/{user}/balance.txt') as f:
        userbal = f.read()
    userbal = int((float(userbal)/buxrate) * 1000)
    print(userbal)
    if userbal >= 2:
        print(f"Attempting a payout of {userbal} robux for {user}")
        cookie = open('cookie.txt', 'r').read()
        with requests.session() as session:
            session.cookies[".ROBLOSECURITY"] = cookie
            xcsrf = session.post("https://auth.roblox.com/")
            xcsrf = xcsrf.headers["X-CSRF-Token"]
            print(xcsrf)
            session.headers["X-CSRF-Token"] = xcsrf
            session.cookies["ROBLOSECURITY"] = cookie
            authinfo = session.get("https://users.roblox.com/v1/users/authenticated")
            
            if authinfo.status_code == 200:
                print("Authenticated")
                datas = {"gamePassId":passid}
                infos = session.get(f"https://api.roblox.com/marketplace/game-pass-product-info", data=datas)
                productid = infos.json()["ProductId"]
                price = infos.json()["PriceInRobux"]
                sellerid = infos.json()["Creator"]["Id"]
                if price <= userbal:
                    data = {"expectedCurrency":1, "expectedPrice":price,"expectedSellerId":sellerid}
                    revokedat = {"id":passid}
                    revoke = session.post("https://www.roblox.com/game-pass/revoke",data=revokedat)
                    buy = session.post(f"https://economy.roblox.com/v1/purchases/products/{productid}",data=data)
                    if buy.status_code == 200:
                        f = open(f'{cwd}/users/{user}/balance.txt', "w")
                        f.write("0")
                        f.close()
                        print("Purchase successful")
                        file_object = open('history.txt', 'a')
                        # Append 'hello' at the end of file
                        file_object.write(f"{user} of {userbal} to {passid}\n")
                        # Close the file
                        file_object.close()
except exception as e:
    print(e)





