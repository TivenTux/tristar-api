## REST API for MorningStar solar charging controllers

Useful for interfacing with smart home systems, graphing, logging, etc. Made for Tristar product category but should also work with most, if not all [MorningStar](https://www.morningstarcorp.com/) products. 

### Environment variables

| Environment Variable  | Description                                                                         |
|-----------------------|-------------------------------------------------------------------------------------|
| `TRISTAR_ADDRESS`     | Please set this to the address of your Solar Controller's Live Data View page. <br/> example: `192.168.1.5:80`              

You can set multiple environment variables, in an environment file (example: `.env`) and then pass the file as an argument in the CLI as documented 
[here](https://docs.docker.com/compose/environment-variables/set-environment-variables/):
```bash
$ docker compose --env-file .env
```
This file path is relative to the current working directory where the Docker Compose command is executed.


### Running the container

After cloning this repository, you can run

```bash
$ docker compose --env-file .env up

```

Will provide API endpoint at **``http://your_IP:8081/tristar``** with the following items:<br>

*Absorption,Ampere Hours daily, Array Current, Array Voltage, Battery Poles Voltage, Battery Sensor Voltage, Battery Temperature, Battery Voltage, Charging Current, Cloud Cover, Controller Status, Controller Temperature, Equalization, Float, Input Power, Kilowatt Hours, LED Status, Max Battery Voltage daily, Max Energy daily, Max Voltage daily, Min Battery Voltage daily, Output Power, Production Today, Production Tomorrow,
 Sweep Pmax, Sweep Vmp, Sweep Voc, Target Voltage, Temperature, Watt Hours daily*


Endpoint ``http://your_IP:8081/tristarclean`` will provide the items without measuring symbols.