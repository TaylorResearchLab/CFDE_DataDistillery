

# Schemas of the various DCCs
#### Jump to DCC:
 
[KidsFirst](#query-to-generate-schema-screenshot)

### **MOTORPAC**
#### Description of schema
The MOTORPAC node is located in the center and has edges with....
<img src="https://github.com/TaylorResearchLab/CFDE_DataDistillery/blob/main/images/MOTORPAC_SCHEMA.png" width="900" height="500">

###### Query to generate schema screenshot
```
match (mp_code:Code {SAB:'MOTORPAC'})-[r1:CODE]-(mp_cui:Concept)-[r2:RO_0001025]-(ub_cui:Concept)-[r3:CODE]-(ub_code:Code {SAB:'UBERON'})-[r9:PT]-(ub_term:Term) 
match (ensembl_code:Code {SAB:'ENSEMBL'})-[r4:CODE]-(ensembl_cui:Concept)-[r5:associated_with]-(mp_cui)-[r6:gender]-(pato_cui:Concept)-[r7:CODE]-(pato_code:Code {SAB:'PATO'})-[r8:PT]-(pato_term:Term) 
return * LIMIT 1
```


### **Kids First**



