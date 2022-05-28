from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/form', methods=['POST'])
def form():
    data = request.form.get('Latom').strip().lower()

    f = open('/var/www/html/site/test_file', 'a')
    print(request.full_path, file=f)
    f.close()

    if data == 'latom':
        return render_template('form_success.html')
    else:
        return render_template('form_failure.html')
