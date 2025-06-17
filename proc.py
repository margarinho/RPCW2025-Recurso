import json

cocktails_json = "data/cocktails.json"
bartenders_json = "data/bartenders.json"
companies_json = "data/companies.json"
quantities_json = "data/quantities.json"
ingredients_json = "data/ingredients.json"

#Base
with open('cocktails_base.ttl', 'r', encoding='utf-8') as file:
    base = file.read()

#cocktails
with open(cocktails_json, 'r', encoding='utf-8') as jsonfile:
    cocktails = json.load(jsonfile)


#bartenders
with open(bartenders_json, 'r', encoding='utf-8') as jsonfile:
    bartenders = json.load(jsonfile)

#companies
with open(companies_json, 'r', encoding='utf-8') as jsonfile:
    companies = json.load(jsonfile)

#quantities
with open(quantities_json, 'r', encoding='utf-8') as jsonfile:
    quantities = json.load(jsonfile)



#Ingedients
with open(ingredients_json, 'r', encoding='utf-8') as jsonfile:
    ingredients = json.load(jsonfile)


## Aplicação / Periodo / cocktails -----
set_cocktails = set()
set_bartenders = set()
set_companies = set()
set_quantities = set()
set_ingredients = set()

dic_id_bartenders = {}
dic_id_companies = {}
dic_id_ingredients = {}
dic_id_cocktails = {}


for item in cocktails:
    nome = item.get('drinkName','')
    set_cocktails.add(nome)
    dic_id_cocktails[item.get('id','')] = nome
    
for item in bartenders:
    nome = item.get('strBartender','')
    set_bartenders.add(nome)
    dic_id_bartenders[item.get('id','')] = nome

for item in companies:
    nome = item.get('strBar','')
    set_companies.add(nome)
    dic_id_companies[item.get('id','')] = nome

for item in quantities:
    nome = item.get('id','')
    set_quantities.add(nome)
    

for item in ingredients:
    nome = item.get('strIngredient','')
    set_ingredients.add(nome)
    dic_id_ingredients[item.get('id','')] = nome
    

dic_cocktails = {c: f'Cocktail_{i}' for i, c in enumerate(set_cocktails)}
dic_bartenders = {d: f'Bartender_{i}' for i, d in enumerate(set_bartenders)}
dic_companies = {m: f'Bar_{i}' for i, m in enumerate(set_companies)}
dic_quantities = {m: f'Quantity_{i}' for i, m in enumerate(set_quantities)}
dic_ingredients = {m: f'Ingredient_{i}' for i, m in enumerate(set_ingredients)}

#String Bar
string_bar = []

for b in companies:
    nome = b.get('strBar', '')
    if not nome:
        continue  

    nome_uri = dic_companies.get(nome)
    if not nome_uri:
        continue 
    associated = b.get("isAssociatedToCocktail", [])
    if associated is None:
        associated = []
    elif not isinstance(associated, list):
        associated = [associated]

    cock_uris = [f":{dic_cocktails[dic_id_cocktails[c]]}" for c in associated if c in dic_id_cocktails]
    s = f":{nome_uri} rdf:type owl:NamedIndividual , :Bar "

    if cock_uris:
        s += f" ;\n\t:isAssociatedToCocktail {', '.join(cock_uris)}"
    s += f" ;\n\t:strBar \"{nome}\" ."

    string_bar.append(s)
    
#String Bartenders
string_bartenders = []
for b in bartenders:
    nome = b.get('strBartender', '')
    nome_uri = dic_bartenders[nome]
    cock_uris = [
    f":{dic_cocktails[dic_id_cocktails[c]]}"
    for c in (b.get("createCocktail", [])
              if isinstance(b.get("createCocktail", []), list)
              else [b.get("createCocktail")])
    if c in dic_id_cocktails
]

    s = f""":{nome_uri} rdf:type owl:NamedIndividual , :Bartender ;"""
    
    if cock_uris:
        s += f"""\n\t:createCocktail {', '.join(cock_uris)} ;"""
    s += f"""\n\t:strBartender "{nome}" ."""
    
    string_bartenders.append(s)
    
