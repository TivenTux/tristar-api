# REST API for MorningStar solar charging controllers

Useful for interfacing with smart home systems, graphing, logging, etc. Made for Tristar product category but should work with most, if not all [MorningStar](https://www.morningstarcorp.com/) products. 

Set env variable **TRISTAR_ADDRESS** with the address of your solar charging controller(ip:port)<br>

install:<br>
**docker compose up**

**provides api endpoint under ``http://your_IP:8081/tristar`` with the following items:<br>

__Absorption,Ampere Hours daily, Array Current, Array Voltage, Battery Poles Voltage, Battery Sensor Voltage, Battery Temperature, Battery Voltage, Charging Current, Cloud Cover, Controller Status, Controller Temperature, Equalization, Float, Input Power, Kilowatt Hours, LED Status, Max Battery Voltage daily, Max Energy daily, Max Voltage daily, Min Battery Voltage daily, Output Power, Production Today, Production Tomorrow,
 Sweep Pmax, Sweep Vmp, Sweep Voc, Target Voltage, Temperature, Watt Hours daily__