"""Hello World app with the Gunicorn WSGI server integrated!"""
import multiprocessing
import gunicorn
from flask import Flask
from gunicorn.app.base import Application, Config  # pylint: disable=unused-import
from gunicorn.workers import sync  # pylint: disable=unused-import
from gunicorn import glogging  # pylint: disable=unused-import
# ignoring pylint 'unused-import' errors because without them
# pyinstaller will not install required dependencies


flask_app = Flask(__name__)


@flask_app.route("/", methods=['POST', 'GET'])
def result():
    """Displaying "Hello world" message"""
    return "Hello World 1.3 green"


def number_of_workers():
    """Specifying amount of workers"""
    return (multiprocessing.cpu_count() * 2) + 1


class StandaloneApplication(gunicorn.app.base.BaseApplication):  # pylint: disable=W0223
    """Gunicorn part"""

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == '__main__':
    flask_options = {
        'bind': '%s:%s' % ('0.0.0.0', '8080'),  # pylint: disable=C0209
        'workers': number_of_workers(),         # Gunicorn example
    }
    StandaloneApplication(flask_app, flask_options).run()
