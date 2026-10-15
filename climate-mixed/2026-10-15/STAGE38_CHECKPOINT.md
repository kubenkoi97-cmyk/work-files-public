# Stage 38 — Hard conflict: Midea MI2-DL R32 vs R410A

**STOP — DO NOT IMPORT AFFECTED REFRIGERANT VALUES.**

The book already carried `R32` for three **exact** Russian SKU models on the basis of MirCli. Independent exact SKU cards on Envok instead show `R410A`:

| Exact SKU | Existing XLSX | Additional evidence |
|---|---|---|
| MI2-45DLDHN18(At) | R32 | R410A |
| MI2-90DLDHN18(At) | R32 | R410A |
| MI2-140DLDHN18(At) | R32 | R410A |

Source URLs and statuses: [STAGE38_MIDEA_DLD_CONFLICTS.csv](STAGE38_MIDEA_DLD_CONFLICTS.csv). Model-coded identification matches, but manufacturer-approved regional edition, compatibility and applicable outdoor system **have not** been determined.

**No conflicting refrigeration cell overwritten.** The three existing cells were highlighted red. The vendor's `R410A` pipe candidates were deliberately **not copied** into the still-empty piping cells: a common catalog SKU can reflect different revisions or compatible systems. Net mass/current were tracked as independent properties but still require an OEM edition audit before final.

The previously known Midea T3 `R410A` vs `R32` contradictions, Daikin FXMQ regional conflicts and other historical disputes remain open and are not hidden in these three new cases.
