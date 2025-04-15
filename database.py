import os
import pandas as pd
import sqlite3
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db():
    from models import Bank, Branch
    
    # Create tables using SQL from indian_banks.sql
    create_tables_from_sql()
    
    # Check if data already exists
    if Branch.query.count() == 0:
        try:
            # Load CSV data
            csv_path = os.path.join('data', 'bank_branches.csv')
            if os.path.exists(csv_path):
                df = pd.read_csv(csv_path)
                
                # Process data and insert into database
                banks = {}
                
                for _, row in df.iterrows():
                    bank_name = row['bank_name']
                    bank_id = row['bank_id']
                    
                    # Create bank if it doesn't exist
                    if bank_id not in banks:
                        # Check if bank already exists in db
                        bank = Bank.query.filter_by(id=bank_id).first()
                        if not bank:
                            bank = Bank(id=bank_id, name=bank_name)
                            db.session.add(bank)
                            db.session.commit()
                        banks[bank_id] = bank.id
                    
                    # Check if branch already exists
                    branch = Branch.query.filter_by(ifsc=row['ifsc']).first()
                    if not branch:
                        # Create branch
                        branch = Branch(
                            ifsc=row['ifsc'],
                            branch=row['branch'],
                            address=row['address'],
                            city=row['city'],
                            district=row['district'],
                            state=row['state'],
                            bank_id=bank_id
                        )
                        db.session.add(branch)
                
                db.session.commit()
                print("Database initialized with CSV data")
            else:
                print(f"Warning: CSV file not found at {csv_path}")
                # Create sample data
                create_sample_data()
        except Exception as e:
            print(f"Error initializing database: {e}")
            db.session.rollback()

def create_tables_from_sql():
    # Read SQL file
    sql_path = 'indian_banks.sql'
    if not os.path.exists(sql_path):
        print(f"Warning: SQL file not found at {sql_path}")
        return
    
    # Extract create table statements from SQL file
    with open(sql_path, 'r', encoding='utf-8') as file:
        sql_content = file.read()
    
    # Read SQL file and extract CREATE TABLE statements
    create_tables_sql = []
    lines = sql_content.split('\n')
    current_statement = []
    in_create_table = False
    
    for line in lines:
        line = line.strip()
        if line.startswith('CREATE TABLE'):
            in_create_table = True
            current_statement = [line]
        elif in_create_table:
            current_statement.append(line)
            if line.endswith(');'):
                create_tables_sql.append('\n'.join(current_statement))
                in_create_table = False
    
    # Convert PostgreSQL syntax to SQLite
    for create_statement in create_tables_sql:
        # Replace PostgreSQL-specific types with SQLite types
        # character varying -> TEXT, bigint -> INTEGER
        statement = create_statement.replace('character varying', 'TEXT')
        statement = statement.replace('bigint', 'INTEGER')
        
        # Execute the CREATE TABLE statement directly using SQLite
        try:
            # Get the SQLite connection from Flask-SQLAlchemy
            engine = db.get_engine()
            conn = engine.raw_connection()
            cursor = conn.cursor()
            cursor.execute(statement)
            conn.commit()
            print(f"Created table from SQL statement")
        except Exception as e:
            print(f"Error creating table: {e}")

def create_sample_data():
    from models import Bank, Branch
    
    # Create sample banks
    sbi = Bank(id=1, name="STATE BANK OF INDIA")
    hdfc = Bank(id=5, name="HDFC BANK")
    icici = Bank(id=60, name="ABHYUDAYA COOPERATIVE BANK LIMITED")
    
    db.session.add_all([sbi, hdfc, icici])
    db.session.commit()
    
    # Create sample branches
    branches = [
        Branch(ifsc="SBIN0001234", branch="Main Branch", address="123 SBI Road", city="Mumbai", 
               district="Mumbai", state="Maharashtra", bank_id=sbi.id),
        Branch(ifsc="HDFC0001234", branch="Central Branch", address="789 HDFC Road", city="Bangalore", 
               district="Bangalore", state="Karnataka", bank_id=hdfc.id),
        Branch(ifsc="ABHY0065001", branch="RTGS-HO", address="ABHYUDAYA BANK BLDG., B.NO.71, NEHRU NAGAR, KURLA (E), MUMBAI-400024", 
               city="MUMBAI", district="GREATER MUMBAI", state="MAHARASHTRA", bank_id=icici.id),
    ]
    
    db.session.add_all(branches)
    db.session.commit()
    print("Sample data created successfully")