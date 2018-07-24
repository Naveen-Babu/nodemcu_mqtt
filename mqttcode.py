from flask import Flask, redirect, url_for, request, render_template, jsonify, json
import os
import paho.mqtt.client as mqtt

app = Flask(__name__)

topic = 'foo'
topic2 = 'bar'
port = 5000

def on_connect(client, userdata, flags, rc):

    if rc == 0:
        print("Connected to broker")
        global Connected                #Use global variable
        Connected = True                #Signal connection 
        client.subscribe(topic)
        client.publish(topic2, "STARTING SERVER")
        client.publish(topic2, "CONNECTED")
 
    else:
        print("Connection failed")


def on_message(client, userdata, msg):
    print("printing under on_message route")
    #print ("")
    print ("Message received: "  + str(msg.payload.decode("utf-8")))
    print (msg.topic)
    print (msg.payload)

    with open('mqtt.json', 'r') as json_file1: #read format
        params1 = json.load(json_file1)
        json_file1.close()

        params1["Message"] = msg.payload
        params1["Topic"] =  msg.topic

    try:
        with open('mqtt.json', 'w') as json_file1:
            json.dump(params1, json_file1)
    except Exception as e2:
        print(str(e2))

    return jsonify(params1)   #returns to client



@app.route("/dummy", methods=['GET'])
def dummies():
    print ("Inside dummies")

    with open('mqtt.json') as json_file:  #read
        d = json.load(json_file)
        print("1234")
        #print (d["Temperature"])

    return jsonify(topic=d["Topic"], msg=d["Message"])    #returns to html in json format



@app.route('/publish', methods= ['POST'])
def publish():
    print("printing inside publish route")
    #if request.method == 'POST':  
          # Then get the data from the form
    topic = request.form['Topic']        # Get the username/password associated with this tag
    msg = request.form['Message']
    client.publish(topic, msg)
    return json.dumps({'status':'OK'})



@app.route('/subscribe', methods= ['POST'])
def subscribe():
    print("printing inside subscribe route")
    topic_subscribe = request.form['Topic_Subscribe'] 
    print (topic_subscribe)
    client.subscribe(topic_subscribe)
    return json.dumps({'status':'OK'})



@app.route('/')
def hello_world():
    #return 'Hello World! I am running on port ' + str(port) 
    return  render_template('ajax.html')



if __name__ == '__main__':

    broker_address= "m12.cloudmqtt.com"  #Broker address
    ports = 15383                        #Broker port
    user = "tvjgzyvl"                    #Connection username
    password = "j1C2hqAC_9gq"            #Connection password
    client = mqtt.Client()
    client.username_pw_set(user, password=password)  
    client.on_connect = on_connect           #calback functions
    client.on_message = on_message
    client.connect(broker_address, port=ports)
    client.loop_start()
    port = int(os.getenv('PORT', 5000))
    app.debug=True        #automatically runs the code when saved
    app.run(host='0.0.0.1', port=port)