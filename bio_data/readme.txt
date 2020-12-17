cog_words_[bac/plasmid].txt

This file contains 'words' from bacterial genomes(or plasmids). 
Word are segments of the genome. A word is defined to be a maximal set of consecutive genes located on the same DNA strand. 
The genes are mapped to COGs. X denotes a gene that is not map to COG.
Two consecutive genes within the same word can be separated by at most two consecutive unmapped genes X.
This means, the if for example the genome is: 438	2274	X	0438	X	X	X	4641	X	0438	0438 
It is seperated to 2 different words: 438	2274	X	0438 and 4641	X	0438	0438
The genome of each bacterial strain is segmented to words as defined above.
An word example:
25#NC_009925#-1#Acaryochloris_marina_MBIC11017_uid58167#494	2319	0811	0848	0848	0226

25: is the word id
NC_009925: is the accession number of the chromosome or the plasmid
-1: is the strand in which the word was extracted from. 1 is the positive strand, -1 is the negative strand
Acaryochloris_marina_MBIC11017_uid58167: is the name of the genomic bacterial strain, correlates to the 'bacteria' field in taxa.txt
494: is the id of the strain, correlates to the 'strain_id' field in taxa.txt
2319	0811	0848	0848	0226: is the word itself, seperated by tabs. 2319 is COG2319 etc.


COG_INFO_TABLE.txt

This file has a description for each COG.
Each line is:
COG_id;COG functional category letter(s);COG functional category high level description of the first letter;COG functional category more specific description of the first letter;COG functional category high level description of the second letter;COG functional category more specific description of the second letter;...;Description of the COG group of genes

for example:
COG0028;EH;METABOLISM;Amino acid transport and metabolism;METABOLISM;Coenzyme transport and metabolism;Acetolactate synthase large subunit or other thiamine pyrophosphate-requiring enzyme;
COG 0028 belong to 2 functional categories: 
E - METABOLISM - Amino acid transport and metabolism
H - METABOLISM - Coenzyme transport and metabolism

The description of this COG is: "Acetolactate synthase large subunit or other thiamine pyrophosphate-requiring enzyme"


taxa.txt

Each line describes a bacterial strain:
kingdom,phylum,class,genus,species,bacteria,strain_id,bacgroup,order

bacteria: equal to the strain name in cog_words_[bac/plasmid].txt
strain_id: equal to the strain id in cog_words_[bac/plasmid].txt
