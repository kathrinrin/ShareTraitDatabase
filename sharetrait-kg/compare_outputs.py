#!/usr/bin/env python3
"""Compare SPARQL query outputs against SQL query outputs column by column."""
import csv, re, sys
from collections import Counter

def norm(v):
    if v is None:
        return ""
    v = str(v).strip()
    if v == "":
        return ""
    try:
        f = float(v)
        if f == int(f):
            return str(int(f))
        else:
            return re.sub(r'\.?0+$', '', v) if '.' in v else v
    except ValueError:
        return v

def compare_csv(sql_path, sparql_path, name, col_map=None, comment_groups=None):
    with open(sql_path, 'r') as f:
        sql_rows = list(csv.DictReader(f))
    with open(sparql_path, 'r') as f:
        sparql_rows = list(csv.DictReader(f))

    print(f"\n{'='*60}")
    print(f"  {name}: SQL={len(sql_rows)} rows, SPARQL={len(sparql_rows)} rows")
    print(f"{'='*60}")

    if len(sql_rows) != len(sparql_rows):
        print("  *** ROW COUNT MISMATCH ***")

    sql_cols = list(sql_rows[0].keys()) if sql_rows else []
    sparql_cols = list(sparql_rows[0].keys()) if sparql_rows else []

    if col_map is None:
        col_map = {c: c for c in sql_cols}
    else:
        merged = {c: c for c in sql_cols}
        merged.update(col_map)
        col_map = merged

    match_count = 0
    mismatch_count = 0
    missing_count = 0

    for sql_col, sparql_col in col_map.items():
        if sql_col not in sql_cols:
            continue
        if sparql_col not in sparql_cols:
            print(f"  MISSING in SPARQL: {sparql_col}")
            missing_count += 1
            continue

        sql_vals = Counter(norm(r.get(sql_col, "")) for r in sql_rows)
        sparql_vals = Counter(norm(r.get(sparql_col, "")) for r in sparql_rows)

        if sql_vals == sparql_vals:
            match_count += 1
        else:
            mismatch_count += 1
            only_sql = sql_vals - sparql_vals
            only_sparql = sparql_vals - sql_vals
            print(f"  MISMATCH: {sql_col}")
            for val, cnt in list(only_sql.most_common(3)):
                disp = repr(val) if val else '(empty)'
                print(f"    SQL-only:    {disp} x{cnt}")
            for val, cnt in list(only_sparql.most_common(3)):
                disp = repr(val) if val else '(empty)'
                print(f"    SPARQL-only: {disp} x{cnt}")

    # Handle grouped comment columns (multiple SQL cols → one SPARQL GROUP_CONCAT col)
    if comment_groups:
        for grp in comment_groups:
            sql_group_cols = grp['sql_cols']
            sparql_col = grp['sparql_col']
            label = grp['label']

            if sparql_col not in sparql_cols:
                print(f"  MISSING in SPARQL: {sparql_col} ({label})")
                missing_count += 1
                continue

            # Collect all non-empty SQL values across the grouped columns
            sql_vals = Counter()
            for r in sql_rows:
                for col in sql_group_cols:
                    v = norm(r.get(col, ""))
                    if v:
                        sql_vals[v] += 1

            # Collect all non-empty SPARQL values (split by |||)
            sparql_vals = Counter()
            for r in sparql_rows:
                raw = str(r.get(sparql_col, "")).strip()
                if raw:
                    for part in raw.split("|||"):
                        v = norm(part)
                        if v:
                            sparql_vals[v] += 1

            only_sql = sql_vals - sparql_vals
            only_sparql = sparql_vals - sql_vals

            if not only_sql and not only_sparql:
                match_count += len(sql_group_cols)
                print(f"  COMMENT GROUP OK: {label} ({len(sql_group_cols)} SQL cols, exact match)")
            elif not only_sql:
                match_count += len(sql_group_cols)
                extra = sum(only_sparql.values())
                print(f"  COMMENT GROUP OK: {label} (all SQL values present; "
                      f"{extra} extra SPARQL values from additional comment sources)")
            else:
                mismatch_count += len(sql_group_cols)
                print(f"  COMMENT GROUP MISMATCH: {label}")
                for val, cnt in list(only_sql.most_common(3)):
                    disp = repr(val) if val else '(empty)'
                    print(f"    SQL-only:    {disp} x{cnt}")
                for val, cnt in list(only_sparql.most_common(3)):
                    disp = repr(val) if val else '(empty)'
                    print(f"    SPARQL-only: {disp} x{cnt}")

    total = match_count + mismatch_count + missing_count
    print(f"\n  RESULT: {match_count}/{total} columns match, {mismatch_count} mismatches, {missing_count} missing")
    return mismatch_count == 0 and missing_count == 0

# Paths relative to workspace root (script is in sharetrait-kg/)
import os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SQL_DIR = os.path.join(ROOT, "sharetrait-database-v1/db-queries")
SPARQL_DIR = os.path.join(ROOT, "sharetrait-kg/sparql-queries")

# danio_data
compare_csv(f"{SQL_DIR}/danio_data-output.csv", f"{SPARQL_DIR}/danio_data-output.csv", "danio_data",
            {"count(measurement.trait_value)": "count_trait_value"})

# Aphidius
compare_csv(f"{SQL_DIR}/Aphidius-output.csv", f"{SPARQL_DIR}/Aphidius-output.csv", "Aphidius")

