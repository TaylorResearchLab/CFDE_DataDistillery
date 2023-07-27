# Guide for how to explore the Data Distillery graph using Cypher



Return HGNC Codes and Concepts
```
MATCH (code:Code {SAB:'HGNC'})-[:CODE]-(concept:Concept)
RETURN * 
LIMIT 5
```

Return an HGNC to GO path (code)-(concept)-(concept)-(code)
```
MATCH (code:Code {SAB:'HGNC'})-[:CODE]-(concept:Concept)-[r]-(concept2:Concept)-[:CODE]-(code2:Code {SAB:'GO'})
RETURN * 
LIMIT 1
```


Find datasets that have connections to the HGNC dataset and return properties in a table.
```
MATCH (code:Code {SAB:'HGNC'})-[:CODE]-(concept:Concept)-[r]-(concept2:Concept)-[:CODE]-(code2:Code)
RETURN DISTINCT code.SAB AS hgnc_start_code, type(r) AS edge, code2.SAB AS SAB_end_code
LIMIT 10
```



Return MOTORPAC to ENSEMBL path
```
MATCH (mp_cui:Concept)-[:CODE]->(mp_code:Code {SAB:'MOTORPAC'}) 
MATCH (mp_cui)-[:associated_with {SAB:'MOTORPAC'}]-(ensRat_cui:Concept)-[:CODE]->(ensRat_code:Code {SAB:'ENSEMBL'})
RETURN *
LIMIT 1
```






