curl  -X GET http://192.168.0.12:8089/v1/svs/$1 -v -H "X-Auth-Token:$tokens"|python -mjson.tool
