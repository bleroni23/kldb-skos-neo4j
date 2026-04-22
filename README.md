# kldb-skos-neo4j
SKOS/RDF-Repräsentation der Klassifikation der Berufe (KldB) 1988/1992 mit Mapping zu ISCO-88, importierbar in Neo4j. CSS-Projektpraktikum (Computational Social Science), Universität Koblenz.


## Datenquellen

Um dieses Projekt zu reproduzieren, müssen die folgenden Quelldateien manuell heruntergeladen und in das Projektverzeichnis gelegt werden. Sie sind aus lizenzrechtlichen Gründen nicht Teil dieses Repositories.

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
- **Hinweis:** Die Datei `Umsteiger_kldb92_in_isco88_stata.txt` befindet sich auf der Seite im Abschnitt **Dokumente**.

### 4. ISCO-/ESCO-Klassifikation (CSV)

- **Quelle:** Europäische Kommission – ESCO-Portal
- **Link:** <https://esco.ec.europa.eu/en/use-esco/download>
- **Hinweis:** Im Bereich *Your ESCO dataset* folgende Einstellungen auswählen:
  - **Version:** `ESCO dataset – v1.2.1`
  - **Content:** `Classification`
  - **File type:** `csv`
  - **Language:** `en`

  Anschließend auf *Add to your package* klicken und das Paket herunterladen. Aus dem Archiv die Datei `ISCOGroups_en.csv` extrahieren.
