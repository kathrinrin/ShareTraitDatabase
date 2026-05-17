# Before the Tutorial: 10-minute Setup

---

## 1. Install Java (required by Protégé)

Protégé Desktop needs a Java runtime (JRE 11 or newer). We recommend **Eclipse Temurin** — the free, open-source OpenJDK build from the Eclipse Adoptium project (the successor of AdoptOpenJDK).

- **macOS:** `brew install --cask temurin` (or download from [Adoptium](https://adoptium.net/))
- **Windows / Linux:** download from [Adoptium](https://adoptium.net/) and run the installer

Check it works:

```bash
java -version
```

You should see a version number (anything 11 or higher is fine).

---

## 2. Install Protégé Desktop 5.x

Download from <https://protege.stanford.edu/> (the "Protégé Desktop" zip, not WebProtégé).

- **macOS:** unzip, drag `Protege.app` to Applications. On first launch, right-click > Open to bypass Gatekeeper.
- **Windows:** unzip and run `Protege.exe`.
- **Linux:** unzip and run `./Protege`.

---

## 3. Open the starter file and confirm it works

Download [`sharetrait-ontology-starter.ttl`](https://drive.google.com/file/d/1WkcXIMcByDiiOgf3DRTLEilGZj4P6FHO/view?usp=sharing) and open it in Protégé:

**File > Open** > select `sharetrait-ontology-starter.ttl`

You should see:

- A class tree with **30 classes** under `owl:Thing` (top-level branches: `TraitMeasurement`, `TraitType`, `Organism`, `Instrument`, `TemperatureRange`, `Realm`, `LifeStage`).
- No errors in red.
- The window title shows `sharetrait-ontology-starter.ttl`.

If the file opens and the class tree looks like the diagram in Step 1 of the tutorial — you are done.

---

## 4. Confirm the reasoner runs

We use an **OWL reasoner** (HermiT) to derive new facts - which classes subsume which, which individuals belong to which classes, whether the ontology is consistent. HermiT ships bundled with Protégé 5.x, so nothing to install; we just confirm it is selected and runs once on the starter file.

1. With `sharetrait-ontology-starter.ttl` open, go to the **Reasoner** menu in the top bar.
2. Make sure **HermiT** is checked (Pellet works too if HermiT is greyed out).
3. Click **Reasoner > Start reasoner**.
4. After a second or two, the status bar at the bottom should read *Reasoner active* with no red error popup.
5. Click **Reasoner > Stop reasoner** before closing the file.

If HermiT starts and stops without complaint, your Java install is healthy and you are ready for Step 11.

---

## 5. Bring to the session

- Laptop (charged) with Protégé installed and the starter file opening cleanly.
- The data file [`sharetrait-data-sample.ttl`](https://drive.google.com/file/d/1pkrQaAREdA4o1i6S00DFtho9h5CxiUxB/view?usp=sharing) (we will load it together in Part 4).
