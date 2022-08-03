#location of your webserver, hosting controller.php
controllerphppath = 'http://192.168.50.40/controller.php'
#if the enviroment is set correctly this should be fine, otherwise use absolute path here
database = './controller.db'
#please ensure chrome is installed and the correct directory set here
chromepath = '/usr/bin/google-chrome'

#physical location of solar installation - for live weather data and estimated production
#change from 'n/a' to enable
#you can find coordinates for your location on websites such as https://www.latlong.net/ or https://www.gps-coordinates.net/
lat='n/a'
lon='n/a'

#solar installation settings - change from 'n/a' to enable
#will produce estimated power stats
#plane declination, 0 is horizontal 90 is vertical
declination = 'n/a'
#plane azimuth, -180 to 180 (-180 = north, -90 = east, 0 = south, 90 = west, 180 = north)
azimuth = 'n/a'
#installed modules power in kilo watt (1 = 1000Watts, 0.43 = 430Watts)
kwatts_production = 'n/a'

weatherapiurl_base = 'https://api.met.no/weatherapi/locationforecast/2.0/compact?'

batteryvoltagediv = 'body > div:nth-child(1)'
targetvoltagediv = 'body > div:nth-child(2)'
chargingcurrentdiv = 'body > div:nth-child(3)'
arrayvoltagediv = 'body > div:nth-child(4)'
arraycurrentdiv = 'body > div:nth-child(5)'
outputpowerdiv = 'body > div:nth-child(6)'
sweepvmpdiv = 'body > div:nth-child(7)'
sweepvocdiv = 'body > div:nth-child(8)'
sweeppmaxdiv = 'body > div:nth-child(9)'
batterytempdiv = 'body > div:nth-child(10)'
controllertempdiv = 'body > div:nth-child(11)'
killowatthoursdiv = 'body > div:nth-child(12)'
controllerstatusdiv = 'body > div:nth-child(13)'
controllerabsorptiondiv = 'body > div:nth-child(14)'
controllerbalancediv = 'body > div:nth-child(15)'
controllerfloatdiv = 'body > div:nth-child(16)'
maxenergydailydiv = 'body > div:nth-child(17)'
amperehoursdailydiv = 'body > div:nth-child(18)'
watthoursdailydiv = 'body > div:nth-child(19)'
maxvoltagedailydiv = 'body > div:nth-child(20)'
maxbatteryvoltagedailydiv = 'body > div:nth-child(21)'
minbatteryvoltagedailydiv = 'body > div:nth-child(22)'
inputpowerdiv = 'body > div:nth-child(23)'
ledstatusdiv = 'body > div:nth-child(24)'
batterypolesvoltagediv = 'body > div:nth-child(25)'
batterysensorvoltagediv = 'body > div:nth-child(26)'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
pypp_user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'