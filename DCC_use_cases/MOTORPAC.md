# MOTORPAC Use Case
[Google Doc to MOTORPAC use cases](https://docs.google.com/spreadsheets/d/1Z1rStygHvT3zBQIDmD61No4U3YogkpglpDxJlD4tIfk/edit#gid=0)

# 1) MoTrPAC Genes affected by exercise, are expressed in matched tissues in humans in GTEx, that are either matches or inverse matches of a perturbation signal in LINCS = compounds or perturbations that might promote or interfere with exercise benefit b) (FUTURE) Genes that are circadian in rat, are a signature match to perturbation in LINCS = compounds that might affect circadian rhythms/behaviors 
```
code
```

# 2) MoTrPAC Genes affected by exercise, are expressed in matched tissues in humans in GTEx, that are either matches or inverse matches of a perturbation signal in LINCS = compounds or perturbations that might promote or interfere with exercise benefit b) (FUTURE) Genes that are circadian in rat, are a signature match to perturbation in LINCS = compounds that might affect circadian rhythms/behaviors 
```
code
```

# 3) Find KF (or other) SNPs or mutations that lead to loss or gain of glycosylation site from GlyGen data, and how many of those genes are expressed in the GTEx liver dataset AND in the MoTrPAC liver data are a Rat-human expression match in liver AND are output RNA-protein correlate in liver
```
code
```

# 4) For a specific drug processing enzyme, find the tissue and assays where these enzymes are highly expressed in the MoTrPAC young adult rats endurance training exercise data, and the related drug profiles in LINCS data.
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
//MATCH (mp_cui)-[:located_in {SAB:'MOTORPAC'}]-(ub_cui:Concept)//-[:CODE]-(ub_code {SAB:'UBERON'})-[:SY]-(ub_term:Term)
RETURN DISTINCT hgnc_term.name AS gene, pubchem_term.name AS LINCS_edge, ub_term.name AS UBERON_tissue, mp_code.CODE AS MOTORPAC_code
//RETURN * LIMIT 1
```



#


