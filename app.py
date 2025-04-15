import os

from flask import Flask, jsonify, request
from flask_graphql import GraphQLView
import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from database import db, init_db
from models import Bank, Branch

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank_branches.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Initialize database directly with app context
with app.app_context():
    init_db()

# ==================================================================
# REST API Endpoints
# ==================================================================

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to Bank Branches API",
        "endpoints": {
            "REST": ["/api/banks", "/api/banks/<bank_id>", "/api/branches", "/api/branches/<ifsc>", "/api/bank/<bank_id>/branches"],
            "GraphQL": "/gql"
        }
    })

@app.route('/api/banks')
def get_banks():
    """Get list of all banks"""
    banks = Bank.query.all()
    result = []
    for bank in banks:
        result.append({
            "id": bank.id,
            "name": bank.name
        })
    return jsonify(result)

@app.route('/api/banks/<int:bank_id>')
def get_bank(bank_id):
    """Get a specific bank by ID"""
    bank = Bank.query.get(bank_id)
    if not bank:
        return jsonify({"error": "Bank not found"}), 404
    
    return jsonify({
        "id": bank.id,
        "name": bank.name
    })

@app.route('/api/branches')
def get_branches():
    """Get list of all branches"""
    branches = Branch.query.all()
    result = []
    for branch in branches:
        result.append({
            "ifsc": branch.ifsc,
            "branch": branch.branch,
            "address": branch.address,
            "city": branch.city,
            "district": branch.district,
            "state": branch.state,
            "bank_id": branch.bank_id,
            "bank": {
                "id": branch.bank.id,
                "name": branch.bank.name
            }
        })
    return jsonify(result)

@app.route('/api/branches/<string:ifsc>')
def get_branch_by_ifsc(ifsc):
    """Get branch details by IFSC code"""
    branch = Branch.query.filter_by(ifsc=ifsc).first()
    if not branch:
        return jsonify({"error": "Branch not found"}), 404
    
    return jsonify({
        "ifsc": branch.ifsc,
        "branch": branch.branch,
        "address": branch.address,
        "city": branch.city,
        "district": branch.district,
        "state": branch.state,
        "bank_id": branch.bank_id,
        "bank": {
            "id": branch.bank.id,
            "name": branch.bank.name
        }
    })

@app.route('/api/bank/<int:bank_id>/branches')
def get_bank_branches(bank_id):
    """Get all branches for a specific bank"""
    branches = Branch.query.filter_by(bank_id=bank_id).all()
    result = []
    for branch in branches:
        result.append({
            "ifsc": branch.ifsc,
            "branch": branch.branch,
            "address": branch.address,
            "city": branch.city,
            "district": branch.district,
            "state": branch.state,
            "bank_id": branch.bank_id
        })
    return jsonify(result)

# ==================================================================
# GraphQL Implementation
# ==================================================================

# Define GraphQL Types
class BankType(SQLAlchemyObjectType):
    class Meta:
        model = Bank
        interfaces = (relay.Node, )

class BranchType(SQLAlchemyObjectType):
    class Meta:
        model = Branch
        interfaces = (relay.Node, )

# Define GraphQL Query
class Query(graphene.ObjectType):
    node = relay.Node.Field()
    
    # Allow querying all branches with pagination
    branches = SQLAlchemyConnectionField(BranchType.connection)
    
    # Allow querying all banks
    banks = SQLAlchemyConnectionField(BankType.connection)
    
    # Query a single bank by ID
    bank = graphene.Field(BankType, id=graphene.Int())
    
    # Query a single branch by IFSC
    branch = graphene.Field(BranchType, ifsc=graphene.String())
    
    def resolve_bank(self, info, id):
        return Bank.query.get(id)
    
    def resolve_branch(self, info, ifsc):
        return Branch.query.filter_by(ifsc=ifsc).first()

# Create GraphQL Schema
schema = graphene.Schema(query=Query)

# Add GraphQL view to Flask app
app.add_url_rule(
    '/gql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # Enable GraphiQL interface
    )
)

# =================================================================
# Main entry point
# =================================================================

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)