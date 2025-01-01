1. Install Prerequisites
   Python and Pip
   Ensure you have Python 3.8 or later installed on your system. You can check with:

```
python3 --version
pip3 --version
```
Install Flask
Install the dependencies specified in requirements.txt:

```
pip install -r requirements.txt
```
2. Start the Service
   Run the app.py file:
```
python3 app.py
```

3. Test the API
   Use a tool like Postman, curl, or a browser to test the API.

Example: Using curl
```
curl -X POST http://127.0.0.1:5000/api/v1/generate-paths \
-H "Content-Type: application/json" \
-d '{
"client": 2,
"service": 4,
"api_split": [2, 3, 2, 1],
"topic": 2,
"consumer_split": [0, 0, 1, 2],
"min_length": 2,
"max_length": 8,
"num_paths": 25
}'
```
```
Expected Response:

json
Copy code
{
"paths": [
"c1-s1a1-t1-s1m1",
"c2-s2a2-s3m1",
"c1-t2-s4m1",
...
]
}
```
Curl for inserting a path manually
```text
curl --location 'http://127.0.0.1:5000/api/v1/insert-paths' \
--header 'Content-Type: application/json' \
--data '{
    "paths": [
        "c1-s1a1-s2a2"
    ]
}'
```

To insert the paths manually use the following curl:
```text
curl --location 'http://127.0.0.1:5000/api/v1/insert-paths' \
--header 'Content-Type: application/json' \
--data '{
    "paths": [
        "c1-s1a2-t1-s2m1"
    ]
}'
```