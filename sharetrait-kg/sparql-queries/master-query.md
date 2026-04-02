# master-query

## Description

Full flat export of the ShareTrait knowledge graph — equivalent to the SQL view `master-query-all`.

Each result row represents one measurement, with all associated metadata joined in: taxonomy, site, location, dataset, publication, experimental conditions (maintenance / acclimation / test), respiratory chamber, acclimation specification, and individual attributes.

**Note on condition pivoting:** The SQL view uses `MAX(CASE WHEN condition_label = '…' THEN … END)` to pivot the three condition types into a single row per measurement. The SPARQL translation uses three separate `OPTIONAL` blocks — one per condition label — to achieve the same result. Rows where a condition type is absent will have unbound variables for those fields.

## SQL source

`sharetrait-database-v1/db-queries/master-query.sql`

## SPARQL query

See `master-query.sparql`
