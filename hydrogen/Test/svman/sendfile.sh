curl -i -X POST http://192.168.0.12:8089/v1/svs -v -H "X-Auth-Token:$tokens" -H "Content-Type:multipart/form-data; boundary=----WebKitFormBoundaryqrVK0aPq2EUo1Lxi" -d '------WebKitFormBoundaryqrVK0aPq2EUo1Lxi
Content-Disposition: form-data; name="svfile"; filename="h.txt"
Content-Type: text/plain

hello test!!!
------WebKitFormBoundaryqrVK0aPq2EUo1Lxi
Content-Disposition: form-data; name="sv_name"

12345
------WebKitFormBoundaryqrVK0aPq2EUo1Lxi
Content-Disposition: form-data; name="vm_id"

1
------WebKitFormBoundaryqrVK0aPq2EUo1Lxi
Content-Disposition: form-data; name="sv_lang"

java
------WebKitFormBoundaryqrVK0aPq2EUo1Lxi
Content-Disposition: form-data; name="sv_desc"

asdfasdsdfasdfasdfasdfasdfasdf
------WebKitFormBoundaryqrVK0aPq2EUo1Lxi
Content-Disposition: form-data; name="input_arg_names"

inname1;inname2;inname3
------WebKitFormBoundaryqrVK0aPq2EUo1Lxi
Content-Disposition: form-data; name="input_arg_name0"

1
------WebKitFormBoundaryqrVK0aPq2EUo1Lxi
Content-Disposition: form-data; name="input_arg_name1"

2
------WebKitFormBoundaryqrVK0aPq2EUo1Lxi
Content-Disposition: form-data; name="input_arg_name2"

3
------WebKitFormBoundaryqrVK0aPq2EUo1Lxi
Content-Disposition: form-data; name="output_arg_names"

outname1;outname2;outname3
------WebKitFormBoundaryqrVK0aPq2EUo1Lxi
Content-Disposition: form-data; name="output_arg_name0"

3
------WebKitFormBoundaryqrVK0aPq2EUo1Lxi
Content-Disposition: form-data; name="output_arg_name1"

2
------WebKitFormBoundaryqrVK0aPq2EUo1Lxi
Content-Disposition: form-data; name="output_arg_name2"

1
------WebKitFormBoundaryqrVK0aPq2EUo1Lxi--'
