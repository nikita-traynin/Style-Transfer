from flask import Flask, render_template, request, redirect, flash
from werkzeug.utils import secure_filename
import os
from endpoints import home, file_upload
from flask_app_config import app
import config.default

app.config.from_object(config.default.default)




