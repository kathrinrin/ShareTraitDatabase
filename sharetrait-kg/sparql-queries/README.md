# ShareTrait SPARQL Queries

SPARQL translations of all SQL queries from the ShareTrait relational database.

## Prefix declarations (used in all queries)

```sparql
PREFIX vocab: <https://sharetrait.org/vocab/>
```

The base IRI is `https://sharetrait.org/`. All entity IRIs follow the pattern `https://sharetrait.org/{type}/{pk}`, e.g. `https://sharetrait.org/measurement/TRAMEA020001`.

---

## Named views (from `sharetrait-database-v1/db-queries/`)

| File | SQL source | Description |
|---|---|---|
| `master-query.sparql` | `master-query.sql` | Full flat export — all measurements with all joined metadata |
| `Aphidius.sparql` | `Aphidius.sql` | Development trait measurements for genus *Aphidius* |
| `danio_data.sparql` | `danio_data.sql` | Datasets and trait types for genus *Danio* |

---

## Ad-hoc queries (from `queries/queries-test-v20240909.md`)

| File | Question |
|---|---|
| `query01.sparql` | All development measurements for genus *Aphidius* with scientific names |
| `query02.sparql` | Count of development measurements per genus, ordered descending |
| `query03.sparql` | Fecundity datasets with DOIs and manuscript DOIs |
| `query04.sparql` | Datasets and trait types for genus *Danio* |
| `query05.sparql` | Measurement counts and units per *Danio* dataset |
| `query06.sparql` | Fecundity datasets: population count, species, DOI |
| `query07.sparql` | All species with development trait measurements |
| `query08.sparql` | Max development trait value per *Rana* population per dataset |
| `query09.sparql` | Test temperatures for *Rana* development traits, with grouped values |
| `query10.sparql` | Development trait value vs body size under test temperature for *Chalcolestes* |

---

## Notes on translation

### Condition pivoting (master-query)
The SQL view uses `MAX(CASE WHEN condition_label = '…' THEN … END)` to pivot maintenance / acclimation / test condition columns into one row per measurement. SPARQL does not have a pivot operation. The SPARQL translation uses three separate `OPTIONAL` blocks — one per condition label — with `vocab:hasConditionLabel` as the filter key.

### DISTINCT and GROUP BY
SQL `DISTINCT` maps directly to `SELECT DISTINCT` in SPARQL. `GROUP BY` with aggregate functions (`COUNT`, `MAX`, `GROUP_CONCAT`) maps to SPARQL aggregates.

### NULL / NOT NULL
SQL `NOT NULL` on a column maps to requiring the variable to be bound, which is the default in SPARQL triple patterns (unbound variables are simply absent). Use `FILTER(BOUND(?var))` to make the check explicit if needed.

### Individual PK extraction
Where the SQL query returns `individual.individual_pk` as a plain string, SPARQL returns the full IRI. `BIND(STRAFTER(STR(?iri), "individual/") AS ?pk)` recovers the local key.
