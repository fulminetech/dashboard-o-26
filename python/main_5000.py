import logging
import threading
import json
import time
# ms = time.time_ns() // 1000000

# Python script for Modbus Read / Write
from pyModbusTCP.client import ModbusClient

# Server Imports
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

# Modbus TCP parameters
SERVER_HOST = "192.168.1.5"
# SERVER_HOST = "192.168.0.99"
SERVER_PORT = 502
# Scan time in seconds
# MBSCAN = 3
MBSCAN =5

# define modbus server host, port
c = ModbusClient()
c.host(SERVER_HOST)
c.port(SERVER_PORT)
# uncomment this line to see debug message
#c.debug(True)

# Modbus Read addresses 
TIME_ADDR = 100

PREC_L_ADDR = 2000
MAIN_L_ADDR = 2200
EJNC_L_ADDR = 2400
AVGC_ADDR = 3204 # LPRE-3204, LMAIN-3208, LEJN-3212
LIMIT_ADDR = 6010 # PREUP-6010 PRELOW-6011 MAINUP-6012 MAINLOW-6013 EJNUP-6014 EJNLOW-6015
STUS_ADDR = 540

# Data format: Dictonary
payload = {
    'connection': False,
    'pLHS_data': [],
    'mLHS_data': [],
    'eLHS_data': [],
    'avg': [],
    'limit': [],
    'pstatus': [],
}

global x

def connect():
    global x
    # open or reconnect TCP to server
    if not c.is_open():
        if not c.open():
            payload['connection'] = "Error"
            logging.error("unable to connect to "+SERVER_HOST+":"+str(SERVER_PORT))
        else:
            payload['connection'] = True
            # if open() is ok, read register (modbus function 0x03)
            if c.is_open():
                logging.info('MODBUS connected!')
                logging.info("Main    : Creating Modbus thread")
                x = threading.Thread(target=xyz, args=(1,), daemon=True)
                x.start()
                
def ptime():
    regs = c.read_holding_registers(TIME_ADDR, 6)
    global x
    if regs:
        logging.debug('Success!: Time')
        x = 'pLHS'
    else:
        logging.error("Time Read Failed")
        x = 'pLHS'

def pLHS():
    regs = c.read_holding_registers(PREC_L_ADDR, 26)
    global x
    if regs:
        # pLHS = [ x/100 for x in regs]
        # payload['pLHS_data'] = pLHS
        # logging.debug('Success!: pre L')
        payload['pLHS_data'] = regs
        x = 'mLHS'
    else:
        logging.error("pLHS Read Failed")
        x = 'mLHS'

def mLHS():
    regs = c.read_holding_registers(MAIN_L_ADDR, 26)
    global x
    if regs:
        # mLHS = [ x/100 for x in regs]
        # payload['mLHS_data'] = mLHS
        # logging.debug('Success!: main L')
        payload['mLHS_data'] = regs
        x = 'eLHS'
    else:
        logging.error("mLHS Read Failed")
        x = 'eLHS'

def eLHS():
    regs = c.read_holding_registers(EJNC_L_ADDR, 26)
    global x
    if regs:
        # eLHS = [ x/100 for x in regs]
        # payload['eLHS_data'] = eLHS
        # logging.debug('Success!: ejn L')
        payload['eLHS_data'] = regs
        x = 'avg'
    else:
        logging.error("eLHS Read Failed")
        x = 'avg'

def avg():
    regs = c.read_holding_registers(AVGC_ADDR, 10)
    global x
    if regs:
        # avg = [ x/100 for x in regs]
        # payload['avg'] = avg
        # logging.debug('Success!: avg')
        payload['avg'] = regs
        x = 'limit'
    else:
        logging.error("avg Read Failed")
        x = 'limit'

def limit():
    # PLHS_UL, PLHS_LL, MLHS_UL, MLHS_LL, ELHS_UL, ELHS_LL, PRHS_UL, PRHS_LL, MRHS_UL, MRHS_LL, ERHS_UL, ERHS_LL + Force line LHS PME, RHS PME + AWC LHS: UP-LP, UM-LM 
    regs = c.read_holding_registers(LIMIT_ADDR, 26)
    global x
    if regs:
        # limit = [ x/100 for x in regs]
        # payload['limit'] = limit
        # logging.debug('Success!: limit')
        payload['limit'] = regs
        x = 'pstatus'
    else:
        logging.error("limit Read Failed")
        x = 'pstatus'

def pstatus():
    regs = c.read_coils(STUS_ADDR, 26)
    global x
    if regs:
        # logging.debug('Success!: pstatus')
        payload['pstatus'] = regs
        x = 'pLHS'
    else:
        logging.error("pstatus Read Failed")
        x = 'pLHS'

def end():
    print("End")
    # print("End: ",+int(time.time_ns() // 1000000 - ms))

def start():
    print("Start")
    # print("Start: ",+int(time.time_ns() // 1000000 - ms))

def xyz(name):
    logging.info("Thread %s: starting", name)
    while True: 
        # start()
        pLHS()
        mLHS()
        eLHS()
        avg()
        limit()
        pstatus()
        
        time.sleep(0.1)
        # end()

# Class for Payload API
class Payload(Resource):
    def get(self, section, subsection):
        if section == "machine" and subsection == "raw":
            return payload
        else:
            return "Invalid Command"

# API Declaration
api.add_resource(Payload, '/api/<section>/<subsection>')

# Start Server
if __name__ == '__main__':
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.DEBUG, datefmt="%H:%M:%S")
    connect()
    app.run(debug=True, port=5001)
