from flask import Flask
from threading import Thread
app = Flask('')
@app.route('/')
def home():
  return "I'm alive"
def run():
  app.run(host='0.0.0.0', port=7000)
def keep_alive():
  t = Thread(target=run)
  t.start()
if __name__ == "__main__":
  keep_alive()
  while True:
    pass  # Keep the main thread running