#String ingredients
string_ingredients = []
for i in ingredients:
    nome = i.get('strIngredient', '')
    nome_uri = dic_ingredients[nome]
    cock_uris = [
    f":{dic_cocktails[dic_id_cocktails[c]]}"
    for c in (b.get("asGarnishCocktail", [])
              if isinstance(b.get("asGarnishCocktail", []), list)
              else [b.get("asGarnishCocktail")])
    if c in dic_id_cocktails
]
    s = f""":{nome_uri} rdf:type owl:NamedIndividual , :Ingredient ;"""
    
    if cock_uris:
        s += f"""\n\t:asGarnishCocktail {', '.join(cock_uris)} ;"""
    s += f"""\n\t:strIngredient "{nome}" ."""
    
    string_ingredients.append(s)

## Strings cocktails
string_cocktails = []

for c in cocktails:
    nome = c.get('drinkName')
    nome_uri = dic_cocktails.get(nome)
    
    bartender_uri = dic_bartenders.get(dic_id_bartenders.get(c.get('createdByBartender')))

    garnish_data = c.get('garnishWithIngredient')
    ingredient_uris = [
    f":{dic_ingredients[dic_id_ingredients[ing_id]]}"
    for ing_id in ([garnish_data] if isinstance(garnish_data, str) else garnish_data or [])
    if ing_id in dic_id_ingredients and dic_id_ingredients[ing_id] in dic_ingredients
]

    quan_uris = [
        f":{dic_quantities[a]}"
        for a in c.get('needQuantity', [])
        if a in dic_quantities
    ]

    preparationEN = c.get('preparationEN', '').replace('"', '')

    
    s = f""":{nome_uri} rdf:type owl:NamedIndividual ,
                :Cocktail ;"""
                
    if bartender_uri:
        s += f"\n\t:createdByBartender :{bartender_uri} ;"

    if ingredient_uris:
        s += f"\n\t:garnishWithIngredient {', '.join(ingredient_uris)} ;"

    if quan_uris:
        s += f"\n\t:hasQuantity {', '.join(quan_uris)} ;"
        
    s += f"""\n\t:drinkName "{nome}" ; :idDrink "{c.get('id')}" ; :preparationEN  "{preparationEN}" ."""
    string_cocktails.append(s)

##String Quantities
string_quantities = []
for q in quantities:
    nome = q.get('id', '')
    nome_uri = dic_quantities[nome]
    ingredient_uri = dic_ingredients[dic_id_ingredients[q.get('useIngredient', '')]]
    quantity = q.get('quantity', '')
    
    cock_uris = [
    f":{dic_cocktails[dic_id_cocktails[c]]}"
    for c in (b.get("isUsedCocktail", [])
              if isinstance(b.get("isUsedCocktail", []), list)
              else [b.get("isUsedCocktail")])
    if c in dic_id_cocktails
    ]
    
    s = f""":{nome_uri} rdf:type owl:NamedIndividual , :Quantity ;"""
    
    if cock_uris:
        s += f"""\n\t:isUsedCocktail {', '.join(cock_uris)} ;"""
    
    if ingredient_uri:
        s += f"""\n\t:useIngredient :{ingredient_uri} ;"""
        
    s += f"""\n\t:quantity "{quantity}" ;
           :quantityName "{nome}" ."""
    
    string_quantities.append(s)
    
conteudo_final = (
    string_bar +
    string_bartenders +
    string_cocktails +
    string_ingredients +
    string_quantities
)

output_filename = 'cocktails_ind.ttl'

with open(output_filename, 'w', encoding='utf-8') as f:
    f.write(base)
    f.write('\n\n'.join(conteudo_final))