

# __Schemas of the various DCCs__
#### _Link to each DCCs section here_ 
### **MOTORPAC:**
#### Description of schema
#### screenshot_here
#[!]()
###### Query to generate schema screenshot
`match (mp_code:Code {SAB:'MOTORPAC'})-[r1:CODE]-(mp_cui:Concept)-[r2:RO_0001025]-(ub_cui:Concept)-[r3:CODE]-(ub_code:Code {SAB:'UBERON'})-[r9:PT]-(ub_term:Term)
match (ensembl_code:Code {SAB:'ENSEMBL'})-[r4:CODE]-(ensembl_cui:Concept)-[r5:associated_with]-(mp_cui)-[r6:gender]-(pato_cui:Concept)-[r7:CODE]-(pato_code:Code {SAB:'PATO'})-[r8:PT]-(pato_term:Term)
return * LIMIT 1`
