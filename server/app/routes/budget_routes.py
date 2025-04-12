from flask import Blueprint
from database import Session
from models.budget import Budget

budget = Blueprint('budget', __name__)