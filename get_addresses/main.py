import json
import requests
from datetime import datetime
import time
import os
from csv_rw import CSVrw

# def get_balance_address_token(address,token,dec = 9):
#     url_p1="https://api.snowtrace.io/api?module=account&action=tokenbalance&contractaddress="
#     url_p2="&address="
#     url_p3="&tag=latest&apikey="
    
#     url = url_p1 + token + url_p2 + address + url_p3 + api_key
#     req = json.loads(requests.get(url).text)
#     try :
#         return float(req['result']/(10**dec))
#     except Exception as e:
#         print(e,": request error")
#         return
    
# def track_address_transactions(addresses):
#     beep = lambda x: os.system("echo -n '\a';sleep 0.2;" * x)
#     beep(1)
#     now = datetime.now()
#     timestamp = str(int(datetime.timestamp(now)))
#     url_b = "https://api.snowtrace.io/api?module=block&action=getblocknobytime&timestamp=" + timestamp + "&closest=before&apikey="+api_key
#     block = json.loads(requests.get(url_b).text)['result']
#     url_p1="https://api.snowtrace.io/api?module=account&action=txlist&address="
#     url_p2="&startblock="
#     url_p3 = "&endblock=99999999&sort=asc&apikey="
    
#     n = {}
#     for a in addresses:
#         n[a] = 0
#     while(1):
#         for a in addresses:
#             url = url_p1 + a + url_p2 + block + url_p3 + api_key
#             req = json.loads(requests.get(url).text)
#             try :
#                 req = req['result']
#                 if len(req)>n[a]:
#                     print(datetime.now().strftime("%H:%M:%S")," ALERT : transaction on : ", a)
#                     beep(3)
#                     n[a] += 1
#             except Exception as e:
#                 print(e,": request error ")
#                 return
#             time.sleep(30)

def get_pair_ERC20_interactors(token,start_block='1',endblock='99999999'):
    # url_p1="https://api.arbiscan.io/api?module=account&action=txlist&address="
    url_p1="https://api.arbiscan.io/api?module=account&action=tokentx&address="
    status = 0
    nb_div = 1
    while(status!=1):
        slice = int((int(endblock)-int(start_block))/nb_div)
        for i in range(1,nb_div+1):
            start_block = int(start_block) + (i-1)*slice
            endblock = int(endblock)  - (nb_div-i)*slice
            print(start_block,endblock)
            url_p2="&start0block="+str(start_block)+"&endblock="+str(endblock) +"&sort=asc&apikey="
            url = url_p1 + token + url_p2 + api_key
            req = json.loads(requests.get(url).text)
            addresses_list = []
            try :
                if req['status'] != "1":
                    print(req)
                    nb_div +=1
                    print("Division par",nb_div)
                else :
                    status = 1
                    req = req['result']
                    for r in req :
                        if (r['from'] not in addresses_list) and (r['from'] != token):
                            addresses_list.append(r['from'])
                    return addresses_list
            except Exception as e:
                print(e,": request error ")
                return []

# def cross_list(l1,l2,l3=None):
#     l4 = []
#     for a in l1:
#         if a in l2:
#             if l3 == None:
#                 l4.append(a)
#             elif a in l3:
#                 l4.append(a)
#     return l4
    
def main():
    # address = ""
    # token = ""
    # get_balance_address_token(address, token)4
    contracts = CSVrw('contracts.csv')
    contracts.read_rows()
    contracts_dict = {}
    for c in contracts.rows:
        contracts_dict[c[3]]={'contrat':c[0],'block1':c[1],'block2':c[2]}
    
    csvfile = CSVrw('adresses.csv')
    addresses = {}

    # print(contracts_dict)
    i = 0
    for c in contracts_dict:
        print("Traitement de",c, "...")
        results = get_pair_ERC20_interactors(contracts_dict[c]['contrat'],contracts_dict[c]['block1'],contracts_dict[c]['block2'])
        print(len(results),"adresses trouvées !")
        for a in results :
            if a in addresses:
                addresses[a] = int(addresses[a]) + 1
            else :
                addresses[a] = 1
        i+=1
        print(int(100*i/len(contracts_dict)),"%")
        time.sleep(1)


    addresses = dict(sorted(addresses.items(), key=lambda x:x[1],reverse=True))
    
    addresses_tab = [] #tableau des adresses avec le nombre de contrats touchés
    for a in addresses:
        addresses_tab.append([str(a)+';'+str(addresses[a])])
    csvfile.write_rows(addresses_tab)
        
 
if __name__ == "__main__":
    main()
    