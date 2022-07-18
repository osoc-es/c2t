# Caso de uso 1: encontrar liberías problemáticas


```python
from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://localhost:3030/grafo")

package = input('Package you want to find')
sparql.setQuery("""
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
PREFIX dct: <https://purl.org/dc/terms/>
prefix dpv: <http://dockerpedia.inf.utfsm.cl/vocab#>
prefix sd: <htttp://w3id.org/okn/o/sd#>
prefix c2t: <https://w3id.org/c2t#>
prefix c2ti: <https://w3id.org/c2t/i/>
SELECT ?tag
WHERE {
?o a dpv:PackageVersion.
?o sd:name '"""+package+"""'.
?o dpv:isInstalledOn ?image.
?image dpv:tag ?tag
} 
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
print(results)
```

    ¿Qué librería desea encontrar? wheel
    ¿Desea seleccionar una versión? (s/n)s
    ¿Qué versión desdea encontrar? 0.37.1
    {'head': {'vars': ['package', 'version']}, 'results': {'bindings': [{'package': {'type': 'uri', 'value': 'https://w3id.org/c2t/i/PackageVersion/pkg%3Apypi%2Fwheel%400.37.1'}}]}}


# Caso de uso 2: Encontrar todas las imágenes


```python
from SPARQLWrapper import SPARQLWrapper, CSV

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
print(results)

```

# Caso de uso 3: 