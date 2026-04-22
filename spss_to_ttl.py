#!/usr/bin/env python3

import re
import sys
from pathlib import Path

TTL_PREFIXES = """\
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix kldb: <http://w3id.org/kldb/> .
@prefix isco: <http://data.europa.eu/esco/isco/C> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .

"""

def convert(input_path, output_path):
    text = Path(input_path).read_bytes().decode("latin-1")

    pairs = re.findall(r'\((\d{4})=(\d+)\)', text)

    lines = []
    for kldb, isco in pairs:
        lines.append(f"kldb:kldb1992_{kldb} skos:exactMatch isco:{isco} .")

    output = TTL_PREFIXES + "\n".join(lines) + "\n"
    Path(output_path).write_text(output, encoding="utf-8")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Verwendung: python spss_to_ttl.py <input_spss.txt> <output.ttl>")
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])
