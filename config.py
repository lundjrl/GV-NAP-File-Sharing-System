import pyrebase

config = {
  "apiKey": "AIzaSyBGhZCVHZ5FPt3cMzxS8r85riLZU_rhMrA",
  "authDomain": "cis457-project2.firebaseapp.com",
  "databaseURL": "https://cis457-project2.firebaseio.com",
  "storageBucket": "cis457-project2"
}

firebase = pyrebase.initialize_app(config)
