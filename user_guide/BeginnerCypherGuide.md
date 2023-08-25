# Guide for how to explore the Data Distillery graph using Cypher
--------
#### This guide is meant to be an introduction for how to write queries to explore the Data Distillery Knowledge graph. A basic understanding of Cypher is assumed. If you are unfamiliar with Cypher please refer to the [Neo4j docs](https://neo4j.com/developer/cypher/). 

#### For documentation concerning how the Data Distillery knowledge graph is generated or for information about the general schema of the graph please see our [github docs page](https://ubkg.docs.xconsortia.org).
#### For documentation concerning the specific schema for a DCCs dataset please see our [Data Dictionary](https://docs.google.com/document/d/1ubKqkQb40rC7jKRxY9z-SxtsdKqRNZg3Nvds8SpTIbM/edit)

#### We assume you have the latest version of the Data Distillery (v3). Some queries will not return anything if you are working with an older version of the graph.
--------


### The simplest way to find a Code in the graph is to search for it using it's source abbreviation (SAB)

#### 1. How can I return a Code node from a specific ontology/dataset, for example an HGNC Code?
Specify the HGNC as the SAB property.
```
MATCH (hgnc_code:Code {SAB:'HGNC'})
RETURN * 
LIMIT 1
```
Return an HPO Code node.
```
MATCH (hgnc_code:Code {SAB:'HPO'})
RETURN * 
LIMIT 1
```
You can also specify properties outside the Node syntax using the `WITH` keyword,
```
WITH 'HPO' AS HPO_SAB
MATCH (hgnc_code:Code {SAB:HPO_SAB})
RETURN * 
LIMIT 1
```
or using the `WHERE` keyword.

```
MATCH (hgnc_code:Code) WHERE hgnc_code.SAB = 'HPO'
RETURN * 
LIMIT 1
```

All of these are equivalent, although sometimes it can be helpful to use the `WHERE` keyword combined with `STARTS WITH` or `CONTAINS` if you can't remember a specific SAB exactly...


or if you want to include multiple SABs from a DCC. This will return 'GTEXEXP' and 'GTEXEQTL'.
```
MATCH (code:Code) WHERE code.SAB CONTAINS 'GTEX'
RETURN DISTINCT code.SAB
```




#### 2. How can I return a Code node and its Concept node from a specific ontology/dataset, for example an HGNC Code node and its Concept node?
Every Code node is connected to a Concept node by a CODE relationship
```
MATCH (hgnc_code:Code {SAB:'HGNC'})-[:CODE]-(concept:Concept)
RETURN * 
LIMIT 1
```



#### 3. Ontologies/datasets are connected to one another through Concept-Concept relationships, so in order to search for 
Return an HGNC to GO path (code)-(concept)-(concept)-(code)
```
MATCH (code:Code {SAB:'HGNC'})-[:CODE]-(concept:Concept)-[r]-(concept2:Concept)-[:CODE]-(code2:Code {SAB:'GO'})
RETURN * 
LIMIT 1
```


#### 4. Another way to query relationships between 2 ontologies/datasets without necessarily including the Code nodes on either end of the query is to know the SAB and/or TYPE of relationship 



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






