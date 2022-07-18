from unittest import result
from SPARQLWrapper import SPARQLWrapper, CSV
import pandas as pd
import io

sparql = SPARQLWrapper("http://localhost:3030/grafo")

sparql.setQuery("""
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dpv: <http://dockerpedia.inf.utfsm.cl/vocab#>
SELECT ?name
WHERE {
?image a dpv:Image.
?image rdfs:label ?name
} 
""")
sparql.setReturnFormat(CSV)

results = sparql.query().convert()
results_2 = io.StringIO(results.decode('utf-8'))
df_results = pd.read_csv(results_2)
print(df_results)