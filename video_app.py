from flask import Flask, render_template, Response, request, redirect, url_for
import cv2
from threading import Thread
import datetime

from videodiagnosis import diagnose_video

app = Flask(__name__, template_folder='./templates')

camera = cv2.VideoCapture(0)

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

global rec, out, video_saved
rec = False
out = None
video_saved = False

def record(out):
    global rec
    while rec:
        success, frame = camera.read()
        if success:
            out.write(frame)

def gen_frames():
    global out, rec
    while True:
        success, frame = camera.read()
        if success:
            if rec:
                frame = cv2.putText(frame, "Recording in progress...", (int((frame.shape[1] - cv2.getTextSize("Recording in progress...", cv2.FONT_HERSHEY_SIMPLEX, 1, 4)[0][0]) / 2), frame.shape[0] - 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 123, 0), 4)
            try:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                print("Error encoding frame:", e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_test')
def video_test():
    global video_saved
    video_saved = False
    return render_template('video_test.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/tasks', methods=['POST'])
def tasks():
    global rec, out, video_saved
    if request.method == 'POST':
        if request.form.get('rec') == 'Start Recording':
            rec = True
            now = datetime.datetime.now()
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter('static/vid_latest.mp4', fourcc, 30.0, (width, height))
            thread = Thread(target=record, args=[out, ])
            thread.start()
        elif request.form.get('rec') == 'Stop Recording':
            rec = False
            if out is not None:
                out.release()
            video_saved = True
            return redirect(url_for('processing'))
    return redirect(url_for('video_test'))

@app.route('/processing')
def processing():
    global video_saved
    if video_saved:
        return render_template('processing.html')
    else:
        return redirect(url_for('video_test'))

@app.route('/diagnose', methods=['POST'])
def diagnose():
    if request.method == 'POST':
        video_path = 'static/vid_latest.mp4'
        video_diagnosis_result = diagnose_video(video_path)
        return render_template('diagnose.html', result=video_diagnosis_result)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

camera.release()
cv2.destroyAllWindows()
