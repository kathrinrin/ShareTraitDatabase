# ShareTrait Knowledge Graph – Build & Query Workflow

All commands run from the **repository root**:

```bash
cd <path-to>/ShareTraitDatabase
```

## Directory structure

```
sharetrait-kg/
├── README.md                   # this file
├── .gitignore                  # excludes derived/downloadable files
├── compare_outputs.py          # validation script (SPARQL vs SQL)
├── rml-scripts/                # one RML mapping per table (*.ttl)
├── sparql-queries/             # SPARQL queries (*.sparql) and docs (*.md)
│
│   — derived / not committed —
├── rmlmapper.jar               # download from §0
├── ttl-output/                 # per-table TTL output (from §1)
├── sharetrait-kg.ttl           # concatenated knowledge graph (from §2)
├── sharetrait-kg-index/        # QLever index files (from §3)
└── sparql-queries/*-output.csv # query results (from §5)
```

---

## 0. Prerequisites

- **Java** – for the RML mapper
- **QLever** – `qlever-index` and `qlever-server`
- **Python 3** – for TTL concatenation and validation
- **SQLite3** – for running SQL reference queries
- **RML mapper** – download from
  <https://github.com/RMLio/rmlmapper-java/releases/>
  and save as `sharetrait-kg/rmlmapper.jar`

---

## 1. Run RML mappings (CSV → TTL)

| Item | Path |
|------|------|
| Source CSVs | `tables/table_values_v04/*.csv` |
| RML scripts | `sharetrait-kg/rml-scripts/*.ttl` |
| Output TTLs | `sharetrait-kg/ttl-output/*.ttl` |

```bash
java -jar sharetrait-kg/rmlmapper.jar -m sharetrait-kg/rml-scripts/acclimation_describe.ttl -o sharetrait-kg/ttl-output/acclimation_describe.ttl
java -jar sharetrait-kg/rmlmapper.jar -m sharetrait-kg/rml-scripts/acclimation_specification.ttl -o sharetrait-kg/ttl-output/acclimation_specification.ttl
java -jar sharetrait-kg/rmlmapper.jar -m sharetrait-kg/rml-scripts/chamber_describe.ttl -o sharetrait-kg/ttl-output/chamber_describe.ttl
java -jar sharetrait-kg/rmlmapper.jar -m sharetrait-kg/rml-scripts/condition.ttl -o sharetrait-kg/ttl-output/condition.ttl
java -jar sharetrait-kg/rmlmapper.jar -m sharetrait-kg/rml-scripts/contains.ttl -o sharetrait-kg/ttl-output/contains.ttl
java -jar sharetrait-kg/rmlmapper.jar -m sharetrait-kg/rml-scripts/dataset.ttl -o sharetrait-kg/ttl-output/dataset.ttl
java -jar sharetrait-kg/rmlmapper.jar -m sharetrait-kg/rml-scripts/describe.ttl -o sharetrait-kg/ttl-output/describe.ttl
java -jar sharetrait-kg/rmlmapper.jar -m sharetrait-kg/rml-scripts/experiment_setup.ttl -o sharetrait-kg/ttl-output/experiment_setup.ttl
java -jar sharetrait-kg/rmlmapper.jar -m sharetrait-kg/rml-scripts/individual.ttl -o sharetrait-kg/ttl-output/individual.ttl
java -jar sharetrait-kg/rmlmapper.jar -m sharetrait-kg/rml-scripts/located_in.ttl -o sharetrait-kg/ttl-output/located_in.ttl
java -jar sharetrait-kg/rmlmapper.jar -m sharetrait-kg/rml-scripts/manuscript.ttl -o sharetrait-kg/ttl-output/manuscript.ttl
java -jar sharetrait-kg/rmlmapper.jar -m sharetrait-kg/rml-scripts/measurement.ttl -o sharetrait-kg/ttl-output/measurement.ttl
java -jar sharetrait-kg/rmlmapper.jar -m sharetrait-kg/rml-scripts/occurrence.ttl -o sharetrait-kg/ttl-output/occurrence.ttl
java -jar sharetrait-kg/rmlmapper.jar -m sharetrait-kg/rml-scripts/place.ttl -o sharetrait-kg/ttl-output/place.ttl
java -jar sharetrait-kg/rmlmapper.jar -m sharetrait-kg/rml-scripts/population.ttl -o sharetrait-kg/ttl-output/population.ttl
java -jar sharetrait-kg/rmlmapper.jar -m sharetrait-kg/rml-scripts/publication.ttl -o sharetrait-kg/ttl-output/publication.ttl
java -jar sharetrait-kg/rmlmapper.jar -m sharetrait-kg/rml-scripts/ref_taxonomy.ttl -o sharetrait-kg/ttl-output/ref_taxonomy.ttl
java -jar sharetrait-kg/rmlmapper.jar -m sharetrait-kg/rml-scripts/respiratory_chamber.ttl -o sharetrait-kg/ttl-output/respiratory_chamber.ttl
java -jar sharetrait-kg/rmlmapper.jar -m sharetrait-kg/rml-scripts/site.ttl -o sharetrait-kg/ttl-output/site.ttl
java -jar sharetrait-kg/rmlmapper.jar -m sharetrait-kg/rml-scripts/taxonomic_label.ttl -o sharetrait-kg/ttl-output/taxonomic_label.ttl
java -jar sharetrait-kg/rmlmapper.jar -m sharetrait-kg/rml-scripts/trait.ttl -o sharetrait-kg/ttl-output/trait.ttl
```

