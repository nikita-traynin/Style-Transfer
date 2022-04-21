from flask import Flask
from werkzeug.serving import run_simple
import web  # this runs init in web
import MLModel  # this runs init in MLModel
import sys

# when you run this module, you must input a single command line argument
# which is the name of the app you want to run.
# it must be either "web" or "MLModel", which is self-explanatory
if len(sys.argv) > 2:
    print('You have too many CLI arguments.')
elif len(sys.argv) < 2:
    print('You did not input a CLI argument.')
else:
    appname = sys.argv[1]
    if __name__ == '__main__':
        if appname == "web":
            run_simple('localhost', 5000, web.app,
                       use_reloader=True, use_debugger=True, use_evalex=True)
        elif appname == "MLModel":
            run_simple('localhost', 5001, MLModel.app,
                       use_reloader=True, use_debugger=True, use_evalex=True)
