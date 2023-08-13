# REST API for tristar solar controllers

Useful for convenient access with smart home systems, graphing, logging, etc. Should work with most, if not all, [MorningStar](https://www.morningstarcorp.com/) products. It is recommended to use a webserver and proxy the traffic to flask and to your solar controller.  

_Able to connect with weather and solar forecast APIs in order to predict future solar production. Disabled by default_

Requires any webserver (with php), pyppeteer, flask, waitress (pip) and chrome or chromium.  

Edit ip_tristar="ip:port" and point to your solar charger, in controller.php  
Edit controllerphppath in constants.py, to point to your webserver that is hosting controller.php  

Run scrape_tristar.py with cron, on the frequency you need to update the data.  

tristar_api.py will provide api endpoint under ``http://your_IP:5715/tristar``  


### kernel
some distros might need this for chrome sandbox support on kernel 
```sh
$ sudo sysctl -w kernel.unprivileged_userns_clone=1
```

### deps
for chrome
```sh
$ sudo apt install gconf-service libasound2 libatk1.0-0 libatk-bridge2.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget
```
