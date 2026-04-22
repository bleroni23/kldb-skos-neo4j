# kldb-skos-neo4j

Maschinenlesbare SKOS/RDF-Darstellung der Klassifikation der Berufe (KldB) 1988 und 1992 mit Mappings zu ISCO-88, zum Import in Neo4j. Modelliert mit SKOS und GLMO. Projekt für das Computational Social Science Projektpraktikum an der Universität Koblenz.

## Projektüberblick

Im Rahmen dieses Projekts wurden die Klassifikation der Berufe (KldB) der Jahrgänge 1988 und 1992 in eine maschinenlesbare, semantisch modellierte Form überführt. Grundlage waren die vom Klassifikationsserver der Bundesagentur für Arbeit bereitgestellten XML-Dateien, die mithilfe eigener Python-Skripte in das Turtle-Format (TTL) umgewandelt wurden. Die Modellierung folgt dem W3C-Standard SKOS (Simple Knowledge Organization System) und der German Labour Market Ontology (GLMO).

Zusätzlich wurde eine kompakte Version der internationalen Klassifikation ISCO-88 aus dem ESCO-Datensatz der Europäischen Kommission erzeugt sowie ein Mapping zwischen der KldB 1992 und ISCO-88 auf Basis des Umsteigeschlüssels des Bundesinstituts für Berufsbildung (BIBB). So werden die deutschen Klassifikationen international anschlussfähig.

Die erzeugten TTL-Dateien können direkt in die Graph-Datenbank Neo4j importiert und dort über Cypher-Abfragen analysiert und visualisiert werden.

## Inhalt des Repositories

**Erzeugte TTL-Dateien (bereit zum Import in Neo4j):**

- `kldb1988.ttl` – SKOS/GLMO-Darstellung der KldB 1988
- `kldb1992.ttl` – SKOS/GLMO-Darstellung der KldB 1992
- `isco88_compact.ttl` – kompakte Darstellung der ISCO-88 (aus ESCO abgeleitet)
- `mapping_kldb92_to_isco88.ttl` – Mapping zwischen KldB 1992 und ISCO-88

**Python-Skripte zur Erzeugung der TTL-Dateien:**

- `kldb_xml_to_ttl.py` – wandelt die KldB-XML-Dateien in TTL um
- `isco_csv_to_ttl.py` – wandelt die ESCO-CSV-Datei in TTL um
- `spss_to_ttl.py` – erzeugt das Mapping aus dem BIBB-Umsteigeschlüssel

Die Skripte dokumentieren das Vorgehen und können bei Bedarf auf die Originalquellen (siehe unten) angewendet werden, um die TTL-Dateien erneut zu erzeugen.

## Datenquellen

Die folgenden Originalquellen wurden für dieses Projekt verwendet. Sie sind aus lizenzrechtlichen Gründen **nicht** Teil dieses Repositories.

### 1. KldB 1988 (XML)

- **Quelle:** Bundesagentur für Arbeit – Klassifikationsserver
- **Link:** <https://www.klassifikationsserver.de/klassService/thyme/variant/kldb1988>
- **Hinweis:** Am unteren Ende der Seite die **XML (Claset)**-Version herunterladen.

### 2. KldB 1992 (XML)

- **Quelle:** Bundesagentur für Arbeit – Klassifikationsserver
- **Link:** <https://www.klassifikationsserver.de/klassService/thyme/variant/kldb1992>
- **Hinweis:** Am unteren Ende der Seite die **XML (Claset)**-Version herunterladen.

### 3. Umsteigeschlüssel KldB 1992 → ISCO-88

- **Quelle:** Bundesinstitut für Berufsbildung (BIBB) – FDZ-Metadatenportal
- **Link:** <https://metadaten.bibb.de/de/classification/detail/2>
- **Hinweis:** Die Datei `Umsteiger_kldb92_in_isco88_spss.txt` befindet sich auf der Seite im Abschnitt **Dokumente**.

### 4. ISCO-/ESCO-Klassifikation (CSV)

- **Quelle:** Europäische Kommission – ESCO-Portal
- **Link:** <https://esco.ec.europa.eu/en/use-esco/download>
- **Hinweis:** Im Bereich *Your ESCO dataset* folgende Einstellungen auswählen:
  - **Version:** `ESCO dataset – v1.2.1`
  - **Content:** `Classification`
  - **File type:** `csv`
  - **Language:** `en`

  Anschließend auf *Add to your package* klicken und das Paket herunterladen. Aus dem Archiv die Datei `ISCOGroups_en.csv` extrahieren.