# master-query: map SQL column names → SPARQL column names where they differ
# Columns with identical names in both outputs don't need explicit mapping
col_map = {}

# Identical columns (77)
for c in [
    'sharetrait_datasetid', 'date_contribution', 'reference_type', 'doi_dataset',
    'doi_manuscript', 'species_reported', 'phylum_name',
    'class_name', 'order_name', 'family_name', 'genus_name', 'species_name',
    'taxonomy_db_name', 'rank_level', 'comment_taxonomy', 'site_realm_general',
    'site_realm_specific', 'elevation_value', 'depth_value', 'origin',
    'location_description', 'location_name', 'latitude', 'longitude',
    'year_collection_initial', 'year_collection_final', 'observation_date_initial',
    'observation_date_final', 'experiment_location',
    'sharetrait_type', 'strategy_of_protection',
    'sex', 'life_stage_general_initial', 'life_stage_general_final',
    'lifestage_specific_initial', 'lifestage_specific_final', 'life_stage_general',
    'life_stage_specific', 'size_type', 'size_units', 'size_value_initial',
    'size_value_final', 'size_value', 'parent_size_type', 'parent_size_units',
    'parental_size_value', 'parent_age', 'parent_age_units', 'mating_method',
    'method_type', 'fecundity_temporal_unit', 'reproductive_stage',
    'offspring_developmental_stage', 'offspring_size_type', 'offspring_size_units',
    'offspring_size_value', 'metabolic_rate_type', 'acclimation_chamber',
    'fasting_time', 'sensor_type', 'respiration_volume', 'delay_time',
    'respiratory_chamber_material', 'incubation_time', 'respirometry_type',
    'breathing_mode', 'trait_value', 'trait_unit',
    'trait_error_estimate', 'trait_error_type', 'sample_size', 'trait_converted',
    'fresh_mass',
]:
    col_map[c] = c

# Renamed columns: SQL name → SPARQL name
col_map.update({
    'maintained': 'maint_method_check',
    'condition-maintenance.duration': 'maint_duration',
    'condition-maintenance.duration_generations': 'maint_duration_generations',
    'condition-maintenance.temperature': 'maint_temperature',
    'condition-maintenance.photoperiod': 'maint_photoperiod',
    'condition-maintenance.humidity': 'maint_humidity',
    'condition-maintenancen.oxygen': 'maint_oxygen',  # note typo in SQL
    'condition-maintenance.carbon_dioxide': 'maint_carbon_dioxide',
    'condition-maintenance.salinity': 'maint_salinity',
    'condition-maintenance.ph': 'maint_ph',
    'condition-maintenance.oxygen_units': 'maint_oxygen_units',
    'condition-maintenance.carbon_dioxide_units': 'maint_carbon_dioxide_units',
    'condition-maintenance.food_type': 'maint_food_type',
    'acclimated': 'accl_method_check',
    'condition-acclimation.duration': 'accl_duration',
    'condition-acclimation.temperature': 'accl_temperature',
    'condition-acclimation.salinity': 'accl_salinity',
    'condition-acclimation.ph': 'accl_ph',
    'condition-acclimation.oxygen': 'accl_oxygen',
    'condition-acclimation.carbon_dioxide': 'accl_carbon_dioxide',
    'condition-acclimation.photoperiod': 'accl_photoperiod',
    'condition-acclimation.humidity': 'accl_humidity',
    'condition-acclimation.oxygen_units': 'accl_oxygen_units',
    'condition-acclimation.carbon_dioxide_units': 'accl_carbon_dioxide_units',
    'condition-acclimation.food_type': 'accl_food_type',
    'condition-test.temperature': 'test_temperature',
    'condition-test.oxygen': 'test_oxygen',
    'condition-test.carbon_dioxide': 'test_carbon_dioxide',
    'condition-test.oxygen_units': 'test_oxygen_units',
    'condition-test.carbon_dioxide_units': 'test_carbon_dioxide_units',
    'condition-test.photoperiod': 'test_photoperiod',
    'condition-test.humidity': 'test_humidity',
    'condition-test.food_type': 'test_food_type',
    'condition-test.salinity': 'test_salinity',
    'condition-test.ph': 'test_ph',
    'comments_reference': 'comments_reference',
    'comment_location': 'comment_location',
    'comment_trait': 'comment_trait',
    'comments_experimental_conditions': 'comments_experimental_conditions',
})

compare_csv(f"{SQL_DIR}/master-query-output.csv", f"{SPARQL_DIR}/master-query-output.csv",
            "master-query", col_map)

# --- Compare query01 to query10 ---
query_col_maps = {
    "query05": {"count (measurement.trait_value)": "count_measurements"},
    "query06": {
        "count(population.population_pk)": "population_count",
        "group_concat(population.species_reported)": "species_list",
    },
    "query08": {"max(measurement.trait_value)": "max_trait_value"},
    "query09": {"group_concat(measurement.trait_value)": "trait_values"},
}
for i in range(1, 11):
    sql_path = f"{SQL_DIR}/query{str(i).zfill(2)}-output.csv"
    sparql_path = f"{SPARQL_DIR}/query{str(i).zfill(2)}-output.csv"
    name = f"query{str(i).zfill(2)}"
    try:
        compare_csv(sql_path, sparql_path, name, query_col_maps.get(name))
    except Exception as e:
        print(f"[WARNING] Could not compare {name}: {e}")
