curl -i -X POST http://192.168.0.12:8089/v1/svs -v -H "X-Auth-Token:$tokens" -H "Content-Type:multipart/form-data; boundary=----WebKitFormBoundaryb4FrxH4rOqSh3wEq" -d '------WebKitFormBoundaryb4FrxH4rOqSh3wEq
Content-Disposition: form-data; name="svfile"; filename="hello.py"
Content-Type: text/plain

hello world!!!
------WebKitFormBoundaryb4FrxH4rOqSh3wEq
Content-Disposition: form-data; name="sv_name"

svname
------WebKitFormBoundaryb4FrxH4rOqSh3wEq
Content-Disposition: form-data; name="vm_id"

4f7b2604-e062-450a-be81-dca6b8eab58a
------WebKitFormBoundaryb4FrxH4rOqSh3wEq
Content-Disposition: form-data; name="sv_lang"

java
------WebKitFormBoundaryb4FrxH4rOqSh3wEq
Content-Disposition: form-data; name="sv_desc"

the test for the sv upload
------WebKitFormBoundaryb4FrxH4rOqSh3wEq
Content-Disposition: form-data; name="input_arg_names"

input_arg1
------WebKitFormBoundaryb4FrxH4rOqSh3wEq
Content-Disposition: form-data; name="input_arg_types"

1
------WebKitFormBoundaryb4FrxH4rOqSh3wEq
Content-Disposition: form-data; name="input_arg_names"

input_arg2
------WebKitFormBoundaryb4FrxH4rOqSh3wEq
Content-Disposition: form-data; name="input_arg_types"

2
------WebKitFormBoundaryb4FrxH4rOqSh3wEq
Content-Disposition: form-data; name="output_arg_names"

output_arg1
------WebKitFormBoundaryb4FrxH4rOqSh3wEq
Content-Disposition: form-data; name="output_arg_types"

2
------WebKitFormBoundaryb4FrxH4rOqSh3wEq
Content-Disposition: form-data; name="output_arg_names"

output_arg2
------WebKitFormBoundaryb4FrxH4rOqSh3wEq
Content-Disposition: form-data; name="output_arg_types"

3
------WebKitFormBoundaryb4FrxH4rOqSh3wEq
Content-Disposition: form-data; name="output_arg_names"

output_arg3
------WebKitFormBoundaryb4FrxH4rOqSh3wEq
Content-Disposition: form-data; name="output_arg_types"

5
------WebKitFormBoundaryb4FrxH4rOqSh3wEq--'
