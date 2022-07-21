from SPARQLWrapper import SPARQLWrapper, CSV
import io
import pandas as pd
import numpy as np

class db():
    def __init__(self,sparql) -> None:
        self.sparql = sparql

    def name_version_image_finder(self,version,package):
        if version is None:
            self.sparql.setQuery(""" 
            PREFIX sd: <https://w3id.org/okn/o/sd#>
            prefix c2t: <https://w3id.org/c2t#> 
            prefix c2ti: <https://w3id.org/c2t/i/> 
            prefix dc: <http://purl.org/dc/elements/1.1/> 
            prefix dpv: <http://dockerpedia.inf.utfsm.cl/vocab#> 
            prefix owl: <http://www.w3.org/2002/07/owl#> 
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
            prefix rr: <http://www.w3.org/ns/r2rml#> 
            prefix rml: <http://semweb.mmlab.be/ns/rml#> 
            prefix ql: <http://semweb.mmlab.be/ns/ql#> 
            prefix : <http://example.org/> 
            prefix dct: <https://purl.org/dc/terms/> 

            SELECT DISTINCT ?tag ?id
            WHERE {
                ?o a dpv:PackageVersion.
                ?o sd:name '"""+package+"""'.
                ?o dpv:isInstalledOn ?image.
                ?image dpv:tag ?tag.
                ?image dct:identifier ?id
            } 
            """)
        else:
            self.sparql.setQuery("""
            PREFIX sd: <https://w3id.org/okn/o/sd#>
            prefix c2t: <https://w3id.org/c2t#> 
            prefix c2ti: <https://w3id.org/c2t/i/> 
            prefix dc: <http://purl.org/dc/elements/1.1/> 
            prefix dpv: <http://dockerpedia.inf.utfsm.cl/vocab#> 
            prefix owl: <http://www.w3.org/2002/07/owl#> 
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
            prefix rr: <http://www.w3.org/ns/r2rml#> 
            prefix rml: <http://semweb.mmlab.be/ns/rml#> 
            prefix ql: <http://semweb.mmlab.be/ns/ql#> 
            prefix : <http://example.org/> 
            prefix dct: <https://purl.org/dc/terms/> 

            SELECT DISTINCT ?tag ?id
            WHERE {
                ?o a dpv:PackageVersion.
                ?o sd:name '"""+package+"""'.
                ?o sd:hasVersionId '"""+version+"""'.
                ?o dpv:isInstalledOn ?image.
                ?image dpv:tag ?tag.
                ?image dct:identifier ?id
            } 
            """)
        self.sparql.setReturnFormat(CSV)
        results_lib = self.sparql.query().convert()
        results_2lib = io.StringIO(results_lib.decode('utf-8'))
        lib_results = pd.read_csv(results_2lib)

        return lib_results
    

    def get_card_resume(self, image_name):
        self.sparql.setQuery("""
        PREFIX sd: <https://w3id.org/okn/o/sd#>
        prefix c2t: <https://w3id.org/c2t#> 
        prefix c2ti: <https://w3id.org/c2t/i/> 
        prefix dc: <http://purl.org/dc/elements/1.1/> 
        prefix dpv: <http://dockerpedia.inf.utfsm.cl/vocab#> 
        prefix owl: <http://www.w3.org/2002/07/owl#> 
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
        prefix rr: <http://www.w3.org/ns/r2rml#> 
        prefix rml: <http://semweb.mmlab.be/ns/rml#> 
        prefix ql: <http://semweb.mmlab.be/ns/ql#> 
        prefix dct: <https://purl.org/dc/terms/> 
        prefix : <http://example.org/> 

        SELECT DISTINCT ?tag ?architecture ?size ?osDescription ?created
        WHERE { ?image a dpv:Image.
        ?image dpv:tag '"""+image_name+"""'.
        ?image dpv:tag ?tag.
        ?os c2t:isOperativeSystemOf ?image .
        ?image c2t:architecture ?architecture .
        ?image dpv:size ?size .
        ?os sd:description ?osDescription .
        ?image c2t:created ?created.  
        } 
        """)
        self.sparql.setReturnFormat(CSV)
        results_card = self.sparql.query().convert()
        results_2card = io.StringIO(results_card.decode('utf-8'))
        card_results = pd.read_csv(results_2card)

        self.sparql.setQuery("""
        PREFIX sd: <https://w3id.org/okn/o/sd#>
        prefix c2t: <https://w3id.org/c2t#> 
        prefix c2ti: <https://w3id.org/c2t/i/> 
        prefix dc: <http://purl.org/dc/elements/1.1/> 
        prefix dpv: <http://dockerpedia.inf.utfsm.cl/vocab#> 
        prefix owl: <http://www.w3.org/2002/07/owl#> 
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        prefix rr: <http://www.w3.org/ns/r2rml#> 
        prefix rml: <http://semweb.mmlab.be/ns/rml#> 
        prefix ql: <http://semweb.mmlab.be/ns/ql#> 
        prefix dct: <https://purl.org/dc/terms/> 
        prefix : <http://example.org/> 

        SELECT DISTINCT ?packageT (COUNT(?package) as ?total)
        WHERE {
            ?image a dpv:Image.
            ?image dpv:tag '"""+image_name+"""'.
            ?package dpv:isInstalledOn ?image;
                    c2t:operativeSystemPackageVersion ?packageT .
        }GROUP BY (?packageT)
        """)
        self.sparql.setReturnFormat(CSV)
        results_card2 = self.sparql.query().convert()
        results_2card2 = io.StringIO(results_card2.decode('utf-8'))
        card_results2 = pd.read_csv(results_2card2)
        package_list = card_results2['packageT'].to_list()
        counter_list = card_results2['total'].to_list()
        card_results["packageT"] = np.nan
        card_results['packageT'] = card_results['packageT'].astype('object')
        card_results.at[0,'packageT'] = package_list
        card_results["total"] = np.nan
        card_results['total'] = card_results['total'].astype('object')
        card_results.at[0,'total'] = counter_list
        print(card_results)
        return card_results


    def get_comparison_meta(self, image1_name, image2_name):
        self.sparql.setQuery("""
        PREFIX sd: <https://w3id.org/okn/o/sd#>
        prefix c2t: <https://w3id.org/c2t#> 
        prefix c2ti: <https://w3id.org/c2t/i/> 
        prefix dc: <http://purl.org/dc/elements/1.1/> 
        prefix dpv: <http://dockerpedia.inf.utfsm.cl/vocab#> 
        prefix owl: <http://www.w3.org/2002/07/owl#> 
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
        prefix rr: <http://www.w3.org/ns/r2rml#> 
        prefix rml: <http://semweb.mmlab.be/ns/rml#> 
        prefix ql: <http://semweb.mmlab.be/ns/ql#> 
        prefix dct: <https://purl.org/dc/terms/> 
        prefix : <http://example.org/> 

        SELECT DISTINCT ?tag ?architecture ?size ?osDescription ?created
        WHERE { ?image a dpv:Image.
        ?image dpv:tag '"""+image1_name+"""'.
        ?image dpv:tag ?tag.
        ?os c2t:isOperativeSystemOf ?image .
        ?image c2t:architecture ?architecture .
        ?image dpv:size ?size .
        ?os sd:description ?osDescription .
        ?image c2t:created ?created.  
        } 
        """)
        self.sparql.setReturnFormat(CSV)
        results_card = self.sparql.query().convert()
        results_2card = io.StringIO(results_card.decode('utf-8'))
        card_results = pd.read_csv(results_2card)


        self.sparql.setQuery("""
        PREFIX sd: <https://w3id.org/okn/o/sd#>
        prefix c2t: <https://w3id.org/c2t#> 
        prefix c2ti: <https://w3id.org/c2t/i/> 
        prefix dc: <http://purl.org/dc/elements/1.1/> 
        prefix dpv: <http://dockerpedia.inf.utfsm.cl/vocab#> 
        prefix owl: <http://www.w3.org/2002/07/owl#> 
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
        prefix rr: <http://www.w3.org/ns/r2rml#> 
        prefix rml: <http://semweb.mmlab.be/ns/rml#> 
        prefix ql: <http://semweb.mmlab.be/ns/ql#> 
        prefix dct: <https://purl.org/dc/terms/> 
        prefix : <http://example.org/> 

        SELECT DISTINCT ?tag ?architecture ?size ?osDescription ?created
        WHERE { ?image a dpv:Image.
        ?image dpv:tag '"""+image2_name+"""'.
        ?image dpv:tag ?tag.
        ?os c2t:isOperativeSystemOf ?image .
        ?image c2t:architecture ?architecture .
        ?image dpv:size ?size .
        ?os sd:description ?osDescription .
        ?image c2t:created ?created.  
        } 
        """)
        self.sparql.setReturnFormat(CSV)
        results_card1 = self.sparql.query().convert()
        results_2card1 = io.StringIO(results_card1.decode('utf-8'))
        card_results1 = pd.read_csv(results_2card1)
        card_result_join = pd.concat([card_results, card_results1])
        return card_result_join


    def get_comparison_pack(self, image1_name, image2_name):
        self.sparql.setQuery("""
        PREFIX sd: <https://w3id.org/okn/o/sd#>
        prefix c2t: <https://w3id.org/c2t#> 
        prefix c2ti: <https://w3id.org/c2t/i/> 
        prefix dc: <http://purl.org/dc/elements/1.1/> 
        prefix dpv: <http://dockerpedia.inf.utfsm.cl/vocab#> 
        prefix owl: <http://www.w3.org/2002/07/owl#> 
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        prefix rr: <http://www.w3.org/ns/r2rml#> 
        prefix rml: <http://semweb.mmlab.be/ns/rml#> 
        prefix ql: <http://semweb.mmlab.be/ns/ql#> 
        prefix dct: <https://purl.org/dc/terms/> 
        prefix : <http://example.org/> 

        SELECT ?name
        WHERE {
            ?image a dpv:Image.
            ?image dpv:tag '"""+image1_name+"""'.
            ?package dpv:isInstalledOn ?image.
            ?package rdfs:label ?name
        }
        """)
        self.sparql.setReturnFormat(CSV)
        results_card = self.sparql.query().convert()
        results_2card = io.StringIO(results_card.decode('utf-8'))
        card_results = pd.read_csv(results_2card)
        package_list1 = card_results['name'].to_list()

        self.sparql.setQuery("""
        PREFIX sd: <https://w3id.org/okn/o/sd#>
        prefix c2t: <https://w3id.org/c2t#> 
        prefix c2ti: <https://w3id.org/c2t/i/> 
        prefix dc: <http://purl.org/dc/elements/1.1/> 
        prefix dpv: <http://dockerpedia.inf.utfsm.cl/vocab#> 
        prefix owl: <http://www.w3.org/2002/07/owl#> 
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        prefix rr: <http://www.w3.org/ns/r2rml#> 
        prefix rml: <http://semweb.mmlab.be/ns/rml#> 
        prefix ql: <http://semweb.mmlab.be/ns/ql#> 
        prefix dct: <https://purl.org/dc/terms/> 
        prefix : <http://example.org/> 

        SELECT ?name
        WHERE {
            ?image a dpv:Image.
            ?image dpv:tag '"""+image2_name+"""'.
            ?package dpv:isInstalledOn ?image.
            ?package rdfs:label ?name
        }
        """)
        self.sparql.setReturnFormat(CSV)
        results_card1 = self.sparql.query().convert()
        results_2card1 = io.StringIO(results_card1.decode('utf-8'))
        card_results1 = pd.read_csv(results_2card1)
        package_list2 = card_results1['name'].to_list()
        similarities = []
        for elem in package_list1:
            if elem in package_list2:
                similarities += [elem]
        diff1 = list(set(package_list1)-set(similarities))
        diff2 = list(set(package_list2)-set(similarities))
        same = pd.DataFrame({image1_name:similarities,image2_name:similarities})
        diff_1 = pd.DataFrame({image1_name: diff1})
        diff_2 = pd.DataFrame({image2_name: diff2})
        diff = pd.concat([diff_1,diff_2], axis=1)
        return diff, same