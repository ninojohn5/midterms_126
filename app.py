from flask import Flask, render_template, Response, jsonify, request
import cv2

app = Flask(__name__)

# Load the face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Global variable to track blur state
blur_enabled = False  # Default is OFF

def generate_frames():
    global blur_enabled
    camera = cv2.VideoCapture(0)

    while True:
        success, frame = camera.read()
        if not success:
            break

        if blur_enabled:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            for (x, y, w, h) in faces:
                face = frame[y:y+h, x:x+w]
                face = cv2.GaussianBlur(face, (99, 99), 30)
                frame[y:y+h, x:x+w] = face

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/toggle_blur')
def toggle_blur():
    global blur_enabled
    status = request.args.get('status')

    if status == "on":
        blur_enabled = True  # Explicitly set ON
    elif status == "off":
        blur_enabled = False  # Explicitly set OFF

    return jsonify({'blur_enabled': blur_enabled})

# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
