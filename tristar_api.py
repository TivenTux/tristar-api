import json, sqlite3, re
from flask import Flask, jsonify
from constants import *
from waitress import serve

#fetch latest data from database
def load_data():
    connection = sqlite3.connect(database)
    cur = connection.cursor()
    try:
        rows = cur.execute(
            '''SELECT batteryvoltage, targetvoltage, chargingcurrent
    , arrayvoltage, arraycurrent, outputpower, sweepvmp, sweepvoc, sweeppmax
    , batterytemp, controllertemp, kilowatthours, status, absorption, balance
    , float, maxenergydaily, amperehoursdaily, watthoursdaily, maxvoltagedaily
    , maxbatteryvoltagedaily, minbatteryvoltagedaily, inputpower, led, batterypolesvoltage
    , batterysensorvoltage, locationtemp, locationcloud, productiontoday, productiontomorrow FROM tristar WHERE id = ?''',
            (0,),
        ).fetchall()
        batteryvoltage = rows[0][0]
        targetvoltage = rows[0][1]
        chargingcurrent = rows[0][2]
        arrayvoltage = rows[0][3]
        arraycurrent = rows[0][4]
        outputpower = rows[0][5]
        sweepvmp = rows[0][6]
        sweepvoc = rows[0][7]
        sweeppmax = rows[0][8]
        batterytemp = rows[0][9]
        controllertemp = rows[0][10]
        kilowatthours = rows[0][11]
        status = rows[0][12]
        absorptionduration = rows[0][13]
        balanceduration = rows[0][14]
        floatduration = rows[0][15]
        maxenergydaily = rows[0][16]
        amperehoursdaily = rows[0][17]
        watthoursdaily = rows[0][18]
        maxvoltagedaily = rows[0][19]
        maxbatteryvoltagedaily = rows[0][20]
        minbatteryvoltagedaily = rows[0][21]
        inputpower = rows[0][22]
        led = rows[0][23]
        batterypolesvoltage = rows[0][24]
        batterysensorvoltage = rows[0][25]
        locationtemp = rows[0][26]
        locationcloud = rows[0][27]
        productiontoday = rows[0][28]
        productiontomorrow = rows[0][29]
                      
    except Exception as e:
        print(e)
    return batteryvoltage, targetvoltage, chargingcurrent, arrayvoltage, arraycurrent, outputpower, sweepvmp, sweepvoc, sweeppmax, batterytemp, controllertemp, kilowatthours, status, absorptionduration, balanceduration, floatduration, maxenergydaily, amperehoursdaily, watthoursdaily, maxvoltagedaily, maxbatteryvoltagedaily, minbatteryvoltagedaily, inputpower, led, batterypolesvoltage, batterysensorvoltage, locationtemp, locationcloud, productiontoday, productiontomorrow

def convert_to_fahrenheit(temperature):
    temperature = temperature.replace('C', '')
    temperature = "{:.2f}".format((float(temperature) * 1.8) + 32) + 'F'
    return temperature

