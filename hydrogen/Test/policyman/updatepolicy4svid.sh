curl -i -X PUT http://192.168.0.12:8089/v1/svs/$1/policies/$2 -H "X-Auth-Token:$tokens" -H "Content-Type:application/json" -d '{"role":"nuser","user_id":"98jjjj2s","timelimit":"100"}'
