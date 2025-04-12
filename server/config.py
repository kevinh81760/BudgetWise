class Config:
    SECRET_KEY = 'your_secret_key'  # For Flask sessions (important for login systems)

    # Optional: if you want to keep database URL here too
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:12345@localhost/budget_app'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # To suppress warnings
