# Building a Traits Ontology: Hands-on Tutorial

> **Duration:** ~2 hours (intro, hands-on, break, real data demo)
> **Tool:** [Protege Desktop](https://protege.stanford.edu/) (version 5.x)
> **Prerequisites:** Protege installed, Java runtime
> **Result:** A small OWL ontology that automatically classifies trait measurements using real ShareTrait data — with one juvenile spangled perch as the worked example

---

## The worked example: one juvenile spangled perch

Throughout this tutorial we keep coming back to a single real measurement from ShareTrait:

| Field | Value |
|---|---|
| Measurement ID | `TRAMEA023773` |
| Species | *Leiopotherapon unicolor* (spangled perch, a small Australian freshwater fish) |
| Life stage | juvenile |
| Body mass | 0.0074 kg (≈ 7.4 g) |
| Trait | standard metabolic rate |
| Value | **117.0165483 mgO2/h/kgFM** |
| Test temperature | 21.5 °C |
| Treatment | control: 0 mg/L NO3−, pH 7.0 |
| Technique | intermittent flow-through respirometry, fiber-optic O2 sensor, 693 mL acrylic chamber (modelled as a `Respirometer` instrument) |
| Source | Gomez Isaza et al. (2020), *Conservation Physiology* 8(1):coz092, [doi:10.1093/conphys/coz092](https://doi.org/10.1093/conphys/coz092) |
| Dataset DOI | [10.14264/80b3353](https://doi.org/10.14264/80b3353) |

In the original study, 300 juvenile spangled perch were exposed for 28 days to a 2 × 3 factorial of pH (7.0 or 4.0) and nitrate (0, 50, or 100 mg/L), then their resting oxygen consumption was measured. Our hero fish (`TRAMEA023773`) is one of the control animals — it tells us what "normal" oxygen demand looks like for a small juvenile of this species at 21.5 °C.

Why this record? It is biologically rich (a real ectotherm under controlled conditions, with a clearly documented method), it has all the contextual fields we want to model (species, life stage, temperature, value), and we have two more records from the same study to use as comparators. By the end of the tutorial, the OWL reasoner will be classifying this measurement automatically into four different categories without us having to label it manually.

---

## Background: ShareTrait and the Problem We Are Solving

### What is ShareTrait?

[ShareTrait](https://sharetrait.org/) is an open database of individual-level trait measurements for ectotherms — animals whose body temperature follows their environment (insects, fish, amphibians, crustaceans, and over 99% of animal species). It currently focuses on three fundamental traits measurable in almost all animals:

- **Metabolic rate** — how fast an animal burns energy (our hero record measures this)
- **Development time** — how long it takes to reach a life stage
- **Fecundity** — how many offspring an animal produces

Each record stores not just the trait value, but rich metadata: the species, collection site, sex, life stage, rearing temperature, acclimation conditions, and measurement technique. As of 2025, ShareTrait holds ~28,000 individual-level records from 45 datasets contributed by researchers worldwide (Leiva et al., *Functional Ecology*, 2025).

The database is built on a **relational SQL structure** — multiple tables linked by primary keys, queryable with SQL. This works well for structured retrieval within the database.

### The problem: ShareTrait is an island

The SQL database answers questions about what is *in* ShareTrait. It cannot easily answer questions about how ShareTrait data relates to the rest of the world. Three concrete limitations, illustrated with the spangled perch record:

1. **Terms are strings, not concepts.** `trait_type = 'metabolic_rate'` is text. An external tool has no way to know that this is the same concept as "respiration rate" in another database, or how it relates to "fecundity".

2. **Taxonomy is a batch pipeline.** To answer "give me all metabolic-rate measurements for freshwater fish" you must first know that *Leiopotherapon unicolor* is a freshwater fish — currently encoded only as a string column.

3. **Integration with external data requires manual pipelines.** Linking the spangled perch record to its IUCN conservation status, its native range, or its phylogenetic relatives means writing custom code each time.

### What an ontology adds

An ontology is a formal vocabulary where terms have stable identifiers, definitions, and explicit relationships. Combining ShareTrait data with an ontology (a **knowledge graph**) addresses each limitation directly:

| # | Advantage | What it means for the spangled perch record |
|---|---|---|
| 1 | **Connect to external databases without manual pipelines** | The fish individual can be joined live with Wikidata (conservation status, distribution) or GBIF occurrences in a single SPARQL query |
| 2 | **Find what is missing, not just what is there** | You can quickly ask "which Australian freshwater fish have no metabolic-rate records yet?" |
| 3 | **Data has meaning, not just values** | `MetabolicRateTrait` is a concept with a definition, not the string `"metabolic_rate"` |
| 4 | **Query across the taxonomic tree using graph traversal** | A single recursive query finds all `Fish` measurements automatically — spangled perch included |
| 5 | **The vocabulary becomes a reusable standard** | `sharetrait-owl.ttl` is a citable artefact other trait databases can align to |

This tutorial builds a small OWL ontology from scratch and then loads the spangled perch (plus five comparator records) into it. By the end you will understand how ontologies work mechanically — which is exactly what you need to read, evaluate, and reuse the ShareTrait knowledge graph.

---

## Part 1: Quick Introduction (10 min)

An ontology is a **formal, shared vocabulary** where the computer understands how terms relate and can check your data for mistakes.

| Plain language | OWL term | Example from our tutorial |
|---|---|---|
| A category | **Class** | `Organism`, `Fish`, `SpangledPerch`, `MetabolicRateTrait`, `Respirometer` |
| A relationship | **Property** | `measuredOnOrganism`, `hasLifeStage`, `usedInstrument` |
| A concrete thing | **Individual** | `organism_Leiopotherapon_unicolor`, `respirometer_001585` |
| A rule | **Axiom** | "every Fish lives in an Aquatic realm" |

We write ontologies in **OWL** (Web Ontology Language). Files use **Turtle** format (`.ttl`).

### Why bother?

- **Shared terms** across labs (no more `metabolic_rate` vs `MR` vs `resp.rate`)
- **Stable URIs** you can look up in a browser
- **Automated reasoning**: the computer draws conclusions from your rules
- **Error detection**: logical contradictions are caught automatically

### A bit of notation

Protégé shows axioms in a readable "Manchester syntax" with four symbols you need to recognise:

| Manchester | DL symbol | Meaning |
|---|---|---|
| `and` | ⊓ | both classes apply |
| `or` | ⊔ | at least one class applies |
| `some` | ∃ | existential restriction ("at least one") |
| `only` | ∀ | universal restriction ("only values of this kind") |

### The open-world assumption

In a database, missing data means "no". In OWL, missing data means "unknown". This matters: if you say our spangled perch measurement `measuresTraitType` some `MetabolicRateTrait` but do not say it *only* involves a metabolic rate, the reasoner thinks "maybe it also measures development time." The fix is a **closure axiom** with `only` — see Step 6.

---

## Part 2: Hands-on in Protege (~55 min)

Create a new ontology:

1. **File > New Ontology**
2. Ontology IRI: `http://sharetrait.org/ontologies/traits`
3. **File > Save As** > Turtle format, name it `sharetrait-ontology.ttl`

Save often!

---

### Step 1: Class hierarchy (10 min)

Build the full class tree. Right-click a class and select **Add subclass** to create children.

```
owl:Thing
├── IndependentEntity
│   ├── TraitMeasurement
│   │   ├── AphidiusDevelopmentStudy
│   │   └── SpangledPerchRespirometryStudy
│   ├── TraitType
│   │   ├── DevelopmentTrait
│   │   ├── FecundityTrait
│   │   └── MetabolicRateTrait
│   ├── Organism
│   │   ├── Insect
│   │   │   ├── ParasitoidWasp
│   │   │   └── FruitFly
│   │   ├── Amphibian
│   │   └── Fish
│   │       └── SpangledPerch
│   └── Instrument
│       └── Respirometer
└── ValuePartition
    ├── TemperatureRange
    │   ├── Cold
    │   ├── Warm
    │   └── Hot
    ├── Realm
    │   ├── Terrestrial
    │   └── Aquatic
    └── LifeStage
        ├── Juvenile
        ├── Adult
        └── Larva
```

That is 28 classes. We will add 7 more later (5 defined + 2 probe = 35 total). Check your tree in Protege against the diagram.

> **Why `SpangledPerch` as its own class?** Our hero record is a *Leiopotherapon unicolor*. Giving the species its own class under `Fish` lets us attach species-level facts (conservation status, native range, an external Wikidata URI) in one place, instead of repeating them on every individual fish.

> **Why `SpangledPerchRespirometryStudy` and not `ZebrafishMetabolicStudy`?** It is a *named class of measurement*, named after the hero study (Gomez Isaza et al. 2020), and fully described by the trait type, organism, temperature, and life stage it must have.

> **Why `LifeStage` as a value partition?** Our hero fish is a juvenile. Life stage is a closed set of categories (juvenile / adult / larva), exactly the kind of thing value partitions are for.

> **Why an `Instrument` class?** The hero record was acquired with a 693 mL acrylic respirometer and a fiber-optic O₂ sensor. The original SQL database stores this as free-text columns on a `respiratory_chamber` row; in the ontology we lift it to a first-class entity so two studies that used the same device can be linked, and so we can ask "give me every metabolic-rate record acquired with a respirometer" with one query.

---

### Step 2: Disjoint classes (5 min)

Disjoint means "these classes can never overlap." Add disjoint axioms for each group of siblings:

1. Select any class, then in the **Description** panel click **+** next to **Disjoint With**.
2. Or right-click a parent class and use **Make all sibling classes disjoint** if available.

Add disjoints for these groups:

| Parent | Disjoint siblings |
|---|---|
| `owl:Thing` | `IndependentEntity`, `ValuePartition` |
| `IndependentEntity` | `TraitMeasurement`, `TraitType`, `Organism`, `Instrument` |
| `TraitType` | `DevelopmentTrait`, `FecundityTrait`, `MetabolicRateTrait` |
| `Organism` | `Insect`, `Amphibian`, `Fish` |
| `Insect` | `ParasitoidWasp`, `FruitFly` |
| `Fish` | `SpangledPerch` (only one for now; no disjoint needed until siblings exist) |
| `Instrument` | `Respirometer` (only one for now) |
| `TemperatureRange` | `Cold`, `Warm`, `Hot` |
| `Realm` | `Terrestrial`, `Aquatic` |
| `LifeStage` | `Juvenile`, `Adult`, `Larva` |
| `TraitMeasurement` | `AphidiusDevelopmentStudy`, `SpangledPerchRespirometryStudy` |

We will test these disjoints later with a probe class.

---

### Step 3: Covering axioms (3 min)

A covering axiom says "these subclasses are the only options." Select the parent class, click **+** next to **Equivalent To**, and enter the union:

- `TemperatureRange`: `Cold or Warm or Hot`
- `Realm`: `Terrestrial or Aquatic`
- `LifeStage`: `Juvenile or Adult or Larva`

Without these, someone could create a fourth life stage and the reasoner would accept it.

---

### Step 4: Properties (10 min)

Switch to the **Object Properties** tab. Create these 11 properties:

| Property | Domain | Range | Characteristics |
|---|---|---|---|
| `hasComponent` | | | |
| `isComponentOf` | | | Inverse of `hasComponent` |
| `measuresTraitType` | `TraitMeasurement` | `TraitType` | SubProperty of `hasComponent` |
| `isTraitTypeOf` | | | Inverse of `measuresTraitType` |
| `measuredOnOrganism` | `TraitMeasurement` | `Organism` | SubProperty of `hasComponent`, **Functional** |
| `isOrganismOf` | | | Inverse of `measuredOnOrganism` |
| `usedInstrument` | `TraitMeasurement` | `Instrument` | SubProperty of `hasComponent`, **Functional** |
| `isInstrumentOf` | | | Inverse of `usedInstrument` |
| `hasTemperatureRange` | `TraitMeasurement` | `TemperatureRange` | **Functional** |
| `hasLifeStage` | `TraitMeasurement` | `LifeStage` | **Functional** |
| `hasRealm` | `Organism` | `Realm` | **Functional** |

For each property:
- Right-click `owl:topObjectProperty` > **Add sub property**
- Set **Domain** and **Range** in the Description panel
- For inverses: click **+** next to **Inverse Of**
- For functional: tick **Functional** under Characteristics

**Functional** means "at most one value." A measurement has one temperature range, one life stage, one primary instrument; an organism lives in one realm.

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

Once this restriction is in place, the spangled perch (an instance of `Fish`) will automatically inherit `hasRealm some Aquatic`. We do not need to state it on the individual.

---

### Step 6: Named measurements — existential restrictions + a closure axiom (8 min)

This is the key step. We describe our two *named measurement classes* as **necessary conditions** (subclass-of axioms) using existential (`some`, ∃) and universal (`only`, ∀) property restrictions.

Select each study class and add these **SubClass Of** restrictions:

**AphidiusDevelopmentStudy:**
```
measuresTraitType   some DevelopmentTrait     -- ∃ measuresTraitType . DevelopmentTrait
measuredOnOrganism  some ParasitoidWasp
hasTemperatureRange some Cold
measuresTraitType   only DevelopmentTrait     -- closure axiom (∀)
```

**SpangledPerchRespirometryStudy:** (the class our hero record belongs to)
```
measuresTraitType   some MetabolicRateTrait
measuredOnOrganism  some Fish
hasTemperatureRange some Warm
hasLifeStage        some Juvenile
usedInstrument      some Respirometer
measuresTraitType   only MetabolicRateTrait   -- closure axiom (∀)
```

**Why both `some` and `only`?**

- `some` (∃) is an **existential restriction**: "at least one value of this type exists." Without it, an empty measurement would trivially satisfy `only`.
- `only` (∀) is a **universal restriction** — a **closure axiom**: "if a value exists for this property, it must be of this type." Without it, the OWA lets the reasoner imagine other trait types attached to the measurement.

We attach these as `SubClassOf` (necessary conditions), *not* `EquivalentTo` (necessary and sufficient). That is the next step.

---

### Step 7: Defined classes — necessary *and sufficient* conditions (6 min)

This is the most important distinction in OWL modelling:

- A **SubClassOf** axiom states *necessary* conditions. Any member of the class must satisfy them, but satisfying them does not make you a member.
- An **EquivalentTo** axiom states *necessary and sufficient* conditions. Anything that satisfies them is automatically classified as a member by the reasoner.

Defined classes use **EquivalentTo** axioms. The reasoner then becomes an automatic classifier — exactly what we want for `JuvenileFishMeasurement` to swallow the spangled perch records.

Create five new classes under `TraitMeasurement`. For each, click **+** next to **Equivalent To**:

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

**JuvenileFishMeasurement:** (the class that should swallow our hero record)
```
TraitMeasurement and (measuredOnOrganism some Fish) and (hasLifeStage some Juvenile)
```

**RespirometryMeasurement:** (any measurement acquired with a respirometer)
```
TraitMeasurement and (usedInstrument some Respirometer)
```

Before running the reasoner, predict which records end up where:

| Defined class | Expected member |
|---|---|
| `AquaticTraitMeasurement` | spangled perch records (fish are aquatic) |
| `ColdExposureMeasurement` | `AphidiusDevelopmentStudy` (cold temperature) |
| `InsectTraitMeasurement` | `AphidiusDevelopmentStudy` (parasitoid wasp is an insect) |
| `JuvenileFishMeasurement` | spangled perch records (fish + juvenile) |
| `RespirometryMeasurement` | spangled perch records (used a respirometer) |

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

Switch to the **Individuals** tab. Create four organism individuals plus one instrument:

| Individual | Type | Data property |
|---|---|---|
| `organism_Leiopotherapon_unicolor` | `SpangledPerch` | `hasScientificName "Leiopotherapon unicolor"` |
| `organism_Aphidius_platensis` | `ParasitoidWasp` | `hasScientificName "Aphidius platensis"` |
| `organism_Rana_temporaria` | `Amphibian` | `hasScientificName "Rana temporaria"` |
| `organism_Drosophila_melanogaster` | `FruitFly` | `hasScientificName "Drosophila melanogaster"` |
| `respirometer_001585` | `Respirometer` | (label only) |

Note that `organism_Leiopotherapon_unicolor` is typed as `SpangledPerch`, not `Fish`. The reasoner will infer `Fish`, `Organism`, and `hasRealm some Aquatic` automatically — that is the whole point of a class hierarchy.

For the four organism individuals, click **+** next to **Different From** and add the other three. OWL does **not** assume individuals are distinct by default (it drops the Unique Name Assumption).

---

### Step 10: Run the reasoner (5 min)

Go to **Reasoner > HermiT** (or Pellet), then **Reasoner > Start reasoner**. The reasoner performs three jobs:

1. **Consistency check** — is the ontology free of contradictions?
2. **Subsumption / classification** — which classes are subclasses of which?
3. **Realisation** — for each individual, which classes does it belong to?

Check these results:

1. **Inferred hierarchy.** Switch to the **Inferred** tab in the class hierarchy. `SpangledPerchRespirometryStudy` should appear under `AquaticTraitMeasurement`, `JuvenileFishMeasurement`, *and* `RespirometryMeasurement`. `AphidiusDevelopmentStudy` should appear under both `ColdExposureMeasurement` and `InsectTraitMeasurement`. `SpangledPerch` appears under `Fish`.

2. **Red class.** `InconsistentDevelopmentMetabolism` is highlighted in red (equivalent to `owl:Nothing` — *unsatisfiable*).

3. **Unclosed class.** `UnclosedTraitMeasurement` is *not* classified under any defined class.

### Try a DL Query

Open the **DL Query** tab (Window > Tabs > DL Query if it is hidden). Type:

```
TraitMeasurement and (measuredOnOrganism some Fish)
```

The Instances panel should list the three spangled-perch measurements once Part 3 data is loaded.

Save: **File > Save**.

---

## Take-aways

1. **Unknown is not false.** The Open World Assumption is the key mental shift.
2. **Existential (∃, `some`) vs universal (∀, `only`).** Both are needed: `some` introduces a value, `only` closes the property.
3. **Necessary vs necessary-and-sufficient.** `SubClassOf` ≠ `EquivalentTo`. Defined classes use `EquivalentTo`.
4. **Disjoint axioms** catch modelling errors automatically.
5. **Defined classes** turn the reasoner into an automatic classifier.

---

## Break (15 min)

---

## Part 3: Applying the Ontology to Real Data (25 min)

Now we load actual measurements from the ShareTrait knowledge graph and let the reasoner classify them. The hero is still `TRAMEA023773`.

### Where the data comes from

The sample data was extracted from `sharetrait-kg.ttl` using a SPARQL `CONSTRUCT` query (`extract-data-sample.sparql`). For each chosen measurement it follows the chain `Measurement → Individual → Population → Taxonomy` for the species, `Measurement → Condition (test)` for the temperature, and `Measurement → hasLifeStageGeneral` for life stage. Then it:

- maps temperatures to our value partitions (< 15 °C = `Cold`, 15–25 °C = `Warm`, ≥ 25 °C = `Hot`),
- maps life-stage strings to `juvenile1` / `adult1` / `larva1` **when the KG records them** (otherwise no `hasLifeStage` triple is emitted), and
- maps species via `CONTAINS` rules (`Leiopotherapon` → `Fish`, `Aphidius` → `ParasitoidWasp`, etc.).

Each measurement is typed **only** as `:TraitMeasurement`. No manual classification.

### The 6 measurements

Three spangled-perch records anchor the demo; three more species give the reasoner variety.

| ID | Species | Trait | Value | Temp | Life stage | Notes |
|---|---|---|---|---|---|---|
| `measurement_023773` | *Leiopotherapon unicolor* | Metabolic rate | **117.0 mgO2/h/kgFM** | 21.5 °C (Warm) | juvenile | **Hero record `TRAMEA023773`**, control |
| `measurement_023776` | *Leiopotherapon unicolor* | Metabolic rate | 110.0 mgO2/h/kgFM | 21.5 °C (Warm) | juvenile | `TRAMEA023776`, control replicate |
| `measurement_023829` | *Leiopotherapon unicolor* | Metabolic rate | 751.4 mgO2/h/kgFM | 21.5 °C (Warm) | juvenile | `TRAMEA023829`, 100 mg/L nitrate stress |
| `measurement_000001` | *Aphidius platensis* | Development | 39 days | < 15 °C (Cold) | *not in KG* | `TRAMEA000001` |
| `measurement_003743` | *Rana temporaria* | Development | 35 days | 15–25 °C (Warm) | *not in KG* | `TRAMEA003743` |
| `measurement_004493` | *Drosophila melanogaster* | Development | 16 days | 15–25 °C (Warm) | *not in KG* | `TRAMEA004493` |

### Expected SPARQL output (Turtle, abridged)

Running `extract-data-sample.sparql` against `sharetrait-kg.ttl` produces triples like these — this is what should end up in `sharetrait-data-sample.ttl`:

```turtle
:measurement_023773 a owl:NamedIndividual , t:TraitMeasurement ;
    rdfs:label              "TRAMEA023773 (hero record)" ;
    t:measuresTraitType     t:MetabolicRateTrait ;
    t:measuredOnOrganism    :organism_Leiopotherapon_unicolor ;
    t:hasTemperatureRange   t:warm1 ;
    t:hasLifeStage          t:juvenile1 ;
    t:usedInstrument        t:respirometer_001585 ;
    t:hasTraitValue         117.0165483 .

:organism_Leiopotherapon_unicolor a owl:NamedIndividual , t:SpangledPerch ;
    t:hasScientificName     "Leiopotherapon unicolor" .

t:respirometer_001585 a owl:NamedIndividual , t:Respirometer ;
    rdfs:label "693 mL acrylic/Plexiglas respirometer, fiber optic-based oxygen analyzer" .
```

The shipped `sharetrait-data-sample.ttl` is the exact serialization of this query (re-grouped by subject and annotated with tutorial commentary), so re-running the SPARQL produces the same triples you load into Protege.

### Load and reason

1. Open your ontology from Part 2 (or the provided `sharetrait-ontology.ttl`).

2. Append the sample data to your ontology file: copy the contents of `sharetrait-data-sample.ttl` and paste them at the end of `sharetrait-ontology.ttl`. Both files use the same namespace, so this works directly.

3. Re-open the combined file in Protege: **File > Open** `sharetrait-ontology.ttl`.

4. Check the **Individuals** tab. You should see the four organism individuals from Part 2, plus the new measurement individuals (`measurement_023773` and friends) and supporting partition individuals (`warm1`, `juvenile1`, …).

5. **Reasoner > HermiT > Start reasoner**.

6. Select each measurement individual and check **Inferred Types** in the Description panel.

### Results

The reasoner classifies the measurements without any manual labels:

- **measurement_023773 (hero)**: `AquaticTraitMeasurement`, `JuvenileFishMeasurement`, `RespirometryMeasurement`, `SpangledPerchRespirometryStudy`
- **measurement_023776**: same four classes — control replicate
- **measurement_023829**: same four classes — the inferred *category* is identical, but the raw trait value (751.4 vs 117.0) reveals the biological story: nitrate stress at 100 mg/L elevates the standard metabolic rate by ~6.4×
- **measurement_000001**: `InsectTraitMeasurement`, `ColdExposureMeasurement`
- **measurement_004493**: `InsectTraitMeasurement`
- **measurement_003743**: no additional type. Amphibians have no realm restriction, warm is not cold, not an insect, not a fish. Open-world assumption in action.

```
6 measurements, 14 inferred classifications, 0 manual labels
```

The hero record alone picks up four inferred classes — fish biology, life stage, instrument, and the named study class — purely from its data triples plus the ontology rules.

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
| `DevelopmentTrait` | — | — | No direct PATO term; development time combines a process with a duration |

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

You do not need to become an ontology engineer. The skills from this tutorial — and the spangled perch record you walked through — are exactly what you need to read, evaluate, and reuse the ontologies that already exist.
