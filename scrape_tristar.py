import time, os, random, requests, json
import asyncio, datetime
import urllib.request, sqlite3
from pyppeteer import launch
from constants import *


#load data testing
async def load_data():
    connection = sqlite3.connect(database)
    cur = connection.cursor()
    try:
        rows = cur.execute(
            "SELECT batteryvoltage FROM tristar WHERE id = ?",
            (0,),
        ).fetchall()
        print(rows)
                                          
    except Exception as e:
        print(e)
    return

async def update_data(recordid, batteryvoltage, targetvoltage, chargingcurrent
    , arrayvoltage, arraycurrent, outputpower, sweepvmp, sweepvoc, sweeppmax
    , batterytemp, controllertemp, kilowatthours, status, absorption, balance
    , controllerfloat, maxenergydaily, amperehoursdaily, watthoursdaily, maxvoltagedaily
    , maxbatteryvoltagedaily, minbatteryvoltagedaily, inputpower, led, batterypolesvoltage
    , batterysensorvoltage):

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
    , batterysensorvoltage) = (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) WHERE id = ?'''
            s1 = cur.execute(sql1, (batteryvoltage, targetvoltage, chargingcurrent
    , arrayvoltage, arraycurrent, outputpower, sweepvmp, sweepvoc, sweeppmax
    , batterytemp, controllertemp, kilowatthours, status, absorption, balance
    , controllerfloat, maxenergydaily, amperehoursdaily, watthoursdaily, maxvoltagedaily
    , maxbatteryvoltagedaily, minbatteryvoltagedaily, inputpower, led, batterypolesvoltage
    , batterysensorvoltage, recordid))    
        connection.commit()    
    except Exception as e: 
        print(e)
    print('done writing db')
    return

async def get_value(page, div):
    element = await page.querySelector(div)
    title = await page.evaluate('(element) => element.textContent', element)
    value = title.partition(':')[2]
    return value

async def scrape_and_update():
    try:
        recordid = 0
        #please ensure chrome is installed and the correct directory set in constants
        browser = await launch(executablePath=chromepath, headless=True, args= [])
        page = await browser.newPage() 
        #await page.setUserAgent("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36");  
        #await page.setViewport({"width": 800, "height": 600})
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
        , batterysensorvoltage)
 
    except Exception as e:
      print(e)   
    await browser.close()
    return


async def Main():
    await scrape_and_update()
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Main())

