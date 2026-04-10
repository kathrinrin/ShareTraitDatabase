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
- **Python 3** – with `pandas` installed
- **SQLite3** – for SQL reference queries
- **QLever** – `qlever-index` and `qlever-server`
- **RML mapper** – download from
  <https://github.com/RMLio/rmlmapper-java/releases/>
  and save as `sharetrait-kg/rmlmapper.jar`

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

Use Python (not `cat`) to guarantee newline separators between files:

```bash
python3 -c "
import glob, pathlib
files = sorted(glob.glob('sharetrait-kg/ttl-output/*.ttl'))
with open('sharetrait-kg/sharetrait-kg.ttl', 'w') as out:
    for f in files:
        out.write(pathlib.Path(f).read_text())
        out.write('\n')
print(f'Concatenated {len(files)} files')
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

### 6. (Optional) Rebuild SQLite database and run SQL queries

```bash
python3 -c "
import sqlite3, pandas as pd, os, glob
db = 'sharetrait-database-v1/sharetrait.db'
conn = sqlite3.connect(db); cur = conn.cursor()
for f in sorted(glob.glob('sharetrait-database-v1/db-tables/*.csv')):
    t = os.path.splitext(os.path.basename(f))[0]
    cur.execute(f'DROP TABLE IF EXISTS [{t}]')
    pd.read_csv(f, dtype=str, keep_default_na=False).to_sql(t, conn, if_exists='replace', index=False)
conn.commit(); conn.close()
"
```

Recreate views, then export:

```bash
for q in danio_data Aphidius master-query; do
  sqlite3 sharetrait-database-v1/sharetrait.db ".read sharetrait-database-v1/db-queries/$q.sql"
done


for q in query01 query02 query03 query04 query05 query06 query07 query08 query09 query10; do
  sqlite3 sharetrait-database-v1/sharetrait.db <<SQL
.mode csv
.headers on
.output sharetrait-database-v1/db-queries/$q-output.csv
.read sharetrait-database-v1/db-queries/$q.sql
SQL
done

sqlite3 sharetrait-database-v1/sharetrait.db <<'SQL'
.mode csv
.headers on
.output sharetrait-database-v1/db-queries/danio_data-output.csv
SELECT * FROM danio_data;
.output sharetrait-database-v1/db-queries/Aphidius-output.csv
SELECT * FROM Aphidius;
.output sharetrait-database-v1/db-queries/master-query-output.csv
SELECT * FROM "master-query-all";
SQL
```

### 7. Compare SPARQL vs SQL output

Per-column multiset comparison with numeric normalization:

```bash
python3 sharetrait-kg/compare_outputs.py
```

### 8. Stop QLever server

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
