from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome to the HTTPS server!'

if __name__ == '__main__':
    app.run(debug=True, ssl_context=('ssl_cert/cert.pem', 'ssl_cert/key.pem'))
