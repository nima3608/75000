from flask import Flask
import redis
import os

app = Flask(__name__)

# Load Redis configuration from environment variables
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

# Attempt to connect to Redis
try:
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
    r.ping()  # Test the connection
except redis.exceptions.ConnectionError:
    print("Fehler: Verbindung zu Redis nicht möglich")
    r = None  # Prevent usage if the connection fails

def test_redis_connection():
    """Function to test Redis set/get operations"""
    if r:
        r.set('key', 'value')
        print(f"Redis Test: {r.get('key')}")

@app.route('/')
def hello():
    """Route that increments visit count in Redis"""
    if r:
        count = r.incr('visits')  # Increment the "visits" key
        return f"Hello Nima Joon! This page has been viewed {count} times."
    else:
        return "Redis-Verbindung nicht verfügbar, kann Besucherzahl nicht speichern."

if __name__ == '__main__':
    test_redis_connection()  # Run test on startup
    app.run(debug=True, host='0.0.0.0', port=5000)
