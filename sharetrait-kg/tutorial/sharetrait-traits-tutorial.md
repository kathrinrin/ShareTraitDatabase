# Building a Traits Ontology: Hands-on Tutorial

> **Duration:** ~2 hours (intro, hands-on, break, real data demo)
> **Tool:** [Protege Desktop](https://protege.stanford.edu/) (version 5.x)
> **Prerequisites:** Protege installed, Java runtime
> **Result:** A small OWL ontology that automatically classifies trait measurements using real ShareTrait data

---

## Background: ShareTrait and the Problem We Are Solving

### What is ShareTrait?

[ShareTrait](https://sharetrait.org/) is an open database of individual-level trait measurements for ectotherms — animals whose body temperature follows their environment (insects, fish, amphibians, crustaceans, and over 99% of animal species). It currently focuses on three fundamental traits measurable in almost all animals:

- **Metabolic rate** — how fast an animal burns energy
- **Development time** — how long it takes to reach a life stage
- **Fecundity** — how many offspring an animal produces

Each record stores not just the trait value, but rich metadata: the species, collection site, sex, life stage, rearing temperature, acclimation conditions, and measurement technique. As of 2025, ShareTrait holds ~28,000 individual-level records from 45 datasets contributed by researchers worldwide (Leiva et al., *Functional Ecology*, 2025).

The database is built on a **relational SQL structure** — multiple tables linked by primary keys, queryable with SQL. This works well for structured retrieval within the database.

### The problem: ShareTrait is an island

The SQL database answers questions about what is *in* ShareTrait. It cannot easily answer questions about how ShareTrait data relates to the rest of the world. Three concrete limitations:

1. **Terms are strings, not concepts.** `trait_type = 'development'` is text. An external tool has no way to know what "development" means, how it relates to "fecundity", or whether it matches a term used in another database.

2. **Taxonomy is a batch pipeline.** ShareTrait generates a phylogenetic tree by calling the Open Tree of Life API in an R script — a step that must be rerun whenever new species are added. Querying "all measurements for insects" requires knowing in advance which species in the database are insects.

3. **Integration with external data requires manual pipelines.** Linking ShareTrait records to conservation status, species occurrence ranges, climate zones, or habitat classifications means writing custom code to download, clean, and join external datasets. This is done once, for one question, and cannot be reused.

### What an ontology adds

An ontology is a formal vocabulary where terms have stable identifiers, definitions, and explicit relationships. Combining ShareTrait data with an ontology (a **knowledge graph**) addresses each limitation directly:

| # | Advantage | What it means in practice |
|---|---|---|
| 1 | **Connect to external databases without manual pipelines** | ShareTrait data can be joined live with Wikidata (conservation status, climate zones), or with GBIF occurrence data loaded into the same index — using a single SPARQL query instead of a custom R script |
| 2 | **Find what is missing, not just what is there** | By comparing ShareTrait species against GBIF observation records, you can detect which animal groups, habitats, or regions have few or no trait measurements |
| 3 | **Data has meaning, not just values** | `con:Development` is a concept with a definition, linked to related concepts — machines can reason over what the data *means*, not just match strings |
| 4 | **Query across the taxonomic tree using graph traversal** | A single query with a recursive property path finds all insect measurements automatically — newly added species are included without any code change |
| 5 | **The vocabulary becomes a reusable standard** | `sharetrait-owl.ttl` is a citable artefact that other trait databases can align to; a SQL schema is invisible to the outside world |

This tutorial builds a small OWL ontology from scratch using real ShareTrait data. By the end you will understand how ontologies work mechanically — which is exactly what you need to read, evaluate, and reuse the ShareTrait knowledge graph.

---

## Part 1: Quick Introduction (10 min)

An ontology is a **formal, shared vocabulary** where the computer understands how terms relate and can check your data for mistakes.

| Plain language | OWL term | Example |
|---|---|---|
| A category | **Class** | `Organism`, `TraitType` |
| A relationship | **Property** | `measuredOnOrganism` |
| A concrete thing | **Individual** | `DanioRerio` |
| A rule | **Axiom** | "every Fish lives in an Aquatic realm" |

We write ontologies in **OWL** (Web Ontology Language). Files use **Turtle** format (`.ttl`).

### Why bother?

- **Shared terms** across labs (no more "development_time" vs "dev.time" vs "DT")
- **Stable URIs** you can look up in a browser
- **Automated reasoning**: the computer draws conclusions from your rules
- **Error detection**: logical contradictions are caught automatically

### The open-world assumption

In a database, missing data means "no". In OWL, missing data means "unknown". This matters: if you say a measurement involves `DevelopmentTrait` but do not say it *only* involves development, the reasoner thinks "maybe it also measures something else." We will see this in action later.

---

## Part 2: Hands-on in Protege (~50 min)

Create a new ontology:

1. **File > New Ontology**
2. Ontology IRI: `http://sharetrait.org/ontologies/traits`
3. **File > Save As** > Turtle format, name it `sharetrait-trait-ontology.ttl`

Save often!

---

### Step 1: Class hierarchy (10 min)

Build the full class tree. Right-click a class and select **Add subclass** to create children.

```
owl:Thing
├── IndependentEntity
│   ├── TraitMeasurement
│   │   ├── AphidiusDevelopmentStudy
│   │   └── ZebrafishMetabolicStudy
│   ├── TraitType
│   │   ├── DevelopmentTrait
│   │   ├── FecundityTrait
│   │   └── MetabolicRateTrait
│   └── Organism
│       ├── Insect
│       │   ├── ParasitoidWasp
│       │   └── FruitFly
│       ├── Amphibian
│       └── Fish
└── ValuePartition
    ├── TemperatureRange
    │   ├── Cold
    │   ├── Warm
    │   └── Hot
    └── Realm
        ├── Terrestrial
        └── Aquatic
```

That is 22 classes. We will add 5 more later (3 defined + 2 probe = 27 total). Check your tree in Protege against the diagram.

---

### Step 2: Disjoint classes (5 min)

Disjoint means "these classes can never overlap." Add disjoint axioms for each group of siblings:

1. Select any class, then in the **Description** panel click **+** next to **Disjoint With**.
2. Or right-click a parent class and use **Make all sibling classes disjoint** if available.

Add disjoints for these groups:

| Parent | Disjoint siblings |
|---|---|
| `owl:Thing` | `IndependentEntity`, `ValuePartition` |
| `IndependentEntity` | `TraitMeasurement`, `TraitType`, `Organism` |
| `TraitType` | `DevelopmentTrait`, `FecundityTrait`, `MetabolicRateTrait` |
| `Organism` | `Insect`, `Amphibian`, `Fish` |
| `Insect` | `ParasitoidWasp`, `FruitFly` |
| `TemperatureRange` | `Cold`, `Warm`, `Hot` |
| `Realm` | `Terrestrial`, `Aquatic` |
| `TraitMeasurement` | `AphidiusDevelopmentStudy`, `ZebrafishMetabolicStudy` |

We will test these disjoints later with a probe class.

---

### Step 3: Covering axioms (3 min)

A covering axiom says "these subclasses are the only options." Select the parent class, click **+** next to **Equivalent To**, and enter the union:

- `TemperatureRange`: `Cold or Warm or Hot`
- `Realm`: `Terrestrial or Aquatic`

Without these, someone could create a fourth temperature range and the reasoner would accept it.

---

### Step 4: Properties (10 min)

Switch to the **Object Properties** tab. Create these 8 properties:

| Property | Domain | Range | Characteristics |
|---|---|---|---|
| `hasComponent` | | | |
| `isComponentOf` | | | Inverse of `hasComponent` |
| `measuresTraitType` | `TraitMeasurement` | `TraitType` | SubProperty of `hasComponent` |
| `isTraitTypeOf` | | | Inverse of `measuresTraitType` |
| `measuredOnOrganism` | `TraitMeasurement` | `Organism` | SubProperty of `hasComponent`, **Functional** |
| `isOrganismOf` | | | Inverse of `measuredOnOrganism` |
| `hasTemperatureRange` | `TraitMeasurement` | `TemperatureRange` | **Functional** |
| `hasRealm` | `Organism` | `Realm` | **Functional** |

For each property:
- Right-click `owl:topObjectProperty` > **Add sub property**
- Set **Domain** and **Range** in the Description panel
- For inverses: click **+** next to **Inverse Of**
- For functional: tick **Functional** under Characteristics

**Functional** means "at most one value." A measurement has one temperature range; an organism lives in one realm.

Then switch to **Data Properties** and create:

| Property | Domain | Range |
|---|---|---|
| `hasTraitValue` | `TraitMeasurement` | `xsd:decimal` |
| `hasScientificName` | `Organism` | `xsd:string` |

---

### Step 5: Restrictions on organisms (3 min)

Go back to the **Classes** tab.

1. Select `Insect`. Click **+** next to **SubClass Of** and enter: `hasRealm some Terrestrial`
2. Select `Fish`. Add: `hasRealm some Aquatic`

We leave `Amphibian` without a realm restriction on purpose. Frogs live in water and on land. The reasoner will not guess.

---

### Step 6: Named measurements with `some` and `only` (8 min)

This is the key step. Select each study class and add these **SubClass Of** restrictions:

**AphidiusDevelopmentStudy:**
```
measuresTraitType some DevelopmentTrait
measuredOnOrganism some ParasitoidWasp
hasTemperatureRange some Cold
measuresTraitType only DevelopmentTrait
```

**ZebrafishMetabolicStudy:**
```
measuresTraitType some MetabolicRateTrait
measuredOnOrganism some Fish
measuresTraitType only MetabolicRateTrait
```

**Why both `some` and `only`?**
- `some` says "at least one value of this type exists"
- `only` says "no other types are allowed" (the closure axiom)

You need both. Without `only`, the open-world assumption means the reasoner thinks there might be other trait types too. Without `some`, `only` alone does not guarantee anything exists.

---

### Step 7: Defined classes (5 min)

Defined classes use **Equivalent To** axioms. The reasoner classifies things into them automatically.

Create three new classes under `TraitMeasurement`. For each, click **+** next to **Equivalent To**:

**AquaticTraitMeasurement:**
```
TraitMeasurement and (measuredOnOrganism some (Organism and (hasRealm some Aquatic)))
```

**ColdExposureMeasurement:**
```
TraitMeasurement and (hasTemperatureRange some Cold)
```

**InsectTraitMeasurement:**
```
TraitMeasurement and (measuredOnOrganism some Insect)
```

Before running the reasoner, predict which studies end up where:

| Defined class | Expected member |
|---|---|
| `AquaticTraitMeasurement` | `ZebrafishMetabolicStudy` (fish are aquatic) |
| `ColdExposureMeasurement` | `AphidiusDevelopmentStudy` (cold temperature) |
| `InsectTraitMeasurement` | `AphidiusDevelopmentStudy` (parasitoid wasp is an insect) |

---

### Step 8: Probe classes (3 min)

Two quick tests to check your understanding.

**InconsistentDevelopmentMetabolism:** Create a class that is a subclass of both `DevelopmentTrait` and `MetabolicRateTrait`. Since they are disjoint, the reasoner will flag this in red. Disjoint axioms catch modelling errors.

**UnclosedTraitMeasurement:** Create a class under `TraitMeasurement` and add these **SubClass Of** restrictions:
```
measuresTraitType some DevelopmentTrait
measuredOnOrganism some Insect
```

Do **not** add a closure axiom. This class will not be fully classified. Compare it with `AphidiusDevelopmentStudy` to see why closure matters.

---

### Step 9: Individuals (3 min)

Switch to the **Individuals** tab. Create four individuals:

| Individual | Type | hasScientificName |
|---|---|---|
| `DanioRerio` | `Fish` | "Danio rerio" |
| `AphidiusPlatensis` | `ParasitoidWasp` | "Aphidius platensis" |
| `RanaTemporaria` | `Amphibian` | "Rana temporaria" |
| `DrosophilaMelanogaster` | `FruitFly` | "Drosophila melanogaster" |

For each, click **+** next to **Different From** and add the other three. OWL does not assume individuals are distinct by default.

---

### Step 10: Run the reasoner (5 min)

Go to **Reasoner > HermiT** (or Pellet), then **Reasoner > Start reasoner**.

Check these results:

1. **Inferred hierarchy.** Switch to the **Inferred** tab in the class hierarchy. `ZebrafishMetabolicStudy` should appear under `AquaticTraitMeasurement`. `AphidiusDevelopmentStudy` should appear under both `ColdExposureMeasurement` and `InsectTraitMeasurement`.

2. **Red class.** `InconsistentDevelopmentMetabolism` is highlighted in red (equivalent to `owl:Nothing`).

3. **Unclosed class.** `UnclosedTraitMeasurement` is *not* classified under any defined class.

Save: **File > Save**.

---

## Take-aways

1. **Unknown is not false.** The open-world assumption is the key mental shift.
2. **Closure axioms** (`only`) are essential for reasoner classification.
3. **Disjoint axioms** catch modelling errors automatically.
4. **Defined classes** turn the reasoner into an automatic classifier.

---

## Break (15 min)

---

## Part 3: Applying the Ontology to Real Data (25 min)

Now we load actual measurements from the ShareTrait knowledge graph and let the reasoner classify them.

### Where the data comes from

The sample data was extracted from `sharetrait-kg.ttl` using a SPARQL CONSTRUCT query (`extract-sample-data.sparql`). It selects 6 real measurements, follows the chain `Measurement > Individual > Population > Taxonomy` for species, and maps temperatures to our value partitions (< 15 C = Cold, 15-25 C = Warm, > 25 C = Hot).

Each measurement is typed **only** as `:TraitMeasurement`. No manual classification.

### The 6 measurements

| ID | Species | Trait | Value | Temp |
|---|---|---|---|---|
| `measurement_aph_001` | *Aphidius platensis* | Development | 39 days | 10 C (Cold) |
| `measurement_aph_002` | *Aphidius platensis* | Development | 46 days | 10 C (Cold) |
| `measurement_dre_001` | *Danio rerio* | Metabolic rate | 0.048 mLO2/h | 26 C (Hot) |
| `measurement_rana_001` | *Rana temporaria* | Development | 35 days | 18 C (Warm) |
| `measurement_dmel_001` | *Drosophila melanogaster* | Development | 16 days | 20 C (Warm) |
| `measurement_dsub_001` | *Drosophila subobscura* | Fecundity | 185 offspring | 21 C (Warm) |

### Load and reason

1. Open your ontology from Part 2 (or the provided `sharetrait-trait-ontology.ttl`).

2. Append the sample data to your ontology file: copy the contents of `sharetrait-trait-data-sample.ttl` and paste them at the end of `sharetrait-trait-ontology.ttl`. Both files use the same namespace, so this works directly.

3. Re-open the combined file in Protege: **File > Open** `sharetrait-trait-ontology.ttl`.

4. Check the **Individuals** tab. You should see the four organism individuals from Part 2, plus the new measurement individuals and supporting individuals (`devTrait`, `cold1`, etc.).

5. **Reasoner > HermiT > Start reasoner**.

6. Select each measurement individual and check **Inferred Types** in the Description panel.

### Results

The reasoner classifies the measurements without any manual labels:

- **measurement_aph_001, measurement_aph_002**: `InsectTraitMeasurement`, `ColdExposureMeasurement` (parasitoid wasp = insect; cold temperature)
- **measurement_dre_001**: `AquaticTraitMeasurement` (fish = aquatic realm)
- **measurement_dmel_001**: `InsectTraitMeasurement` (fruit fly = insect)
- **measurement_dsub_001**: `InsectTraitMeasurement` (fruit fly = insect)
- **measurement_rana_001**: no additional type (amphibian has no realm; warm, not cold; not an insect). Open-world assumption in action.

```
6 measurements, 8 inferred classifications, 0 manual labels
```

This scales to the full knowledge graph. The ShareTrait KG lives in [QLever](https://github.com/ad-freiburg/qlever) for SPARQL querying. QLever itself does not do OWL reasoning. You run the reasoner in Protege first, export the inferred triples, and then load everything into QLever for querying.

---

## What Comes Next

Now that you know how to build an ontology from scratch, you know how to read and reuse one. Reuse is almost always the better choice.

### Replace, don't rebuild

Some of the trait classes we built today already exist in [PATO](http://purl.obolibrary.org/obo/pato.owl) (Phenotypic Quality Ontology):

| Our class | PATO term | URI | Notes |
|---|---|---|---|
| `FecundityTrait` | "fecundity" | `PATO:0000273` | Exact match |
| `MetabolicRateTrait` | "rate" | `PATO:0000161` | Too broad (PATO defines rate as "occurrence per unit time" in general) |
| `DevelopmentTrait` | -- | -- | No direct PATO term; development time combines a process with a duration |

Not everything maps cleanly. `DevelopmentTrait` has no single PATO equivalent because development time combines a biological process with a temporal quality. That is normal: you will often need to combine terms from several ontologies, or keep some local terms where no good match exists.

In practice, you use the external URI directly instead of inventing your own. For example, instead of defining a local `FecundityTrait` class, you use `http://purl.obolibrary.org/obo/PATO_0000273` in your data and restrictions. No need to import the entire PATO ontology.

Where to find terms:
- [OBO Foundry](http://obofoundry.org/) for curated bio-ontologies
- [Ontology Lookup Service (OLS)](https://www.ebi.ac.uk/ols4/) to search individual terms across 1,000+ ontologies

### The pipeline

The full pipeline from CSV to queryable knowledge graph is documented in the [sharetrait-kg README](../README.md).

```
Spreadsheet / Database
        |
        v
   RML Mapping           (rows to RDF triples)
        |
        v
   Knowledge Graph        (RDF with external ontology URIs)
        |
        v
   SPARQL Querying        (QLever)
```

| Step | Tool |
|---|---|
| Mapping | [RML.io](https://rml.io/) / [YARRRML](https://rml.io/yarrrml/) |
| Storing and querying | [QLever](https://github.com/ad-freiburg/qlever) |
| Reasoning | HermiT / Pellet (in Protege) |

You do not need to become an ontology engineer. The skills from this tutorial are exactly what you need to read, evaluate, and reuse the ontologies that already exist.
