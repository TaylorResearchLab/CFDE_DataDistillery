

# Use Case #4 LINCS Use case

<u>For a specific drug transporter or drug processing enzyme, find the tissue where these transporters and enzymes are highly expressed (GTEx), and the drugs that may induce or suppress the expression of these genes (LINCS).</u>

### Starting with IDG
```
// start with IDG (pubchem to uniprot)
match (pubchem_code:Code {SAB:'PUBCHEM'})-[:CODE]-(pubchem_cui:Concept)-[:bioactivity]-(uniprot_cui:Concept)-[:CODE]-(uniprot_code:Code {SAB:"UNIPROTKB"})
match (uniprot_cui)-[:gene_product_of]-(hgnc_cui:Concept)-[:CODE]-(hgnc_code:Code {SAB:'HGNC'})
match (hgnc_cui)-[:expresses]->(gtexexp_cui:Concept)-[:CODE]-(gtexexp_code:Code {SAB:'GTEXEXP'})
// match the expression bins node and the uberon node
match (expbins_code:Code {SAB:'EXPBINS'})-[:CODE]-(expbins_cui:Concept)-[:has_expression]-(gtexexp_cui)-[:expressed_in]-(ub_cui:Concept)-[:CODE]-(co:Code {SAB:'UBERON'})
//match (ub_cui)-[:PREF_TERM]-(ub_term:Term {name:'hypothalamus'})
where expbins_code.lowerbound > 0.45
return * LIMIT 1
```

### Return TPM for every tissue above threshold for a given gene
```
// start with IDG (pubchem to uniprot)
match (pubchem_code:Code {SAB:'PUBCHEM'})<-[:CODE]-(pubchem_cui:Concept)-[:bioactivity]-(uniprot_cui:Concept)-[:CODE]->(uniprot_code:Code {SAB:"UNIPROTKB"})
match (uniprot_cui)-[:gene_product_of]->(hgnc_cui:Concept)-[:CODE]->(hgnc_code:Code {SAB:'HGNC'})-[:SY]->(hgnc_term:Term {name:'OAT1'})
match (hgnc_cui)-[:expresses]->(gtexexp_cui:Concept)-[:CODE]->(gtexexp_code:Code {SAB:'GTEXEXP'})
// match the expression bins node and the uberon node
match (expbins_code:Code {SAB:'EXPBINS'})<-[:CODE]-(expbins_cui:Concept)-[:has_expression]-(gtexexp_cui)-[:expressed_in]->(ub_cui:Concept)-[:CODE]->(ub_code:Code {SAB:'UBERON'})-[:PT]-(ub_term:Term)
where expbins_code.lowerbound > 0.45
//with ub_cui
//match (ub_cui)-[:PREF_TERM]->(ub_term:Term) //  {name:'hypothalamus'}
return DISTINCT ub_term.name AS TISSUE, expbins_code.lowerbound as TPM ORDER BY TPM DESCENDING

```

### Count HGNC nodes with TPM threshold
```
match (hgnc_cui:Concept)-[:CODE]-(hgnc_code:Code {SAB:'HGNC'})
match (hgnc_cui)-[:expresses]->(gtexexp_cui:Concept)-[:CODE]-(gtexexp_code:Code {SAB:'GTEXEXP'})
match (expbins_code:Code {SAB:'EXPBINS'})-[:CODE]-(expbins_cui:Concept)-[:has_expression]-(gtexexp_cui)
where expbins_code.lowerbound > 50
return count(hgnc_code)
```

### Latest finalized query WITH IDG
```
// start with IDG (pubchem to uniprot)
match (pubchem_term:Term)-[a]-(pubchem_code:Code {SAB:'PUBCHEM'})<-[:CODE]-(pubchem_cui:Concept)-[:bioactivity]-(uniprot_cui:Concept)-[:CODE]->(uniprot_code:Code {SAB:"UNIPROTKB"})-[b:PT]-(uniprot_term:Term)
match (uniprot_cui)-[:gene_product_of]->(hgnc_cui:Concept)-[:CODE]->(hgnc_code:Code {SAB:'HGNC'})-[:SY]->(hgnc_term:Term {name:'OAT1'})
match (hgnc_cui)-[:expresses]->(gtexexp_cui:Concept)-[:CODE]->(gtexexp_code:Code {SAB:'GTEXEXP'})
// match the expression bins node and the uberon node
match (expbins_code:Code {SAB:'EXPBINS'})<-[:CODE]-(expbins_cui:Concept)-[:has_expression]-(gtexexp_cui)-[:expressed_in]->(ub_cui:Concept)-[:CODE]->(ub_code:Code {SAB:'UBERON'})-[:PT]-(ub_term:Term)
//where expbins_code.lowerbound > 0.45
//with ub_cui
//match (ub_cui)-[:PREF_TERM]->(ub_term:Term) //  {name:'hypothalamus'}
match (hgnc_cui)-[pubchem_rel:positively_regulated_by {SAB:'LINCS'}]-(pubchem_cui2:Concept)-[:CODE]-(pubchem_code2:Code {SAB:'PUBCHEM'}) //-[:PT]-(pubchem_2_term:Term)
match (pubchem_cui2)-[:PREF_TERM]-(pubchem_2_term:Term)
return * LIMIT 1
```

