from flask import Flask, render_template
from backend.RedisStore import RedisStore

app = Flask(__name__)
store = RedisStore()

@app.route('/')
def index():
    tweets = store.getTweets()
    return render_template('index.html', tweets=tweets)

if __name__ == '__main__':
    app.run(debug=True)
