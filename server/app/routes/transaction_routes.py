from flask import Blueprint, request, jsonify
from server.database import Session
from server.models.transaction import UserTransaction
from datetime import datetime

# Blueprint for handling transaction-related routes
transaction = Blueprint('transaction', __name__)

@transaction.route('/transactions', methods=['POST'])
def add_transaction():
    """
    Adds a new transaction (income or expense) to the database.

    Request JSON:
        {
            "user_id": <int>,
            "category": <string>,
            "amount": <float>,
            "type": <"income" or "expense">,
            "date_created": "YYYY-MM-DD"
        }

    Returns:
        JSON response with a success message or error with HTTP status code.
    """
    data = request.get_json()
    session_db = Session()

    # Validate and convert the provided date string
    try:
        date_obj = datetime.strptime(data['date_created'], "%Y-%m-%d")
    except (KeyError, ValueError):
        return jsonify({"error": "Invalid or missing date format. Use YYYY-MM-DD."}), 400

    
    # Create a new UserTransaction object
    new_transaction = UserTransaction(
        user_id=data['user_id'],
        category=data['category'],
        amount=data['amount'],
        type=data['type'],
        date_created=date_obj
    )
    session_db.add(new_transaction) # Add to DB
    session_db.commit()
    session_db.close()

    return jsonify({"message": "Transaction added!"}), 201

@transaction.route('/transactions/<int:user_id>', methods=['GET'])
def get_transactions(user_id):
    """
    Retrieves all transactions for a specific user.

    Parameters:
        user_id (int): ID of the user whose transactions are to be fetched.

    Returns:
        JSON list of transaction objects.
    """
    session_db = Session()
    transactions = session_db.query(UserTransaction).filter_by(user_id=user_id).all()
    
    # Serialize results into a JSON-compatible format
    result = [
        {
            "id": t.id,
            "user_id": t.user_id,
            "category": t.category,
            "amount": t.amount,
            "type": t.type,
            "date_created": t.date_created.strftime('%Y-%m-%d')
        }
        for t in transactions
    ]
    session_db.close()
    return jsonify(result)

@transaction.route('/transaction/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    """
    Deletes a specific transaction based on its ID.

    Parameters:
        transaction_id (int): ID of the transaction to delete.

    Returns:
        JSON response confirming deletion or error if not found.
    """
    session_db = Session()
    transaction = session_db.query(UserTransaction).get(transaction_id)

    if not transaction:
        session_db.close()
        return jsonify({"error": "Transaction not found"}), 404

    session_db.delete(transaction) # Remove from DB
    session_db.commit()
    session_db.close()

    return jsonify({"message": "Transaction deleted successfully."}), 200
