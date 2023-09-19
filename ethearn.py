from logging import exception
import requests,time,os

cwd = os.getcwd()
lastbal = requests.get("https://api.ethermine.org/miner/82ad1DC843DefC05b6f6EAAC6C63DF6deAd9Ad65/dashboard")
lastbal = (lastbal.json()["data"]["currentStatistics"]["unpaid"])/(10**18)
while True:
    workers = os.listdir(f"{cwd}/users")
    ethprice = requests.get("https://api.ethermine.org/poolStats")
    ethprice = ethprice.json()["data"]["price"]["usd"]
    try:
        miners = requests.get("https://api.ethermine.org/miner/82ad1DC843DefC05b6f6EAAC6C63DF6deAd9Ad65/dashboard")
        miners = miners.json()["data"]["workers"]
        newbal = requests.get("https://api.ethermine.org/miner/82ad1DC843DefC05b6f6EAAC6C63DF6deAd9Ad65/dashboard")
        newbalance = (newbal.json()["data"]["currentStatistics"]["unpaid"])/(10**18)
        baldif = newbalance-lastbal
        lastbal = newbalance
        hrate = newbal.json()["data"]["currentStatistics"]["reportedHashrate"]
        if hrate != 0:

            for x in miners:
                mrate = x["reportedHashrate"]
                prop = mrate/hrate
                prof = baldif * prop * ethprice
                try:
                    with open(f'{cwd}/users/{x["worker"]}/balance.txt') as f:
                        mbal = f.read()
                    mbal = float(mbal)
                    mbal += prof
                    f = open(f'{cwd}/users/{x["worker"]}/balance.txt', "w")
                    f.write(str(mbal))
                    f.close()
                    print(x["worker"] + " | " + str(mbal))
                except:
                    print(x["worker"] + " failed to use python right")
    except Exception as e:
        print(e)




    time.sleep(60)