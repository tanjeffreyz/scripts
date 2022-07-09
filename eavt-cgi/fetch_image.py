import os
import json

result = {}
for param in os.environ.keys():
    result[param] = os.environ[param]

print('Access-Control-Allow-Origin: *\n\n')
print('Content-type: application/json\n\n')
print(json.dumps(result))
