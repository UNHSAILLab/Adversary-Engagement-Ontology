# Validator
## Contributor: Bibek Upadhayay
This repo contains the code for the validator. It valdiates the RDF graphs against SHACL graphs and finds the difference in subject and predicates that are in the example graph but not in the ontology graph.

`-og`: ontology graph , graph to validate with
`-eg`: example graph, graph which needs to validate

`-ogtyp`: type of ontology graph, (turtle, json-ld)
`-egtyp`: type of ontology grah, (turtule, json-ld)

`--val=1 `: Validation of RDF graphs against SHACL graphs : 
`--diff=1 `: RDF Diff, any entry in the example graph thats not in the ontology will be displayed


Examples files are already in the folder.
Please use anyof the following CLI commands

## Example #1
`python val_diff.py -og ae_ontology.ttl -ogtyp turtle -eg honeypot.jsonld -egtyp json-ld -val 1 -diff 1`

## Example #2
`python val_diff.py -og case5.ttl -ogtyp turtle -eg case5sub.ttl -egtyp turtle -val 1 -diff 1`

## Example #3
`python val_diff.py -og ae_ontology.ttl -ogtyp turtle -eg honeypot.jsonld -egtyp json-ld -val 1 -diff 1`

