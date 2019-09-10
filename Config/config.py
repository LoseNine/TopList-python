import os

class Config:
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'this is important secret_key'
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True
    SQLALCHEMY_DATABASE_URI='mysql://root:root@localhost/toplist'
