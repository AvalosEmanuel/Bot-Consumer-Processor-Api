from datetime import datetime
import api_secret
import websocket
import json
import ssl
import boto3
import logging
from send_logs import update_cloudwatch
from botocore.exceptions import ParamValidationError

websocket.enableTrace(True)
counter = 0
class ApiConection:
    """Connection to Alchemy node through 'AWS Secret Manager', 
    for greater security in API_KEY management"""
    
    logging.basicConfig(filename='api_loggs.log', format='%(levelname)s:%(message)s', level=logging.INFO)
    secret = api_secret.get_secret()
    API_ALCHEMY = "wss://eth-mainnet.alchemyapi.io/v2/" + str(secret)

    def on_open(ws):
        print('Opened Connection')
        logging.info('< Opened Connection >')
        try:
            update_cloudwatch('< Opened Connection >')
        except Exception:
            print("Error in cloudwatch logs.. 'on_open'..")

        ws.send(json.dumps({
            "jsonrpc":"2.0",
            "id": 1, 
            "method": "eth_subscribe", 
            "params": 
                ["alchemy_filteredNewFullPendingTransactions", 
                {"address": "0x3819f64f282bf135d62168C1e513280dAF905e06"}] 
        }))

    def on_close(ws, close_status_code, close_msg):
        print('Closed Connection')
        logging.info('< Closed Connection >')
        try:
            update_cloudwatch('< Closed Connection >')
            if close_status_code or close_msg:
                update_cloudwatch("close status code: " + str(close_status_code))
                update_cloudwatch("close message: " + str(close_msg))

        except Exception:
            print("Error in cloudwatch logs.. 'on_close'..")

    def on_message(ws, message):
        """Receiver of transactions and their metrics, via a websocket connection, 
        filters out data and publishes them in a 'SNS AWS' topic"""
        global counter
        topic_arn = "arn:aws:sns:us-east-1:360729631529:AlchemyTx"
        sns_client = boto3.client("sns")
        data = json.loads(message)
        
        if counter < 100000:
            if 'id' in data.keys():
                print ("Mensaje filtrado.. " + str(data))
                logging.info('Mensaje filtrado >> ' + str(data))
                try:
                    update_cloudwatch('Mensaje filtrado >> ' + str(data)) 
                except Exception as e:
                    print("Error in cloudwatch logs.. 'on_message - if'.." + str(e))            
            else:
                sns_client.publish(TopicArn= topic_arn, Message= json.dumps(data['params']['result']))
                counter += 1
                print ("Mensaje enviado a SNS.. " + str(data['params']['result']))
                logging.info('Mensaje publicado en SNS>> ' + str(data['params']['result']))
                try:
                    update_cloudwatch('Mensaje enviado a SNS>> ' + str(data['params']['result']))      
                except Exception as e:
                    print("Error in cloudwatch logs.. 'on_message - else'.." + str(e))
        else:
            print("Control cut off... 100k transactions were sent...")
            logging.warning('< Control cut off... 100k transactions were sent >')
            update_cloudwatch('< Control cut off... 100k transactions were sent >')
            
    def on_error(ws, err):
        print("Got a an error: ", str(err))
        logging.error('< Got a an error >> ' + str(err))
        try:
            update_cloudwatch('< Error Connection >')
            update_cloudwatch(str(err))
        except ParamValidationError:
            print("< ParamValidationError >")
        except Exception as e:
            print("Error in cloudwatch logs.. 'on_error'.." + str(e))

    def on_ping(wsapp, message):
        update_cloudwatch(f'{str(datetime.now())}   ### Got a Ping! ###')


    def on_pong(wsapp, message):
        update_cloudwatch(f'{str(datetime.now())}   ### Send a Pong! ###')
    
    while True:
        ws = websocket.WebSocketApp(API_ALCHEMY, 
                                    on_open=on_open, 
                                    on_close=on_close, 
                                    on_message=on_message, 
                                    on_error=on_error, 
                                    on_ping=on_ping,
                                    on_pong=on_pong)
        connection_status = ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE}, ping_interval=60, ping_timeout=30)
        if connection_status == False:
            update_cloudwatch("< Websocket connection stopped >")   
        
    


    

      

 

    
    

    
    
    
    