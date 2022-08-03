import time, os, random, requests, json
import asyncio, datetime
import urllib.request, sqlite3
from pyppeteer import launch
from constants import *

#check if webserver is running
def check_webserver(url):
    return requests.head(url, timeout=5).status_code < 400

#fetch weather data
def get_weather():
    try:
        if lat == 'n/a' or lon == 'n/a':
            return 'n/a', 'n/a'
        response = requests.get((weatherapiurl_base + 'lat=' + str(lat.replace(',', '.')) + '&' + 'lon=' + str(lon.replace(',', '.'))), timeout=5, headers=headers)
        payload = json.loads(response.text)
        return payload['properties']['timeseries'][0]['data']['instant']['details']['air_temperature'], payload['properties']['timeseries'][0]['data']['instant']['details']['cloud_area_fraction']
    except Exception as e:
        print(e)
    return 'n/a', 'n/a'

#push updates to database
async def update_data(recordid, batteryvoltage, targetvoltage, chargingcurrent
    , arrayvoltage, arraycurrent, outputpower, sweepvmp, sweepvoc, sweeppmax
    , batterytemp, controllertemp, kilowatthours, status, absorption, balance
    , controllerfloat, maxenergydaily, amperehoursdaily, watthoursdaily, maxvoltagedaily
    , maxbatteryvoltagedaily, minbatteryvoltagedaily, inputpower, led, batterypolesvoltage
    , batterysensorvoltage, locationtemp, locationcloud):

    connection = sqlite3.connect(database, isolation_level=None)
    cur = connection.cursor()
    try:
        with connection:
            cur = connection.cursor()
            connection.execute('pragma journal_mode=wal')
            sql1 = '''UPDATE tristar SET (batteryvoltage, targetvoltage, chargingcurrent
    , arrayvoltage, arraycurrent, outputpower, sweepvmp, sweepvoc, sweeppmax
    , batterytemp, controllertemp, kilowatthours, status, absorption, balance
    , float, maxenergydaily, amperehoursdaily, watthoursdaily, maxvoltagedaily
    , maxbatteryvoltagedaily, minbatteryvoltagedaily, inputpower, led, batterypolesvoltage
    , batterysensorvoltage, locationtemp, locationcloud) = (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) WHERE id = ?'''
            s1 = cur.execute(sql1, (batteryvoltage, targetvoltage, chargingcurrent
    , arrayvoltage, arraycurrent, outputpower, sweepvmp, sweepvoc, sweeppmax
    , batterytemp, controllertemp, kilowatthours, status, absorption, balance
    , controllerfloat, maxenergydaily, amperehoursdaily, watthoursdaily, maxvoltagedaily
    , maxbatteryvoltagedaily, minbatteryvoltagedaily, inputpower, led, batterypolesvoltage
    , batterysensorvoltage, locationtemp, locationcloud, recordid))    
        connection.commit()    
    except Exception as e: 
        print(e)
    print('done writing db')
    return

#update cache stats
def update_cache(recordid, lastweather):

    connection = sqlite3.connect(database, isolation_level=None)
    cur = connection.cursor()
    try:
        with connection:
            cur = connection.cursor()
            connection.execute('pragma journal_mode=wal')
            sql1 = '''UPDATE cache SET (lastweather) = (?) WHERE id = ?'''
            s1 = cur.execute(sql1, (lastweather, recordid))    
        connection.commit()    
    except Exception as e: 
        print(e)
    print('updated cache')
    return

#access cache data
def read_cache():
    connection = sqlite3.connect(database)
    cur = connection.cursor()
    try:
        rows = cur.execute(
            "SELECT lastweather FROM cache WHERE id = ?",
            (0,),
        ).fetchall()
        lastweather = rows[0][0]
        return lastweather                
    except Exception as e:
        print(e)
    return

#load data from database
def load_data():
    connection = sqlite3.connect(database)
    cur = connection.cursor()
    try:
        rows = cur.execute(
            '''SELECT locationtemp, locationcloud FROM tristar WHERE id = ?''',
            (0,),
        ).fetchall()
        locationtemp = rows[0][0]
        locationcloud = rows[0][1]
        return locationtemp, locationcloud
    except Exception as e:
        print(e)
    return

