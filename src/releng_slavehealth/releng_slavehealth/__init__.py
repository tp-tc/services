# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import

import os

import flask

import backend_common
import backend_common.db

import releng_slavehealth.api


DEBUG = bool(os.environ.get('DEBUG', __name__ == '__main__'))
HERE = os.path.dirname(os.path.abspath(__file__))
APP_SETTINGS = os.path.abspath(os.path.join(HERE, '..', 'settings.py'))


def favicon():
    return flask.send_from_directory(
        os.path.dirname(__file__),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon',
    )


def init_app(app):
    app.api.register(
        os.path.join(os.path.dirname(__file__), 'api.yml'))

    for proxy in ["buildapi", "slavealloc", "slaveapi"]:
        app.add_url_rule(
            '/' + proxy,
            proxy + '_proxy',
            getattr(releng_slavehealth.api, proxy + "_proxy"),
        )
        app.add_url_rule(
            '/' + proxy + '/<path:path>',
            proxy + '_proxy',
            getattr(releng_slavehealth.api, proxy + "_proxy"),
        )

    app.add_url_rule('/favicon.ico', 'favicon', favicon)

    return None


if DEBUG and not os.environ.get('DATABASE_URL'):
    os.environ['DATABASE_URL'] = 'sqlite:///%s' % (
        os.path.abspath(os.path.join(HERE, '..', 'app.db')))

if not os.environ.get('APP_SETTINGS') and \
       os.path.isfile(APP_SETTINGS):
    os.environ['APP_SETTINGS'] = APP_SETTINGS


app = backend_common.create_app(
    "releng_slavehealth",
    extensions=[init_app, backend_common.db],
    debug=DEBUG,
    debug_src=HERE,
)


if __name__ == "__main__":
    app.run(**app.run_options())