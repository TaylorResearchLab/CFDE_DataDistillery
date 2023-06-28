

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

### Count HGNC nodes with TPM threshold
```
match (hgnc_cui:Concept)-[:CODE]-(hgnc_code:Code {SAB:'HGNC'})
match (hgnc_cui)-[:expresses]->(gtexexp_cui:Concept)-[:CODE]-(gtexexp_code:Code {SAB:'GTEXEXP'})
match (expbins_code:Code {SAB:'EXPBINS'})-[:CODE]-(expbins_cui:Concept)-[:has_expression]-(gtexexp_cui)
where expbins_code.lowerbound > 50
return count(hgnc_code)
```



