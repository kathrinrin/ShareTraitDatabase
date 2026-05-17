# Building a Traits Ontology: Hands-on Tutorial

> **Duration:** 2 hours (intro, ShareTrait, two hands-on blocks with plenaries, break, wrap-up)
> **Tool:** [Protégé Desktop](https://protege.stanford.edu/) (version 5.x)
> **Prerequisites:** Protégé and Java pre-installed and confirmed working before the session - see `setup-before-tutorial.md`. Bring `sharetrait-ontology-starter.ttl` opening cleanly in Protégé.
> **Result:** A small OWL ontology that automatically classifies trait measurements using real ShareTrait data - with one juvenile spangled perch as the worked example

The starter file `sharetrait-ontology-starter.ttl` is *almost* complete: one real element of each modelling layer (one class, one disjoint axiom, one covering axiom, one object property, one data property) has been left empty so participants create it themselves in Steps 1–5 of the live session. Steps 6–11 then build on top of the completed starter. The tutorial text below walks through every step in detail so it can also be used to rebuild the ontology from scratch later.

---

## Running order (120 min)

| Time | Block | Mode |
|---|---|---|
| 0:00–0:10 | Part 1 - Intro to ontologies | demo |
| 0:10–0:20 | Part 2 - ShareTrait introduction | presentation |
| 0:20–0:50 | Part 3 - Hands-on Block A (Steps 1–8) | hands-on |
| 0:50–1:00 | Plenary A | discussion |
| 1:00–1:10 | Break | - |
| 1:10–1:40 | Part 4 - Hands-on Block B (Steps 9–11 + data) | hands-on + demo |
| 1:40–1:50 | Plenary B - what the reasoner inferred | discussion |
| 1:50–2:00 | Part 5 - Reuse, what comes next, Q&A | discussion |

Work in **pairs**. Save as you go.

---

## Research question for today

> **How does standard metabolic rate scale with body mass in freshwater fish at ~21 °C - and does environmental stress (here: nitrate exposure) shift that scaling?**

This is the question that motivates today's modelling work. Three things to note:

- It needs **body mass *and* metabolic rate** on the same record - exactly what ShareTrait stores.
- One study (Gomez Isaza et al. 2020) gives us 3 juvenile spangled perch in the dataset: body masses 7.4 g / 9.6 g / 12.4 g, control SMR ≈ **117 mgO₂/h/kgFM**, nitrate-stressed (100 mg/L NO₃⁻) ≈ **751 mgO₂/h/kgFM** - ~6.4× higher.
- A scaling *curve* needs many more studies than that. The point of an ontology is to make those studies findable and combinable across labs - we return to what the tutorial does and does not answer at the end (Part 5).

Throughout the rest of the tutorial we keep coming back to one of those three perch records (`TRAMEA023773`) as the worked example.

---

## The worked example: one juvenile spangled perch

Here is the full record for `TRAMEA023773`:

| Field | Value |
|---|---|
| Measurement ID | `TRAMEA023773` |
| Species | *Leiopotherapon unicolor* (spangled perch, a small Australian freshwater fish) |
| Life stage | juvenile |
| Body mass | ≈ 7.4 g |
| Trait | standard metabolic rate |
| Value | **117.0165483 mgO2/h/kgFM** |
| Test temperature | 21.5 °C |
| Treatment | control: 0 mg/L NO3−, pH 7.0 |
| Technique | intermittent flow-through respirometry, fiber-optic O2 sensor, 693 mL acrylic chamber (modelled as a `Respirometer` instrument) |
| Source | Gomez Isaza et al. (2020), *Conservation Physiology* 8(1):coz092, [doi:10.1093/conphys/coz092](https://doi.org/10.1093/conphys/coz092) |
| Dataset DOI | [10.14264/80b3353](https://doi.org/10.14264/80b3353) |

In the original study, 300 juvenile spangled perch were exposed for 28 days to a 2 × 3 factorial of pH (7.0 or 4.0) and nitrate (0, 50, or 100 mg/L), then their resting oxygen consumption was measured. Our hero fish (`TRAMEA023773`) is one of the control animals - it tells us what "normal" oxygen demand looks like for a small juvenile of this species at 21.5 °C.

Why this record? It is biologically rich (a real ectotherm under controlled conditions, with a clearly documented method), it has all the contextual fields we want to model (species, life stage, temperature, value), and we have two more records from the same study to use as comparators. By the end of the tutorial, the OWL reasoner will be classifying this measurement automatically into three inferred categories (`AquaticTraitMeasurement`, `JuvenileFishMeasurement`, `RespirometryMeasurement`) without us having to label it manually.

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

---

## Concept cheat sheet (reference)

Keep this table open in a side tab during the hands-on, or printed on the table next to your laptop. Every concept the tutorial touches, in one place, with the spangled-perch example for each:

| Concept | What it does | From our fish |
|---|---|---|
| *Vocabulary primitives* | | |
| **Class** | A category of things | `SpangledPerch`, `Fish`, `MetabolicRateTrait`, `Respirometer` |
| **Property** | A relationship between things (object property) or between a thing and a literal (data property) | `measuredOnOrganism` (object), `hasTraitValue` (data) |
| **Individual** | A concrete thing | `organism_Leiopotherapon_unicolor`, `measurement_023773` |
| **Axiom** | A logical statement the reasoner can use | "every `Fish` lives in an `Aquatic` realm" |
| *Class axioms* | | |
| **SubClassOf** (⊑) | "Is-a"; *necessary* condition. Members must satisfy it, but satisfying it does not make you a member | `SpangledPerch ⊑ Fish` |
| **EquivalentTo** (≡) | Necessary *and sufficient*; defined class; anything matching is automatically classified | `JuvenileFishMeasurement ≡ TraitMeasurement and (measuredOnOrganism some Fish) and (hasLifeStage some Juvenile)` |
| **Disjoint Classes** | "These classes can never overlap" | `Insect`, `Amphibian`, `Fish` are pairwise disjoint |
| **Covering axiom** | "These subclasses are the only options"; `EquivalentTo` a disjunction of the subclasses | `LifeStage ≡ Juvenile or Adult or Larva` |
| **`owl:Nothing`** (empty class, ⊥) | The class with no members; any class proven equivalent to it is **unsatisfiable** (the reasoner flags it red) | `InconsistentDevelopmentMetabolism` collapses to `owl:Nothing` because it inherits from two disjoint trait types |
| *Logical connectives* | | |
| **Conjunction** (`and`, ⊓) | Both classes apply | `Fish and (hasRealm some Aquatic)` |
| **Disjunction** (`or`, ⊔) | At least one of the classes applies | `Juvenile or Adult or Larva` |
| *Property restrictions (quantifiers)* | | |
| **Existential restriction** (`some`, ∃) | "At least one value of this kind exists" | `Fish ⊑ hasRealm some Aquatic` |
| **Universal restriction** (`only`, ∀) | "If a value exists for this property, it must be of this kind"; a **closure axiom** | `SpangledPerchRespirometryStudy ⊑ measuresTraitType only MetabolicRateTrait` |
| *Property characteristics* | | |
| **Functional** property | "At most one value" | `measuredOnOrganism`: one measurement, one organism |
| **Transitive** property | If `a R b` and `b R c`, then `a R c` | Not used in this tutorial; a classic example is `partOf`: if a fin is part of a perch and the perch is part of a population, the fin is part of the population |
| **Inverse Of** | Two properties pointing opposite ways; state once, reasoner derives both | `measuredOnOrganism` / `isOrganismOf` |
| *Reasoner concepts* | | |
| **Realisation** (instance classification) | Reasoner deciding which classes each individual belongs to | `measurement_023773` → `JuvenileFishMeasurement`, `AquaticTraitMeasurement`, `RespirometryMeasurement` |
| **Open-world assumption (OWA)** | Missing data means "unknown", not "no"; the reason `only` closure axioms are needed | Without `only` on `measuresTraitType`, the reasoner could imagine the perch measurement also has a `DevelopmentTrait` |

---

## Part 2: ShareTrait - what it is and why an ontology on top (10 min)

A short presentation from the ShareTrait team. No hands-on action. The presentation covers:

- What the **ShareTrait database** is, what it covers, and who contributes.
- How a record is structured (species, individual, condition, technique, trait, value, body size).
- Why we are now adding an **ontology layer** on top - and where this tutorial fits in.

The short version of why we are adding an ontology on top of ShareTrait:

| # | Advantage | What it means for the spangled perch record |
|---|---|---|
| 1 | **Terms have meaning, not just values** | `MetabolicRateTrait` is a concept with a definition; the species is `Leiopotherapon unicolor` joinable to Wikidata, GBIF, or IUCN in one SPARQL query |
| 2 | **Reasoning over the taxonomy** | A single query finds all `Fish` measurements automatically - spangled perch included |
| 3 | **Find what is missing, not just what is there** | "Which Australian freshwater fish have no metabolic-rate records yet?" becomes a one-line query |
| 4 | **The vocabulary becomes a reusable standard** | Other trait databases can align to it instead of re-inventing terms |

The rest of this tutorial builds a small OWL ontology and loads six real measurements into it - the hero spangled perch (`TRAMEA023773`), two more spangled perch from the same study (one control, one nitrate-stressed), and three records from different species (parasitoid wasp, frog, fruit fly). By the end you will understand how ontologies work mechanically. 

---

## Part 3: Hands-on in Protégé - Block A (30 min)

Open the **starter file** in Protégé:

**File > Open** > `sharetrait-ontology-starter.ttl`

**The pedagogical pattern for the rest of the tutorial.** The starter is *almost* complete: in each of Steps 1–5 exactly **one** real element of that modelling layer (one class, one disjoint axiom, one covering axiom, one object property, one data property) has been left out for you to create. You learn how to create one real, meaningful element of each kind yourself, while the facilitator demonstrates the same action on screen. Steps 6–8 then build new axioms (realm restrictions, named measurement classes with closure, and five defined classes) on top of the completed starter. By the end of Block A your file is the full base ontology - 34 classes, 11 object properties, 2 data properties - built with your own hands.

Save as you go: **File > Save**.

> The eight Block A sub-steps and the four Block B sub-steps in this tutorial are deliberately bite-sized - each one targets exactly one OWL concept (class, disjoint, covering, property, restriction, closure, defined class, individual). The facilitator demonstrates the same action on screen, so you can still see how it is done even if you fall behind.

---

### Step 1 [hands-on]: Add one class - `SpangledPerch` (2 min)

The starter contains 26 classes; the hero species class is missing. You add it.

1. In the **Classes** tab, expand `owl:Thing > Organism > Fish`.
2. Right-click `Fish` and choose **Add subclass**.
3. Name it `SpangledPerch`.

The full class tree once you are done (27 classes):

```
owl:Thing
├── TraitMeasurement
│   ├── AphidiusDevelopmentStudy
│   └── SpangledPerchRespirometryStudy
├── TraitType
│   ├── DevelopmentTrait
│   ├── FecundityTrait
│   └── MetabolicRateTrait
├── Organism
│   ├── Insect
│   │   ├── ParasitoidWasp
│   │   └── FruitFly
│   ├── Amphibian
│   └── Fish
│       └── SpangledPerch          ← you add this
├── Instrument
│   └── Respirometer
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

That is 27 classes. We will add 7 more in Steps 8–9 (5 defined + 2 probe = 34 total).

> **Why `SpangledPerch` as its own class?** Species-level facts (conservation status, native range, external Wikidata URI) attach in one place instead of being repeated on every individual fish.

> **Why `SpangledPerchRespirometryStudy` (a study-shaped class)?** It is described by the trait type, organism, temperature, life stage, and instrument it must have - exactly the pattern we will exercise in Step 7.

> **Why `LifeStage` as a value partition?** It is a small closed set (juvenile / adult / larva) - the textbook use case for value partitions.

> **Why an `Instrument` class?** Lifting the respirometer from a free-text column to a first-class entity lets the reasoner answer "every metabolic-rate record acquired with a respirometer" with one query.

---

### Step 2 [hands-on]: Add one disjoint-class axiom - Insect / Amphibian / Fish (2 min)

Disjoint means "these classes can never overlap." The starter declares disjointness for every sibling group *except* the three organism kinds - you add that one.

1. Select `Insect`.
2. In the **Description** panel, click **+** next to **Disjoint With**.
3. Add `Amphibian` and `Fish`.

Protégé propagates the symmetric axiom - you only need to state it once. The probe class in Step 9 will demonstrate what disjoint axioms catch.

The full set of disjoint axioms in your file is now:

| Parent | Disjoint siblings |
|---|---|
| `owl:Thing` | `TraitMeasurement`, `TraitType`, `Organism`, `Instrument` |
| `TraitType` | `DevelopmentTrait`, `FecundityTrait`, `MetabolicRateTrait` |
| **`Organism`** | **`Insect`, `Amphibian`, `Fish`** ← you add this |
| `Insect` | `ParasitoidWasp`, `FruitFly` |
| `TemperatureRange` | `Cold`, `Warm`, `Hot` |
| `Realm` | `Terrestrial`, `Aquatic` |
| `LifeStage` | `Juvenile`, `Adult`, `Larva` |
| `TraitMeasurement` | `AphidiusDevelopmentStudy`, `SpangledPerchRespirometryStudy` |

---

### Step 3 [hands-on]: Add one covering axiom - `LifeStage` (2 min)

A covering axiom says "these subclasses are the only options." The starter declares covering for `TemperatureRange` and `Realm` - you add it for `LifeStage`.

1. Select `LifeStage`.
2. In the **Description** panel, click **+** next to **Equivalent To**.
3. Enter: `Juvenile or Adult or Larva`.

Your file now has all three covering axioms:

- `TemperatureRange`: `Cold or Warm or Hot`
- `Realm`: `Terrestrial or Aquatic`
- **`LifeStage`: `Juvenile or Adult or Larva`** ← you add this

Without these, someone could create a fourth life stage and the reasoner would accept it.

---

### Step 4 [hands-on]: Add one object property - `hasLifeStage` (5 min)

Switch to the **Object Properties** tab. Ten of the eleven object properties needed by the rest of the tutorial are pre-loaded. You add the eleventh: `hasLifeStage`.

A **Functional** property means "at most one value per subject" - one measurement has one organism, one instrument, one temperature range, one life stage. An **inverse** pair (declared with `owl:inverseOf`) links two properties pointing in opposite directions: stating `m measuredOnOrganism o` once lets the reasoner derive `o isOrganismOf m`. In the starter, `measuredOnOrganism`, `usedInstrument`, `hasTemperatureRange`, and `hasRealm` are already declared **Functional**, and the four inverse pairs are already set; you declare `hasLifeStage` Functional as well.

**Your turn:**

1. Right-click `owl:topObjectProperty` > **Add sub property** → name it `hasLifeStage`.
2. In the Description panel:
   - **Domains** → `TraitMeasurement`
   - **Ranges** → `LifeStage`
   - Tick **Functional** under *Characteristics*.

Full reference (yours plus the pre-loaded ten):

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
| **`hasLifeStage`** | **`TraitMeasurement`** | **`LifeStage`** | **Functional** ← you add this |
| `hasRealm` | `Organism` | `Realm` | **Functional** |

---

### Step 5 [hands-on]: Add one data property - `hasScientificName` (3 min)

Switch to the **Data Properties** tab. One data property is pre-loaded (`hasTraitValue`, range `xsd:decimal`). You add the second, which carries species labels on organism individuals in Step 10.

1. Right-click `owl:topDataProperty` > **Add sub property** → name it `hasScientificName`.
2. In the Description panel:
   - **Domains** → `Organism`
   - **Ranges** → `xsd:string`

Your file now has both data properties:

| Property | Domain | Range |
|---|---|---|
| `hasTraitValue` | `TraitMeasurement` | `xsd:decimal` |
| **`hasScientificName`** | **`Organism`** | **`xsd:string`** ← you add this |

Only two data properties - we keep the tutorial focused on the Measurement → Trait → Organism story. Body size is *not* modelled here; see the note in Part 5.

---

### Step 6 [hands-on]: Realm restrictions on `Insect` and `Fish` (3 min)

Go back to the **Classes** tab.

1. Select `Insect`. Click **+** next to **SubClass Of** and enter: `hasRealm some Terrestrial`
2. Select `Fish`. Add: `hasRealm some Aquatic`

We leave `Amphibian` without a realm restriction on purpose. Frogs live in water and on land. The reasoner will not guess.

Once this restriction is in place, the spangled perch (an instance of `Fish`) will automatically inherit `hasRealm some Aquatic`. We do not need to state it on the individual.

---

### Step 7 [hands-on]: Named measurements - existential restrictions + a closure axiom (8 min)

This is the key modelling step. We describe our two *named measurement classes* as **necessary conditions** (subclass-of axioms) using existential (`some`, ∃) and universal (`only`, ∀) property restrictions.

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
- `only` (∀) is a **universal restriction** - a **closure axiom**: "if a value exists for this property, it must be of this type." Without it, the OWA lets the reasoner imagine other trait types attached to the measurement.

We attach these as `SubClassOf` (necessary conditions), *not* `EquivalentTo` (necessary and sufficient). The contrast - and what `EquivalentTo` buys us - is the topic of the next step (on a different set of classes).

---

### Step 8 [hands-on]: Defined classes - necessary *and sufficient* conditions (6 min)
This is the most important distinction in OWL modelling:

- A **SubClassOf** axiom states *necessary* conditions. Any member of the class must satisfy them, but satisfying them does not make you a member.
- An **EquivalentTo** axiom states *necessary and sufficient* conditions. Anything that satisfies them is automatically classified as a member by the reasoner.

Defined classes use **EquivalentTo** axioms. The reasoner then becomes an automatic classifier - exactly what we want for `JuvenileFishMeasurement` to swallow the spangled perch records.

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

## Plenary A - checkpoint after Step 8 (10 min)

Quick group check before the break. Things to look at together:

- Inferred class hierarchy: does `SpangledPerchRespirometryStudy` appear under `JuvenileFishMeasurement`?
- The role of the closure axiom (`only`) under the open-world assumption.
- The difference between `SubClassOf` (named class) and `EquivalentTo` (defined class).
- Anyone stuck - fix together so Block B starts clean.

---

## Break (10 min)

---

## Part 4: Hands-on in Protégé - Block B (30 min)

In Block B you add probe classes, create the organism individuals, run the reasoner, then load six real ShareTrait measurements and watch the reasoner classify them.

---

### Step 9 [hands-on]: Probe classes (3 min)

Two quick tests to check your understanding.

**InconsistentDevelopmentMetabolism:** Create a class that is a subclass of both `DevelopmentTrait` and `MetabolicRateTrait`. Since they are disjoint, the reasoner will flag this in red. Disjoint axioms catch modelling errors.

**UnclosedTraitMeasurement:** Create a class under `TraitMeasurement` and add these **SubClass Of** restrictions:
```
measuresTraitType some DevelopmentTrait
measuredOnOrganism some Insect
```

Do **not** add a closure axiom. This class will not be fully classified. Compare it with `AphidiusDevelopmentStudy` to see why closure matters.

---

### Step 10 [hands-on]: Individuals (3 min)

Switch to the **Individuals** tab. Create four organism individuals plus one instrument:

| Individual | Type | Data property |
|---|---|---|
| `organism_Leiopotherapon_unicolor` | `SpangledPerch` | `hasScientificName "Leiopotherapon unicolor"` |
| `organism_Aphidius_platensis` | `ParasitoidWasp` | `hasScientificName "Aphidius platensis"` |
| `organism_Rana_temporaria` | `Amphibian` | `hasScientificName "Rana temporaria"` |
| `organism_Drosophila_melanogaster` | `FruitFly` | `hasScientificName "Drosophila melanogaster"` |
| `respirometer_001585` | `Respirometer` | (label only) |

Note that `organism_Leiopotherapon_unicolor` is typed as `SpangledPerch`, not `Fish`. The reasoner will infer `Fish`, `Organism`, and `hasRealm some Aquatic` automatically - that is the whole point of a class hierarchy.

For the four organism individuals, click **+** next to **Different From** and add the other three. OWL does **not** assume individuals are distinct by default (it drops the Unique Name Assumption).

---

### Step 11 [hands-on]: Run the reasoner (5 min)

Go to **Reasoner > HermiT** (or Pellet), then **Reasoner > Start reasoner**. The reasoner performs three jobs:

1. **Consistency check** - is the ontology free of contradictions?
2. **Subsumption / classification** - which classes are subclasses of which?
3. **Realisation** (instance classification) - for each individual, which classes does it belong to?

Check these results:

1. **Inferred hierarchy.** Switch to the **Inferred** tab in the class hierarchy. `SpangledPerchRespirometryStudy` should appear under `AquaticTraitMeasurement`, `JuvenileFishMeasurement`, *and* `RespirometryMeasurement`. `AphidiusDevelopmentStudy` should appear under both `ColdExposureMeasurement` and `InsectTraitMeasurement`. `SpangledPerch` appears under `Fish`.

2. **Red class.** `InconsistentDevelopmentMetabolism` is highlighted in red (equivalent to `owl:Nothing` - *unsatisfiable*).

3. **Unclosed class.** `UnclosedTraitMeasurement` is *not* classified under any defined class.

### Try a DL Query

Open the **DL Query** tab (Window > Tabs > DL Query if it is hidden). Type:

```
TraitMeasurement and (measuredOnOrganism some Fish)
```

At this point there are no measurement individuals yet, so the Instances panel will be empty. We will re-run this query after loading the real data and it will list the three spangled-perch measurements.

Save: **File > Save**.

---

### Load the real data and re-run the reasoner (15 min)

Now we load six real ShareTrait measurements on top of the ontology you just built. The hero is still `TRAMEA023773`. The facilitator drives this part from the front; participants follow on their own laptops.

**The 6 measurements** - three spangled-perch records anchor the demo; three more species give the reasoner variety.

| ID | Species | Trait | Value | Temp | Life stage |
|---|---|---|---|---|---|
| `measurement_023773` | *Leiopotherapon unicolor* | Metabolic rate | **117.0 mgO2/h/kgFM** | 21.5 °C (Warm) | juvenile |
| `measurement_023776` | *Leiopotherapon unicolor* | Metabolic rate | 110.0 mgO2/h/kgFM | 21.5 °C (Warm) | juvenile |
| `measurement_023829` | *Leiopotherapon unicolor* | Metabolic rate | 751.4 mgO2/h/kgFM | 21.5 °C (Warm) | juvenile |
| `measurement_000001` | *Aphidius platensis* | Development | 39 days | < 15 °C (Cold) | *not in KG* |
| `measurement_003743` | *Rana temporaria* | Development | 35 days | 15–25 °C (Warm) | *not in KG* |
| `measurement_004493` | *Drosophila melanogaster* | Development | 16 days | 15–25 °C (Warm) | *not in KG* |

**Steps:**

1. Open the data sample `sharetrait-data-sample.ttl` and copy its contents.
2. Paste at the end of your `sharetrait-ontology-starter.ttl`. Both files share the same namespace.
3. Re-open the combined file in Protégé: **File > Open**.
4. **Reasoner > HermiT > Start reasoner**.
5. Select `measurement_023773` and check **Inferred Types** in the Description panel.

The sample was extracted from the full ShareTrait knowledge graph with a SPARQL `CONSTRUCT` query (`extract-data-sample.sparql`). Temperatures are mapped to value partitions (< 15 °C = `Cold`, 15–25 °C = `Warm`, ≥ 25 °C = `Hot`); life-stage strings to `juvenile1` / `adult1` / `larva1` when present; organism individuals are typed by genus. Each measurement is typed **only** as `:TraitMeasurement` - every other class membership comes from the reasoner.

Save: **File > Save**.

---

## Plenary B - what the reasoner inferred (10 min)

Review the inferred-types results together:

- **measurement_023773 (hero)**: `AquaticTraitMeasurement`, `JuvenileFishMeasurement`, `RespirometryMeasurement`
- **measurement_023776**: same three classes - control replicate
- **measurement_023829**: same three classes - the *category* is identical, but the raw trait value (751.4 vs 117.0) reveals the biological story: nitrate stress at 100 mg/L elevates the standard metabolic rate by ~6.4×
- **measurement_000001**: `InsectTraitMeasurement`, `ColdExposureMeasurement`
- **measurement_004493**: `InsectTraitMeasurement`
- **measurement_003743**: no additional type. Amphibians have no realm restriction, warm is not cold, not an insect, not a fish. Open-world assumption in action.

```
6 measurements, 12 inferred classifications, 0 manual labels
```

Note that `SpangledPerchRespirometryStudy` is *not* inferred for the individuals: it is a `SubClassOf` description (Step 7), not a defined class (Step 8), so the reasoner only places it in the **class hierarchy** under `AquaticTraitMeasurement`/`JuvenileFishMeasurement`/`RespirometryMeasurement` - not the individuals into it. Convert it to `EquivalentTo` if you want individuals classified automatically.

### Did we answer the research question?

Recall the research question from the top of the tutorial: *how does SMR scale with body mass in freshwater fish at ~21 °C, and does nitrate stress shift that scaling?* Be explicit with the group:

- **Answered - the retrieval problem.** From raw triples typed only as `:TraitMeasurement`, the reasoner identifies the 3 perch records as `JuvenileFishMeasurement ⊓ AquaticTraitMeasurement ⊓ RespirometryMeasurement`. A DL Query for that expression returns exactly the candidate rows for a scaling analysis. The nitrate contrast (117 vs 751) is visible in `hasTraitValue`.
- **Not answered - the analytical question itself.** Three perch records are not a scaling curve; one shifted mean is not a shifted scaling exponent. That regression runs *outside* Protégé, on the assembled dataset.
- **The punchline.** Ontologies don't run regressions - they make sure you can find every input row you need across studies, units, and naming conventions, so the regression is possible at all. That is what ShareTrait + this ontology buys you.

This scales to the full knowledge graph. The ShareTrait KG lives in [QLever](https://github.com/ad-freiburg/qlever) for SPARQL querying. QLever itself does not do OWL reasoning. You run the reasoner in Protégé first, export the inferred triples, and then load everything into QLever for querying.

---

## Part 5: What Comes Next + Q&A (10 min)

Now that you know how to build an ontology from scratch, you know how to read and reuse one. Reuse is almost always the better choice.

### Replace, don't rebuild - trait qualities with PATO

Some of the trait classes we built today already exist in [PATO](http://purl.obolibrary.org/obo/pato.owl) (Phenotype And Trait Ontology):

| Our class | PATO term | URI | Notes |
|---|---|---|---|
| `FecundityTrait` | "fecundity" | `PATO:0000273` | Exact match |
| `MetabolicRateTrait` | "rate" | `PATO:0000161` | Too broad (PATO defines rate as "occurrence per unit time" in general) |
| `DevelopmentTrait` | - | - | No direct PATO term; development time combines a process with a duration |

PATO is an actively maintained OBO Foundry ontology and remains the standard vocabulary for phenotypic *qualities* - rate, mass, length, viability, motility. It is used by HPO, Monarch, and most cross-species phenotype work. The limit is exactly that: PATO models qualities, not whole trait *types*. Compound traits like "development time" or "sperm progressive motility percentage" usually need a PATO quality combined with a process or anatomy term, or a local class linked to PATO via `skos:closeMatch`.

In practice, you use the external URI directly instead of inventing your own. For example, instead of defining a local `FecundityTrait` class, you use `http://purl.obolibrary.org/obo/PATO_0000273` in your data and restrictions. No need to import the entire PATO ontology.

### A note on body size

The research question at the top of the tutorial asks how metabolic rate scales with body mass - and the ShareTrait KG of course carries body mass for the perch records. We left it out of *this* tutorial on purpose: keeping the modelled subset tight on Measurement → Trait → Organism makes the reasoning story crisper in two hours. Tidying up the body-size representation (its own `BodySizeMeasurement` linked to the organism, units from OM/QUDT, quality from PATO) is on the roadmap for a follow-up session.

### Other relevant OWL ontologies

PATO is one piece. A trait record also has a species, an anatomy, an environment, an experimental condition, a life stage, and a unit - each with a mature OWL ontology worth knowing about:

| Slot | Ontology | What it gives you |
|---|---|---|
| Taxonomy | **NCBITaxon** | OWL serialisation of NCBI Taxonomy; reasoner can walk species → genus → family |
| Anatomy | **UBERON** | Cross-species anatomy, includes invertebrates |
| Habitat / environment | **ENVO** | Biome and environmental-material terms (freshwater, marine, terrestrial, …) |
| Experimental conditions | **ECTO** | Treatments and exposures (temperature regimes, chemical stressors); built on ENVO + PATO |
| Life stage | **Uberon life-stages** | Generic life-cycle plus species-specific stage ontologies |
| Units | **OM** (Ontology of Units of Measure) | OWL 2, SI plus domain units, supports unit conversion |
| Vertebrate traits | **VT** (Vertebrate Trait Ontology) | Mature trait ontology - but **vertebrate-only**; invertebrates still need local terms or PATO combinations |
| Observation framework | **OBOE** (Extensible Observation Ontology) | OWL pattern for `Observation → Measurement → Entity / Characteristic / Standard / Protocol` - the same shape we built today around `TraitMeasurement` |

All eight are OWL, all are looked up the same way:
- [OBO Foundry](http://obofoundry.org/) for the bio-ontologies
- [Ontology Lookup Service (OLS)](https://www.ebi.ac.uk/ols4/) to search individual terms
- [OM browser](http://www.ontology-of-units-of-measure.org/) for units
- [OBOE on GitHub](https://github.com/NCEAS/oboe) / [BioPortal entry](https://bioportal.bioontology.org/ontologies/OBOE) for the observation framework

A note on OBOE specifically: unlike PATO/UBERON/ENVO it is a *structural* pattern, not a term list. Aligning ShareTrait's `TraitMeasurement` with OBOE's `Measurement`, our `Organism` with OBOE's `Entity`, and our `TraitType` with OBOE's `Characteristic` would let other ecological datasets annotated with OBOE (e.g. via DataONE) interoperate with ShareTrait without per-database re-mapping. Last release is 2019 - stable rather than rapidly evolving, which suits our purpose. It is on the roadmap for a follow-up modelling session alongside the body-size cleanup.

Not every external resource is an OWL ontology - taxonomic checklists, gazetteers, and identifier registries (ORCID, ROR, GeoNames, Catalogue of Life) are valuable for linking but cannot be reasoned over the way the eight above can.

### The pipeline

The full pipeline from CSV to queryable knowledge graph is documented in the [sharetrait-kg README](../README.md).

```
Spreadsheet / Database
        |
        v
   RML Mapping            (rows → RDF triples)
        |
        v
   Knowledge Graph        (RDF with external ontology URIs)
        |
        v
   Reasoning              (HermiT / Pellet in Protégé)
        |
        v
   SPARQL querying        (QLever)
```

Reasoning runs in **Protégé**; QLever stores and queries but does no OWL reasoning. Export inferred triples from Protégé, then load into QLever.

| Step | Tool |
|---|---|
| Mapping | [RML.io](https://rml.io/) / [YARRRML](https://rml.io/yarrrml/) |
| Reasoning | HermiT / Pellet (in Protégé) |
| Storing and querying | [QLever](https://github.com/ad-freiburg/qlever) |

You do not need to become an ontology engineer. The skills from this tutorial - and the spangled perch record you walked through - are exactly what you need to read, evaluate, and reuse the ontologies that already exist.
