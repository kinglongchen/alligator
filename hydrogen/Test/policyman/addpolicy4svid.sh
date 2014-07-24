curl -i -X POST http://192.168.0.12:8089/v1/svs/$1/policies -H "X-Auth-Token:$tokens" -H "Content-Type:application/json" -d '{"role":"dev","user_id":"123124","timelimit":"20"}'