---

## 2. Concatenate TTL files into a single knowledge graph

> **Important:** Use Python (not plain `cat`) to ensure newline separators between files, which prevents TTL parse errors from missing trailing newlines.

```bash
python3 -c "
import glob, pathlib
files = sorted(glob.glob('sharetrait-kg/ttl-output/*.ttl'))
with open('sharetrait-kg/sharetrait-kg.ttl', 'w') as out:
    for f in files:
        out.write(pathlib.Path(f).read_text())
        out.write('\n')
print(f'Concatenated {len(files)} TTL files')
"
```

---

## 3. Build QLever index

Remove old index files first, then build:

```bash
rm -f sharetrait-kg/sharetrait-kg-index/myindex.*

qlever-index \
  -i sharetrait-kg/sharetrait-kg-index/myindex \
  -f sharetrait-kg/sharetrait-kg.ttl \
  -F ttl
```

---

## 4. Start QLever server

Use `nohup` + `disown` to fully detach the server process so it doesn't block the terminal, then verify with a quick triple-count query:

```bash
pkill -f qlever-server 2>/dev/null; sleep 1

nohup qlever-server -i sharetrait-kg/sharetrait-kg-index/myindex -p 7001 > /dev/null 2>&1 & disown

sleep 2
curl -s 'http://localhost:7001/' \
  --data-urlencode 'query=SELECT (COUNT(*) AS ?c) WHERE { ?s ?p ?o }' \
  -H 'Accept: text/csv'
```

---

## 5. Run SPARQL queries and save output CSVs

```bash
curl -s 'http://localhost:7001/' -H 'Accept: text/csv' \
  --data-urlencode "query=$(cat sharetrait-kg/sparql-queries/danio_data.sparql)" \
  -o sharetrait-kg/sparql-queries/danio_data-output.csv

curl -s 'http://localhost:7001/' -H 'Accept: text/csv' \
  --data-urlencode "query=$(cat sharetrait-kg/sparql-queries/Aphidius.sparql)" \
  -o sharetrait-kg/sparql-queries/Aphidius-output.csv

curl -s 'http://localhost:7001/' -H 'Accept: text/csv' \
  --data-urlencode "query=$(cat sharetrait-kg/sparql-queries/master-query.sparql)" \
  -o sharetrait-kg/sparql-queries/master-query-output.csv
```

---

## 6. Run SQL queries and save output CSVs

Uses the SQLite database built by `sharetrait-database-v1/db-tools/build-sharetrait-db-v1.py`:

```bash
sqlite3 sharetrait-database-v1/sharetrait.db <<'SQL'
.mode csv
.headers on
.output sharetrait-database-v1/db-queries/danio_data-output.csv
.read sharetrait-database-v1/db-queries/danio_data.sql
.output sharetrait-database-v1/db-queries/Aphidius-output.csv
.read sharetrait-database-v1/db-queries/Aphidius.sql
.output sharetrait-database-v1/db-queries/master-query-output.csv
.read sharetrait-database-v1/db-queries/master-query.sql
SQL
```

---

## 7. Validate SPARQL output against SQL output

Runs a per-column multiset comparison with numeric normalization. Expects 100% match on all 112 columns of the master query:

```bash
python3 sharetrait-kg/compare_outputs.py
```

---

## 8. (Optional) Start QLever UI via Docker

See the [QLever UI install docs](https://github.com/qlever-dev/qlever-ui/blob/master/docs/install_qleverui.md).

```bash
docker run -it -p 7002:7000 \
  -v "$(pwd)/db:/app/db" \
  --name qleverui \
  qleverui
```

---

## 9. Stop QLever server

```bash
pkill -f qlever-server
```
