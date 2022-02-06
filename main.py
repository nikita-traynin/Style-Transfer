from flask import Flask
from werkzeug.serving import run_simple
import web # this runs init in web
import MLModel # this runs init in MLModel
import sys


appname = sys.argv[1]
if __name__ == '__main__':
    if appname == "web":
        run_simple('localhost', 5000, web.app,
               use_reloader=True, use_debugger=True, use_evalex=True)
    elif appname == "MLModel":
        run_simple('localhost', 5001, MLModel.app,
               use_reloader=True, use_debugger=True, use_evalex=True)
