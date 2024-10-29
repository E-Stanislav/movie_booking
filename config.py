class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///movies.db'
    JWT_SECRET_KEY = 'jwt_secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
