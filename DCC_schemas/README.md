

# Schemas of the various DCCs
#### Jump to DCC section:

[MOTORPAC](#motorpac)  
[Kids First](#kids-first)

----
## **MOTORPAC**
#### Description of schema
The MOTORPAC node is located in the center and has edges with....
<img src="https://github.com/TaylorResearchLab/CFDE_DataDistillery/blob/main/images/MOTORPAC_SCHEMA_2.png" width="900" height="500">

###### Query to generate MOTORPAC schema screenshot
```
match (mp_code:Code {SAB:'MOTORPAC'})-[r1:CODE]-(mp_cui:Concept)-[r2:RO_0001025]-(ub_cui:Concept)-[r3:CODE]-(ub_code:Code {SAB:'UBERON'})-[r9:PT]-(ub_term:Term) 
match (ensembl_code:Code {SAB:'ENSEMBL'})-[r4:CODE]-(ensembl_cui:Concept)-[r5:associated_with]-(mp_cui)-[r6:gender]-(pato_cui:Concept)-[r7:CODE]-(pato_code:Code {SAB:'PATO'})-[r8:PT]-(pato_term:Term) 
return * LIMIT 1

Data Dictionary Schema Query:
MATCH (mp_cui:Concept)-[:CODE]->(mp_code:Code {SAB:'MOTRPAC'}) 
WHERE mp_code.CODE CONTAINS 'liver'
MATCH (mp_cui)-[:associated_with {SAB:'MOTRPAC'}]-(ensRat_cui:Concept)-[:CODE]->(ensRat_code:Code {SAB:'ENSEMBL'})
MATCH (ensRat_cui)-[:has_human_ortholog]-(ensHum_cui:Concept)-[:CODE]-(ensHum_code:Code {SAB:'ENSEMBL'})-[:GENCODE_PT]-(ensHum_term:Term)
MATCH (ensHum_cui)-[:RO]-(hgnc_cui:Concept)-[:PREF_TERM]-(hgnc_term:Term)
MATCH (mp_cui)-[:sex {SAB:'MOTRPAC'}]->(pato_cui:Concept)-[:PREF_TERM]-(pato_term:Term)
RETURN * LIMIT 1
```
----

## **Kids First**
#### Description of schema
The MOTORPAC node is located in the center and has edges with....
<img src="https://github.com/TaylorResearchLab/CFDE_DataDistillery/blob/main/images/KF_SCHEMA.png" width="900" height="500">

###### Query to generate Kids First schema screenshot
```
match (kfpt_code:Code {SAB:'KFPT'})-[:CODE]-(kfpt_cui:Concept)-[:has_phenotype]-(hpo_cui:Concept)-[:CODE]-(hpo_code:Code {SAB:'HPO'}) 
match (kfpt_cui)-[:belongs_to_cohort]-(cohort_cui:Concept)-[:CODE]-(cohort_code:Code)-[rn]-(cohort_term:Term)
match (cohort_cui)-[:belongs_to_cohort]-(varbin_cui:Concept)-[:CODE]-(varbin_code:Code {SAB:'KFVARBIN'})
match (varbin_cui)-[:location_has_variants]-(chlo_cui:Concept)-[:CODE]-(chlo_code:Code {SAB:'CHLO'})
return * LIMIT 1
```
