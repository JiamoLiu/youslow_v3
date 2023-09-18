from flask import Flask, request, render_template_string

app = Flask(__name__)

# HTML template for the input form and greeting
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Greeting App</title>
</head>
<body>
    <h1>Greeting App</h1>
    <form method="POST">
        <label for="name">Enter your name:</label>
        <input type="text" id="name" name="name" required>
        <input type="submit" value="Submit">
    </form>
    <p>{{ greeting }}</p>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def greet():
    if request.method == 'POST':
        name = request.form.get('name')
        greeting = f"Hello {name}, welcome to the site"
        return render_template_string(html_template, greeting=greeting)
    else:
        return render_template_string(html_template, greeting='')

if __name__ == '__main__':
    app.run(host = "localhost", port=8000,debug=False)