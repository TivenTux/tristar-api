import time
import os
import requests
import json
import asyncio
from datetime import datetime, timedelta
import sqlite3
from pyppeteer import launch
from constants import *

#check if webserver is running
def check_webserver(url):
    '''
    Checks url and finds webserver status
    '''
    return requests.head(url, timeout=5).status_code < 400

#fetch weather data
def get_weather():
    '''
    Returns weather data according to gps coordinates in conf
    '''
    try:
        if lat == 'n/a' or lon == 'n/a':
            return 'n/a', 'n/a'
        response = requests.get((weatherapiurl_base + 'lat=' + str(lat.replace(',', '.')) + '&' + 'lon=' + str(lon.replace(',', '.'))), timeout=5, headers=headers)
        payload = json.loads(response.text)
        return str(payload['properties']['timeseries'][0]['data']['instant']['details']['air_temperature']) + 'C', payload['properties']['timeseries'][0]['data']['instant']['details']['cloud_area_fraction']
    except Exception as e:
        print(e)
    return 'n/a', 'n/a'

#get solar production data
def get_solar():
    '''
    Calculates future estimated solar production according to various options set in conf.
    '''
    try:
        if lat == 'n/a' or lon == 'n/a' or azimuth == 'n/a' or kwatts_production == 'n/a' or declination == 'n/a':
            return 'n/a', 'n/a'
        response = requests.get((solarapiurl_base + str(lat.replace(',', '.')) + '/' + str(lon.replace(',', '.')) + '/' + str(declination) + '/' + str(azimuth) + '/' + str(kwatts_production)), timeout=5, headers=headers)
        payload = json.loads(response.text)
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrowdate = tomorrow.strftime('%Y-%m-%d')
        return str(payload['result']['watt_hours_day'][(time.strftime('%Y-%m-%d'))]) + 'W', str(payload['result']['watt_hours_day'][tomorrowdate]) + 'W'
    except Exception as e:
        print(e)
    return 'n/a', 'n/a'

