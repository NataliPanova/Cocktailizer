from flask import Flask, render_template
import json

app = Flask(__name__)

with open('cocktailizer.json', encoding='utf-8') as f:
    cocktails = json.load(f)

@app.route('/')
def home():
    return render_template('cocktailizer.html')
@app.route('/alkoholiga')
def alkoholiga():
    filtered = [c for c in cocktails if c['type'] == 'alkoholiga']
    return render_template('alkoholiga.html', cocktails=filtered)

@app.route('/ilma-alkoholita')
def ilma_alkoholita():
    filtered = [c for c in cocktails if c['type'] == 'ilma-alkoholita']
    return render_template('ilma-alkoholita.html', cocktails=filtered)

@app.route('/recipe/<name>')
def recipe(name):
    for c in cocktails:
        if c['name'].lower() == name.lower():
            return render_template('recipe.html', cocktail=c)
    return "Retsept ei leitud", 404

if __name__ == '__main__':
    app.run()