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
    categories = {
        'alkohol': set(),
        'vili': set(),
        'muu jook': set(),
        'lisand': set()
    }

    for i in cocktails:
        if i['type'] == 'alkoholiga':
            for j in i['ingredients']: # kuna koostisosad on lisatud sõnastikutele, siis tsükkel läbib kõik sõnastikud
                cat = j.get('category', 'lisand') #  saame koostisosa kategooriat, kui seda pole olemas, siis eeldame, et see on lisand
                categories.setdefault(cat, set()).add(j['name']) # lisame koostisosa kategooriasse

    if selected:
        filtered = [
            i for i in cocktails
            if i['type'] == 'alkoholiga' and
               any(j['name'] in selected for j in i['ingredients']) # filtreerimine vähemalt 1 koostisosa järgi
        ]
    else:
        filtered = [i for i in cocktails if i['type'] == 'alkoholiga'] # kui midagi ei ole valitud, siis näidakse kõik kokteilid

    return render_template(
        'alkoholiga.html',
        cocktails=filtered,
        ingredients={k: sorted(v) for k, v in categories.items()},
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
