# Project name: Back-end


## Getting Started Guide


### requirements

To run this project, you need to have the following programs installed:

- Python 3.10+
- Django 3.2+
- інші необхідні бібліотеки (зазначте їх тут)

### Installation

1. Clone this repository to your local computer.

git clone https://github.com/VitalyBashkiser/Back-end.git


2. Create and activate a virtual environment.

python -m venv venv
venv\Scripts\activate (Windows)


3. Install the necessary libraries.

pip install -r requirements.txt


4. Start the Django server.

python manage.py runserver

5. Now you can follow the link (http://127.0.0.1:8000/) in your browser.


##Testing

python manage.py test


## Endpoint "health check"

Your project has an endpoint `/` that returns a JSON response with status 200, details "ok" and result "working".

```json

{
  "status_code": 200,
  "detail": "ok",
  "result": "working"
}


