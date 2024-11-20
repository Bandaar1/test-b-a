from flask import Flask, request, render_template
import os
from analyze import analyze_file

# تحديد المسار الصحيح للقوالب
app = Flask(__name__, template_folder='templates')

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'لا يوجد ملف', 400
    file = request.files['file']
    if file.filename == '':
        return 'لم يتم اختيار ملف', 400
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        result = analyze_file(filepath)
        return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
