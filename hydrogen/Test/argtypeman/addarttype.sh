curl -i -X POST http://192.168.0.12:8089/v1/argtypes -v -H "X-Auth-Token:$tokens" -H "Content-Type:application/json"  -d '{"arg_type_name":"string","arg_type_desc":"the description of string"}'