app = Flask(__name__)
#endpoint without measurement symbols
@app.route('/tristarclean' , methods=['GET'])
def tristarclean():
    batteryvoltage, targetvoltage, chargingcurrent, arrayvoltage, arraycurrent, outputpower, sweepvmp, sweepvoc, sweeppmax, batterytemp, controllertemp, kilowatthours, status, absorptionduration, balanceduration, floatduration, maxenergydaily, amperehoursdaily, watthoursdaily, maxvoltagedaily, maxbatteryvoltagedaily, minbatteryvoltagedaily, inputpower, led, batterypolesvoltage, batterysensorvoltage, locationtemp, locationcloud, productiontoday, productiontomorrow = load_data()
    availableitems = [batteryvoltage, targetvoltage, chargingcurrent, arrayvoltage, arraycurrent, outputpower, sweepvmp, sweepvoc, sweeppmax, batterytemp, controllertemp, kilowatthours, status, absorptionduration, balanceduration, floatduration, maxenergydaily, amperehoursdaily, watthoursdaily, maxvoltagedaily, maxbatteryvoltagedaily, minbatteryvoltagedaily, inputpower, led, batterypolesvoltage, batterysensorvoltage, locationtemp, locationcloud, productiontoday, productiontomorrow]    
    nolabelitems = []
    x = 0
    #remove measurement labels except specific items
    for i in availableitems:
        dont_alter = [23, 12, 13, 14, 15]
        if x not in dont_alter:
            i = re.sub('[^\d\.]', '', i)
        nolabelitems.append(i)
        x += 1
    cleandump = ({'Battery Voltage': nolabelitems[0], 'Target Voltage': nolabelitems[1], 'Charging Current': nolabelitems[2],
                    'Array Voltage': nolabelitems[3], 'Array Current': nolabelitems[4], 'Output Power': nolabelitems[5],
                    'Sweep Vmp': nolabelitems[6], 'Sweep Voc': nolabelitems[7], 'Sweep Pmax': nolabelitems[8], 'Battery Temperature': nolabelitems[9], 'Controller Temperature': nolabelitems[10],
                    'Kilowatt Hours': nolabelitems[11], 'Controller Status': nolabelitems[12], 'Absorption': nolabelitems[13], 'Equalization': nolabelitems[14],  'Float': nolabelitems[15], 
                    'Max Energy daily': nolabelitems[16], 'Ampere Hours daily': nolabelitems[17], 'Watt Hours daily': nolabelitems[18], 'Max Voltage daily': nolabelitems[19],  
                    'Max Battery Voltage daily': nolabelitems[20], 'Min Battery Voltage daily': nolabelitems[21], 'Input Power': nolabelitems[22], 'LED Status': nolabelitems[23],
                    'Battery Poles Voltage': nolabelitems[24], 'Battery Sensor Voltage': nolabelitems[25], 'Temperature': nolabelitems[26], 'Cloud Cover': nolabelitems[27], 'Production Today': nolabelitems[28], 'Production Tomorrow': nolabelitems[29]})
    return cleandump

@app.route('/tristar', methods=['GET'])
#tristar endpoint
def tristar():
    batteryvoltage, targetvoltage, chargingcurrent, arrayvoltage, arraycurrent, outputpower, sweepvmp, sweepvoc, sweeppmax, batterytemp, controllertemp, kilowatthours, status, absorptionduration, balanceduration, floatduration, maxenergydaily, amperehoursdaily, watthoursdaily, maxvoltagedaily, maxbatteryvoltagedaily, minbatteryvoltagedaily, inputpower, led, batterypolesvoltage, batterysensorvoltage, locationtemp, locationcloud, productiontoday, productiontomorrow = load_data()
    if weather.upper() == 'ON' and temppreference.upper() == 'F':
        controllertemp = convert_to_fahrenheit(controllertemp)
        batterytemp = convert_to_fahrenheit(batterytemp)
        locationtemp = convert_to_fahrenheit(locationtemp)
    return jsonify({'Battery Voltage': batteryvoltage, 'Target Voltage': targetvoltage, 'Charging Current': chargingcurrent,
                    'Array Voltage': arrayvoltage, 'Array Current': arraycurrent, 'Output Power': outputpower,
                    'Sweep Vmp': sweepvmp, 'Sweep Voc': sweepvoc, 'Sweep Pmax': sweeppmax, 'Battery Temperature': batterytemp, 'Controller Temperature': controllertemp,
                    'Kilowatt Hours': kilowatthours, 'Controller Status': status, 'Absorption': absorptionduration, 'Equalization': balanceduration,  'Float': floatduration, 
                    'Max Energy daily': maxenergydaily, 'Ampere Hours daily': amperehoursdaily, 'Watt Hours daily': watthoursdaily, 'Max Voltage daily': maxvoltagedaily,  
                    'Max Battery Voltage daily': maxbatteryvoltagedaily, 'Min Battery Voltage daily': minbatteryvoltagedaily, 'Input Power': inputpower, 'LED Status': led,
                    'Battery Poles Voltage': batterypolesvoltage, 'Battery Sensor Voltage': batterysensorvoltage, 'Temperature': locationtemp, 'Cloud Cover': locationcloud, 'Production Today': productiontoday, 'Production Tomorrow': productiontomorrow})


#app.run(host='0.0.0.0', port=5715)

serve(app, host="0.0.0.0", port=5715)