## Import in Neo4j

Die TTL-Dateien dieses Repositories können direkt in Neo4j importiert werden. Voraussetzungen:

- **Neo4j Community Edition** (getestet mit Version 4.4.46)
- **neosemantics (n10s)** – offizielles Neo4j-Plugin für den Umgang mit RDF-Daten

### Schritt 1: TTL-Dateien in den Neo4j-Import-Ordner kopieren

Alle vier TTL-Dateien in den `import/`-Ordner der Neo4j-Installation kopieren. Bei einer typischen Installation liegt dieser Ordner z. B. unter:

- **macOS/Linux:** `~/apps/neo4j/neo4j-community-4.4.46/import/`
- **Windows:** `C:\Users\<Name>\Neo4j\neo4j-community-4.4.46\import\`

### Schritt 2: Neo4j starten und anmelden

Neo4j starten und im Browser unter <http://localhost:7474> öffnen. Anmelden mit den eigenen Zugangsdaten.

### Schritt 3: Datenbank vorbereiten

In der Cypher-Shell (Query-Leiste oben) folgende Befehle nacheinander ausführen.

Datenbank leeren (falls bereits Daten vorhanden sind):

```cypher
MATCH (n) DETACH DELETE n;
```

neosemantics initialisieren, damit RDF-URIs auf kurze Namen gemappt werden:

```cypher
CALL n10s.graphconfig.init({handleVocabUris: "MAP"});
```

### Schritt 4: TTL-Dateien importieren

Die Pfade in den folgenden Befehlen entsprechend der eigenen Installation anpassen.

```cypher
CALL n10s.rdf.import.fetch("file:///PFAD/ZU/import/kldb1988.ttl", "Turtle");
CALL n10s.rdf.import.fetch("file:///PFAD/ZU/import/kldb1992.ttl", "Turtle");
CALL n10s.rdf.import.fetch("file:///PFAD/ZU/import/isco88_compact.ttl", "Turtle");
CALL n10s.rdf.import.fetch("file:///PFAD/ZU/import/mapping_kldb92_to_isco88.ttl", "Turtle");
```

### Schritt 5: Beispielabfragen

Nach erfolgreichem Import können die Daten mit Cypher abgefragt werden. Beispielsweise lassen sich alle Berufsordnungen der KldB 1992 im Bereich *Rechnungskaufleute, Informatiker/Informatikerinnen* anzeigen:

```cypher
MATCH (n:KldB1992)
WHERE n.notation IN [
  '77',
  '771', '772', '773', '774', '775', '776',
  '7741', '7742', '7743', '7744', '7745', '7749',
  '7750', '7751', '7752', '7753',
  '7761', '7762', '7763', '7764'
]
RETURN n
```

## Lizenz

Die Python-Skripte in diesem Repository stehen unter der MIT-Lizenz (siehe `LICENSE`). Die erzeugten TTL-Dateien werden unter der Creative Commons Attribution 4.0 International Lizenz (CC-BY-4.0) bereitgestellt. Die ursprünglichen Quelldaten (siehe Abschnitt *Datenquellen*) unterliegen den Nutzungsbedingungen der jeweiligen Anbieter.

## Zitation

## Zitation

Januzi, B., & Wilinski, A. (2026). *kldb-skos-neo4j* [Software und Daten]. GitHub. https://github.com/bleroni23/kldb-skos-neo4j

Die Modellierung baut maßgeblich auf folgenden Arbeiten auf:

- **GLMO (German Labour Market Ontology):**  
  Dörpinghaus, J., Binnewitt, J., Winnige, S., Hein, K., & Krüger, K. (2023). Towards a German labor market ontology: Challenges and applications. *Applied Ontology, 18*(4), 343–365. <https://doi.org/10.3233/AO-230027>  
  Ontologie-Website: <https://tm4vetr.github.io/glmo/>

- **SKOS (Simple Knowledge Organization System):**  
  Miles, A., & Bechhofer, S. (2009). *SKOS Simple Knowledge Organization System Reference* (W3C Recommendation). World Wide Web Consortium. <https://www.w3.org/TR/skos-reference/>

## Autoren

- **Bleron Januzi** – bjanuzi@uni-koblenz.de
- **Alan Wilinski** – awilinski@uni-koblenz.de

Betreut durch Dr. Jens Dörpinghaus, Universität Koblenz / BIBB.
