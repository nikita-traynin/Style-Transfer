from flask import Flask
app = Flask(__name__)

print('hi')
import style_transfer.views
print('hola')
