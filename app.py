from flask import Flask, render_template, request, redirect, url_for, flash, Markup
import re

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Patterns for XSS and SQL injection
XSS_PATTERN = re.compile(r'(<.*?>)|(["\'])|((alert|confirm|prompt)\s*\()|((?:script|on\w+)\s*=)', re.IGNORECASE)
SQLI_PATTERN = re.compile(r'(?:--|\b(OR|AND)\b\s+\d+=\d+|;|\'|")', re.IGNORECASE)

# Input validation function
def validate_input(input_text):
    if XSS_PATTERN.search(input_text):
        return False
    if SQLI_PATTERN.search(input_text):
        return False
    return True

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        search_term = request.form['search_term']
        if validate_input(search_term):
            sanitized_search_term = Markup.escape(search_term)
            return redirect(url_for('result', search_term=sanitized_search_term))
        else:
            flash("Please try again.")
            return redirect(url_for('home'))

    return render_template('home.html')

@app.route('/result')
def result():
    search_term = request.args.get('search_term')
    return render_template('result.html', search_term=search_term)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
