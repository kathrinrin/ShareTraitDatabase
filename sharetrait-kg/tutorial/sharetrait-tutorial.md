# Building a Traits Ontology: Hands-on Tutorial

> **Duration:** 2 hours (intro, ShareTrait, two hands-on blocks with plenaries, break, wrap-up)
> **Tool:** [Protégé Desktop](https://protege.stanford.edu/) (version 5.x)
> **Prerequisites:** Protégé and Java pre-installed and confirmed working before the session - see `setup-before-tutorial.md`. Bring [`sharetrait-ontology-starter.ttl`](https://drive.google.com/file/d/1WkcXIMcByDiiOgf3DRTLEilGZj4P6FHO/view?usp=sharing) opening cleanly in Protégé.
> **Result:** A small OWL ontology that automatically classifies trait measurements using real ShareTrait data - with one juvenile spangled perch as the worked example

The starter file `sharetrait-ontology-starter.ttl` is *almost* complete. The live session unfolds in 11 short steps:

- **Steps 1–5** — in each of these the starter is missing exactly one element of one modelling layer (one class, one disjoint axiom, one covering axiom, one object property, one data property). Participants add the missing element themselves to see how each layer is created in Protégé.
- **Steps 6–8** — participants add new axioms on top of the completed starter: a property restriction on `Fish` (Step 6), a closure axiom on `MetabolicRateRespirometryStudy` (Step 7), and one defined class (Step 8). For Step 7, two `some` axioms are already pre-filled on the class; participants add only the `only` closure axiom on top. For Step 8, three of the four defined classes are already in the starter as reference patterns; participants inspect those and build only the fourth (`RespirometryMeasurement`).
- **Steps 9–11** — participants start the reasoner, load real ShareTrait data, and look at the inferred types. A DL Query exercise is included in the Optional extra at the end for those who finish early or want to return to the material later.

The tutorial text below walks through every step in detail so it can also be used to rebuild the ontology from scratch later.

---

## Running order (120 min)

| Time | Block | Mode |
|---|---|---|
| 0:00–0:10 | Part 1 - Intro to ontologies | demo |
| 0:10–0:20 | Part 2 - ShareTrait introduction | presentation |
| 0:20–0:50 | Part 3 - Hands-on Block A (Steps 1–8): build the ontology | hands-on |
| 0:50–1:00 | Plenary A - build checkpoint (no reasoner yet) | discussion |
| 1:00–1:10 | Break | - |
| 1:10–1:40 | Part 4 - Hands-on Block B (Steps 9–11): run the reasoner, load real data, inspect inferred types | hands-on + demo |
| 1:40–1:50 | Plenary B - what the reasoner inferred | discussion |
| 1:50–2:00 | Part 5 - Reuse, what comes next, Q&A | discussion |

Work in **pairs**. Save as you go. Block A is pure modelling - we keep the reasoner *off* until after the break so all reasoning runs together in Block B. One short hands-on exercise (the probe classes from the original Step 9) is kept as an **optional extra** at the very end of this document - skip during the live session, return to it afterwards if you want to.

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

Why this record? It is biologically rich (a real ectotherm under controlled conditions, with a clearly documented method), it has all the contextual fields we want to model (species, life stage, temperature, value), and we have two more records from the same study to use as comparators. By the end of the tutorial, the OWL reasoner will be classifying this measurement automatically into two inferred categories (`JuvenileFishMeasurement`, `RespirometryMeasurement`) without us having to label it manually.

---

## Part 1: Quick Introduction (10 min)

An ontology is a **formal, shared vocabulary** where the computer understands how terms relate and can check your data for mistakes.

| Plain language | OWL term | Example from our tutorial |
|---|---|---|
| A category | **Class** | `Organism`, `Fish`, `SpangledPerch`, `MetabolicRateTrait`, `Respirometer` |
| A relationship | **Property** | `measuredOnOrganism`, `hasLifeStage`, `usedInstrument` |
| A concrete thing | **Individual** | `organism_023773`, `respirometer_001585` |
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
| **Individual** | A concrete thing | `organism_023773`, `measurement_023773` |
| **Axiom** | A logical statement the reasoner can use | "every `Fish` lives in an `Aquatic` realm" |
| *Class axioms* | | |
| **SubClassOf** (⊑) | "Is-a"; *necessary* condition. Members must satisfy it, but satisfying it does not make you a member | `SpangledPerch ⊑ Fish` |
| **EquivalentTo** (≡) | Necessary *and sufficient*; defined class; anything matching is automatically classified | `JuvenileFishMeasurement ≡ TraitMeasurement and (measuredOnOrganism some Fish) and (hasLifeStage some Juvenile)` |
| **Disjoint Classes** | "These classes can never overlap" | `Insect`, `Amphibian`, `Fish` are pairwise disjoint |
| **Covering axiom** | "These subclasses are the only options"; `EquivalentTo` a disjunction of the subclasses | `LifeStage ≡ Juvenile or Adult or Embryo` |
| **`owl:Nothing`** (empty class, ⊥) | The class with no members; any class proven equivalent to it is **unsatisfiable** (the reasoner flags it red) | `InconsistentDevelopmentMetabolism` collapses to `owl:Nothing` because it inherits from two disjoint trait types |
| *Logical connectives* | | |
| **Conjunction** (`and`, ⊓) | Both classes apply | `Fish and (hasRealm some Aquatic)` |
| **Disjunction** (`or`, ⊔) | At least one of the classes applies | `Juvenile or Adult or Embryo` |
| *Property restrictions (quantifiers)* | | |
| **Existential restriction** (`some`, ∃) | "At least one value of this kind exists" | `Fish ⊑ hasRealm some Aquatic` |
| **Universal restriction** (`only`, ∀) | "For all values of this property, the value must be of this kind"; a **closure axiom** | `MetabolicRateRespirometryStudy ⊑ measuresTraitType only MetabolicRateTrait` |
| *Property characteristics* | | |
| **Functional** property | "At most one value" | `measuredOnOrganism`: one measurement, one organism |
| **Transitive** property | If `a R b` and `b R c`, then `a R c` | Not used in this tutorial; a classic example is `partOf`: if a fin is part of a perch and the perch is part of a population, the fin is part of the population |
| **Inverse Of** | Two properties pointing opposite ways; state once, reasoner derives both | `measuredOnOrganism` / `isOrganismOf` |
| *Reasoner concepts* | | |
| **Realisation** (instance classification) | Reasoner inferring which classes each individual belongs to, based on the individual's asserted facts and the class axioms | `measurement_023773` → `JuvenileFishMeasurement`, `RespirometryMeasurement` |
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

**The pedagogical pattern for the rest of the tutorial.** The starter is *almost* complete: in each of Steps 1–5 exactly **one** real element of that modelling layer (one class, one disjoint axiom, one covering axiom, one object property, one data property) has been left out for you to create. You learn how to create one real, meaningful element of each kind yourself, while the facilitator demonstrates the same action on screen. Steps 6–8 then build new axioms (a realm restriction on `Fish`, a closure axiom on `MetabolicRateRespirometryStudy`, and one defined class - the other three are pre-filled in the starter as reference patterns) on top of the completed starter. The reasoner stays off throughout Block A - we want all reasoning to happen together in Block B, after the break, when the model is complete. By the end of Block A your file is the full base ontology - 31 classes, 11 object properties, 2 data properties - built with your own hands.

Save as you go: **File > Save**.

> The eight Block A sub-steps and the three Block B sub-steps in this tutorial are deliberately bite-sized - each one targets exactly one OWL concept (class, disjoint, covering, property, restriction, closure, defined class, then reasoner / data / inferred types). The facilitator demonstrates the same action on screen, so you can still see how it is done even if you fall behind.

---

### Step 1 [hands-on]: Add one class - `SpangledPerch` (2 min)

The starter contains 29 classes; the hero species class is missing. You add it.

1. In the **Classes** tab, expand `owl:Thing > Organism > Fish`.
2. Right-click `Fish` and choose **Add subclass**.
3. Name it `SpangledPerch`.

The full class tree once you are done (30 classes):

```
owl:Thing
├── TraitMeasurement
│   ├── AphidiusDevelopmentStudy
│   ├── ColdExposureMeasurement          (defined, pre-filled - inspected in Step 8)
│   ├── InsectTraitMeasurement           (defined, pre-filled - inspected in Step 8)
│   ├── JuvenileFishMeasurement          (defined, pre-filled - inspected in Step 8)
│   └── MetabolicRateRespirometryStudy
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
    └── Embryo
```

That is 30 classes after Step 1 (the 29 in the starter plus `SpangledPerch`). One more (`RespirometryMeasurement`) is added in Step 8, bringing the total at the end of Block A to 31. The two probe classes in the Optional Extra would bring it to 33.

> **Why `SpangledPerch` as its own class?** Species-level facts (conservation status, native range, external Wikidata URI) attach in one place instead of being repeated on every individual fish.

> **Why `MetabolicRateRespirometryStudy` (a study-shaped class)?** It is described by the trait type and the instrument it must have - exactly the pattern we will exercise in Step 7.

> **Why `LifeStage` as a value partition?** It is a small closed set (embryo / juvenile / adult) - the textbook use case for value partitions.

> **Why an `Instrument` class?** Lifting the respirometer from a free-text column to a first-class entity lets the reasoner answer "every metabolic-rate record acquired with a respirometer" with one query.

> **On naming.** `Fish`, `Insect`, `Amphibian`, `FruitFly`, `ParasitoidWasp`, and `SpangledPerch` are vernacular labels chosen so the OWL mechanics stay visible in two hours. In production you replace them with NCBITaxon URIs - see Part 5.

---

### Step 2 [hands-on]: Add one disjoint-class axiom - Insect / Amphibian / Fish (2 min)

Disjoint means "these classes can never overlap." The starter declares disjointness for every sibling group *except* the three organism kinds - you add that one.

1. Select `Insect`.
2. In the **Description** panel, click **+** next to **Disjoint With**.
3. Add `Amphibian` and `Fish`.

Protégé propagates the symmetric axiom - you only need to state it once. The probe class in the Optional Extra at the end of this document demonstrates what disjoint axioms catch.

The full set of disjoint axioms in your file is now:

| Parent | Disjoint siblings |
|---|---|
| `owl:Thing` | `TraitMeasurement`, `TraitType`, `Organism`, `Instrument` |
| `TraitType` | `DevelopmentTrait`, `FecundityTrait`, `MetabolicRateTrait` |
| **`Organism`** | **`Insect`, `Amphibian`, `Fish`** ← you add this |
| `Insect` | `ParasitoidWasp`, `FruitFly` |
| `TemperatureRange` | `Cold`, `Warm`, `Hot` |
| `Realm` | `Terrestrial`, `Aquatic` |
| `LifeStage` | `Juvenile`, `Adult`, `Embryo` |
| `TraitMeasurement` | `AphidiusDevelopmentStudy`, `MetabolicRateRespirometryStudy` |

---

### Step 3 [hands-on]: Add one covering axiom - `LifeStage` (2 min)

A covering axiom says "these subclasses are the only options." It is your first use of **`EquivalentTo`** — here in its *enumerative* form: `LifeStage` is *exactly* the union of these three named subclasses. Step 8 will use the same operator differently — to *define* a class by a restriction. The starter declares covering for `TemperatureRange` and `Realm` - you add it for `LifeStage`.

1. Select `LifeStage`.
2. In the **Description** panel, click **+** next to **Equivalent To**.
3. Enter: `Juvenile or Adult or Embryo`.

Your file now has all three covering axioms:

- `TemperatureRange`: `Cold or Warm or Hot`
- `Realm`: `Terrestrial or Aquatic`
- **`LifeStage`: `Juvenile or Adult or Embryo`** ← you add this

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

Switch to the **Data Properties** tab. One data property is pre-loaded (`hasTraitValue`, range `xsd:decimal`). You add the second, which will carry the species label on each organism individual once the real ShareTrait data is loaded in Block B.

1. Right-click `owl:topDataProperty` > **Add sub property** → name it `hasScientificName`.
2. In the Description panel:
   - **Domains** → `Organism`
   - **Ranges** → `xsd:string`

Your file now has both data properties:

| Property | Domain | Range |
|---|---|---|
| `hasTraitValue` | `TraitMeasurement` | `xsd:decimal` |
| **`hasScientificName`** | **`Organism`** | **`xsd:string`** ← you add this |

Only two data properties - we keep the tutorial focused on the Measurement → Trait → Organism story. 

---

### Steps 6–8 — read this first (2 min)

In Steps 6–8 you constrain classes by attaching **class expressions** built from the properties declared in Steps 4–5. Each expression you write in these steps combines one property restriction (table 1) with one axiom type (table 2). Keep both tables visible until the end of Step 8.

**1. Property restriction.** A property restriction describes class members in terms of one of their properties: *which* values are required (`some`), or *which* are the only ones allowed (`only`).

| Manchester syntax | OWL construct | Reads as |
|---|---|---|
| `hasRealm some Aquatic` | `owl:someValuesFrom` | Each member is connected via `hasRealm` to at least one individual of class `Aquatic` |
| `measuresTraitType only MetabolicRateTrait` | `owl:allValuesFrom` | For each member, *every* `measuresTraitType` value must be a `MetabolicRateTrait` — no other trait type allowed (*closure axiom*) |

**2. Axiom type.** Whatever expression you write, you still have to tell Protégé *how* it attaches to the class: as a one-way necessary condition (`SubClassOf`) or as a two-way definition (`EquivalentTo`). Only the latter triggers automatic classification.

| Manchester syntax | OWL construct | Meaning |
|---|---|---|
| `SubClassOf` | `rdfs:subClassOf` | *Necessary*: every instance of the class is also an instance of the expression — but not vice versa (*primitive class*) |
| `EquivalentTo` | `owl:equivalentClass` | *Necessary and sufficient*: the class and the expression have precisely the same instances, so the reasoner **automatically classifies** any matching individual into the class (*defined class*) |

---

### Step 6 [hands-on]: A realm restriction on `Fish` (3 min)

**What and why.** Step 6 attaches the first **property restriction** to a class - stated once on `Fish`, it holds for every current and future fish. Read `hasRealm some Aquatic` as: "every individual in this class is related via `hasRealm` to at least one individual of class `Aquatic`". Attached as `SubClassOf` it is a *necessary* condition: being a `Fish` implies having an aquatic realm, but having an aquatic realm does not by itself make you a fish.

**Your turn.** Back in the **Classes** tab, select `Fish`. Click **+** next to **SubClass Of** and enter: `hasRealm some Aquatic`.

**Why only `Fish`?** We deliberately leave `Insect` and `Amphibian` unrestricted. Some insects are aquatic (diving beetles, mayfly nymphs) and frogs live in water *and* on land, so neither `Aquatic` nor `Terrestrial` alone is a necessary condition for those classes. Under the Open World Assumption the reasoner will not invent a realm for them; absence of the axiom correctly expresses "varies / unknown". `Fish`, on the other hand, are uniformly aquatic in our scope - so the restriction is biologically safe.

---

### Step 7 [hands-on]: A closure axiom on `MetabolicRateRespirometryStudy` (3 min)

**What and why.** `MetabolicRateRespirometryStudy` already carries two `some` axioms in the starter — the same `some` + `SubClassOf` shape you just used on `Fish`:

```
measuresTraitType   some MetabolicRateTrait
usedInstrument      some Respirometer
```

Together they read: "every member of this class measures *at least one* metabolic-rate trait *and* uses *at least one* respirometer." Step 7 adds the genuinely new bit: an `only` axiom that *closes* the description.

**Your turn.** In the **Classes** tab, select `MetabolicRateRespirometryStudy`. Click **+** next to **SubClass Of** and add:

```
measuresTraitType   only MetabolicRateTrait
```

Read this as: "*for all* values of `measuresTraitType` on this study, the value must be a `MetabolicRateTrait` - no other trait type is allowed here."

**Why pair `some` with `only` on the same property?** `some` says *something is there*; `only` says *nothing else is there*. Together they pin the property down: at least one metabolic-rate trait, and *only* metabolic-rate traits. Without the `only` axiom, the Open World Assumption lets the reasoner imagine extra values you never mentioned - which could later mis-classify the study.

`AphidiusDevelopmentStudy` (pre-filled in the starter) follows the same pattern, with a temperature and an organism `some` axiom added so the reasoner has more to chew on in Step 9:

```
measuresTraitType   some DevelopmentTrait
measuredOnOrganism  some ParasitoidWasp
hasTemperatureRange some Cold
measuresTraitType   only DevelopmentTrait
```

All four axioms here are `SubClassOf` (necessary), not `EquivalentTo` (necessary *and* sufficient) - the difference is the topic of Step 8.

---

### Step 8 [hands-on]: Defined classes - `EquivalentTo` (5 min)

Step 8 reuses the same `some` restrictions from Steps 6–7, but attaches them as `EquivalentTo` instead of `SubClassOf` (table 2 in the intro above) — turning those classes into *defined* classes that the reasoner can auto-classify. You already met `EquivalentTo` in Step 3, where it *enumerated* `LifeStage` as the union of three named subclasses; here it does something different — it *defines* a class by a restriction, and that is what lets the reasoner auto-classify individuals into it.

#### Inspect three pre-filled defined classes

Under `TraitMeasurement` in the **Classes** tab, click each of these and read its **Equivalent To**. From simplest to most complex:

**ColdExposureMeasurement** — one conjunct:
```
TraitMeasurement and (hasTemperatureRange some Cold)
```
Read this as: "a `ColdExposureMeasurement` is *exactly* any `TraitMeasurement` whose temperature range is `Cold`" — the `EquivalentTo` makes it a two-way definition, so the reasoner will automatically classify any matching individual into this class.

**InsectTraitMeasurement** — one conjunct, but the reasoner will use subsumption (`ParasitoidWasp` and `FruitFly` are both subclasses of `Insect`) to also classify wasps and fruit flies:
```
TraitMeasurement and (measuredOnOrganism some Insect)
```

**JuvenileFishMeasurement** — two conjuncts joined by `and`; this is the one that will automatically pick up the spangled-perch records in Step 11:
```
TraitMeasurement and (measuredOnOrganism some Fish) and (hasLifeStage some Juvenile)
```

#### Your turn — build the fourth defined class

Right-click `TraitMeasurement` > **Add subclass**, name it `RespirometryMeasurement`, then click **+** next to **Equivalent To** and enter:

```
TraitMeasurement and (usedInstrument some Respirometer)
```

Read this as: "a `RespirometryMeasurement` is *exactly* any `TraitMeasurement` that uses some `Respirometer` as its instrument" — same `EquivalentTo` shape as the three pre-filled definitions you just inspected, but on `usedInstrument`, so any individual that uses a respirometer will be automatically classified into this class in Block B.

Save the file. The reasoner stays off for now - we start it together in Block B.

---

## Plenary A - build checkpoint after Step 8 (10 min)

A quick consolidation before the break. The reasoner is still off - that is deliberate. Block A is pure modelling; Block B is where the reasoner runs.

### What you have in your file now

- 31 classes, 11 object properties, 2 data properties (33 classes if you also added the two probes in the Optional Extra)
- One new disjoint-class axiom (Insect / Amphibian / Fish), on top of the ones already pre-loaded
- A covering axiom on `LifeStage` (Juvenile / Adult / Embryo)
- A realm restriction on `Fish` (`hasRealm some Aquatic`)
- A closure axiom on `MetabolicRateRespirometryStudy` (`measuresTraitType only MetabolicRateTrait`) on top of the two `some` axioms pre-filled in the starter
- Four defined classes under `TraitMeasurement` (three pre-filled, one of them yours: `RespirometryMeasurement`)

### Discuss as a group

- `SubClassOf` vs `EquivalentTo`: only one of them triggers automatic classification by the reasoner. Which one, and why? (Hint: `EquivalentTo` says "necessary *and* sufficient" - tick the boxes and you are in.)
- The closure axiom (`measuresTraitType only MetabolicRateTrait`) on `MetabolicRateRespirometryStudy` does not affect the reasoner's classification of *today's* data. So why is it there? (Answer: without it, the reasoner is free to *imagine* extra trait values the study did not mention, which could mis-classify it later. Closure says "what you see is all there is".)
- Why did we put `hasRealm some Aquatic` on `Fish` but not on `Insect` or `Amphibian`?
- Anyone stuck or red-flagged in their file - fix together so Block B starts clean.

Save: **File > Save**.

---

## Break (10 min)

---

## Part 4: Hands-on in Protégé - Block B (30 min)

In Block B you start the reasoner for the first time, watch it classify your hand-built classes, then load six real ShareTrait measurements and watch it classify those individuals too. Three short steps - all reasoning lives here. A DL Query exercise is in the Optional extra at the end for participants who want to slice the inferred data themselves.

---

### Step 9 [hands-on]: Start the reasoner - class-hierarchy inferences (10 min)

Start the reasoner together: **Reasoner > HermiT** (if it is not already ticked), then **Reasoner > Start reasoner**. Switch the class hierarchy panel to the **Inferred** view (top-left dropdown).

#### What the reasoner does

Every time you start or synchronise the reasoner, HermiT runs two jobs (a third one - realisation - kicks in once we add individuals in Step 11):

1. **Consistency check** - is the ontology free of contradictions? If you had accidentally said e.g. `Fish SubClassOf Insect`, the reasoner would flag it now. A clean ontology silently passes.
2. **Subsumption / classification** - for every pair of classes, is one a subclass of the other? This is what builds the **Inferred** class hierarchy you are about to look at.

#### What you should see

Under `TraitMeasurement` the inferred tree now looks roughly like this:

```
TraitMeasurement
├── ColdExposureMeasurement
│   └── AphidiusDevelopmentStudy
├── InsectTraitMeasurement
│   └── AphidiusDevelopmentStudy
├── JuvenileFishMeasurement
└── RespirometryMeasurement
    └── MetabolicRateRespirometryStudy
```

You did not type a single one of these `is-a` links. The reasoner inferred them all.

#### How the reasoner figured this out

Think of it as the reasoner asking, for each named study class, *"does this study's description tick all the boxes of some defined class?"* It only uses what you already told it.

**Why `MetabolicRateRespirometryStudy` is a `RespirometryMeasurement`.** The defined class says: a respirometry measurement is *any trait measurement that used a respirometer*. The reasoner checks the perch study:

- Is it a `TraitMeasurement`? Yes (you asserted that as the parent class).
- Does it use a respirometer? Yes — `usedInstrument some Respirometer` is one of the two `some` axioms pre-filled on `MetabolicRateRespirometryStudy` in the starter.

Both boxes ticked, so the reasoner classifies it as a `RespirometryMeasurement`. The closure axiom you added in Step 7 does not generate a new classification here, but it locks the description down so the reasoner cannot imagine extra trait types later.

**Why `AphidiusDevelopmentStudy` lands in both `ColdExposureMeasurement` and `InsectTraitMeasurement`.** Same recipe. The starter says aphidius studies are on `ParasitoidWasp` (which is an `Insect`) and are at `Cold` temperature, so they tick the boxes of both defined classes. Note that the reasoner used subsumption here: you said `measuredOnOrganism some ParasitoidWasp`, and `ParasitoidWasp` is a subclass of `Insect`, so the `InsectTraitMeasurement` definition (`measuredOnOrganism some Insect`) is satisfied.

**Why `JuvenileFishMeasurement` is empty so far.** Its definition needs `measuredOnOrganism some Fish` *and* `hasLifeStage some Juvenile`. Neither named study class asserts both, so neither falls under it at the class level. Step 11 will fill it - with *individuals* from the real data.

#### The key lesson

You wrote *descriptions* of two studies (`SubClassOf`, Steps 6–7) and *definitions* of four categories (`EquivalentTo`, Step 8). The reasoner did the matching - and crucially, only the `EquivalentTo` axioms triggered classifications. That is the two-axis table from the start of Step 6 in action: `SubClassOf` axioms constrain, `EquivalentTo` axioms classify.

---

### Step 10 [hands-on]: Load the real ShareTrait data (5 min)

Now we load six real ShareTrait measurements on top of the ontology you just built. The hero is still `TRAMEA023773`. The facilitator drives the data-load from the front; participants follow on their own laptops.

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

1. Make sure [`sharetrait-data-sample.ttl`](https://drive.google.com/file/d/1pkrQaAREdA4o1i6S00DFtho9h5CxiUxB/view?usp=sharing) sits in the **same folder** as your starter file (Protégé resolves local imports by relative path).
2. In Protégé, with your ontology still open, open the **Active ontology** tab and find the **Ontology imports** section (lower half of the tab). Next to **Direct Imports**, click the **+** button.
3. In the wizard, choose **Import an ontology contained in a specific file**, browse to `sharetrait-data-sample.ttl`, then click through with the defaults. Protégé adds one `owl:imports` axiom and pulls in the six measurements, four organisms, six closed-set individuals (`cold1`/`warm1`/`hot1`, `juvenile1`/`adult1`/`embryo1`) and one respirometer. The data appears under the same `:` namespace, so the imported individuals link straight into the classes you built.
4. Confirm the import worked: switch to the **Individuals** tab - the six measurements appear with their human-friendly labels (`TRAMEA023773 (hero record)`, `TRAMEA023776 (control replicate)`, ...). You should also see `organism_023773`, `respirometer_001585` and the six closed-set individuals. If they are missing, return to **Active ontology > Ontology imports** and re-add the file.

Save: **File > Save**. The import axiom is now part of your file - re-opening it later will pull the data back in automatically.

The sample was extracted from the full ShareTrait knowledge graph with a SPARQL `CONSTRUCT` query (`extract-data-sample.sparql`). Temperatures are mapped to the `TemperatureRange` individuals (< 15 °C = `cold1`, 15–25 °C = `warm1`, ≥ 25 °C = `hot1`); life-stage strings to `juvenile1` / `adult1` / `embryo1` when present (the source string `"larva"` is left unmapped, since the tutorial ontology models three stages); organism individuals are typed by genus (`SpangledPerch`, `ParasitoidWasp`, `Amphibian`, `FruitFly`) and carry `hasScientificName`. Each measurement is typed **only** as `:TraitMeasurement` - every other class membership comes from the reasoner.

> **A note on naming.** The measurement IRIs are `measurement_023773` etc., but each one carries an `rdfs:label` like `"TRAMEA023773 (hero record)"`. Protégé renders entities by their label when one is available, so the Individuals panel shows the label form. The two refer to the same individual.

Save: **File > Save**.

---

### Step 11 [hands-on]: Re-run the reasoner - inferred types on individuals (10 min)

With the data loaded, run the reasoner again: **Reasoner > Start reasoner** (or **Synchronise reasoner** if it is still running). On top of the consistency check and class-hierarchy classification from Step 9, the reasoner now performs a third job:

3. **Realisation** (instance classification) - for each individual, which classes does it belong to?

The class hierarchy itself does not change - the data adds no new axioms about classes. What is new is that every individual now gets placed into every class whose conditions it satisfies.

**Click-by-click:**

1. Open the **Individuals by class** tab (Window > Tabs > Individuals by class if it is hidden). In the bottom-left **Direct instances** panel, make sure the small toggle is set to show **inferred** instances.
2. In the class hierarchy on the left, click `TraitMeasurement`. The Direct instances panel lists the six measurements.
3. Click `TRAMEA023773 (hero record)`. Look at the **Description** panel (middle): the **Types** box now shows
   - `TraitMeasurement` (white background = asserted)
   - `JuvenileFishMeasurement` (yellow = inferred)
   - `RespirometryMeasurement` (yellow = inferred)
4. Look at the **Property assertions** panel (right). The asserted assertions (`hasLifeStage juvenile1`, `measuredOnOrganism organism_023773`, `usedInstrument ...`, etc.) are white. Below them, yellow lines show inferred property assertions such as `hasComponent organism_023773` and `hasComponent MetabolicRateTrait` - those come from the inverse properties `isOrganismOf` / `isComponentOf` declared in the starter.

**Now check the organism:**

5. In the Property assertions panel, double-click `organism_023773` (the value of `measuredOnOrganism`). The Individuals panel jumps to it.
6. Its **Types** box shows only `SpangledPerch` (asserted). No yellow entries - the inferred parents (`Fish`, `Organism`) are superclasses Protégé hides as redundant ancestors. The class hierarchy on the left (set to **Inferred**) shows the chain `Organism > Fish > SpangledPerch` - that is the inference, made visible there instead of here.
7. The yellow entries to notice on the organism are in the **Property assertions** panel: `isComponentOf TRAMEA023773` and `isOrganismOf TRAMEA023773` - inferred via the inverse-property declarations.

Save: **File > Save**.

---

## Plenary B - what the reasoner inferred (10 min)

Review the inferred-types results together:

- **measurement_023773 (hero)**: `JuvenileFishMeasurement`, `RespirometryMeasurement`
- **measurement_023776**: same two classes - control replicate
- **measurement_023829**: same two classes - the *category* is identical, but the raw trait value (751.4 vs 117.0) shows the effect of treatment: nitrate stress at 100 mg/L elevates the standard metabolic rate by ~6.4×
- **measurement_000001**: `InsectTraitMeasurement`, `ColdExposureMeasurement`
- **measurement_004493**: `InsectTraitMeasurement`
- **measurement_003743**: no additional type. Amphibians have no realm restriction, warm is not cold, not an insect, not a fish. Open-world assumption in action.

```
6 measurements, 9 inferred classifications, 0 manual labels
```

Note that `MetabolicRateRespirometryStudy` is *not* inferred for the individuals: it is a `SubClassOf` description (Step 7), not a defined class (Step 8), so the reasoner only places it in the **class hierarchy** under `RespirometryMeasurement` - not the individuals into it. Convert it to `EquivalentTo` if you want individuals classified automatically. That is the two-axis lesson once more: `SubClassOf` constrains, `EquivalentTo` classifies.

### Did we answer the research question?

Recall the research question from the top of the tutorial: *how does SMR scale with body mass in freshwater fish at ~21 °C, and does nitrate stress shift that scaling?* Be explicit with the group:

- **Answered - the retrieval problem.** From raw triples typed only as `:TraitMeasurement`, the reasoner derives that the 3 perch records are `RespirometryMeasurement` (because each has `usedInstrument some Respirometer` and that matches the `EquivalentTo` definition you wrote in Step 8) and that their organism is a `Fish` (because `SpangledPerch` is a subclass of `Fish`). In the **Individuals by class** view (Step 11) they appear under both classes; the optional DL Query exercise at the end of the document shows how `RespirometryMeasurement and (measuredOnOrganism some Fish)` returns exactly the candidate rows for a scaling analysis. The nitrate contrast (117 vs 751) is visible in `hasTraitValue`.
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

### A note on the organism classes - replace with NCBITaxon in production

The vernacular organism classes from Step 1 (`Fish`, `Insect`, `Amphibian`, `FruitFly`, `SpangledPerch`, `ParasitoidWasp`) are placeholders. In the production KG, each organism individual is typed by its NCBITaxon URI:

```
organism_X a <http://purl.obolibrary.org/obo/NCBITaxon_317033> .
```

(Browse `317033` at the [NCBI Datasets Taxonomy Browser](https://www.ncbi.nlm.nih.gov/datasets/taxonomy/317033/) - that is the spangled perch, *Leiopotherapon unicolor*.)

NCBITaxon ships the full Linnaean hierarchy as `rdfs:subClassOf` axioms, so the reasoner can still walk `species → genus → family → order → class`. It also carries the scientific name as `rdfs:label`, so the local `hasScientificName` property is no longer needed. The vernacular and morphological classes collapse into NCBITaxon classes once you align. An ecological class like `:Fish` only survives if you still want it to carry `hasRealm some Aquatic`; otherwise the realm restriction moves to a habitat-typed class derived from ENVO.

### A note on body size

The research question references body mass, which the ShareTrait KG carries for the perch records. It is left out of this tutorial to keep the modelled subset focused on Measurement → Trait → Organism. A full treatment would add a `BodySizeMeasurement` linked to the organism, with units from OM/QUDT and quality from PATO.

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

A note on OBOE specifically: unlike PATO/UBERON/ENVO it is a *structural* pattern, not a term list. Aligning ShareTrait's `TraitMeasurement` with OBOE's `Measurement`, our `Organism` with OBOE's `Entity`, and our `TraitType` with OBOE's `Characteristic` would let other ecological datasets annotated with OBOE (e.g. via DataONE) interoperate with ShareTrait without per-database re-mapping. Last release is 2019 - stable rather than rapidly evolving, which suits our purpose.

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

---

## Optional extra (do this on your own time)

Two short exercises that fit on top of the finished ontology. Skip during the live session; return to them afterwards.

### Optional Step A: DL Query — slicing the inferred data

Open the **DL Query** tab (Window > Tabs > DL Query if it is hidden). On the right-hand **Query for** panel, tick **Instances** (and untick **Subclasses** unless you also want classes that satisfy the expression). Without **Instances** ticked, the Query results panel only shows matching *classes* (e.g. `JuvenileFishMeasurement`, `MetabolicRateRespirometryStudy`, `owl:Nothing`) and you will not see the actual measurement records.

**The research-question query.** Recall the question from the top of the tutorial: *how does SMR scale with body mass in freshwater fish at ~21 °C, and does nitrate stress shift that scaling?* The candidate rows for that analysis are the metabolic-rate measurements on fish, acquired by respirometry - no juvenile constraint required. In the DL Query box, type:

```
RespirometryMeasurement and (measuredOnOrganism some Fish)
```

Click **Execute**. The Query results panel lists the three spangled-perch measurements (`TRAMEA023773`, `TRAMEA023776`, `TRAMEA023829`). None of those individuals were asserted as `RespirometryMeasurement` in the data - the reasoner derived it from `usedInstrument some Respirometer` matching the `EquivalentTo` definition you wrote in Step 8. The DL Query then intersects that with the fish constraint to return the rows a scaling analysis would need.

Try a couple more to see how the same machinery slices the data differently:

```
JuvenileFishMeasurement and RespirometryMeasurement
TraitMeasurement and (measuredOnOrganism some Fish)
ColdExposureMeasurement
```

The first narrows further to juveniles (here all three perch records, because the data sample happens to contain only juveniles); the second drops the respirometry constraint and still returns the three perch records (no other fish in the sample); the third returns the Aphidius record.

### Optional Step B: Probe classes - disjointness and closure

Two quick tests of what the reasoner can catch.

**`InconsistentDevelopmentMetabolism`:** Create a class that is a subclass of both `DevelopmentTrait` and `MetabolicRateTrait`. Since they are disjoint (Step 2's idea, applied to traits), the reasoner highlights it in red - it is *unsatisfiable*, equivalent to `owl:Nothing`. Disjoint axioms catch modelling errors automatically.

**`UnclosedTraitMeasurement`:** Create a class under `TraitMeasurement` with these **SubClass Of** restrictions:

```
measuresTraitType some DevelopmentTrait
measuredOnOrganism some Insect
```

Do **not** add a closure axiom (`measuresTraitType only DevelopmentTrait`). The reasoner will not fully classify this class. Compare with `AphidiusDevelopmentStudy`, which does carry closure, to see the difference.
