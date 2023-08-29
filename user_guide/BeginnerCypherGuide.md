# Guide for exploring the Data Distillery graph using Cypher
--------
#### This guide is meant to be an introduction for how to write queries to explore the Data Distillery Knowledge graph. A basic understanding of Cypher is assumed. If you are unfamiliar with Cypher please refer to the [Neo4j docs](https://neo4j.com/developer/cypher/). 

#### For documentation concerning how the Data Distillery knowledge graph is generated or for information about the general schema of the graph please see our [github docs page](https://ubkg.docs.xconsortia.org).
#### For documentation concerning the specific schema for a DCCs dataset please see our [Data Dictionary](https://docs.google.com/document/d/1ubKqkQb40rC7jKRxY9z-SxtsdKqRNZg3Nvds8SpTIbM/edit).

#### We assume you have the latest version of the Data Distillery (v3). Some queries will fail to return anything if you are working with an older version of the graph.
--------


### The simplest way to find a Code in the graph is to search for it using it's source abbreviation (SAB)

#### 1. How can I return a Code node from a specific ontology/dataset, for example an HGNC Code?
Specify the HGNC as the SAB property.
```cypher
MATCH (hgnc_code:Code {SAB:'HGNC'})
RETURN * 
LIMIT 1
```

You can also specify properties outside the Node syntax using the `WITH` keyword,
```cypher
WITH 'HGNC' AS HGNC_SAB
MATCH (hgnc_code:Code {SAB:HGNC_SAB})
RETURN * 
LIMIT 1
```
or using the `WHERE` keyword.

```cypher
MATCH (hgnc_code:Code) WHERE hgnc_code.SAB = 'HGNC'
RETURN * 
LIMIT 1
```

All of these are equivalent, although sometimes it can be helpful to use the `WHERE` keyword combined with `STARTS WITH` or `CONTAINS` if you can't remember a specific SAB exactly...


or if you want to include multiple SABs from a DCC (this will return 'GTEXEXP' and 'GTEXEQTL').
```cypher
MATCH (code:Code) WHERE code.SAB CONTAINS 'GTEX'
RETURN DISTINCT code.SAB
```


#### 2. How can I return a Code node and its Concept node from a specific ontology/dataset, for example an HGNC Code node and its Concept node?
Every Code node is connected to a Concept node by a `CODE` relationship
```cypher
MATCH (hgnc_code:Code {SAB:'HGNC'})-[:CODE]-(concept:Concept)
RETURN * 
LIMIT 1
```

#### 3. To return the human-readable string that a Code represents you can return the Term node along with the Code. 
Not all Codes have Terms attached to them. If a Code does have Term nodes then it will almost always have a 'preferred term'. This 'preferred term' is always attached to it's Code by the `PT` relationship

```cypher
MATCH (hgnc_code:Code {SAB:'HGNC'})-[:PT]-(term:Term)
RETURN * 
LIMIT 1
```

You can also directly access the the 'preferred term' through the corresponding Concept node through a `PREF_TERM` relationship
```cypher
MATCH (hgnc_code:Code {SAB:'HGNC'})-[:CODE]-(concept:Concept)-[:PREF_TERM]-(term:Term)
RETURN * 
LIMIT 1
```

#### 4. Ontologies/datasets are connected to one another through Concept-Concept relationships, so you must query the concept space
Return an HGNC to GO path (code)-(concept)-(concept)-(code)
```cypher
MATCH (code:Code {SAB:'HGNC'})-[:CODE]-(concept:Concept)-[r]-(concept2:Concept)-[:CODE]-(code2:Code {SAB:'GO'})
RETURN * 
LIMIT 1
```


#### 5. Another way to query relationships between 2 ontologies/datasets without necessarily including the Code nodes on either end of the query is to know the SAB and/or TYPE of relationship 

```cypher
MATCH (code:Code {SAB:'HGNC'})-[:CODE]-(concept:Concept)-[r:process_involves_gene {SAB:'NCI'}]-(concept2:Concept)-[:CODE]-(code2:Code {SAB:'GO'})
RETURN * 
LIMIT 1
```


#### 6. How can I find out what relationships exist between my ontology/dataset and other ontologies/datasets
Find datasets that have relationships to HGNC genes and return properties in a table.
```cypher
MATCH (code:Code {SAB:'HGNC'})-[:CODE]-(concept:Concept)-[r]-(concept2:Concept)-[:CODE]-(code2:Code)
RETURN DISTINCT code.SAB AS hgnc_start_code, type(r) AS edge_TYPE, r.SAB AS edge_SAB,  code2.SAB AS SAB_end_code
LIMIT 10
```

we can go a step further and return the Terms on either end of this query,

