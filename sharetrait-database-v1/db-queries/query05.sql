Select dataset.dataset_pk, population.species_reported, measurement.trait_type, count (measurement.trait_value), measurement.trait_unit
from dataset, describe, population, taxonomic_label, ref_taxonomy, contains, individual, measurement
where ref_taxonomy.genus_name = "Danio" AND ref_taxonomy.taxonomy_pk = taxonomic_label.taxonomy_pk AND taxonomic_label.population_pk = population.population_pk AND population.population_pk = describe.population_pk AND describe.dataset_pk = dataset.dataset_pk
AND population.population_pk = contains.population_pk AND contains.individual_pk = individual.individual_pk AND individual.individual_pk = measurement.individual_pk 
Group by dataset.dataset_pk;