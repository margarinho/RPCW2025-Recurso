from rdflib import Graph, Namespace, RDF
from rdflib.namespace import OWL, RDFS

# Caminho para o ficheiro OWL
ontologia_ficheiro = "cocktails_ind.ttl"

# Carregar a ontologia
g = Graph()
g.parse(ontologia_ficheiro, format="ttl")  # ou "turtle" se for TTL

# Definir o namespace
namespace = "http://www.di.uminho.pt/rpcw2025/PG55921/"
ns = Namespace(namespace)
g.bind("", ns)

before = len(g)

g.add((ns.workedAt, RDF.type, OWL.ObjectProperty))
g.add((ns.workedAt, RDFS.domain, ns.Bartender))
g.add((ns.workedAt, RDFS.range, ns.Bar))

# Propriedade hasIngredient: Cocktail tem Ingrediente
g.add((ns.hasIngredient, RDF.type, OWL.ObjectProperty))
g.add((ns.hasIngredient, RDFS.domain, ns.Cocktail))
g.add((ns.hasIngredient, RDFS.range, ns.Ingredient))

inferencias = [
    """
    INSERT {
      ?bartender :workedAt ?bar .
    }
    WHERE {
      ?bartender :createCocktail ?cocktail .
      ?bar :isAssociatedToCocktail ?cocktail .
    }
    """,
    
    """
    INSERT {
      ?cocktail :hasIngredient ?ingredient .
    }
    WHERE {
      ?cocktail a :Cocktail ;
            :hasQuantity ?quantity .
      ?quantity :useIngredient ?ingredient .
    }
    """
]

for query in inferencias:
    g.update(f"PREFIX : <http://www.di.uminho.pt/rpcw2025/PG55921/>\n{query}")

after = len(g)
added = after - before

g.serialize(destination="cocktails_ind_inserts.ttl", format="turtle")
print("Inferências aplicadas e guardadas em 'cocktails_ind_inserts.ttl'")
print(f"{after} triplos foram acrescentados ao grafo.")