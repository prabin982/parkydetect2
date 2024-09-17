from flask import Flask, render_template, flash, redirect, url_for, request
from audiodiagnosis import diagnose_audio
import crepe

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your own secret key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    if request.form.get('name'):
        flash('Form submitted successfully!', 'success')
        # Example usage of crepe
        result = crepe.predict('audio.wav')
        diagnosis = diagnose_audio(result)
        flash(diagnosis, 'info')
    else:
        flash('An error occurred. Please try again.', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
