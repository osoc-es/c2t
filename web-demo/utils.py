from dbm.ndbm import library
from ensurepip import version
from SPARQLWrapper import SPARQLWrapper, JSON, CSV
import io
import pandas as pd
sparql = SPARQLWrapper("http://localhost:3030/graph%22)

def name_version_image_finder(version,package):
    if version == '':
    sparql.setQuery("""
    PREFIX sd: https://w3id.org/okn/o/sd#
    prefix c2t: https://w3id.org/c2t# 
    prefix c2ti: https://w3id.org/c2t/i/ 
    prefix dc: http://purl.org/dc/elements/1.1/ 
    prefix dpv: http://dockerpedia.inf.utfsm.cl/vocab# 
    prefix owl: http://www.w3.org/2002/07/owl# 
    prefix rdfs: http://www.w3.org/2000/01/rdf-schema# 
    prefix rr: http://www.w3.org/ns/r2rml# 
    prefix rml: http://semweb.mmlab.be/ns/rml# 
    prefix ql: http://semweb.mmlab.be/ns/ql# 
    prefix : http://example.org/ 


    SELECT ?tag
    WHERE {
        ?o a dpv:PackageVersion.
        ?o sd:name '"""+package+"""'.
        ?o dpv:isInstalledOn ?image.
        ?image dpv:tag ?tag
    } 
    """)
    else:
    sparql.setQuery("""
    PREFIX sd: https://w3id.org/okn/o/sd#
    prefix c2t: https://w3id.org/c2t# 
    prefix c2ti: https://w3id.org/c2t/i/ 
    prefix dc: http://purl.org/dc/elements/1.1/ 
    prefix dpv: http://dockerpedia.inf.utfsm.cl/vocab# 
    prefix owl: http://www.w3.org/2002/07/owl# 
    prefix rdfs: http://www.w3.org/2000/01/rdf-schema# 
    prefix rr: http://www.w3.org/ns/r2rml# 
    prefix rml: http://semweb.mmlab.be/ns/rml# 
    prefix ql: http://semweb.mmlab.be/ns/ql# 
    prefix : http://example.org/ 


    SELECT ?tag
    WHERE {
        ?o a dpv:PackageVersion.
        ?o sd:name '"""+package+"""'.
        ?o sd:hasVersionId '"""+version+"""'.
        ?o dpv:isInstalledOn ?image.
        ?image dpv:tag ?tag
    } 
    """)
    sparql.setReturnFormat(CSV)
    results_lib = sparql.query().convert()
    results_2lib = io.StringIO(results_lib.decode('utf-8'))
    lib_results = pd.read_csv(results_2lib)

    return lib_results