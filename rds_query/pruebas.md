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
  FILTER(contains(?name, "python")) }
```

### Resumen de una imagen
``` sql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dct: <https://purl.org/dc/terms/>
prefix dpv: <http://dockerpedia.inf.utfsm.cl/vocab#>
prefix sd: <htttp://w3id.org/okn/o/sd#>
prefix c2t: <https://w3id.org/c2t#>
prefix c2ti: <https://w3id.org/c2t/i/>
SELECT ?image ?tag ?architecture ?size ?osDescription ?pacLicense ?pacLanguage ?pacName
WHERE { ?image a dpv:Image .
  ?os c2t:isOperativeSystemOf ?image .
  ?packages dpv:isInstalledOn ?image .
  OPTIONAL {?image dpv:tag ?tag } .
  OPTIONAL {?image c2t:architecture ?architecture } .
  OPTIONAL {?image dpv:size ?size } .
  OPTIONAL {?os sd:description ?osDescription } .
  OPTIONAL {?packages dct:license ?pacLicense } .
  OPTIONAL {?packages sd:programmingLanguage ?pacLanguage } .
  OPTIONAL {?packages sd:name ?pacName }
} 
```
