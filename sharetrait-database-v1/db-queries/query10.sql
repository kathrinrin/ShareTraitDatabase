Select ref_taxonomy.genus_name, measurement.trait_type, measurement.trait_value, measurement.trait_unit, measurement.size_value_final, measurement.size_units, measurement.size_type, condition.temperature, experiment_setup.condition_label
FROM ref_taxonomy
LEFT JOIN taxonomic_label ON taxonomic_label.taxonomy_pk = ref_taxonomy.taxonomy_pk
LEFT JOIN population ON population.population_pk = taxonomic_label.population_pk
LEFT JOIN contains ON contains.population_pk = population.population_pk
LEFT JOIN individual ON individual.individual_pk = contains.individual_pk
LEFT JOIN measurement ON measurement.individual_pk = individual.individual_pk 
LEFT JOIN experiment_setup ON experiment_setup.measurement_pk = measurement.measurement_pk 
LEFT JOIN condition ON condition.condition_pk = experiment_setup.condition_pk
WHERE ref_taxonomy.genus_name = "Chalcolestes" AND measurement.trait_type = "development" AND experiment_setup.condition_label = "test" AND measurement.trait_value NOT NULL;