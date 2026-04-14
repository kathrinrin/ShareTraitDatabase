"""Validate sharetrait-traits.ttl — run with: python sharetrait-kg/validate_traits.py"""
from rdflib import Graph, OWL, RDF, RDFS, URIRef, Namespace
from rdflib.collection import Collection

g = Graph()
g.parse('sharetrait-kg/sharetrait-traits.ttl', format='turtle')
NS = Namespace("http://sharetrait.org/ontologies/traits#")

named_cls = sorted([s for s in g.subjects(RDF.type, OWL.Class) if isinstance(s, URIRef)], key=str)
obj_props = sorted([s for s in g.subjects(RDF.type, OWL.ObjectProperty) if isinstance(s, URIRef)], key=str)
data_props = sorted([s for s in g.subjects(RDF.type, OWL.DatatypeProperty) if isinstance(s, URIRef)], key=str)
func_props = sorted([s for s in g.subjects(RDF.type, OWL.FunctionalProperty) if isinstance(s, URIRef)], key=str)
indivs = sorted([s for s in g.subjects(RDF.type, OWL.NamedIndividual) if isinstance(s, URIRef)], key=str)
equiv = [(s, o) for s, o in g.subject_objects(OWL.equivalentClass) if isinstance(s, URIRef)]
disj_nodes = list(g.subjects(RDF.type, OWL.AllDisjointClasses))
svf = list(g.subject_objects(OWL.someValuesFrom))
avf = list(g.subject_objects(OWL.allValuesFrom))
inv = [(s, o) for s, o in g.subject_objects(OWL.inverseOf) if isinstance(s, URIRef)]
alldiff = list(g.subjects(RDF.type, OWL.AllDifferent))

n = lambda u: u.split('#')[-1]

print(f"Triples: {len(g)}")
print(f"Named classes: {len(named_cls)}")
print(f"Object props: {len(obj_props)}, Data props: {len(data_props)}, Functional: {len(func_props)}")
print(f"Individuals: {len(indivs)}")
print(f"EquivClass: {len(equiv)}, AllDisjointClasses: {len(disj_nodes)}")
print(f"someValuesFrom: {len(svf)}, allValuesFrom: {len(avf)}")
print(f"Inverse pairs: {len(inv)}, AllDifferent: {len(alldiff)}")

# Consistency checks
all_cls = set(s for s in g.subjects(RDF.type, OWL.Class) if isinstance(s, URIRef))
all_props = set(s for s in g.subjects(RDF.type, OWL.ObjectProperty)) | set(s for s in g.subjects(RDF.type, OWL.DatatypeProperty))
issues = []
for pred in [OWL.someValuesFrom, OWL.allValuesFrom]:
    for _, t in g.subject_objects(pred):
        if isinstance(t, URIRef) and str(t).startswith(str(NS)) and t not in all_cls:
            issues.append(f"Undeclared class in restriction: {n(t)}")
for _, o in g.subject_objects(RDFS.domain):
    if isinstance(o, URIRef) and str(o).startswith(str(NS)) and o not in all_cls:
        issues.append(f"Undeclared domain: {n(o)}")
for _, o in g.subject_objects(RDFS.range):
    if isinstance(o, URIRef) and str(o).startswith(str(NS)) and o not in all_cls:
        issues.append(f"Undeclared range: {n(o)}")
for dn in disj_nodes:
    mn = list(g.objects(dn, OWL.members))
    if mn:
        for m in Collection(g, mn[0]):
            if isinstance(m, URIRef) and str(m).startswith(str(NS)) and m not in all_cls:
                issues.append(f"Undeclared disjoint member: {n(m)}")

# Pizza check
ttl = open('sharetrait-kg/sharetrait-traits.ttl').read()
md = open('sharetrait-kg/sharetrait-traits-tutorial.md').read()
p_ttl = sum(1 for l in ttl.split('\n') if 'pizza' in l.lower())
p_md = sum(1 for l in md.split('\n') if 'pizza' in l.lower())
if p_ttl: issues.append(f"Pizza refs in TTL: {p_ttl}")
if p_md: issues.append(f"Pizza refs in MD: {p_md}")

if issues:
    for i in issues: print(f"  ISSUE: {i}")
else:
    print("All checks passed — no issues found")