#push updates to database
async def update_data(recordid, batteryvoltage, targetvoltage, chargingcurrent
    , arrayvoltage, arraycurrent, outputpower, sweepvmp, sweepvoc, sweeppmax
    , batterytemp, controllertemp, kilowatthours, status, absorption, balance
    , controllerfloat, maxenergydaily, amperehoursdaily, watthoursdaily, maxvoltagedaily
    , maxbatteryvoltagedaily, minbatteryvoltagedaily, inputpower, led, batterypolesvoltage
    , batterysensorvoltage, locationtemp, locationcloud, productiontoday, productiontomorrow):

    '''
    Takes all available scraped data and pushes to the database
    '''
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
    , batterysensorvoltage, locationtemp, locationcloud, productiontoday, productiontomorrow) = (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) WHERE id = ?'''
            s1 = cur.execute(sql1, (batteryvoltage, targetvoltage, chargingcurrent
    , arrayvoltage, arraycurrent, outputpower, sweepvmp, sweepvoc, sweeppmax
    , batterytemp, controllertemp, kilowatthours, status, absorption, balance
    , controllerfloat, maxenergydaily, amperehoursdaily, watthoursdaily, maxvoltagedaily
    , maxbatteryvoltagedaily, minbatteryvoltagedaily, inputpower, led, batterypolesvoltage
    , batterysensorvoltage, locationtemp, locationcloud, productiontoday, productiontomorrow, recordid))    
        connection.commit()    
    except Exception as e: 
        print(e)
    print('done writing db')
    return

#update cache stats
def update_cache(recordid, type, cachedata):
    '''
    Caches weather and solar production data to make it easier on the APIs.
    '''
    connection = sqlite3.connect(database, isolation_level=None)
    cur = connection.cursor()
    try:
        with connection:
            if type == 'weather':
                cur = connection.cursor()
                connection.execute('pragma journal_mode=wal')
                sql1 = '''UPDATE cache SET (lastweather) = (?) WHERE id = ?'''
                s1 = cur.execute(sql1, (cachedata, recordid))    
            if type == 'solar':
                cur = connection.cursor()
                connection.execute('pragma journal_mode=wal')
                sql1 = '''UPDATE cache SET (lastsolar) = (?) WHERE id = ?'''
                s1 = cur.execute(sql1, (cachedata, recordid))   
        connection.commit()    
    except Exception as e: 
        print(e)
    print('updated cache')
    return

#access cache data
def read_cache():
    '''
    Loads cached solar and weather data.
    '''
    connection = sqlite3.connect(database)
    cur = connection.cursor()
    try:
        rows = cur.execute(
            "SELECT lastweather, lastsolar FROM cache WHERE id = ?",
            (0,),
        ).fetchall()
        lastweather = rows[0][0]
        lastsolar = rows[0][1]
        return lastweather, lastsolar                
    except Exception as e:
        print(e)
    return

#load data from database
def load_data(type):
    '''
    Loads data from the database
    '''
    connection = sqlite3.connect(database)
    cur = connection.cursor()
    try:
        if type == 'weather':
            rows = cur.execute(
                '''SELECT locationtemp, locationcloud FROM tristar WHERE id = ?''',
                (0,),
            ).fetchall()
            locationtemp = rows[0][0]
            locationcloud = rows[0][1]
            return locationtemp, locationcloud
        if type == 'solar':
            rows = cur.execute(
                '''SELECT productiontoday, productiontomorrow FROM tristar WHERE id = ?''',
                (0,),
            ).fetchall()
            productiontoday = rows[0][0]
            productiontomorrow = rows[0][1]
            return productiontoday, productiontomorrow            
    except Exception as e:
        print(e)
    return

#scrape php page
async def get_value(page, div):
    '''
    Takes page, css div and returns scraped value.
    '''
    element = await page.querySelector(div)
    title = await page.evaluate('(element) => element.textContent', element)
    value = title.partition(':')[2]
    return value
#scrape data and push updates
async def scrape_and_update():
    '''
    Scrapes data and calls functions to update db.
    '''
    try:
        recordid = 0
        locationtemp = 'n/a'
        locationcloud = 'n/a'
        webserverfound = ''
        productiontoday = 'n/a'
        productiontomorrow = 'n/a'
        timenow = int(time.time()) 
        lastweather, lastsolar = read_cache()
        if weather.upper() == 'ON':
            #check cache age, update if old
            if (timenow - int(lastweather)) > 350:
                try:
                    locationtemp, locationcloud = get_weather()
                    update_cache(recordid, 'weather', timenow)
                    print('cache is old, fetching new weather data')
                except Exception as e:
                    print(e)   
            else:
                locationtemp, locationcloud = load_data('weather')
                print('using cached weather data')
        if solarproduction.upper() == 'ON':
        #check solar production cache and update if old
            if (timenow - int(lastsolar)) > 950:
                try:
                    productiontoday, productiontomorrow = get_solar()
                    update_cache(recordid, 'solar', timenow)
                    print('cache is old, fetching new solar data')
                except Exception as e:
                    print(e)   
            else:
                productiontoday, productiontomorrow = load_data('solar')
                print('using cached solar data')   
        #check if webserver is setup correctly         
        try:
            webserver_status = check_webserver(controllerphppath)  
        except Exception as e:
            webserverfound = 'error'
            print(e)
        if webserverfound == 'error' or webserver_status != True:
            print('webserver error or phppath incorrect')
            return
        #please ensure chrome is installed and the correct directory set in constants
        browser = await launch(executablePath=chromepath, headless=True, args= ['--no-sandbox'])
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
        , batterysensorvoltage, locationtemp, locationcloud, productiontoday, productiontomorrow)
 
    except Exception as e:
      print(e)   
    await browser.close()
    return


async def Main():
    await scrape_and_update()
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Main())

