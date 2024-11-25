from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Конфігурація бази даних
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///health.db'  # Замініть на вашу конфігурацію, якщо використовуєте PostgreSQL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель даних
class HealthData2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    pressure = db.Column(db.String(50))  # низький, нормальний, високий
    temperature = db.Column(db.String(50))  # низька, нормальна, висока
    pulse = db.Column(db.String(50))  # низький, нормальний, високий
    risk_level = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Ініціалізація бази даних
with app.app_context():
    db.create_all()

# Логіка оцінки рівня ризику
def calculate_risk(pressure, temp, pulse):
    """
    Оцінює рівень ризику на основі тиску, температури та пульсу.
    """
    if pressure == "високий" or temp == "висока" or pulse == "високий":
        return "високий"
    elif pressure == "нормальний" and temp == "нормальна" and pulse == "нормальний":
        return "низький"
    else:
        return "середній"

# Головна сторінка
@app.route('/')
def index():
    return render_template('index.html')

# Обробка діагностики
@app.route('/diagnose', methods=['POST'])
def diagnose():
    try:
        data = request.get_json()
        name = data.get('name')
        age = int(data.get('age'))
        pressure = data.get('pressure')
        temp = data.get('temp')
        pulse = data.get('pulse')

        # Оцінка рівня ризику
        risk_level = calculate_risk(pressure, temp, pulse)

        # Збереження в базу даних
        health_record = HealthData2(
            name=name,
            age=age,
            pressure=pressure,
            temperature=temp,
            pulse=pulse,
            risk_level=risk_level
        )
        db.session.add(health_record)
        db.session.commit()

        return jsonify({"risk_level": risk_level}), 200
    except Exception as e:
        print("Error processing request:", e)
        return jsonify({"error": "Something went wrong on the server"}), 500

# Маршрут для отримання історії
@app.route('/history', methods=['GET'])
def history():
    records = HealthData2.query.order_by(HealthData2.created_at.desc()).all()
    return jsonify([
        {
            "id": record.id,
            "name": record.name,
            "age": record.age,
            "pressure": record.pressure,
            "temperature": record.temperature,
            "pulse": record.pulse,
            "risk_level": record.risk_level,
            "created_at": record.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        for record in records
    ])

# Маршрут для видалення запису
@app.route('/delete-history/<int:record_id>', methods=['DELETE'])
def delete_history(record_id):
    try:
        record = HealthData2.query.get(record_id)
        if not record:
            return jsonify({"error": "Record not found"}), 404

        db.session.delete(record)
        db.session.commit()
        return jsonify({"message": "Record deleted successfully"}), 200
    except Exception as e:
        print(f"Error deleting record: {e}")
        return jsonify({"error": "Failed to delete record"}), 500

if __name__ == '__main__':
    app.run(debug=True)
