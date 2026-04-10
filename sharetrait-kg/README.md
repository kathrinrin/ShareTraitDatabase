# ShareTrait Knowledge Graph

All commands run from the **repository root**.

## Directory structure

```
sharetrait-kg/
├── compare_outputs.py          # validation script (SPARQL vs SQL)
├── rml-scripts/                # one RML mapping per table (*.ttl)
├── sparql-queries/             # SPARQL queries (*.sparql) and docs (*.md)
│   — derived / not committed —
├── rmlmapper.jar               # download (see prerequisites)
├── ttl-output/                 # per-table TTL output
├── sharetrait-kg.ttl           # concatenated knowledge graph
├── sharetrait-kg-index/        # QLever index files
└── sparql-queries/*-output.csv # query results
```

## Prerequisites

- **Java** – for the RML mapper
- **Python 3** – with `pandas` installed (see below)
- **SQLite3** – for SQL reference queries
- **QLever** – `qlever-index` and `qlever-server`
- **RML mapper** – download from
  <https://github.com/RMLio/rmlmapper-java/releases/>
  and save as `sharetrait-kg/rmlmapper.jar`

### Python virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pandas
```

Activate the venv (`source .venv/bin/activate`) before running any Python
commands in the pipeline below.

---

## Validation Pipeline

End-to-end pipeline: CSV → TTL → KG → SPARQL output, then compare against SQL output.

### 1. Run all RML mappings (CSV → TTL)

```bash
mkdir -p sharetrait-kg/ttl-output
for script in sharetrait-kg/rml-scripts/*.ttl; do
  name=$(basename "$script" .ttl)
  java -jar sharetrait-kg/rmlmapper.jar -m "$script" -o "sharetrait-kg/ttl-output/$name.ttl"
done
```

### 2. Concatenate TTL files

Use Python (not `cat`) to guarantee newline separators between files.
Lines with invalid WKT literals (e.g. `POINT(NA …)`), invalid typed
literals (e.g. `"NA"^^xsd:decimal`), or plain `"NA"` string literals are
stripped during concatenation so they never enter the index. URL-encoded
spaces (`%20`) in concept URIs are normalised to underscores as a safety
net (the RML join-based concept mapping should already produce clean
CamelCase URIs).

The SKOS vocabulary (`sharetrait-skos.ttl`) is appended to the KG so that
SPARQL queries can resolve `skos:prefLabel` for concept URIs.

```bash
python3 -c "
import glob, pathlib, re
files = sorted(glob.glob('sharetrait-kg/ttl-output/*.ttl'))
bad_wkt = re.compile(r'POINT\([^)]*\bNA\b')
bad_typed_na = re.compile(r'\"NA\"\^\^<')
bad_plain_na = re.compile(r'\"NA\" [;.]')
concept_pct20 = re.compile(r'(https://sharetrait\.org/concept/[^>]*)%20')
prefix_line = re.compile(r'^@(prefix|base)\s')
dropped = 0
with open('sharetrait-kg/sharetrait-kg.ttl', 'w') as out:
    out.write('@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n')
    out.write('@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n')
    out.write('@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n')
    out.write('@prefix con: <https://sharetrait.org/concept/> .\n\n')
    for f in files:
        for line in pathlib.Path(f).read_text().splitlines(keepends=True):
            if bad_wkt.search(line) or bad_typed_na.search(line) or bad_plain_na.search(line):
                dropped += 1
            else:
                while concept_pct20.search(line):
                    line = concept_pct20.sub(r'\1_', line)
                out.write(line)
        out.write('\n')
    # Append SKOS vocabulary (skip its @prefix/@base declarations)
    for line in pathlib.Path('sharetrait-kg/sharetrait-skos.ttl').read_text().splitlines(keepends=True):
        if not prefix_line.match(line):
            out.write(line)
print(f'Concatenated {len(files)} files + SKOS vocab, dropped {dropped} invalid lines')
"
```

### 3. Build QLever index

```bash
rm -f sharetrait-kg/sharetrait-kg-index/myindex.*
qlever-index \
  -i sharetrait-kg/sharetrait-kg-index/myindex \
  -f sharetrait-kg/sharetrait-kg.ttl \
  -F ttl
```

### 4. Start QLever server

```bash
pkill -f qlever-server 2>/dev/null; sleep 1
nohup qlever-server -i sharetrait-kg/sharetrait-kg-index/myindex -p 7001 > /dev/null 2>&1 & disown
sleep 2
curl -s 'http://localhost:7001/' \
  --data-urlencode 'query=SELECT (COUNT(*) AS ?c) WHERE { ?s ?p ?o }' \
  -H 'Accept: text/csv'
```

### 5. Run SPARQL queries

```bash
for q in danio_data Aphidius master-query query01 query02 query03 query04 query05 query06 query07 query08 query09 query10; do
  curl -s 'http://localhost:7001/' -H 'Accept: text/csv' \
    --data-urlencode "query=$(cat sharetrait-kg/sparql-queries/$q.sparql)" \
    -o "sharetrait-kg/sparql-queries/$q-output.csv"
done
```

### 6. Compare SPARQL vs SQL output

The SQL query outputs in `sharetrait-database-v1/db-queries/*-output.csv` are
the committed ground truth. **Do not regenerate them.** The comparison script
reads the existing SQL CSVs and compares them against the SPARQL output:

```bash
python3 sharetrait-kg/compare_outputs.py
```

### 7. Stop QLever server

```bash
pkill -f qlever-server
```

---

## Optional: QLever UI via Docker

```bash
docker run -it -p 7002:7000 \
  -v "$(pwd)/db:/app/db" \
  --name qleverui qleverui
```

See the [QLever UI docs](https://github.com/qlever-dev/qlever-ui/blob/master/docs/install_qleverui.md).

## Optional: Petrimaps (map visualisation without Docker)

[Petrimaps](https://petrimaps.2comp.org/) renders SPARQL query results on
a map. It connects directly to a running QLever endpoint — no Docker required.

### Setup

1. Download the latest release from
   <https://github.com/2comp/petrimaps/releases/> and unpack it.
2. Build it and then start it: 

```bash
./build/petrimaps -p 9090
```

3. Open **http://localhost:7002** in your browser.

### Example geo query

Paste the following query. Petrimaps detects the `geo:wktLiteral` column
and places markers on the map automatically.

```sparql
PREFIX geo: <http://www.opengis.net/ont/geosparql#>
PREFIX vocab: <https://sharetrait.org/vocab/>

SELECT ?site ?locationName ?locationDesc ?wkt WHERE {
  ?site geo:hasGeometry/geo:asWKT ?wkt .
  ?place vocab:locatedIn ?site .
  OPTIONAL { ?place vocab:hasLocationName ?locationName }
  OPTIONAL { ?place vocab:hasLocationDescription ?locationDesc }
}
ORDER BY ?site
```
