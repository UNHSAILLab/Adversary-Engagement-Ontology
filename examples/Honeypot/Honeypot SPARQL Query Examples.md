```python
narrative_example = "Narrative/02-02-2023-Updated_HoneypotNarrativeExample.jsonld"
```


```python
operation_example = "Operational/02-02-2023-OperationalHoneypot.jsonld"
```

## Example Query: "How many Storylines are there in the Narrative?"

In case a Narrative has multiple storylines, one can check the exclusive `engage:hasStoryline` property.


```python
import rdflib
g = rdflib.Graph()
g.parse(narrative_example)

query = """
PREFIX engage: <https://ontology.adversaryengagement.org/ae/engage/>

SELECT (COUNT(DISTINCT ?p) as ?count)

WHERE {
 ?s engage:hasStoryline ?p
}
"""

for row in g.query(query):
    print(row)
```

    (rdflib.term.Literal('1', datatype=rdflib.term.URIRef('http://www.w3.org/2001/XMLSchema#integer')),)
    

## Example Query: "How many events are in `storyline1`?"

To answer this question, UCO version 1.0.0 has a `types:Thread` class designed to describe partially ordered lists of objects with a property `co:element`


```python
import rdflib
g = rdflib.Graph()
g.parse(narrative_example)

query = """
PREFIX co: <http://purl.org/co/>
PREFIX kb: <http://example.org/kb/>

SELECT (COUNT(DISTINCT ?o)  as ?count)

WHERE {
 kb:storyline1 co:element ?o .
}
"""

for row in g.query(query):
    print(row)
```

    (rdflib.term.Literal('4', datatype=rdflib.term.URIRef('http://www.w3.org/2001/XMLSchema#integer')),)
    

## Example Query: "What PlannedEvents use engage:Alert?"


```python
import rdflib
g = rdflib.Graph()
g.parse(narrative_example)

query = """
PREFIX uco-action: <https://ontology.unifiedcyberontology.org/uco/action/> 
PREFIX uco-core: <https://ontology.unifiedcyberontology.org/uco/core/> 

SELECT ?event

WHERE {
 ?alert ?p engage:Alert .
 ?event ?s ?alert .
}
"""

for row in g.query(query):
    print(row)
```

    (rdflib.term.URIRef('http://example.org/kb/Event2'),)
    (rdflib.term.URIRef('http://example.org/kb/Event3'),)
    (rdflib.term.URIRef('http://example.org/kb/Event4'),)
    

## Example Query: "What PlannedEvent(s) had uco-identity:Person action performers?"


```python
import rdflib
g = rdflib.Graph()
g.parse(narrative_example)

query = """
PREFIX uco-action: <https://ontology.unifiedcyberontology.org/uco/action/> 
PREFIX uco-core: <https://ontology.unifiedcyberontology.org/uco/core/> 


SELECT ?event

WHERE {
 ?personid ?p uco-identity:Person .
 ?action ?s ?personid .
 ?event ?y ?action
}
"""

for row in g.query(query):
    print("\n")
    print(row)
```

    
    
    (rdflib.term.URIRef('http://example.org/kb/Event1'),)
    
