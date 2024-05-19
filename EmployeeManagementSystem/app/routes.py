from flask import render_template, request, redirect, url_for
import pandas as pd
from app import app, db
from app.models import Employee

@app.route('/')
def index():
    employees = Employee.query.all()
    return render_template('index.html', employees=employees)

def import_employees_from_excel(excel_path='./data/employees.xlsx'):
    df = pd.read_excel(excel_path, engine='openpyxl')
    for index, row in df.iterrows():
        employee = Employee.query.filter_by(email=row['Email']).first()
        if employee:
            employee.name = row['Name']
            employee.department = row['Department']
        else:
            new_employee = Employee(name=row['Name'], department=row['Department'], email=row['Email'])
            db.session.add(new_employee)
    db.session.commit()

@app.route('/import', methods=['GET'])
def import_data():
    import_employees_from_excel()
    return redirect(url_for('index'))
