import requests,time,os,random

cwd = os.getcwd()
xmrtext = ""
while True:
    proxies = ""
    try:
       
        workers = os.listdir(f"{cwd}/users")
        for x in workers:
            
            if x == "userbase":
                workers.remove(x)
        xmrest = requests.get('https://api.nanopool.org/v1/xmr/block_stats/0/1')
        xmrtext = xmrest.text
        print("got ere")
        xmrest = xmrest.json()
        xmrdif = xmrest["data"][0]["difficulty"]
        xmrprice = requests.get("https://min-api.cryptocompare.com/data/price?fsym=XMR&tsyms=USD")
        xmrprice = xmrprice.json()["USD"]
        prox_ = ""
        with open(f'{cwd}/proxies.txt') as f:
            prox_ = f.read()
        proxies = prox_.splitlines()
        for worker in workers:
            proxy = random.choice(proxies)
            x = proxy.split(":")
            proxy = {
                'http':f'http://' + x[2] + ":" + x[3] + "@" + x[0] + ":" + x[1],
                'https':f'http://' + x[2] + ":" + x[3] + "@" + x[0] + ":" + x[1]
            }
            workertot = 0
            wlist = requests.get("https://minexmr.com/api/main/user/workers?address=42ijCzdtKYrJd2jMvFiBNyEqL2pVVoq3WUij4byhqxajeQC299q84dQA2MdWQ8LrxFaF1sKf4UujrHiVRwCuKr2HHcfFtxr&27436352",proxies=proxy)
            wlist = wlist.json()
            target = {}
            
            for x in wlist:
                a_dictionary = x
                b_in_dict =  "name" in a_dictionary
                if b_in_dict == True:
                    if x['name'].lower() == worker:
                        target = x
                else:
                    wxyxw = 1
            if target != {}:
                with open(f'{cwd}/users/{worker}/lastshares.txt') as f:
                    lasthashes = f.read()
                hashdif = int(target["hashes"]) - int(lasthashes)
                f = open(f'{cwd}/users/{worker}/lastshares.txt', "w")
                f.write(target["hashes"])
                f.close()
                dollartot = (hashdif/xmrdif) * xmrprice
                workertot += dollartot
                
                bal = ""
                with open(f'{cwd}/users/{worker}/balance.txt') as f:
                   bal = f.read()
                bal = float(bal)
                bal += workertot
                f = open(f'{cwd}/users/{worker}/balance.txt', "w")
                f.write(str(bal))
                f.close()
            else:
                x = 0  
        print("Updated all user's XMR totals")
    except Exception as e:
        print("Errored")
        print(e)
    
    
    
    time.sleep(150)