#scrape php page
async def get_value(page, div):
    element = await page.querySelector(div)
    title = await page.evaluate('(element) => element.textContent', element)
    value = title.partition(':')[2]
    return value

async def scrape_and_update():
    try:
        recordid = 0
        locationtemp = 'n/a'
        locationcloud = 'n/a'
        webserverfound = ''
        timenow = int(time.time()) 
        lastweather = read_cache()
        #check cache age, update if old
        if (timenow - int(lastweather)) > 350:
            try:
                locationtemp, locationcloud = get_weather()
                update_cache(recordid, timenow)
                print('cache is old, fetching new weather data')
            except Exception as e:
                print(e)   
        else:
            locationtemp, locationcloud = load_data()
            print('using cached weather data')
        try:
            webserver_status = check_webserver(controllerphppath)   
        except Exception as e:
            webserverfound = 'error'
            print(e)
        if webserverfound == 'error':
            print('webserver not running or phppath incorrect')
            return
        #please ensure chrome is installed and the correct directory set in constants
        browser = await launch(executablePath=chromepath, headless=True, args= [])
        page = await browser.newPage() 
        ##await page.setUserAgent(pypp_user_agent);  
        await page.goto(controllerphppath, {"waitUntil" : ["load","domcontentloaded","networkidle2"], "timeout" : 8000}) 
        #enough time for everything to load
        await asyncio.sleep(2.5)  
        #scrape all values
        led = await get_value(page, ledstatusdiv)
        batteryvoltage = await get_value(page, batteryvoltagediv)
        targetvoltage = await get_value(page, targetvoltagediv)
        chargingcurrent = await get_value(page, chargingcurrentdiv)
        arrayvoltage = await get_value(page, arrayvoltagediv)
        arraycurrent = await get_value(page, arraycurrentdiv)
        outputpower = await get_value(page, outputpowerdiv)
        sweepvmp = await get_value(page, sweepvmpdiv)
        sweepvoc = await get_value(page, sweepvocdiv)
        sweeppmax = await get_value(page, sweeppmaxdiv)
        batterytemp = await get_value(page, batterytempdiv)
        controllertemp = await get_value(page, controllertempdiv)
        kilowatthours = await get_value(page, killowatthoursdiv)
        status = await get_value(page, controllerstatusdiv)
        absorption = await get_value(page, controllerabsorptiondiv)
        balance = await get_value(page, controllerbalancediv)
        controllerfloat = await get_value(page, controllerfloatdiv)
        maxenergydaily = await get_value(page, maxenergydailydiv)
        amperehoursdaily = await get_value(page, amperehoursdailydiv)
        watthoursdaily = await get_value(page, watthoursdailydiv)
        maxvoltagedaily = await get_value(page, maxvoltagedailydiv)
        maxbatteryvoltagedaily = await get_value(page, maxbatteryvoltagedailydiv)
        minbatteryvoltagedaily = await get_value(page, minbatteryvoltagedailydiv)
        batterypolesvoltage = await get_value(page, batterypolesvoltagediv)
        batterysensorvoltage = await get_value(page, batterysensorvoltagediv)
        inputpower = await get_value(page, inputpowerdiv)
        #update database with values
        await update_data(recordid, batteryvoltage, targetvoltage, chargingcurrent
        , arrayvoltage, arraycurrent, outputpower, sweepvmp, sweepvoc, sweeppmax
        , batterytemp, controllertemp, kilowatthours, status, absorption, balance
        , controllerfloat, maxenergydaily, amperehoursdaily, watthoursdaily, maxvoltagedaily
        , maxbatteryvoltagedaily, minbatteryvoltagedaily, inputpower, led, batterypolesvoltage
        , batterysensorvoltage, locationtemp, locationcloud)
 
    except Exception as e:
      print(e)   
    await browser.close()
    return


async def Main():
    await scrape_and_update()
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Main())

