from flask import Flask, request, jsonify
import uuid
from datetime import datetime, timedelta
import random
import re

app = Flask(__name__)

@app.route('/availability', methods=['GET'])
def get_availability():
    appointments = []
    for _ in range(6):
        random_days = random.randint(0, 14)
        random_seconds = random.randint(0, 86400)  # Seconds in a day
        starts_at = (datetime.now() + timedelta(days=random_days, seconds=random_seconds)).isoformat()
        
        appointment = {
            "id": str(uuid.uuid4()),  # Using UUID v4 as v7 is not standard in Python's uuid module
            "starts_at": starts_at
        }
        appointments.append(appointment)
    
    return jsonify({ "appointments": appointments })

@app.route('/reserve', methods=['POST'])
def reserve():
    if request.args.get('conflict', '').lower() == 'true':
        return jsonify({"error": "Conflict occurred"}), 409
    
    data = request.json
    required_fields = ['name', 'email', 'phone', 'appointment_id']
    
    for field in required_fields:
        value = data.get(field, '').strip()
        if len(value) < 1:
            return jsonify({"error": f"Invalid {field}"}), 400
    
    # Email validation
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, data['email']):
        return jsonify({"error": "Invalid email format"}), 400
    
    # UUID validation
    try:
        uuid.UUID(data['appointment_id'])
    except ValueError:
        return jsonify({"error": "Invalid appointment_id format"}), 400
    
    # Successful reservation
    return jsonify({"appointment_id": data['appointment_id']})

if __name__ == '__main__':
    app.run(debug=True)