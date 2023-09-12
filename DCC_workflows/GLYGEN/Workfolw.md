The assertion data recieved form GlyGen in n-triples format (glycan.nt and proteoform.nt) were imported into the No4j environment using the n10s plug-in functions through the following script:
```cypher
CREATE CONSTRAINT n10s_unique_uri ON (r:Resource) ASSERT r.uri IS UNIQUE
call n10s.graphconfig.init()
CALL n10s.rdf.import.fetch("file:///Path/glycan.nt","N-Triples");
```
Once the data was imported for each of the glycans and proteoform datasets, subgraphs were created using the following command:
```cypher
CALL gds.graph.create.cypher(
'glycans',
'MATCH (n) RETURN id(n) AS id',
"MATCH (n)-[r]->(m) RETURN id(n) AS source, id(m) AS target")
YIELD
graphName AS graph, nodeQuery, nodeCount AS nodes, relationshipQuery, relationshipCount AS rels
```
Finally, the resulting graph nodes and edges were exported as .csv files using APOC plug-in procedures:
```cypher
CALL apoc.export.csv.all("glycans", {})
```
The resulting nodes and edges reformatted by curating the relationship names and adding SABs for all entities (either by using existing SABs e.g. UNIPROTKB and GLYTOUCAN or creating custom SABs e.g. GLYGEN.MOTIF or GLYCOPROTEIN) and saved as the OWLNETS_node_metadata.tsv and OWLNETS_edgelist.tsv for ingestion.
