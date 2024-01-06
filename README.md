# Post Bot
Bot that posts on Twitter (𝕏).

### Patents Bot
Fetch a new patent from the government official public data source and post it once a day.

### Weather Bot
Fetch the weather from openweathermap API and post it once a day.

Stack:
- Python 3.10
- Twitter API (tweepy)
- GCP Firebase - Firestore
- AWS Lambda
- AWS Secrets Manager
- data.gov.il public API
- Docker

### Setup
#### Cloud
https://docs.aws.amazon.com/lambda/latest/dg/python-image.html
#### Local
```bashx
pip install -r requirements.txt
python patent_bot/local_runner.py
```
