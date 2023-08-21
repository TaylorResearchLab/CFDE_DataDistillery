33# What do you need to know before hand

- [ ]  Users need to have some level of understanding of Neo4j. Check this [link](https://graphacademy.neo4j.com/courses/neo4j-fundamentals/) for a tutorial if you don't
- [ ]  Users need to have some level of understanding of Cypher query languag. Refer to this [link](https://graphacademy.neo4j.com/courses/cypher-fundamentals/) if you do not
- [ ]  Users need to have some level of understanding of gene ontologies and their structure
- [ ]  Users need to have some level of understanding of HuBMAP UMLS

Next, to shorten the length of the tutorial we have several abbreviations that we will continuously use to refer to different subjects. We will list some here but we also have a data dictionary at this [link](https://github.com/TaylorResearchLab/CFDE_DataDistillery/blob/main/user_guide/GLOSSARY.md) that will list out all of the used abbreviations so you can refer to these if you are ever confused.  

# What can you do with the queries

Queries into a neo4j database operate on Cypher, parallel to how relational databases use SQL.

So you can use queries to ask complex questions that link data across multiple ontologies to derive all new answers to questions that you were not able to ask before. And the best part is that not only are the queries simple to construct, they often do not take very long to run like it would in a more traditional relational database. We will give you a break down of the query structure and some example queries in the following sections. 

# The schema of the database

The schema structures data based on the idea of concept nodes. 

A “**CONCEPT”** is an ***entity*** in the UBKG. A **concept** is represented with a ***code*** in a source ontology and a ***CUI(*Concept Unique Identifier)** in the overall UBKG.

**Concept** nodes are those unifying principles that can support connections to multiple terminology systems. 

A “**CODE”** is the identifier for a ***concept*** in a ***vocabulary*** or ***ontology*** in the UMLS. A code is unique to the ontology. For example, both the SNOMED_CT and the NCI Thesaurus vocabularies have different “**CODES**” to represent the ***concept*** of “kidney”; however, because these codes are ***cross-referenced*** to the same UMLS concept, the codes share a **CUI**(**Concept Unique Identifier)**.

A “**CUI”** is a unique identifier for a ***concept*** in the UBKG. A **CUI** can be cross-referenced by ***codes*** from many ***ontologies***, allowing for associations between entities in different ontologies.

For example, the **CUI** for the concept of *methanol* in UMLS is cross-referenced by codes in a number of ontologies and vocabularies, such as SNOMED_CT and NCI. The use of the CUI allows for questions such as “How many different ways do all of the ontologies in the UBKG refer to methanol?” An example of a CUI being used can be seen in the picture below. The following illustration shows, a knowledge graph can reveal that terms from different ontologies include “methanol”, “Methyl Alcohol”, and “METHYL ALCOHOL”.


![202924294-9b232793-ae36-4fdd-8363-44a2ddedbe3e-2](https://github.com/TaylorResearchLab/CFDE_DataDistillery/assets/16074732/ccc71e6b-33d3-416d-904f-4a72cd83aca8)


An “**ENTITY”** represents a member of an ***ontology***. **Entities** associate with other entities in an ontology via ***relationships***.

An example of an entity is *5'-AMP-activated protein kinase subunit gamma-1*, which is a protein in the Protein Ontology (PR), ***encoded*** with ***code*** 000013225.

In a ***knowledge graph***, an entity is represented by a ***node***.

The UBKG adopts the UMLS practice of identifying source ontologies with a **Source Abbreviation** (SAB). Examples of UMLS SABs include SNOMED_CT and UBERON. UBKG uses published acronyms for ontologies when possible–e.g., PATO.

A “**TERM**” is usually a short text identifier for a ***code*** in an **_ontology**_. For example, a term for code 64033007 in SNOMED_CT is “kidney”.

A **term** can be a *preferred term* or a *synonym*.

# Break Down Query construction

Now here are some examples of query construction. We have a very basic query that is going to return all HGNC Codes and Concepts. In this example we use a “**code:Code**”(how to select all Code nodes in the graph) and add the label **SAB** (Source Abbreviation) as “**HGNC**” and set the relationship as “**:CODE**” to select all of the relationships that are connected to “**concept:Concept**” (which is how you select all concepts in the graph). We return all of the matches and place a limit of 5 on the number of results returned. The purpse of the “code” before the semi colon is to give that identifier a variable name so that if we want to run a following query we have a way to identify that section of the query (same with the “concept” before the semicolon).

```
MATCH (code:Code {SAB:'HGNC'})-[:CODE]-(concept:Concept)
RETURN *
LIMIT 5
```

![hgnc](https://github.com/TaylorResearchLab/CFDE_DataDistillery/assets/16074732/ede0fe15-478f-4fd6-8f26-3c9ab0398e53)


In this example we are returning all HGNC nodes that are connected to GO nodes. Again we use “**code:Code**” to select all nodes and give it the **SAB** **HGNC**. We set the relationship to “:**CODE**” so we can get all the nodes that have a :CODE relationship. Then we set the relationship to “**[r]**” (this is how we select all relationships of a node). We create a second concept named “**concept2**” (now we are getting all concept to concept2 relationships) and finally we make a “**:CODE**” relationship to select all code relationships attached to **concept2**. Lastly we make **code2** and give it the **SAB** of “**GO**” and that is how we set our query up to match all **HGNC** nodes and to find all concepts from **HGNC** that match a concept from **GO**. The final thing we do is return * and put a limit of 1 so we can analyze one output and see how these connections look in a neo4j graph output.

```
MATCH (code:Code {SAB:'HGNC'})-[:CODE]-(concept:Concept)-[r]-(concept2:Concept)-[:CODE]-(code2:Code {SAB:'GO'})
RETURN *
LIMIT 1
```
![hgnc-sab](https://github.com/TaylorResearchLab/CFDE_DataDistillery/assets/16074732/9de6e4a4-31d3-4b1c-8520-600d8124216f)



In the next example we are using all of the skills that we have seen so far to give us more of a tabular output from our query. We start the same way we did before with selecting all code nodes that have a **SAB** of **HGNC**, and then selecting all **CODE** relationships from those nodes to all concept nodes. We then get all relationships from those concept nodes and connect them to a second group of concept nodes named concept2. We then take all nodes with a **CODE** relationship and select all :**Code** nodes and name that “**code2**”. This is very similar to the example that we did above. The big difference this time is that instead of returning everything, we now return “********************DISTINCT”******************** results only. And we now get to see how we use the variable naming that we have been attaching to our code nodes and concept nodes in previous examples. We used code.SAB (which is equivalent to the “(code:Code {SAB:'HGNC'})” portion of this query) and we give it a new name of “hence_start_code” by using the “**AS**” keyword. We then set r (which is the relationships of concept nodes to concept2 nodes) and rename that as edge using the “**AS**” keyword. Lastly we use code2.SAB and give these nodes the name “SAB_end_code” with the “**AS**” keyword and set a limit of 10 results to be outputted. Below we show what the results of this query look like. 

```
MATCH (code:Code {SAB:'HGNC'})-[:CODE]-(concept:Concept)-[r]-(concept2:Concept)-[:CODE]-(code2:Code)
RETURN DISTINCT code.SAB AS hgnc_start_code, type(r) AS edge, code2.SAB AS SAB_end_code
LIMIT 10
```

<img width="1129" alt="Screenshot 2023-08-21 at 12 14 13 PM" src="https://github.com/TaylorResearchLab/CFDE_DataDistillery/assets/16074732/28a945c0-5935-4862-8729-96b05b3da9fb">


# 1st simple use case query example

Now that we have seen some basic queries in action and have a better understanding of how they work. Let's look at some helpful use cases to get a feel for what kinds of questions we can ask using this graphical database. 

##### I believe this section will have to be adjusted since the database has changed #######

### Basic "Level 1" queries

1. Exploring GTEx experimental data.

Let's look at an example of a tissue-gene pair expression data point from the GTEx project.

Here we will select out TPM data (transcripts per million) which are used to quantify how much of a gene is expressed within a sample.

In our query, we use "Limit 1" to prevent us from returning all the GTEx TPM values in the DB.

To make each GTEx TPM point unique, we store each TPM value as a tissue-gene pair.

This example just extracts tissue-gene pairs and the TPM associated with that tissue-gene pair.

The first tutorial has plenty of examples to pull from including a GTEX query 

```
MATCH (gtex_cui:Concept)-[r0:CODE]-(gtex_code:Code {SAB:'GTEX_EXP'})-[:TPM]-(gtex_term:Term)
RETURN * LIMIT 1
```

INSERT PICTURE FROM TUTORIAL

You can see from the above image, where I've moused over the Code node (purple), that this node represents an Ensembl ID + a tissue descriptor. The term associated with this code node is a binned TPM value ranging between 9 and 10 which can be used to select or display TPM ranges of interest. In a future release of this knowledge graph, the numerical type values will also be shown.

Let's add the concept node of the gene represented by this TPM value:

```
MATCH (gtex_cui:Concept)-[r0:CODE]-(gtex_code:Code {SAB:'GTEX_EXP'})-[:TPM]-(gtex_term:Term)
MATCH (gtex_cui)-[r1]-(hgnc_concept:Concept)-[r2]-(hgnc_code:Code {SAB:'HGNC'})
RETURN * LIMIT 1
```

INSERT PICTURE FROM TUTORIAL

Next, let's add the concept code for the tissue related to this TPM value and gene.

```
MATCH (gtex_cui:Concept)-[r0:CODE]-(gtex_code:Code {SAB:'GTEX_EXP'})-[:TPM]-(gtex_term:Term)
MATCH (gtex_cui)-[r1]-(hgnc_concept:Concept)-[r2]-(hgnc_code:Code {SAB:'HGNC'})
MATCH (gtex_cui)-[r3]-(ub_concept:Concept)-[r4]-(ub_code:Code {SAB:'UBERON'})
RETURN * LIMIT 1
```

INSERT PICTURE FROM TUTORIAL

This query represented by the plot above also displays the current graph structure of all the GTEx expression concept code relations: HGNC gene <-> TPM value <-> Uberon ID. It can be used to help build additional queries combining GTEx data with other datasets in the knowledge graph.

# Another use case query example

Here is another example of the kinds of questions that we can ask. 

Can we find all phenotype-gene relationships given a certain phenotype?

For instance, given a HPO (phenotype) term, can we return all linked gene names?

We can accomplish this by leveraging the HPO-to-gene links in the knowledge graph, imported from the HPO-to-gene relationship list curated by Peter Robinson's group at Jax. That list was derived from Orphanet and OMIM.

```
WITH 'HP:0001631' AS HPO_CODE
MATCH (hpoTerm:Term)-[:PT]-(hpoCode:Code {CODE: HPO_CODE})-[r1:CODE]-(hpo_concept)-[r2]-(hgnc_concept:Concept)-[r3:CODE]-(hgnc_code:Code {SAB:'HGNC'})-[:PT]-(hgnc_term:Term)
RETURN * LIMIT 10
```

INSERT PICTURE FROM TUTORIAL 

A Concept (blue), Code (purple) and Term (green) node from HPO (left side) and HGNC (right side) and the bidirectional relationships between the two Concept nodes.

Instead of a limited graph visual, can obtain all the genes associated with a phenotype in a table by asking for specific outputs in the RETURN statement:

```
WITH 'HP:0001631' AS HPO_CODE
MATCH (hpoTerm:Term)-[:PT]-(hpoCode:Code {CODE: HPO_CODE})-[r1:CODE]-(hpo_concept)-[r2]-(hgnc_concept:Concept)-[r3:CODE]-(hgnc_code:Code {SAB:'HGNC'})-[:PT]-(hgnc_term:Term)
RETURN hgnc_code.CODE AS HGNC_ID, hgnc_term.name AS GENE_SYMBOL
```