```cypher
MATCH (hgnc_term:Term)-[:PT]-(code:Code {SAB:'HGNC'})-[:CODE]-(concept:Concept)-[r]-(concept2:Concept)-[:CODE]-(code2:Code)-[:PT]-(term2:Term)
RETURN DISTINCT hgnc_term.name AS gene_name, code.SAB AS hgnc_start_code, type(r) AS edge_TYPE, r.SAB AS edge_SAB,  code2.SAB AS SAB_end_code, term2.name AS end_term
LIMIT 10
```



---------------------------
Return MOTORPAC to ENSEMBL path
```cypher
MATCH (mp_cui:Concept)-[:CODE]->(mp_code:Code {SAB:'MOTORPAC'}) 
MATCH (mp_cui)-[:associated_with {SAB:'MOTORPAC'}]-(ensRat_cui:Concept)-[:CODE]->(ensRat_code:Code {SAB:'ENSEMBL'})
RETURN *
LIMIT 1
```



## Simple Optimization techniques

#### If you're worried about the speed of a query it's a good idea to include as much information as you can and to be as specific as possible.
For example, including the Concept-to-Concept relationship types as well as the Code SAB types will speed up the query significantly.



## DCC specific queries



### 4D Nucleome (4DN)	

### Extracellular RNA Communication Program (ERCC)	RBP	 Regulatory Element	

### GlyGen	

### Genotype Tissue Expression (GTEx)	

Show the GTEXEXP node and its three edges to an HGNC node, an UBERON node and an EXPBINS node. The EXPBINS node is where the TPM value from GTEx is located (on the upperbound and lowerbound properties).
```cypher
MATCH (gtex_cui:Concept)-[r0:CODE]-(gtex_exp_code:Code {SAB:'GTEXEXP'}) 
MATCH (gtex_cui)-[r1:expressed_in]-(hgnc_concept:Concept)-[r2:CODE]-(hgnc_code:Code {SAB:'HGNC'})
MATCH (gtex_cui)-[r3:expressed_in]-(ub_concept:Concept)-[r4:CODE]-(ub_code:Code {SAB:'UBERON'})
MATCH (gtex_cui)-[r5:has_expression]-(expbin_concept:Concept)-[r6:CODE]-(expbin_code:Code {SAB:'EXPBINS'})
RETURN * LIMIT 1
```

Show the GTEXEQTL node and its three edges to an HGNC node, an UBERON node and a PVALUEBINS node. The PVALUEBINS node is where the p-value for the eQTL is located (on the upperbound and lowerbound properties).
```cypher
MATCH (gtex_cui:Concept)-[r0:CODE]-(gtex_exp_code:Code {SAB:'GTEXEQTL'}) 
MATCH (gtex_cui)-[r1]-(hgnc_concept:Concept)-[r2:CODE]-(hgnc_code:Code {SAB:'HGNC'})
MATCH (gtex_cui)-[r3:located_in]-(ub_concept:Concept)-[r4:CODE]-(ub_code:Code {SAB:'UBERON'})
MATCH (gtex_cui)-[r5:p_value]-(pvalbin_concept:Concept)-[r6:CODE]-(pvalbin_code:Code {SAB:'PVALUEBINS'} ) 
RETURN * LIMIT 1
```

### The Human BioMolecular Atlas Program (HuBMAP)

### Illuminating the Druggable Genome (IDG)	

Show the IDGP mapping between PUBCHEM and UNIPROTKB
```cypher 
MATCH (pubchem_code:Code {SAB:'PUBCHEM'})-[:CODE]-(pubchem_cui:Concept)-[:bioactivity {SAB:'IDGP'}]-(uniprot_cui:Concept)-[:CODE]-(uniprot_code:Code {SAB:"UNIPROTKB"})
RETURN * LIMIT 1
```

Show the IDGD mapping between PUBCHEM and SNOMEDUS_CT

### Gabriella Miller Kids First (GMKF)	

### The Library of Integrated Network-Based Cellular Signatures (LINCS)	

Show the LINCS edge which maps HGNC nodes to PUBCHEM nodes. There is also a `negatively_regulated_by` relationship 
```cypher
MATCH (hgnc_cui:Concept)-[:CODE]->(hgnc_code:Code {SAB:'HGNC'})-[]->(hgnc_term:Term)
MATCH (hgnc_cui)-[:positively_regulated_by {SAB:'LINCS'}]-(pubchem_cui:Concept)-[:CODE]-(pubchem_code:Code {SAB:'PUBCHEM'})
RETURN * LIMIT 1 
```

### The Molecular Transducers of Physical Activity Consortium (MoTrPAC)	

### Metabolomics Workbench (MW)	

### Stimulating Peripheral Activity to Relieve Conditions (SPARC)	






Additional Datasets	
CLINVAR	
CMAP
HPOMP
HGNCHPO	
NCOPHGNC
HCOPMP
MSIGDB
HSCLO







