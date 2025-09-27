from flask import Flask, render_template, request
import json

app = Flask(__name__)

with open('cocktailizer.json', encoding='utf-8') as f:
    cocktails = json.load(f)

@app.route('/')
def home():
    return render_template('cocktailizer.html')


@app.route('/alkoholiga')
def alkoholiga():
    selected = request.args.getlist('ingredients')
    all_ingredients = set()

    for cocktail in cocktails:
        if cocktail['type'] == 'alkoholiga':
            for j in cocktail['ingredients']: # kuna koostisosad on lisatud sõnastikutele, siis tsükkel läbib kõik sõnastikud 
                all_ingredients.add(j['name'])

    if selected:
        filtered = [
            i for i in cocktails
            if i['type'] == 'alkoholiga' and
               any(j['name'] in selected for j in i['ingredients']) # vähemalt 1 koostisosa
        ]
    else:
        filtered = [i for i in cocktails if i['type'] == 'alkoholiga'] # kui ei ole midagi valitud

    return render_template(
        'alkoholiga.html',
        cocktails=filtered,
        ingredients=sorted(all_ingredients),
        selected=selected
    )



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

def get_all_ingredients():
    all_ingredients = set()
    for i in cocktails:
        all_ingredients.update(i['ingredients'])
    return sorted(all_ingredients)

if __name__ == '__main__':
    app.run()
