from flask import Flask
from server.database import engine
from server.database import Base
from server.app.routes.auth_routes import auth
from server.app.routes.transaction_routes import transaction
from server.app.routes.budget_routes import budget

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Register routes
app.register_blueprint(auth)
app.register_blueprint(transaction)
app.register_blueprint(budget)

# Create DB tables
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    app.run(debug=True)
