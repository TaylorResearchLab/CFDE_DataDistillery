

# Use Case #4 Development queries 

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


