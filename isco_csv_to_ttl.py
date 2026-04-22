#!/usr/bin/env python3

import csv
import sys
from pathlib import Path

TTL_PREFIXES = """\
@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix isco: <http://data.europa.eu/esco/isco/C> .

"""

SCHEME = """\
<http://data.europa.eu/esco/concept-scheme/isco>
    a skos:ConceptScheme ;
    rdfs:label "ISCO-88"^^xsd:string ;
    skos:notation "ISCO-88"^^xsd:string .

"""

def escape(t):
    return t.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')

def convert(input_path, output_path):
    blocks = []
    with open(input_path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            uri   = row.get("conceptUri", "").strip()
            label = row.get("preferredLabel", "").strip()
            code  = row.get("code", "").strip()
            if not uri or not label or not code:
                continue

            if not uri.startswith("http://data.europa.eu/esco/isco/C"):
                continue

            local = uri.replace("http://data.europa.eu/esco/isco/C", "")
            block = (
                f"isco:{local}\n"
                f"    a skos:Concept ;\n"
                f"    skos:inScheme <http://data.europa.eu/esco/concept-scheme/isco> ;\n"
                f'    skos:notation "{escape(code)}"^^xsd:string ;\n'
                f'    skos:prefLabel "{escape(label)}"@en .\n'
            )
            blocks.append(block)

    out = TTL_PREFIXES + SCHEME + "\n".join(blocks)
    Path(output_path).write_text(out, encoding="utf-8")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Verwendung: python isco_csv_to_ttl.py <ISCOGroups_en.csv> <output.ttl>")
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])
