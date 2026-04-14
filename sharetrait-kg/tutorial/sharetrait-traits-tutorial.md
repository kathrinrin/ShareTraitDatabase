# Building a Traits Ontology: Hands-on Tutorial

> **Duration:** ~2 hours (intro, hands-on, break, real data demo)
> **Tool:** [Protege Desktop](https://protege.stanford.edu/) (version 5.x)
> **Prerequisites:** Protege installed, Java runtime
> **Result:** A small OWL ontology that automatically classifies trait measurements using real ShareTrait data

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
│   │   ├── AphidiusDevelopmentAssay
│   │   └── ZebrafishMetabolicAssay
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
| `TraitMeasurement` | `AphidiusDevelopmentAssay`, `ZebrafishMetabolicAssay` |

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

This is the key step. Select each assay class and add these **SubClass Of** restrictions:

**AphidiusDevelopmentAssay:**
```
measuresTraitType some DevelopmentTrait
measuredOnOrganism some ParasitoidWasp
hasTemperatureRange some Cold
measuresTraitType only DevelopmentTrait
```

**ZebrafishMetabolicAssay:**
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

Before running the reasoner, predict which assays end up where:

| Defined class | Expected member |
|---|---|
| `AquaticTraitMeasurement` | `ZebrafishMetabolicAssay` (fish are aquatic) |
| `ColdExposureMeasurement` | `AphidiusDevelopmentAssay` (cold temperature) |
| `InsectTraitMeasurement` | `AphidiusDevelopmentAssay` (parasitoid wasp is an insect) |

---

### Step 8: Probe classes (3 min)

Two quick tests to check your understanding.

**InconsistentDevelopmentMetabolism:** Create a class that is a subclass of both `DevelopmentTrait` and `MetabolicRateTrait`. Since they are disjoint, the reasoner will flag this in red. Disjoint axioms catch modelling errors.

**UnclosedTraitMeasurement:** Create a class with these **SubClass Of** restrictions:
```
TraitMeasurement
and (measuresTraitType some DevelopmentTrait)
and (measuredOnOrganism some Insect)
```

Do **not** add a closure axiom. This class will not be fully classified. Compare it with `AphidiusDevelopmentAssay` to see why closure matters.

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

1. **Inferred hierarchy.** Switch to the **Inferred** tab in the class hierarchy. `ZebrafishMetabolicAssay` should appear under `AquaticTraitMeasurement`. `AphidiusDevelopmentAssay` should appear under both `ColdExposureMeasurement` and `InsectTraitMeasurement`.

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

2. Open the sample data: **File > Open** `sharetrait-trait-data-sample.ttl`. Since both files share the same namespace, Protege merges them.

   Alternatively, copy the sample data into the end of your ontology file before opening.

3. Check the **Individuals** tab. You should see the four organism individuals from Part 2, plus the new measurement individuals and supporting individuals (`devTrait`, `cold1`, etc.).

4. **Reasoner > HermiT > Start reasoner**.

5. Select each measurement individual and check **Inferred Types** in the Description panel.

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

This scales to the full knowledge graph. The ShareTrait KG lives in [QLever](https://github.com/ad-freiburg/qlever); loading the ontology alongside the data lets SPARQL queries use the inferred classifications.

---

## What Comes Next

Now that you know how to build an ontology from scratch, you know how to read and reuse one. Reuse is almost always the better choice.

### Replace, don't rebuild

The classes we built today have equivalents in established ontologies:

| Our class | Replace with | URI |
|---|---|---|
| `DevelopmentTrait` | PATO "developmental process" | `PATO:0001309` |
| `FecundityTrait` | PATO "fecundity" | `PATO:0000273` |
| `MetabolicRateTrait` | PATO "metabolic rate" | `PATO:0001413` |
| `Fish` | NCBI Taxonomy "Actinopteri" | `NCBITaxon:7898` |
| `Insect` | NCBI Taxonomy "Insecta" | `NCBITaxon:50557` |
| `Aquatic` | ENVO "aquatic biome" | `ENVO:00002030` |

In practice, you replace local URIs with external ones directly rather than importing entire ontologies. Your data uses the real URIs; your restrictions reference those URIs.

Where to find terms:
- [OBO Foundry](http://obofoundry.org/) for curated bio-ontologies
- [BioPortal](https://bioportal.bioontology.org/) to browse 1,000+ ontologies
- [Ontology Lookup Service](https://www.ebi.ac.uk/ols4/) to search across ontologies

### Validate with SHACL

Once you replace local classes with external URIs, you need a way to describe and enforce the expected structure of your data. That is what SHACL (Shapes Constraint Language) does.

SHACL shapes define rules like:
- Every `TraitMeasurement` must have exactly one `measuresTraitType`
- The value of `measuredOnOrganism` must be an instance of a known organism class
- `hasTraitValue` must be a decimal

This is complementary to OWL reasoning. OWL tells you what *can be inferred*. SHACL tells you what *must be present*. We already use SHACL shapes in the ShareTrait project to validate the full knowledge graph.

### The pipeline

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
   SHACL Validation       (check structure and completeness)
        |
        v
   SPARQL + Reasoning     (query with inferred facts)
```

| Step | Tool |
|---|---|
| Mapping | [RML.io](https://rml.io/) / [YARRRML](https://rml.io/yarrrml/) |
| Storing and querying | [QLever](https://github.com/ad-freiburg/qlever) |
| Validation | [pySHACL](https://github.com/RDFLib/pySHACL) |
| Reasoning | HermiT / Pellet (in Protege) |

You do not need to become an ontology engineer. The skills from this tutorial are exactly what you need to read, evaluate, and reuse the ontologies that already exist.
