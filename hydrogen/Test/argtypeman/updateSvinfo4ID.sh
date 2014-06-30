curl -i -X PUT http://192.168.0.12:8089/v1/argtypes/$1 -H "X-Auth-Token:$tokens" -H "Content-Type:application/json" -d '{"arg_type_name":"float","arg_type_desc":"a test for the argtype update"}'
