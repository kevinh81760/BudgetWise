from flask import Blueprint, request, jsonify
from datetime import datetime
from server.models.budget import Budget
from server.database import Session

# Blueprint for handling budget-related routes
budget = Blueprint('budget', __name__)

# Add a new budget goal
@budget.route('/budget', methods=['POST'])
def add_budget():
    """
    Adds a new budget goal for a user.

    Request JSON:
        {
            "user_id": <int>,
            "category": <string>,
            "limit_amount": <float>,
            "start_date": "YYYY-MM-DD",
            "end_date": "YYYY-MM-DD"
        }

    Returns:
        JSON response with success message or error with HTTP status code.
    """
    data = request.get_json()
    user_id = data.get('user_id')
    category = data.get('category')
    limit_amount = data.get('limit_amount')
    start_date_str = data.get('start_date')
    end_date_str = data.get('end_date')

    # Ensure all required fields are present
    if not all([user_id, category, limit_amount, start_date_str, end_date_str]):
        return jsonify({"error": "Missing fields"}), 400

    # Validate and convert date strings to datetime objects
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    session = Session()
    
    # Create new budget entry
    new_budget = Budget(
        user_id=user_id,
        category=category,
        limit_amount=limit_amount,
        start_date=start_date,
        end_date=end_date
    )

    session.add(new_budget)
    session.commit()
    session.close()

    return jsonify({"message": "Budget goal added successfully!"}), 201

@budget.route('/budgets/<int:user_id>', methods=['GET'])
def get_budgets(user_id):
    """
    Retrieves all budget goals for a given user.

    Parameters:
        user_id (int): ID of the user whose budgets are to be retrieved.

    Returns:
        JSON list of all budgets for the user.
    """
    session = Session()
    budgets = session.query(Budget).filter_by(user_id=user_id).all()
    
    # Format result for JSON serialization
    result = [{
        "id": b.id,
        "category": b.category,
        "limit_amount": b.limit_amount,
        "start_date": b.start_date.strftime('%Y-%m-%d'),
        "end_date": b.end_date.strftime('%Y-%m-%d')
    } for b in budgets]
    session.close()
    return jsonify(result)

@budget.route('/budget/<int:budget_id>', methods=['DELETE'])
def delete_budget(budget_id):
    """
    Deletes a specific budget goal by its ID.

    Parameters:
        budget_id (int): ID of the budget to delete.

    Returns:
        JSON response with confirmation or error message.
    """
    session = Session()
    budget_entry = session.query(Budget).get(budget_id)

    if not budget_entry:
        session.close()
        return jsonify({"error": "Budget not found"}), 404

    # Delete the budget entry
    session.delete(budget_entry)
    session.commit()
    session.close()

    return jsonify({"message": "Budget deleted successfully."}), 200
