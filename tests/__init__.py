import os
import shutil
import six
import functools

import pytest
from flask_sqlalchemy import model

from .run import app, db


class BaseTest(object):
    root_path = os.path.split(os.path.abspath(__name__))[0]

    @classmethod
    def setup_class(cls):
        with app.app_context():
            db.create_all()

    @classmethod
    def teardown_class(cls):
        with app.app_context():
            db.drop_all()

    def teardown_method(self, method):
        with app.app_context():
            for m in [m for m in db.Model._decl_class_registry.values()
                      if isinstance(m, model.DefaultMeta)]:
                db.session.query(m).delete()
                db.session.commit()


def rmdir(path):
    if os.path.exists(path):
        shutil.rmtree(path)


def chdir(path):
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            cwd = os.getcwd()
            if not os.path.exists(path):
                os.makedirs(path)
            os.chdir(path)
            func(*args, **kwargs)
            os.chdir(cwd)
        return inner
    return wrapper


python2_only = pytest.mark.skipif(not six.PY2, reason='only support Python2')
python3_only = pytest.mark.skipif(not six.PY3, reason='only support Python3')
