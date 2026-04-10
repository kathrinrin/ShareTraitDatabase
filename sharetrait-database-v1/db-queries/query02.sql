Select ref_taxonomy.genus_name, count(measurement.trait_value) AS TRAIT_MEASURE
FROM measurement
LEFT JOIN individual ON individual.individual_pk = measurement.individual_pk
LEFT JOIN contains ON contains.individual_pk = individual.individual_pk
LEFT JOIN population ON population.population_pk = contains.population_pk
LEFT JOIN taxonomic_label ON taxonomic_label.population_pk = population.population_pk
LEFT JOIN ref_taxonomy ON ref_taxonomy.taxonomy_pk = taxonomic_label.taxonomy_pk
LEFT JOIN trait ON trait.trait_pk = measurement.trait_pk
WHERE measurement.trait_type = "development" AND measurement.trait_value NOT NULL 
GROUP by ref_taxonomy.genus_name
ORDER by TRAIT_MEASURE DESC;