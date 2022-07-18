import shutil
import unittest
import os
import json
from pathlib import Path

import morph_kgc

from src import syft_parser

test_data_path = str(Path(__file__).parent / "data") #+ os.path.sep


class TestCLI(unittest.TestCase):
    # def test_rdf_has_license(self):
    #     self.assertEqual(True, True)  # add assertion here

    def test_mapping(self):
        # create tmp folder
        os.makedirs("tmp", exist_ok=True)
        # save jsons in tmp file
        shutil.copy(os.path.join(test_data_path, 'inspect.json'), os.path.join("tmp", 'inspect1.json'))
        shutil.copy(os.path.join(test_data_path, 'syft.json'), os.path.join("tmp", 'syft.json'))
        shutil.copy(os.path.join('../../config.ini'), os.path.join("tmp", 'config.ini'))
        shutil.copy('../../mappings/mapping2.ttl', os.path.join("tmp", 'mapping.ttl'))
        f = open(os.path.join("tmp", 'syft.json'))
        syft = f.read()
        syft_parser.parse_data(syft, os.path.join("tmp", 'result1.json'), os.path.join("tmp", 'inspect1.json'))
        # call morph
        g = morph_kgc.materialize('./tmp/config.ini')
        g.serialize(destination=os.path.join("tmp", "graph.nt"), format="ntriples")
        # perform queries
        # query for packages with license (there is one)
        query = """
        PREFIX dct: <https://purl.org/dc/terms/>
        SELECT DISTINCT ?license 
        WHERE {
            ?p dct:license ?license.
        }
        """
        qres = g.query(query)
        self.assertEqual(len(qres), 1)

        # Query for packages in Java installed on an image (there is one result)
        # The image tag is python:3.9
        query = """
                PREFIX dct: <https://purl.org/dc/terms/>
                PREFIX dpv: <http://dockerpedia.inf.utfsm.cl/vocab#>
                PREFIX sd: <https://w3id.org/okn/o/sd#>
                SELECT DISTINCT ?package 
                WHERE {
                    ?p a dpv:PackageVersion;
                       dpv:isInstalledOn ?img;
                       sd:programmingLanguage "java" .
                    ?img dpv:tag "python:3.9".
                }
                """
        qres = g.query(query)
        self.assertEqual(len(qres), 1)

        #Query for testing OS
        query = """
        PREFIX dct: <https://purl.org/dc/terms/> 
        PREFIX c2t: <https://w3id.org/c2t#>
        PREFIX dpv: <http://dockerpedia.inf.utfsm.cl/vocab#>
        PREFIX sd: <https://w3id.org/okn/o/sd#>
        SELECT DISTINCT ?os 
        WHERE {
            ?os sd:name ?nom ;
                a dpv:OperatingSystem;
                sd:hasVersionId ?ver;
                c2t:distributionOf ?os2;
                c2t:isOperativeSystemOf ?image;
                sd:description ?desc;
                sd:issueTracker ?tracker;
                sd:website ?website.
            ?image c2t:architecture ?arch.
        }
        """
        #
        qres = g.query(query)
        self.assertEqual(len(qres), 1)

        # delete tmp folder
        shutil.rmtree("tmp")


if __name__ == '__main__':
    unittest.main()
    
