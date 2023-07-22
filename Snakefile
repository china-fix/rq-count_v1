import os

relative_dir = os.path.dirname(os.path.abspath(workflow.snakefile))

configfile: relative_dir+"/config/config.yaml"
# print(config["general_config"]["threads_n"])

SAMPLES, = glob_wildcards("in/{sample}1.fq.gz")
REFS, = glob_wildcards("in/REF/{ref}")




include: "rules/fastp.smk"
include: "rules/mapping.smk"
include: "rules/picard_rmdup.smk"



rule all:
    input:
        #fastp
        # expand("out_clean_read/{sample}1.fq.gz", sample=SAMPLES),
        # expand("out_clean_read/{sample}2.fq.gz", sample=SAMPLES),
        #bwa
        # expand("out_mapping/{sample}_{ref}.sam", sample=SAMPLES, ref=REFS),
        #samtools
        # expand("out_mapping/{sample}_{ref}.bam", sample=SAMPLES, ref=REFS),
        # expand("out_mapping/{sample}_{ref}.bam.sorted", sample=SAMPLES, ref=REFS),
        #bedtools
        expand("report/{sample}_{ref}.tab", sample=SAMPLES, ref=REFS),
        expand("report/{sample}_{ref}_rmdup.tab", sample=SAMPLES, ref=REFS),
        