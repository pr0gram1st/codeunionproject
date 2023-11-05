# codeunionproject

All Dependencies listed in requierments.txt

1. Go to the project directory by running the command ``` cd codeunionproject ```
2. Install all dependencies by running the command ``` pip install requirements.txt ```
3. To run unit tests run command: ``` python3 manage.py test ```
4. Ensure that all tests are passed
5. Run the server (``` python3 manage.py runserver ```) and go to the http://127.0.0.1:8000/api/currencies and ensure that there's no access to the api
6. Use one of the existing tokens (9d0f5bc008b0ff5d7e2ce43cc6225bea25290c17 for example) and type this to che Terminal: ``` curl -X GET http://127.0.0.1:8000/api/currencies/ 'Authorization: Token 9d0f5bc008b0ff5d7e2ce43cc6225bea25290c17' ```
