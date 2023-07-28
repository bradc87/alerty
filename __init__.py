from flask import Flask
import routes
app = Flask(__name__, static_folder='static')
app.run(debug=True, use_reloader=False, port=8080)