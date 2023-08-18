

# Schemas of the various DCCs
#### Jump to DCC section:

[MOTORPAC](#motorpac)  
[Kids First](#kids-first)

----
## **MOTRPAC**
<img src="https://github.com/TaylorResearchLab/CFDE_DataDistillery/blob/main/images/MOTORPAC_SCHEMA_2.png" width="900" height="500">

###### MOTRPAC
```
match (mp_code:Code {SAB:'MOTORPAC'})-[r1:CODE]-(mp_cui:Concept)-[r2:RO_0001025]-(ub_cui:Concept)-[r3:CODE]-(ub_code:Code {SAB:'UBERON'})-[r9:PT]-(ub_term:Term) 
match (ensembl_code:Code {SAB:'ENSEMBL'})-[r4:CODE]-(ensembl_cui:Concept)-[r5:associated_with]-(mp_cui)-[r6:gender]-(pato_cui:Concept)-[r7:CODE]-(pato_code:Code {SAB:'PATO'})-[r8:PT]-(pato_term:Term) 
return * LIMIT 1

Data Dictionary Schema Query:
MATCH (mp_cui:Concept)-[:CODE]->(mp_code:Code {SAB:'MOTRPAC'}) 
WHERE mp_code.CODE CONTAINS 'liver'
MATCH (mp_cui)-[:associated_with {SAB:'MOTRPAC'}]-(ensRat_cui:Concept)-[:CODE]->(ensRat_code:Code {SAB:'ENSEMBL'})
MATCH (ensRat_cui)-[:has_human_ortholog]-(ensHum_cui:Concept)-[:CODE]-(ensHum_code:Code {SAB:'ENSEMBL'})-[:GENCODE_PT]-(ensHum_term:Term)
MATCH (ensHum_cui)-[:RO ]-(hgnc_cui:Concept)-[:CODE]-(hgnc_code:Code {SAB:'HGNC'})-[:ACR]-(hgnc_term:Term)
MATCH (mp_cui)-[:sex {SAB:'MOTRPAC'}]->(pato_cui:Concept)-[:PREF_TERM]-(pato_term:Term)
RETURN * LIMIT 1
```
----

## **Kids First**
<img src="https://github.com/TaylorResearchLab/CFDE_DataDistillery/blob/main/images/KF_SCHEMA.png" width="900" height="500">

###### Gabriella Miller Kids First 
```
match (kfpt_code:Code {SAB:'KFPT'})-[:CODE]-(kfpt_cui:Concept)-[:has_phenotype]-(hpo_cui:Concept)-[:CODE]-(hpo_code:Code {SAB:'HPO'}) 
match (kfpt_cui)-[:belongs_to_cohort]-(cohort_cui:Concept)-[:CODE]-(cohort_code:Code)-[rn]-(cohort_term:Term)
match (cohort_cui)-[:belongs_to_cohort]-(varbin_cui:Concept)-[:CODE]-(varbin_code:Code {SAB:'KFVARBIN'})
//match (varbin_cui)-[:location_has_variants]-(chlo_cui:Concept)-[:CODE]-(chlo_code:Code {SAB:'HSCLO'})
return * LIMIT 1
```

## GTEx
###### GTEXEXP
```
match (gtex_exp:Concept)-[r0]-(gtex_exp_code:Code) where gtex_exp_code.SAB = 'GTEXEXP' 
match (gtex_exp)-[r1]-(hgnc_concept:Concept)-[r2]-(hgnc_code:Code) where hgnc_code.SAB = 'HGNC'
match (gtex_exp)-[r3]-(ub_concept:Concept)-[r4]-(ub_code:Code) where ub_code.SAB = 'UBERON'
match (gtex_exp)-[r5]-(exp_concept:Concept)-[r6]-(exp_code:Code) where exp_code.SAB = 'EXPBINS' 
return * limit 1
```
###### GTEXEQTL
```
match (gtex_exp:Concept)-[r0]-(gtex_exp_code:Code) where gtex_exp_code.SAB = 'GTEXEQTL' 
match (gtex_exp)-[r1:located_in]-(hgnc_concept:Concept)-[r2]-(hgnc_code:Code) where hgnc_code.SAB = 'HGNC'
match (gtex_exp)-[r3:located_in]-(ub_concept:Concept)-[r4]-(ub_code:Code) where ub_code.SAB = 'UBERON'
match (gtex_exp)-[r5:p_value]-(exp_concept:Concept)-[r6]-(exp_code:Code) where exp_code.SAB = 'PVALUEBINS'  
//match  (gtex_exp)-[r7]-(hsclo_concept:Concept)-[r8]-(hsclo_code:Code) where hsclo_code.SAB = 'HSCLO'  
return * limit 1
```


## ERCC
###### ERCCREG (Regulary Elements)
```
match (eca_cui:Concept)-[:CODE]-(eca_code:Code {SAB:'ENCODE.CCRE.ACTIVITY' })
match (eca_cui)-[:regulates {SAB:'ERCCREG'}]-(ens_cui:Concept)-[:CODE]-(ens_code:Code {SAB:'ENSEMBL'}) 
match (eca_cui)-[:part_of{SAB:'ERCCREG'}]-(ub_cui:Concept)-[:CODE]-(ub_code:Code {SAB:'UBERON'}) 
match (eca_cui)-[:part_of{SAB:'ERCCREG'}]-(ec_cui:Concept)-[:CODE]-(ec_code:Code {SAB:'ENCODE.CCRE'}) 
match (eca_cui)-[:isa{SAB:'ERCCREG'}]-(ech_cui:Concept)-[:CODE]-(ech_code:Code {SAB:'ENCODE.CCRE.H3K4ME3'}) 
match (eca_cui)-[:isa{SAB:'ERCCREG'}]-(ech2_cui:Concept)-[:CODE]-(ech2_code:Code {SAB:'ENCODE.CCRE.H3K27AC'}) 
match (eca_cui)-[:isa{SAB:'ERCCREG'}]->(ecc_cui:Concept)-[:CODE]-(ecc_code:Code {SAB:'ENCODE.CCRE.CTCF'}) 
match (ec_cui)-[:located_in{SAB:'ERCCREG'}]-(car_cui:Concept)-[:CODE]-(car_code:Code {SAB:'CLINGEN.ALLELE.REGISTRY'}) 
match (car_cui)-[:part_of {SAB:'ERCCREG'}]-(eqtl_cui:Concept)-[:CODE]-(eqtl_code:Code {SAB:'GTEXEQTL'})
match (eqtl_cui)-[{SAB:'ERCCREG'}]-(ens2_cui:Concept)-[:CODE]-(ens2_code:Code {SAB:'ENSEMBL'})
return * limit 1
```

###### ERCCRBP (exRNA RBP)     missing ENCODE.RBS.HepG2 and ENCODE.RBS.HepG2.K562 CUIs
match (t:Term)-[q]-(eR150_cui:Concept)-[:CODE]-(er150_code:Code {SAB:'ENCODE.RBS.150.NO.OVERLAP' })
match (eR150_cui)-[:overlaps {SAB:"ERCCRBP"}]-(ens_cui:Concept)-[:CODE]-(ens_code:Code {SAB:'ENSEMBL'}) 
//match (eR150_cui)-[r:is_subsequence_of {SAB:"ERCCRBP"}]-(erh_cui:Concept)-[:CODE]-(erh_code:Code {SAB:'ENCODE.RBS.HepG2'}) 
match (eR150_cui)-[:is_subsequence_of {SAB:"ERCCRBP"}]-(erk_cui:Concept)-[:CODE]-(erk_code:Code {SAB:'ENCODE.RBS.K562'}) 
//match (eR150_cui)-[:is_subsequence_of {SAB:"ERCCRBP"}]-(erhk_cui:Concept)-[:CODE]-(erhk_code:Code {SAB:'ENCODE.RBS.HEPG2.K562'}) 
match (eR150_cui)-[:correlated_in {SAB:"ERCCRBP"}]-(ub_cui:Concept)-[:CODE]-(ub_code:Code {SAB:'UBERON'}) // edge could also = 'not_correlated_in'
match (ub_cui)-[:predicted_in {SAB:"ERCCRBP"}]-(uni_cui:Concept)-[:CODE]-(uni_code:Code {SAB:'UNIPROTKB'}) // edge could also be 'not_predicted_in'
match (uni_code2:Code {SAB:'UNIPROTKB'})-[:CODE]-(uni_cui2:Concept)-[:molecularly_interacts_with {SAB:"ERCCRBP"}]-(erK2_cui:Concept)-[:CODE]-(erK2_code:Code {SAB:'ENCODE.RBS.K562'})
return * limit 1



## IDG
###### IDGP (compound to protein)

```
match (pubchem_code:Code {SAB:'PUBCHEM'})-[:CODE]-(pubchem_cui:Concept)-[:bioactivity {SAB:'IDGP'}]-(uniprot_cui:Concept)-[:CODE]-(uniprot_code:Code {SAB:"UNIPROTKB"})
match (pubchem_cui)-[:PREF_TERM]-(t:Term)
match (uniprot_cui)-[:PREF_TERM]-(t2:Term)
return * limit 1
```

###### IDGD (compound to disease)

```
match (pubchem_code:Code {SAB:'PUBCHEM'})-[:CODE]-(pubchem_cui:Concept)-[:indication {SAB:'IDGD'}]-(snomed_cui:Concept)-[:CODE]-(snomed_code:Code {SAB:"SNOMEDCT_US"})
match (pubchem_cui)-[:PREF_TERM]-(t:Term)
match (snomed_cui)-[:PREF_TERM]-(t2:Term)
return * limit 1
```

## GLYGEN



## LINCS



## SPARC


## METABOLICS WORKBENCH



