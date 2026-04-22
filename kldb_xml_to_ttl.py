#!/usr/bin/env python3

import re
from pathlib import Path
from lxml import etree

TTL_PREFIXES = """\
@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix glmo: <http://w3id.org/glmo#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix kldb: <http://w3id.org/kldb/> .

"""

FILES = [
    ("KLDB1988-1988-09-01-Classification__complete_.xml", "kldb1988.ttl"),
    ("KLDB1992-1992-01-01-Classification__complete_.xml", "kldb1992.ttl"),
]

GLMO_MAP = {
    "1970": "glmo:KldB1970",
    "1975": "glmo:KldB1975",
    "1988": "glmo:KldB1988",
    "1992": "glmo:KldB1992",
}

LEVEL_NAMES = {
    1: "Berufsbereich",
    2: "Berufsabschnitt",
    3: "Berufsgruppe",
    4: "Berufsordnung",
    5: "Berufsklasse",
}


def safe(t):
    return re.sub(r"[^A-Za-z0-9_\-]", "_", t.strip())


def lit(t, l="de"):
    return f'"{t.replace(chr(92),"\\\\").replace(chr(34),chr(92)+chr(34)).replace(chr(10),"\\n")}"@{l}'


def get_labels(el):
    out = {}
    for lt in el.findall("Label/LabelText"):
        lg = lt.get("language", "").lower()
        tx = (lt.text or "").strip()
        if lg and tx:
            out[lg] = tx
    return out


def infer_parent(code, level, last):
    if level == 5 and len(code) >= 3:
        return code[:3]
    if level == 4 and len(code) >= 2:
        return code[:2]
    if level == 3:
        return last.get(2)
    if level == 2:
        return last.get(1)
    return None


class KldbConverter:
    def __init__(self, path):
        self.path = Path(path)
        root = etree.parse(str(path)).getroot()
        self.root = root
        clf = root.find(".//Classification")
        self.scheme_id = clf.get("id", self.path.stem) if clf is not None else self.path.stem
        m = re.search(r"(\d{4})", self.scheme_id)
        self.year = m.group(1) if m else "0000"
        self.glmo = GLMO_MAP.get(self.year, "glmo:Occupation")
        self.blocks = []

    def su(self):
        return f"kldb:{self.scheme_id}"

    def cu(self, c):
        return f"kldb:{self.scheme_id}_{safe(c)}"

    def emit_scheme(self):
        clf = self.root.find(".//Classification")
        labels = get_labels(clf) if clf is not None else {}
        lns = [
            f"{self.su()}",
            f"    a skos:ConceptScheme, {self.glmo} ;",
            f'    rdfs:label "KldB {self.year}"^^xsd:string ;',
        ]
        for lg, tx in labels.items():
            lns.append(f"    skos:prefLabel {lit(tx, lg)} ;")
        lns.append(f'    skos:notation "{self.year}"^^xsd:string ;')
        lns.append(".\n")
        self.blocks.append("\n".join(lns))

    def emit_item(self, code, level, labels, parent):
        lns = [
            f"{self.cu(code)}",
            f"    a skos:Concept, {self.glmo} ;",
            f"    skos:inScheme {self.su()} ;",
            f'    skos:notation "{code}"^^xsd:string ;',
            f'    skos:scopeNote "{LEVEL_NAMES.get(level, str(level))}"@de ;',
        ]
        for lg, tx in labels.items():
            lns.append(f"    skos:prefLabel {lit(tx, lg)} ;")
        if parent:
            lns.append(f"    skos:broader {self.cu(parent)} ;")
        else:
            lns.append(f"    skos:topConceptOf {self.su()} ;")
        lns.append(".\n")
        self.blocks.append("\n".join(lns))

    def convert(self):
        self.emit_scheme()
        last = {}
        for item in self.root.findall(".//Item"):
            code = item.get("id", "").strip()
            ls = item.get("idLevel", "0").strip()
            if not code or not ls.isdigit():
                continue
            level = int(ls)
            labels = get_labels(item)
            parent = infer_parent(code, level, last)
            self.emit_item(code, level, labels, parent)
            last[level] = code
        return TTL_PREFIXES + "\n".join(self.blocks)


def main():
    for xml_file, ttl_file in FILES:
        c = KldbConverter(xml_file)
        ttl = c.convert()
        Path(ttl_file).write_text(ttl, encoding="utf-8")
        n = sum(1 for b in c.blocks if "skos:Concept" in b)


if __name__ == "__main__":
    main()
