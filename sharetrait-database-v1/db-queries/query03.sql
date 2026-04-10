Select distinct dataset.dataset_pk, dataset.doi_dataset, dataset.dataset_publisher, manuscript.doi_manuscript
FROM measurement
LEFT JOIN individual ON individual.individual_pk = measurement.individual_pk
LEFT JOIN contains ON contains.individual_pk = individual.individual_pk
LEFT JOIN population ON population.population_pk = contains.population_pk
LEFT JOIN taxonomic_label ON taxonomic_label.population_pk = population.population_pk
LEFT JOIN ref_taxonomy ON ref_taxonomy.taxonomy_pk = taxonomic_label.taxonomy_pk
LEFT JOIN describe ON population.population_pk = describe.population_pk
LEFT JOIN dataset ON describe.dataset_pk = dataset.dataset_pk
LEFT JOIN publication ON dataset.dataset_pk = publication.dataset_pk
LEFT JOIN manuscript ON publication.manuscript_pk = manuscript.manuscript_pk
LEFT JOIN trait ON trait.trait_pk = measurement.trait_pk
WHERE measurement.trait_type = "fecundity";