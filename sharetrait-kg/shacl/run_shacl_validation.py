"""Run SHACL validation on the ShareTrait KG."""
from pathlib import Path

from pyshacl import validate
from rdflib import Graph

# Resolve paths relative to this script's location (sharetrait-kg/shacl/)
HERE = Path(__file__).resolve().parent
KG_DIR = HERE.parent  # sharetrait-kg/

print("Loading KG data graph...", flush=True)
data_graph = Graph()
data_graph.parse(KG_DIR / "sharetrait-kg.ttl", format="turtle")
print(f"  Data graph loaded: {len(data_graph)} triples", flush=True)

data_graph.parse(KG_DIR / "sharetrait-skos.ttl", format="turtle")
print(f"  + SKOS vocab loaded: {len(data_graph)} triples total", flush=True)

print("Loading SHACL shapes (OWL)...", flush=True)
shapes_owl = Graph()
shapes_owl.parse(HERE / "sharetrait-shacl.ttl", format="turtle")
print(f"  OWL shapes: {len(shapes_owl)} triples", flush=True)

print("Loading SHACL shapes (SKOS)...", flush=True)
shapes_skos = Graph()
shapes_skos.parse(HERE / "sharetrait-skos-shacl.ttl", format="turtle")
print(f"  SKOS shapes: {len(shapes_skos)} triples", flush=True)

shapes_graph = shapes_owl + shapes_skos
print(f"  Combined shapes: {len(shapes_graph)} triples", flush=True)

print("Running SHACL validation (this may take a while)...", flush=True)
conforms, results_graph, results_text = validate(
    data_graph,
    shacl_graph=shapes_graph,
    inference="none",
    abort_on_first=False,
    allow_infeasible_inverse=True,
    meta_shacl=False,
    advanced=False,
)

print("=" * 60)
print(f"Conforms: {conforms}")
print("=" * 60)
print(results_text[:20000])

results_graph.serialize(HERE / "sharetrait-shacl-report.ttl", format="turtle")
with open(HERE / "sharetrait-shacl-report.txt", "w") as f:
    f.write(results_text)
print(f"Full report saved to shacl/sharetrait-shacl-report.ttl and shacl/sharetrait-shacl-report.txt")
