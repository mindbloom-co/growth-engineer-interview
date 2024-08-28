from flask import Flask, request, jsonify
import uuid
from datetime import datetime, timedelta
import random
import re
import pytz

app = Flask(__name__)

@app.route('/availability', methods=['GET'])
def get_availability():
    appointments = []
    pacific_tz = pytz.timezone('US/Pacific')
    now = datetime.now(pacific_tz)
    
    for _ in range(16):
        random_days = random.randint(0, 14)
        random_minutes = random.randint(0, 660)  # 11 hours in minutes (8AM - 7PM)
        
        appointment_date = now.date() + timedelta(days=random_days)
        appointment_time = datetime.combine(appointment_date, datetime.min.time())
        appointment_time = pacific_tz.localize(appointment_time)
        
        starts_at = appointment_time.replace(hour=8) + timedelta(minutes=random_minutes)
        
        appointment = {
            "id": str(uuid.uuid4()),
            "starts_at": starts_at.isoformat()
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