###### use this to list tissues and their TPM for a gene: `return distinct ub_term.name, expbins_code.lowerbound as TPM order by TPM DESC`



###### No IDG, gets the nodes/edge that are attached to the UBERON tissue with the MAX() TPM value of the EXPBINS Codes lowerbound
```
match (hgnc_cui:Concept)-[:CODE]->(hgnc_code:Code {SAB:'HGNC'})-[:SY]->(hgnc_term:Term {name:'OAT1'})
match (hgnc_cui)-[:expresses]->(gtexexp_cui:Concept)-[:CODE]->(gtexexp_code:Code {SAB:'GTEXEXP'})
// match the expression bins node and the uberon node
match (expbins_code:Code {SAB:'EXPBINS'})<-[:CODE]-(expbins_cui:Concept)-[:has_expression]-(gtexexp_cui)-[:expressed_in]->(ub_cui:Concept)-[:CODE]->(ub_code:Code {SAB:'UBERON'})-[:PT]-(ub_term:Term)
match (hgnc_cui)-[pubchem_rel:positively_regulated_by {SAB:'LINCS'}]-(pubchem_cui2:Concept)-[:CODE]-(pubchem_code2:Code {SAB:'PUBCHEM'}) 
return * ORDER BY expbins_code.lowerbound DESC LIMIT 1
```

### Return gene TPM for the 5 CYP450 enzymes
```
WITH ['CYP1A2', 'CYP2C9', 'CYP2D6', 'CYP3A4',  'CYP3A5'] AS GENE_LIST
MATCH (gtexexp_code:Code {SAB:'GTEXEXP'})<-[:CODE]-(gtexexp_cui:Concept)<-[:expresses]-(hgnc_cui:Concept)-[:CODE]->(hgnc_code:Code {SAB:'HGNC'})-[]->(hgnc_term:Term)
WHERE hgnc_term.name IN GENE_LIST
MATCH (expbins_code:Code {SAB:'EXPBINS'})<-[:CODE]-(expbins_cui:Concept)-[:has_expression]-(gtexexp_cui)-[:expressed_in]->(ub_cui:Concept)-[:CODE]-(ub_code:Code {SAB:'UBERON'})
WITH REDUCE(m='',word in split(gtexexp_code.CODE,'-')[2..] | m+word+' ') AS tissueStr, expbins_code.lowerbound AS TPM_lb,expbins_code.upperbound AS TPM_ub, hgnc_term.name AS Gene
RETURN DISTINCT Gene, tissueStr, TPM_lb,TPM_ub ORDER BY TPM_lb DESC LIMIT 5
```

### Return PUBCHEM IDs as well
```
WITH ['CYP1A2', 'CYP2C9', 'CYP2D6', 'CYP3A4',  'CYP3A5'] AS GENE_LIST
MATCH (hgnc_cui:Concept)-[:CODE]->(hgnc_code:Code {SAB:'HGNC'})-[]->(hgnc_term:Term)
WHERE hgnc_term.name IN GENE_LIST
MATCH (hgnc_cui)-[:expresses]->(gtexexp_cui:Concept)-[:CODE]->(gtexexp_code:Code {SAB:'GTEXEXP'})
MATCH (expbins_code:Code {SAB:'EXPBINS'})<-[:CODE]-(expbins_cui:Concept)-[:has_expression]-(gtexexp_cui)-[:expressed_in]->(ub_cui:Concept)-[:CODE]-(ub_code:Code {SAB:'UBERON'})
WITH REDUCE(mergedString='',word in split(gtexexp_code.CODE,'-')[2..] | mergedString+word+' ') AS tissueStr, expbins_code.lowerbound AS TPM_lb, expbins_code.upperbound AS TPM_ub,
hgnc_term.name AS Gene, hgnc_cui
MATCH (hgnc_cui)-[:positively_regulated_by {SAB:'LINCS'}]-(pubchem_cui:Concept)-[:CODE]-(pubchem_code:Code {SAB:'PUBCHEM'})
RETURN DISTINCT Gene, tissueStr, COLLECT(pubchem_code.CodeID) AS PUBCHEM_IDs LIMIT 5
```

-- add tissue specification

#### Show how many genes are effected by these compounds in the liver vs in the kidney vs in the heart

Compounds that inhibit CYP450 enzymes we want to check


# Tahas queries







