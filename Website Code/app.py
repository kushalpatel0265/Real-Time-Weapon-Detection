from flask import Flask, render_template, Response, request, redirect, url_for, jsonify
from database import init_db, log_detection, get_recent_detections
import os
from datetime import datetime
import cv2
import numpy as np
from ultralytics import YOLO
import os
import json
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client

app = Flask(__name__)

# Global variables
settings = {
    'email': '',
    'phone': '',
    'active_camera': 0,
    'last_email_time': None,
    'last_sms_time': None
}

# Twilio configuration
TWILIO_ACCOUNT_SID = 'AC98962f21ff6f0b297485141c78320e93'
TWILIO_AUTH_TOKEN = '96823a9dfc5f00c024770970e104d7d3'
TWILIO_PHONE_NUMBER = '+919879580177'
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Email cooldown period in seconds (15 seconds)
EMAIL_COOLDOWN = 15

# Initialize YOLO model
import os

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'best.pt')
print(f"Loading model from: {MODEL_PATH}")

try:
    model = YOLO(MODEL_PATH)
    MODEL_LOADED = True
except Exception as e:
    print(f"Error loading model: {e}")
    MODEL_LOADED = False
    model = None

def can_send_alert(last_time):
    if last_time is None:
        return True
    
    current_time = datetime.now()
    time_diff = (current_time - last_time).total_seconds()
    return time_diff >= EMAIL_COOLDOWN

def send_sms(detection_type, confidence, detections_count):
    if not settings['phone']:
        print("No phone number configured. Please set up phone in settings.")
        return
    
    if not can_send_alert(settings['last_sms_time']):
        time_until_next = EMAIL_COOLDOWN
        if settings['last_sms_time']:
            time_until_next = EMAIL_COOLDOWN - (datetime.now() - settings['last_sms_time']).total_seconds()
        print(f"SMS cooldown active. Next SMS can be sent in {time_until_next:.0f} seconds")
        return
    
    try:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message_body = f"⚠️ Threat Detected!\n"
        message_body += f"Object: {detection_type}\n"
        message_body += f"Time: {current_time}\n"
        message_body += f"Confidence: {confidence:.2f}%"
        
        account_sid = TWILIO_ACCOUNT_SID
        auth_token = TWILIO_AUTH_TOKEN
        client = Client(account_sid, auth_token)
        
        message = client.messages.create(
            from_=TWILIO_PHONE_NUMBER,
            body=message_body,
            to=settings['phone']
        )
        
        settings['last_sms_time'] = datetime.now()
        print(f"SMS alert sent to {settings['phone']} (SID: {message.sid})")
        
    except Exception as e:
        print(f"Error sending SMS: {str(e)}")

def send_alert(detection_type, confidence, detections_count):
    # Send SMS alert
    send_sms(detection_type, confidence, detections_count)
    
    # Send email alert
    if not settings['email']:
        print("No email address configured. Please set up email in settings.")
        return
    
    if not can_send_alert(settings['last_email_time']):
        time_until_next = EMAIL_COOLDOWN
        if settings['last_email_time']:
            time_until_next = EMAIL_COOLDOWN - (datetime.now() - settings['last_email_time']).total_seconds()
        print(f"Email cooldown active. Next email can be sent in {time_until_next:.0f} seconds")
        return
    
    try:
        # Email configuration
        sender_email = "kbpatel0265@gmail.com"  # Your Gmail address
        app_password = "Kushal2018"  # Your Gmail App Password
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = settings['email']
        msg['Subject'] = f"ALERT: Weapon Detection"
        
        body = f"Alert Summary:\n\n"
        body += f"Weapon type: {detection_type}\n"
        body += f"Confidence: {confidence:.2f}%\n"
        body += f"Number of detections in last 2 minutes: {detections_count}\n"
        body += f"Camera: {settings['active_camera']}\n"
        body += f"Time: {datetime.now()}"
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.send_message(msg)
            
            settings['last_email_time'] = datetime.now()
            print(f"Email alert sent to {settings['email']}")
            
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        if 'server' in locals():
            try:
                server.quit()
            except:
                pass

def generate_frames():
    cap = cv2.VideoCapture(settings['active_camera'])
    
    while True:
        success, frame = cap.read()
        if not success:
            break
        
        if MODEL_LOADED and model is not None:
            try:
                try:
                    # Run YOLOv8 inference
                    results = model(frame)
                    
                    # Process detections
                    for result in results:
                        try:
                            boxes = result.boxes
                            for box in boxes:
                                try:
                                    # Get box coordinates
                                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                                    conf = float(box.conf[0])
                                    cls = int(box.cls[0])
                                    class_name = result.names[cls]
                                    
                                    print(f"Detection: {class_name} with confidence {conf:.2f}")
                                    
                                    # Draw bounding box
                                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                    cv2.putText(frame, f"{class_name}: {conf:.2f}", 
                                               (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                                    
                                    # Send alert and log detection if confidence is high enough
                                    if conf > 0.5:
                                        try:
                                            # Save detection to database
                                            detection_id = log_detection(
                                                weapon_type=class_name,
                                                confidence=conf * 100,
                                                camera_id=settings['active_camera']
                                            )
                                            print(f"Logged detection ID: {detection_id}")
                                            
                                            # Get count of detections in last 2 minutes
                                            recent_detections = len(get_recent_detections(
                                                weapon_type=class_name,
                                                minutes=2
                                            ))
                                            print(f"Recent detections count: {recent_detections}")
                                            
                                            # Send alert with detection count
                                            send_alert(class_name, conf * 100, recent_detections)
                                        except Exception as e:
                                            print(f"Error in alert/logging: {str(e)}")
                                except Exception as e:
                                    print(f"Error processing box: {str(e)}")
                        except Exception as e:
                            print(f"Error processing result: {str(e)}")
                except Exception as e:
                    print(f"Error in model inference: {str(e)}")
            except Exception as e:
                print(f"Error processing frame: {str(e)}")
        else:
            print("YOLOv8 model not loaded - place 'best.pt' in project directory")
        
        # Convert frame to jpg
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', settings=settings)

@app.route('/save_settings', methods=['POST'])
def save_settings():
    settings['email'] = request.form.get('email', '')
    settings['phone'] = request.form.get('phone', '')
    return redirect(url_for('dashboard'))

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/set_camera', methods=['POST'])
def set_camera():
    camera_id = request.form.get('camera_id', 0)
    settings['active_camera'] = int(camera_id)
    return jsonify({'status': 'success'})

@app.route('/detections')
def detections():
    recent_detections = get_recent_detections()
    return render_template('detections.html', detections=recent_detections)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
