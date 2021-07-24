from flask import Flask, json
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)
import requests

# Data format: Dictonary
payload = {
    'connection': False,
    'pstatus': [],
    'pLHS_data': [],
    'pLHS_processed': [],
    'mLHS_data': [],
    'mLHS_processed': [],
    'eLHS_data': [],
    'eLHS_processed': [],
    'avg': []
}

def process(processedlist, lowerlimit, upperlimit):
    # Values above and below limits are set red and in between are blue
    for index, items in enumerate(processedlist):
        if items > upperlimit:
            processedlist[index] = "#C0392B"
        elif items < lowerlimit:
            processedlist[index] = "#F1C40F"
        elif items >= lowerlimit and items <= upperlimit:
            processedlist[index] = "blue"
    return processedlist

def processor():

    # Make HTTP request
    r = requests.get('http://127.0.0.1:5001/api/machine/raw')

    # Convert response to JSON
    response = r.json()

    regs = response["pLHS_data"]
    pLHS = [ x/100 for x in regs]

    regs2 = response["mLHS_data"]
    mLHS = [ x/100 for x in regs2]

    regs4 = response["eLHS_data"]
    eLHS = [ x/10 for x in regs4]

    regs6 = response["avg"]
    avg = [x / 100 for x in regs6]
    # LPRE-3204, LMAIN-3208, LEJN-3212
    avg_new = [ avg[0], avg[4], avg[7]]

    regs7 = response["limit"]
    limit = [x / 100 for x in regs7]
    # PREUP-6010 PRELOW-6011 MAINUP-6012 MAINLOW-6013 EJNUP-6014 EJNLOW-6015
    limit_new = [ limit[0], limit[1], limit[2], limit[3], limit[4], limit[5]]

    payload['connection'] = True
    payload['pLHS_data'] = pLHS 
    
    payload['mLHS_data'] = mLHS
    
    payload['eLHS_data'] = eLHS
    
    payload['pstatus'] = response["pstatus"]
    payload['avg'] = avg_new
    payload['limit'] = limit_new

    # Copy of data from raw server
    pLHS_data = payload['pLHS_data'].copy()
    mLHS_data = payload['mLHS_data'].copy()
    eLHS_data = payload['eLHS_data'].copy()
    

    # MLHS_LL, MLHS_UL, MRHS_LL, MRHS_UL, PLHS_LL, PLHS_UL, PRHS_LL, PRHS_UL, ELHS_LL, ELHS_UL, ERHS_LL, ERHS_UL
    payload['mLHS_processed'] = process(mLHS_data, limit_new[3], limit_new[2])
    payload['pLHS_processed'] = process(pLHS_data, limit_new[1], limit_new[0])
    payload['eLHS_processed'] = process(eLHS_data, limit_new[5], limit_new[4])
    
# print(payload)

class Payload(Resource):
    def get(self):
        if self:
            processor()
            return payload
        else:
            return "Invalid Request"

api.add_resource(Payload, '/api/machine/processed')

if __name__ == '__main__':
    app.run(debug=True, port=5050)
