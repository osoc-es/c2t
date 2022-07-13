### Images that have a package:

``` sql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix dpv: <http://dockerpedia.inf.utfsm.cl/vocab#>
prefix sd: <htttp://w3id.org/okn/o/sd#>
prefix c2t: <https://w3id.org/c2t#>
prefix c2ti: <https://w3id.org/c2t/i/>
SELECT ?image ?name
WHERE {
  ?package dpv:isInstalledOn ?image;
      sd:name "apt". 
  ?image dpv:tag ?name
  FILTER(contains(?name, "python"))
```
### Image name
``` sql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix dpv: <http://dockerpedia.inf.utfsm.cl/vocab#>
prefix sd: <htttp://w3id.org/okn/o/sd#>
prefix c2t: <https://w3id.org/c2t#>
prefix c2ti: <https://w3id.org/c2t/i/>
SELECT ?image ?name
WHERE {
  ?package dpv:isInstalledOn ?image;
      sd:name "apt". 
  ?image dpv:tag ?name
  FILTER(contains(?name, "python"))
```