import os

from flask import Flask, render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE="mongodb://ben:testing@ec2-3-8-124-209.eu-west-2.compute.amazonaws.com:27017/test?authSource=train-database&readPreference=primary&appname=MongoDB%20Compass%20Community&ssl=false",
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
        print("Instance Folder Created")
    except OSError:
        pass

    from . import tube_lines
    app.register_blueprint(tube_lines.bp)
    # a simple page that says hello
    @app.route('/')
    def hello():
        return render_template("/main.html")

    return app