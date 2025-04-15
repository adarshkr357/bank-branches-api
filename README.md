# Bank Branches API

A simple API server for querying bank branches data using both REST API and GraphQL approaches.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://dashboard.heroku.com/new?template=https%3A%2F%2Fgithub.com%2Fadarshkr357%2Fbank-branches-api)
## Features

- REST API endpoints for querying bank and branch information
- GraphQL API at `/gql` for more flexible querying
- Ready for Heroku deployment

## Setup and Installation

1. Clone the repository
2. Create a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the application:
   ```
   python app.py
   ```
5. Access the API at http://localhost:5000

## API Endpoints

### REST API

- `GET /api/banks` - Get all banks
- `GET /api/banks/{bank_id}` - Get a specific bank by ID
- `GET /api/branches` - Get all branches
- `GET /api/branches/{ifsc}` - Get a specific branch by IFSC code
- `GET /api/bank/{bank_id}/branches` - Get all branches for a specific bank

### GraphQL API

- `/gql` - GraphQL endpoint with GraphiQL interface

Example query:
```graphql
query {
  branches {
    edges {
      node {
        branch
        bank {
          name
        }
        ifsc
      }
    }
  }
}
```

## Database

The application uses SQLite for simplicity but can be easily configured to use other databases like PostgreSQL for production deployment.

## Deployment to Heroku

### Option 1: One-Click Deployment
Click the "Deploy to Heroku" button at the top of this README to deploy the application with a single click.

### Option 2: Manual Deployment
1. Create a Heroku account if you don't have one
2. Install the Heroku CLI
3. Login to Heroku:
   ```
   heroku login
   ```
4. Create a new Heroku app:
   ```
   heroku create your-app-name
   ```
5. Push to Heroku:
   ```
   git push heroku main
   ```

## Time Taken

Approximately 4 hours to complete this assignment.

## Code Structure

- `app.py` - Main application file with both REST and GraphQL implementations
- `models.py` - Database models
- `database.py` - Database connection and initialization
- `data/bank_branches.csv` - Sample data
- `requirements.txt` - Dependencies
- `Procfile` - Heroku deployment configuration