# rq-count\_v1

***

*In Silico* Workflow for Calculating the Richness of Gene Deletion Mutants in Mixed Samples from Raw Paired-End Short-Read Whole Genome Sequencing Data

# Introduction

***

rq-count\_v1 is a comprehensive *in silico* workflow designed to simplify the processing of raw paired-end short-read whole genome sequencing (WGS) data derived from bacterial samples containing various gene-deletion mutant strains. This workflow includes a well-structured Snakemake script for reads pre-processing and mapping. Additionally, the "scripts" folder houses corresponding Python scripts that allow for the extraction of mapping information and the calculation of mutant richness within the sample.

## Key Features

***

* **Snakemake Script:** The provided Snakemake script efficiently handles reads pre-processing and mapping, ensuring a smooth and organized workflow.
* **Python Scripts:** The "scripts" folder houses Python scripts that enable users to extract mapping information and calculate the richness of gene deletion mutants in their samples.

# Dependencies

***

1. [python 3.11.3](https://www.python.org/) and following librarires are required;

* [Biopython 1.79](https://biopython.org/)
* [pandas 1.4.2](https://pandas.pydata.org/)
* [scikit-learn 1.1.1](https://scikit-learn.org/)

2. [snakemake 7.25.3](https://snakemake.github.io/);
3. [conda 23.5.0](https://docs.conda.io/);

# Workflow overview

***

![](workflow_overview.png?raw=true)

* Overview of rq-count\_v1 workflow.

# Quick Start (run it on Linux system)

***

## Installation

* [ ]  git clone the rq-count\_v1 folder to your local computer;

```
$ git clone https://github.com/china-fix/rq-count_v1.git
```

* [ ]  export the rq-count\_v1 folder to PATH (optional);
* [ ]  install conda and create a new snakemake env;

```
$ conda install -n base -c conda-forge mamba
$ conda activate base
$ conda activate snakemake
$ snakemake --help
```

* [ ]  install python biopython pandas scikit-learn

```
$ conda install python biopython pandas scikit-learn -n snakemake
```

## Usage

### Raw reads pre-processing and mapping

* [ ] In your working folder, establish a structured directory with the following arrangement:

1. The primary directory is named "in."
2. Inside the "in" directory, create a subfolder named "REF."In this "REF" subfolder, you should place the reference genome in FASTA format. Ensure that the reference file is named with a ".REF" extension. For example, you can name it "reference\_genome.fasta.REF."
3. Alongside the "REF" subfolder, place your raw sequencing reads data files. Each sample should consist of two files, typically denoted as "\_1.fq.gz" and "\_2.fq.gz" to represent the paired-end reads.
    For instance, if you have two samples, "sample1" and "sample2," you would place their corresponding read files as "your\_raw\_reads\_sample1\_1.fq.gz," "your\_raw\_reads\_sample1\_2.fq.gz," "your\_raw\_reads\_sample2\_1.fq.gz," and "your\_raw\_reads\_sample2\_2.fq.gz."
    This organized folder structure will facilitate efficient data management and analysis for your sequencing project.

```.
└── in
    ├── REF
    │   └── your_reference_fasta_file.REF
    ├── your_raw_reads_sample1_1.fq.gz
    ├── your_raw_reads_sample1_2.fq.gz
    ├── your_raw_reads_sample2_1.fq.gz
    └── your_raw_reads_sample2_2.fq.gz
```

* [ ] run the command in your working direcotry

```
snakemake -s Snakefile -c 8 --use-conda
```

* [ ] New folder named `report` will be created in your working directory, the `.tab` file recorded the mapping depth which is comare with our python script `relative_mapping_caculation_V2.0.py `

### Calculate the relative richness of deletion-mutant

* [ ] prepare a fasta file recording all your gene-deletion sequence, the format looks like below
```
>KO_gene1
tacagcaacggactgaagaagtaaaacagtcgctcggcgacacgttgccataatggacgttttagccataaacgggcatcgagcagacgtgaacgcgaaatataatcgtcctgaacggcggcgaggtcagcaccaaaacctttatcgtcgattgccagggtaatctcgaaatttagccacagactacgcatatcaaggttaactgtgccaaccagacttagttcgccatcgaccagcacgctcttggtatgcagtaacccgccttcaaactgataaattttaaccccagcagccagcagttccgtaaagaatgcgcgactggcccagccgaccagcatcgagtcattttttcgcggaaggataatactgacatccaccccgcgctgcgccgccgtgcaaatcgcatgaagtaaatcatcgcttggcacaaagtagggcgtggtcatgatcaaatattcacgcgccgaataagccgcagtcaataatgcctggtgaatgagatcttccggaaagccggggccagaagcaattgtgtgaatggtgtgaccgctggcctgttcaaacggcataatattgacatctggtggtggcggcagaatacgttttccggtttcaatctcccagtcgcaggaataaataatccccatcgcggtggcgatagggccttccatacgcgccatcagatcaatccattgccctacgcccgcatcttgtttgaagtagcgaggatcgaccatattcatgctgccggtgtacgcgatgtaattatcgatcatgatcatcttgcgatgttggcgcaggtccatacggcgtaaaaacacacgcatcagattgacctttaaggcttcgaccacttcaataccggcattacgcattagctcgggccacgggctgcggaaaaaagccacactcccggcggagtcgagcatcaatcggcaatgaatgccgcgtcgcgcagccgccattaatgattcagccacctggtccgccatgccgccgggctgccagatataaaacaccatctcaatattatggcgcgcgagctggatgtcgcggattaacgcctgcatcacatcatctgactcggtcatcagttgtagctgattccctttgaccccagcgatcccctgacgacgctcgcaaagcttgaataatggcgcagcgacactgctattttcttcggcgaagatatgcttacaggctttaaggtcgttaagccattttgcggtggaaggccacatcgctctggcgcgctcagcgcggcgtttgcctaaatggagctcgccaacggcaagataggcaataattccgactaacggcagaatgtaaataatcaacagccaggccatcgcggagggaactgcgcgtcgtttcattagaatgcgtaaagttacgcctgcaatgagcaaccagtatcccagaatggccaaccaactcaccaacgtataaacggttgtcat
>KO_gene2
atgaataaaatcctgttagttgatgatgaccgagagctgacttattaaaggagctgctcgagatggaaggcttcaacgtgattgttgcccacgatggggaacaggcgcttgatcttctggacgacagcattgatttacttttgcttgacgtaatgatgccgaagaaaaatggtatcgacacattaaaagcacttcgccagacacaccagacgcctgtcattatgttgacggcgcgcggcagtgaacttgatcgcgttctcggccttgagctgggcgcagatgactatctcccgaaaccgtttaatgatcgtgagctggtggcacgtattcgcgcgatcctgcgccgttcgcactggagcgagcaacagcaaaacaacgacaacggttcaccgacactggaagttgatgccttagtgctgaatccaggccgtcaggaagccagcttcgacgggcaaacgctggagttaaccggtactgagtttaccctgctctatttgctggcacagcatctgggtcaggtggtttcccgtgaacatttaagccaggaagtgttgggcaaacgcctgacgcctttcgaccgcgctattgatatgcacatttccaacctgcgtcgtaaactgccggatcgtaaagatggtcacccgtggtttaaaaccttgcgtggtcgcggctatctgatggtttctgcttcatga
>KO_gene3
aatcagcccggtaataacggacaagaccgcgacccgtggggaagcagcaaacctggcggcaactctgagggaaatggaaacaaaggcggtcgcgatcaagggccacctgatttagatgatatcttccgcaaactgagcaaaaagctcggtggtctgggcggcggtaaaggcaccggatctggcggtggcagttcatcgcaaggcccgcgcccgcagcttggcggtcgtgtcgttaccatcgcagcggcagcgattgtcattatctgggcggccagtggtttctataccattaaagaagccgaacgcggcgtggtaacacgctttggtaaattcagccatctggttgagccgggtctgaactggaaaccgacgtttatcgacgaagtcaaaccggtgaacgtggaagccgtgcgtgaactggccgcttctggtgtgatgctgacgtcggacgagaacgtagtgcgcgttgagatgaacgtgcagtaccgcgtcaccaatccggaaaaatatctgtatagcgtgaccagcccggatgacagcctgcgtcaggctaccgacagcgccctgcgtggagttatcggtaaatacaccatggaccgcattctgacggaaggtcgtaccgtgattcgtagcgatactcagcgcgaactggaagagacgattcgtccgtatgacatgggtatcacgctgctggacgtcaacttccaggctgctcgtccgccggaagaagtaaaagcggcgtttgacgatgcgattgccgcgcgtgaaaacgaacagcaatacattcgtgaagcagaagcgtataccaacgaagttcagccgcgtgcgaacggtcaggcgcaacgtatcctcgaagaggcgcgtgcgtacaaggcccagaccatcctggaagctcagggtgaagtggcgcgctttgctaaacttctgccggaatataaagccgcgccggaaattactcgcgagcgtctgtatatcgagacgatggaaaaagtgttgggtaacacccgcaaagtgctggttaacgataaaggtggcaacctgatggttctgccgttagaccagatgctgaaaggtggtaacgcccctgcggcgaagagcgataacggtgccagcaatctgctgcgtctgccgccagcctcttcctccacaaccagtggagcaagcaacacgtcgtccaccagtcagggcgatattatggaccaacgccgcgccaacgcgcagcgtaacgactaccagcgtcagggggaataacgatgcgtaagtcagttatcgcgattatcatcatcgtgctggtagtgctttacatgtctgtctttgtcgtcaaagaaggtgagcgcggtattacgctgcgttttggtaaggtactgcgtgacgatgacaacaaacctctggtttatgagccgggtctgcatttcaagataccgttcattgaaacggtgaaaatgctcgacgcacgtattcagaccatggacaaccaggccgaccgctttgtgaccaaagagaagaaagacctgatcgtcgactcttacatcaaatggcgcatcagcgatttcagccgttactacctggcaacgggtggtggcgacatttcgcaagcggaagtgctgttgaaacgtaagttctctgaccgtctgcgttctgaaattggtcgcctggacgtgaaagatatcgtcaccgattcccgtggtcgtctgaccctcgaagtacgtgacgcgctgaactccggttctgcgggtacagaagatgaagttactaccccggcggcagataacgccattgccgaagcggcagagcgcgtaacggctgagacgaagggcaaagttccggtcatcaacccgaacagtatggcggcgctgggtattgaagttgtcgatgtgcgtatcaagcagatcaacctgccgaccgaagtgtctgaagcgatctacaaccgtatgcgcgccgagcgtgaagcggtagcgcgtcgtcaccgttcacaaggtcaggaagaagcggaaaaactgcgcgcgactgccgactatgaagtgaccagaacgctggcagaagctgagcgtcagggccgcatcatgcgtggtgaaggcgatgccgaagcagccaaactgtttgctgatgcattcagtaaagatccggacttctacgcattcatccgtagcctgcgtgcttatgagaacagcttctctggcaatcaggacgtgatggtcatgagcccggatagcgatttcttccgctacatgaagacgccgacttccgca
...
```

#### Usage: relative_mapping_caculation_V2.0.py

```
options:
  -h, --help            show this help message and exit
  --MAPPING_REF FILENAME
                        the fasta filename you used for bwa mapping reference
  --TARGETS FILENAME    the fasta file includes all the tested gene sequences you want to measure
  --DEPTH_TAB FILENAME  the tab file describe the mapping depth of every base
  --CUTLEN DEFAULT 5000
                        the flanking seq length for target catulation part (extracted for model learning)
  --FIXLEN FIXLEN       flanking seq length you want to drop near the deletion edge location (default is 0)
  --OUT FILENAME        Output file name, report as default
  --DEV                 for developping and testing only normal user can just ignore this
```
# Scaling proportion of individual deletion mutants based on median values (optional)
The method described subjects bacterial mutants in equal proportions to macrophage infection assays, expressing the result as a relative fitness of each mutant, based on comparison to the original (1:1:1:1 in our case) proportion. However, this may not provide an optimal measure of relative fitness across different sets. For instance, if one mutant shows a very low survival ability in mixed pools after 2 h of macrophage infection, other mutants in the pool will appear as artificially good survivors at this time point because the largely reduced proportion of one mutant will be passively occupied by the others. To address this, we introduced a scaling method to normalize proportion values across different sets. This involves identifying the median proportion value in each set and calculating the scaling factor by taking the reciprocal of the median value. Subsequently, this scaling factor is applied to adjust all proportion values (each value is multiplied by the scaling factor) within the set. This approach ensures that the median value becomes 1 across all different sets, while other values are appropriately scaled. We refer to these normalized values as Relative Fitness (RF) values.
* [ ] Note: comments for this method:
We nervous about this scaling method to normalize proportion values (Relative Fitness). In the absence of a wild-type control strain these values may not encompass the possibility that mutants may, in fact, all be better (or all be worse) than wild-type at growing under certain conditions. So, adding a control strain (perhaps with a deletion in a region known to have no effect on growth behavior, perhaps a pseudogene) to each mix would be necessary to allow a more stable and reliable normalization. Total signal is fine as normalization for mixes of a high number of mutants (most of which are not expected to show a phenotype), but in cases of only a handful of these, normalization based on a control strain might be more prudent.


# Citation

....

# Acknowledgments

