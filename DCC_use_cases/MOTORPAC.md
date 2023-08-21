# MOTORPAC Use Case
[Google Doc to MOTORPAC use cases](https://docs.google.com/spreadsheets/d/1Z1rStygHvT3zBQIDmD61No4U3YogkpglpDxJlD4tIfk/edit#gid=0)

**NOTE:** The KF `value` parameter represents the number of (HIGH impact and de Novo) variants associated with each gene. The MOTORPAC nodes are represented by tissue-gene-gender Codes which means you can get the same KF gene showing up multiple times for unique MOTORPAC connections like in the image below.

<img src="https://github.com/TaylorResearchLab/CFDE_DataDistillery/blob/main/images/KF_MOTORPAC_screenshot.png" width="650" height="250">

Query used:
```
LOAD CSV FROM 'file:///Glycoenzymes.csv' AS glyco_genes WITH REDUCE(s = [], list IN collect(glyco_genes) | s + list) AS glyco_list
MATCH  (hgnc_term:Term)-[:ACR]-(hgnc_code:Code {SAB:'HGNC'})-[:CODE]-(hgnc_cui)-[:gene_has_variants]-(kf_cui:Concept)-[:CODE]-(kf_code:Code {SAB:'KFGENEBIN'}) WHERE hgnc_term.name IN glyco_list
MATCH (mp_code:Code {SAB:'MOTORPAC'})<-[:CODE]-(mp_cui:Concept)-[:associated_with {SAB:'MOTORPAC'}]-(ensRat_cui:Concept)-[:CODE]->(ensRat_code:Code {SAB:'ENSEMBL'})
MATCH (ensRat_cui)-[:has_human_ortholog]-(ensHum_cui:Concept)-[:CODE]-(ensHum_code:Code {SAB:'ENSEMBL'})-[:GENCODE_PT]-(ensHum_term:Term) MATCH (ensHum_cui)-[:RO]-(hgnc_cui:Concept) RETURN DISTINCT hgnc_term.name AS glycoGene, mp_code.CODE, kf_code.value AS variantCnt
```





### 1) MoTrPAC Genes affected by exercise, are expressed in matched tissues in humans in GTEx, that are either matches or inverse matches of a perturbation signal in LINCS = compounds or perturbations that might promote or interfere with exercise benefit b) (FUTURE) Genes that are circadian in rat, are a signature match to perturbation in LINCS = compounds that might affect circadian rhythms/behaviors 
```
//Graphical representation showing the first line of results as a graph
match (motrpac_code:Code {SAB:"MOTRPAC"})<-[:CODE]-(motrpac_concept:Concept)-[r1:associated_with]->(rat_gene_concept:Concept)-[r2:has_human_ortholog]->(hgnc_concept:Concept)<-[r3 {SAB:"LINCS"}]-(perturbagen_concept:Concept),
(motrpac_concept:Concept)-[r4:located_in]->(tissue_concept_1:Concept)-[r5:part_of]-(tissue_concept_2:Concept)-[r6:expresses {SAB:"GTEXEXP"}]->(gtex_concept:Concept)-[r7:expressed_in {SAB:"GTEXEXP"}]-(hgnc_concept:Concept),
(gtex_concept:Concept)-[r8:has_expression {SAB:"GTEXEXP"}]->(expr_concept:Concept)-[:CODE]->(expr_code:Code),
(hgnc_concept:Concept)-[:PREF_TERM]->(hgnc_term:Term),
(perturbagen_concept:Concept)-[:PREF_TERM]->(perturbagen_term:Term),
(tissue_concept_1:Concept)-[:PREF_TERM]->(tissue_term_1:Term),
(tissue_concept_2:Concept)-[:PREF_TERM]->(tissue_term_2:Term),
(rat_gene_concept:Concept)-[:CODE]->(rat_gene_code:Code)
return * limit 1

//Returning 20 line of results in tabular format
match (motrpac_code:Code {SAB:"MOTRPAC"})<-[:CODE]-(motrpac_concept:Concept)-[r1:associated_with]->(rat_gene_concept:Concept)-[r2:has_human_ortholog]->(hgnc_concept:Concept)<-[r3 {SAB:"LINCS"}]-(perturbagen_concept:Concept),
(motrpac_concept:Concept)-[r4:located_in]->(tissue_concept_1:Concept)-[r5:part_of]-(tissue_concept_2:Concept)-[r6:expresses {SAB:"GTEXEXP"}]->(gtex_concept:Concept)-[r7:expressed_in {SAB:"GTEXEXP"}]-(hgnc_concept:Concept),
(gtex_concept:Concept)-[r8:has_expression {SAB:"GTEXEXP"}]->(expr_concept:Concept)-[:CODE]->(expr_code:Code),
(hgnc_concept:Concept)-[:PREF_TERM]->(hgnc_term:Term),
(perturbagen_concept:Concept)-[:PREF_TERM]->(perturbagen_term:Term),
(tissue_concept_1:Concept)-[:PREF_TERM]->(tissue_term_1:Term),
(tissue_concept_2:Concept)-[:PREF_TERM]->(tissue_term_2:Term),
(rat_gene_concept:Concept)-[:CODE]->(rat_gene_code:Code)
return distinct motrpac_code.CODE as MoTrPac_DS, rat_gene_code.CODE as rat_gene, hgnc_term.name as human_gene,tissue_term_1.name as tissue_MoTrPac, tissue_term_2.name as tissue_GTEx, expr_code.CODE as TPM,perturbagen_term.name as perturbagen,type(r3) as effect_direction limit 20

```

### 2) MoTrPAC Genes affected by exercise, are expressed in matched tissues in humans in GTEx, that are either matches or inverse matches of a perturbation signal in LINCS = compounds or perturbations that might promote or interfere with exercise benefit b) (FUTURE) Genes that are circadian in rat, are a signature match to perturbation in LINCS = compounds that might affect circadian rhythms/behaviors 
```
//Graphical representation showing the first line of results as a graph
match (motrpac_code:Code {SAB:"MOTRPAC"})<-[:CODE]-(motrpac_concept:Concept)-[r1:associated_with]->(rat_gene_concept:Concept)-[r2:has_human_ortholog]->(hgnc_concept:Concept)-[r3:causally_influences {SAB:"MW"}]->(metabolite_concept:Concept)-[r9:correlated_with_condition {SAB:"MW"}]->(condition_concept:Concept),
(metabolite_concept:Concept)-[r10:produced_by {SAB:"MW"}]->(tissue_concept_1:Concept),
(motrpac_concept:Concept)-[r4:located_in]->(tissue_concept_1:Concept)-[r5:part_of]-(tissue_concept_2:Concept)-[r6:expresses {SAB:"GTEXEXP"}]->(gtex_concept:Concept)-[r7:expressed_in {SAB:"GTEXEXP"}]-(hgnc_concept:Concept),
(gtex_concept:Concept)-[r8:has_expression {SAB:"GTEXEXP"}]->(expr_concept:Concept)-[:CODE]->(expr_code:Code),
(hgnc_concept:Concept)-[:PREF_TERM]->(hgnc_term:Term),
(metabolite_concept:Concept)-[:PREF_TERM]->(metabolite_term:Term),
(condition_concept:Concept)-[:PREF_TERM]->(condition_term:Term),
(tissue_concept_1:Concept)-[:PREF_TERM]->(tissue_term_1:Term),
(tissue_concept_2:Concept)-[:PREF_TERM]->(tissue_term_2:Term),
(rat_gene_concept:Concept)-[:CODE]->(rat_gene_code:Code)
return * limit 1

//Returning 20 line of results in tabular format
match (motrpac_code:Code {SAB:"MOTRPAC"})<-[:CODE]-(motrpac_concept:Concept)-[r1:associated_with]->(rat_gene_concept:Concept)-[r2:has_human_ortholog]->(hgnc_concept:Concept)-[r3:causally_influences {SAB:"MW"}]->(metabolite_concept:Concept)-[r9:correlated_with_condition {SAB:"MW"}]->(condition_concept:Concept),
(metabolite_concept:Concept)-[r10:produced_by {SAB:"MW"}]->(tissue_concept_1:Concept),
(motrpac_concept:Concept)-[r4:located_in]->(tissue_concept_1:Concept)-[r5:part_of]-(tissue_concept_2:Concept)-[r6:expresses {SAB:"GTEXEXP"}]->(gtex_concept:Concept)-[r7:expressed_in {SAB:"GTEXEXP"}]->(hgnc_concept:Concept),
(gtex_concept:Concept)-[r8:has_expression {SAB:"GTEXEXP"}]->(expr_concept:Concept)-[:CODE]->(expr_code:Code),
(hgnc_concept:Concept)-[:PREF_TERM]->(hgnc_term:Term),
(metabolite_concept:Concept)-[:PREF_TERM]->(metabolite_term:Term),
(condition_concept:Concept)-[:PREF_TERM]->(condition_term:Term),
(tissue_concept_1:Concept)-[:PREF_TERM]->(tissue_term_1:Term),
(tissue_concept_2:Concept)-[:PREF_TERM]->(tissue_term_2:Term),
(rat_gene_concept:Concept)-[:CODE]->(rat_gene_code:Code)
return distinct motrpac_code.CODE as MoTrPac_DS, rat_gene_code.CODE as rat_gene, hgnc_term.name as human_gene,tissue_term_1.name as tissue_MoTrPac_MW, tissue_term_2.name as tissue_GTEx, expr_code.CODE as TPM,metabolite_term.name as metabolite,condition_term.name as condition limit 20

```

### 3) Find KF (or other) SNPs or mutations that lead to loss or gain of glycosylation site from GlyGen data, and how many of those genes are expressed in the GTEx liver dataset AND in the MoTrPAC liver data are a Rat-human expression match in liver AND are output RNA-protein correlate in liver
```
// put Glycoenzymes.csv in the import folder of your neo4j db
// then use collect and reduce to flatten list of genes
LOAD CSV FROM 'file:///Glycoenzymes.csv' AS glyco_genes
WITH REDUCE(s = [], list IN collect(glyco_genes) | s + list) AS glyco_list
MATCH  (hgnc_term:Term)-[:ACR]-(hgnc_code:Code {SAB:'HGNC'})-[:CODE]-(hgnc_cui)-[:gene_has_variants]-(kf_cui:Concept)-[:CODE]-(kf_code:Code {SAB:'KFGENEBIN'})
WHERE hgnc_term.name IN glyco_list
MATCH (mp_code:Code {SAB:'MOTORPAC'})<-[:CODE]-(mp_cui:Concept)-[:associated_with {SAB:'MOTORPAC'}]-(ensRat_cui:Concept)-[:CODE]->(ensRat_code:Code {SAB:'ENSEMBL'})
MATCH (ensRat_cui)-[:has_human_ortholog]-(ensHum_cui:Concept)-[:CODE]-(ensHum_code:Code {SAB:'ENSEMBL'})-[:GENCODE_PT]-(ensHum_term:Term)
WHERE mp_code.CODE CONTAINS 'liver'
MATCH (ensHum_cui)-[:RO]-(hgnc_cui:Concept)
RETURN DISTINCT hgnc_term.name AS glycoGene, mp_code.CODE AS MOTORPAC_code, kf_code.value AS variantCnt, mp_code.value AS p_value
```

### 4) For a specific drug processing enzyme, find the tissue and assays where these enzymes are highly expressed in the MoTrPAC young adult rats endurance training exercise data, and the related drug profiles in LINCS data.
```
MATCH (mp_cui:Concept)-[:CODE]->(mp_code:Code {SAB:'MOTORPAC'}) 
WHERE mp_code.CODE CONTAINS 'liver'
MATCH (mp_cui)-[:associated_with {SAB:'MOTORPAC'}]-(ensRat_cui:Concept)-[:CODE]->(ensRat_code:Code {SAB:'ENSEMBL'})
MATCH (ensRat_cui)-[:has_human_ortholog]-(ensHum_cui:Concept)-[:CODE]-(ensHum_code:Code {SAB:'ENSEMBL'})-[:GENCODE_PT]-(ensHum_term:Term)
MATCH (ensHum_cui)-[:RO]-(hgnc_cui:Concept)-[:PREF_TERM]-(hgnc_term:Term)
WHERE hgnc_term.name = 'CYP1B1 gene'
MATCH (hgnc_cui)-[:expresses]->(gtex_cui:Concept)-[:CODE]-(gtex_code:Code {SAB:'GTEXEXP'})
MATCH (hgnc_cui)-[:positively_regulated_by {SAB:'LINCS'}]-(pubchem_cui:Concept)-[:CODE]-(pubchem_code:Code {SAB:'PUBCHEM'})-[:IDGD_PT]-(pubchem_term:Term)
MATCH (gtex_cui)-[:expressed_in]-(ub_cui:Concept)-[:CODE]-(ub_code:Code {SAB:'UBERON'})-[:PT]-(ub_term:Term)
WHERE ub_term.name CONTAINS 'liver'
MATCH (mp_cui)-[:gender {SAB:'MOTORPAC'}]->(pato_cui:Concept)-[:PREF_TERM]-(pato_term:Term)
RETURN DISTINCT hgnc_term.name AS gene, mp_code.CODE AS MOTORPAC_code, ub_term.name AS UBERON_tissue, mp_code.value AS p_value, collect(pubchem_term.name) AS pubchem_names
```



#



