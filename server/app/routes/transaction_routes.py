from flask import Blueprint, request, jsonify
from server.database import Session
from server.models.transaction import UserTransaction
from datetime import datetime

transaction = Blueprint('transaction', __name__)

@transaction.route('/transactions', methods=['POST'])
def add_transaction():
    data = request.get_json()
    session_db = Session()

    try:
        date_obj = datetime.strptime(data['date_created'], "%Y-%m-%d")
    except (KeyError, ValueError):
        return jsonify({"error": "Invalid or missing date format. Use YYYY-MM-DD."}), 400

    new_transaction = UserTransaction(
        user_id=data['user_id'],
        category=data['category'],
        amount=data['amount'],
        type=data['type'],
        date_created=date_obj
    )
    session_db.add(new_transaction)
    session_db.commit()
    session_db.close()

    return jsonify({"message": "Transaction added!"}), 201

@transaction.route('/transactions/<int:user_id>', methods=['GET'])
def get_transactions(user_id):
    session_db = Session()
    transactions = session_db.query(UserTransaction).filter_by(user_id=user_id).all()
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
    session_db = Session()
    transaction = session_db.query(UserTransaction).get(transaction_id)

    if not transaction:
        session_db.close()
        return jsonify({"error": "Transaction not found"}), 404

    session_db.delete(transaction)
    session_db.commit()
    session_db.close()

    return jsonify({"message": "Transaction deleted successfully."}), 200
