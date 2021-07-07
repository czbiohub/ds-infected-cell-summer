FASTQ_DIR1=/mnt/ibm_lg/jacklyn.luu/fastqs/
FASTQ_DIR2=/mnt/ibm_lg/elianna/fastqs/
OUTPUT_DIR=/mnt/ibm_lg/elianna/output

# HAV_library_A HAV_library_B DENV_library_A DENV_library_B HCV_library_A
#EV_library_A EV_library_B RV_library_A RV_library_B Wang_229E_library_A Wang_229E_library_B Wang_OC43_library_A Wang_OC43_library_B Wang_SARS-CoV2_library_A Wang_SARS-CoV2_library_B

all:HCV_library_B

# HAV_library_A:
# 	nextflow run \
# 		olgabot/crispr-screen-nf \
# 		-r patch-2 \
# 		--treatment_fastq ${FASTQ_DIR1}/$@/'HAV*fastq.gz' \
# 		--control_fastq ${FASTQ_DIR1}/$@/'control*fastq.gz' \
# 		--library ${FASTQ_DIR1}/$@/Human_GeCKOv2_Library_A_3_mageck.csv \
# 		--output_prefix $@ \
# 		--output ${OUTPUT_DIR}
# 
# HAV_library_B:
# 	nextflow run \
#                 olgabot/crispr-screen-nf \
#                 -r patch-2 \
#                 --treatment_fastq ${FASTQ_DIR1}/$@/'HAV*fastq.gz' \
#                 --control_fastq ${FASTQ_DIR1}/$@/'control*fastq.gz' \
#                 --library ${FASTQ_DIR1}/$@/Human_GeCKOv2_Library_B_1_mageck.csv \
#                 --output_prefix $@ \
#                 --output ${OUTPUT_DIR}
# 
# DENV_library_A:
# 	nextflow run \
#                 olgabot/crispr-screen-nf \
#                 -r patch-2 \
#                 --treatment_fastq ${FASTQ_DIR2}/$@/'*treatment.fastq.gz' \
#                 --control_fastq ${FASTQ_DIR2}/$@/'*control.fastq.gz' \
#                 --library ${FASTQ_DIR2}/$@/Human_GeCKOv2_Library_A_3_mageck.csv \
# 		--output_prefix $@ \
#                 --output ${OUTPUT_DIR}
# DENV_library_B:
# 	nextflow run \
#                 olgabot/crispr-screen-nf \
#                 -r patch-2 \
#                 --treatment_fastq ${FASTQ_DIR2}/$@/'*treatment.fastq.gz' \
#                 --control_fastq ${FASTQ_DIR2}/$@/'*control.fastq.gz' \
#                 --library ${FASTQ_DIR2}/$@/Human_GeCKOv2_Library_B_1_mageck.csv \
#                 --output_prefix $@ \
# 		--output ${OUTPUT_DIR}
# 
# HCV_library_A:
# 	nextflow run \
#                 olgabot/crispr-screen-nf \
#                 -r patch-2 \
#                 --treatment_fastq ${FASTQ_DIR2}/$@/'*treatment.fastq.gz' \
#                 --control_fastq ${FASTQ_DIR2}/$@/'*control.fastq.gz' \
#                 --library ${FASTQ_DIR2}/$@/Human_GeCKOv2_Library_A_3_mageck.csv \
#                 --output_prefix $@ \
#                 --output ${OUTPUT_DIR}
# 
HCV_library_B:
	nextflow run \
                 olgabot/crispr-screen-nf \
                 -r patch-2 \
                 --treatment_fastq ${FASTQ_DIR2}/$@/'*treatment.fastq.gz' \
                 --control_fastq ${FASTQ_DIR2}/$@/'*control.fastq.gz' \
                 --library ${FASTQ_DIR2}/$@/Human_GeCKOv2_Library_B_1_mageck.csv \
                 --output_prefix $@ \
                 --output ${OUTPUT_DIR}
 
# EV_library_A:
# 	 nextflow run \
#                 olgabot/crispr-screen-nf \
#                 -r patch-2 \
#                 --treatment_fastq ${FASTQ_DIR2}/$@/'*treatment.fastq.gz' \
#                 --control_fastq ${FASTQ_DIR2}/$@/'*control.fastq.gz' \
#                 --library ${FASTQ_DIR2}/$@/Human_GeCKOv2_Library_A_3_mageck.csv \
#                 --output_prefix $@ \
#                 --output ${OUTPUT_DIR}
# 
# EV_library_B:
# 	nextflow run \
#                 olgabot/crispr-screen-nf \
#                 -r patch-2 \
#                 --treatment_fastq ${FASTQ_DIR2}/$@/'*treatment.fastq.gz' \
#                 --control_fastq ${FASTQ_DIR2}/$@/'*control.fastq.gz' \
#                 --library ${FASTQ_DIR2}/$@/Human_GeCKOv2_Library_B_1_mageck.csv \
#                 --output_prefix $@ \
#                 --output ${OUTPUT_DIR}
# 
# RV_library_A:
# 	nextflow run \
#                 olgabot/crispr-screen-nf \
#                 -r patch-2 \
#                 --treatment_fastq ${FASTQ_DIR2}/$@/'*treatment.fastq.gz' \
#                 --control_fastq ${FASTQ_DIR2}/$@/'*control.fastq.gz' \
#                 --library ${FASTQ_DIR2}/$@/Human_GeCKOv2_Library_A_3_mageck.csv \
#                 --output_prefix $@ \
#                 --output ${OUTPUT_DIR}
# 
# RV_library_B:
# 	nextflow run \
#                 olgabot/crispr-screen-nf \
#                 -r patch-2 \
#                 --treatment_fastq ${FASTQ_DIR2}/$@/'*treatment.fastq.gz' \
#                 --control_fastq ${FASTQ_DIR2}/$@/'*control.fastq.gz' \
#                 --library ${FASTQ_DIR2}/$@/Human_GeCKOv2_Library_B_1_mageck.csv \
#                 --output_prefix $@ \
#                 --output ${OUTPUT_DIR}
# 
# Wang_229E_library_A:
# 	nextflow run \
#                 olgabot/crispr-screen-nf \
#                 -r patch-2 \
#                 --treatment_fastq ${FASTQ_DIR2}/$@/'*treatment.fastq.gz' \
#                 --control_fastq ${FASTQ_DIR2}/$@/'*control.fastq.gz' \
#                 --library ${FASTQ_DIR2}/$@/Human_GeCKOv2_Library_A_3_mageck.csv \
#                 --output_prefix $@ \
#                 --output ${OUTPUT_DIR}
# 
# Wang_229E_library_B:
# 	nextflow run \
#                 olgabot/crispr-screen-nf \
#                 -r patch-2 \
#                 --treatment_fastq ${FASTQ_DIR2}/$@/'*treatment.fastq.gz' \
#                 --control_fastq ${FASTQ_DIR2}/$@/'*control.fastq.gz' \
#                 --library ${FASTQ_DIR2}/$@/Human_GeCKOv2_Library_B_1_mageck.csv \
#                 --output_prefix $@ \
#                 --output ${OUTPUT_DIR}
# Wang_OC43_library_A:
# 	nextflow run \
#                 olgabot/crispr-screen-nf \
#                 -r patch-2 \
#                 --treatment_fastq ${FASTQ_DIR2}/$@/'*treatment.fastq.gz' \
#                 --control_fastq ${FASTQ_DIR2}/$@/'*control.fastq.gz' \
#                 --library ${FASTQ_DIR2}/$@/Human_GeCKOv2_Library_A_3_mageck.csv \
#                 --output_prefix $@ \
#                 --output ${OUTPUT_DIR}
# 
# Wang_OC43_library_B: 
# 	nextflow run \
#                 olgabot/crispr-screen-nf \
#                 -r patch-2 \
#                 --treatment_fastq ${FASTQ_DIR2}/$@/'*treatment.fastq.gz' \
#                 --control_fastq ${FASTQ_DIR2}/$@/'*control.fastq.gz' \
#                 --library ${FASTQ_DIR2}/$@/Human_GeCKOv2_Library_B_1_mageck.csv \
#                 --output_prefix $@ \
#                 --output ${OUTPUT_DIR}
# 
# Wang_SARS-CoV2_library_A:
# 	nextflow run \
#                 olgabot/crispr-screen-nf \
#                 -r patch-2 \
#                 --treatment_fastq ${FASTQ_DIR2}/$@/'*treatment.fastq.gz' \
#                 --control_fastq ${FASTQ_DIR2}/$@/'*control.fastq.gz' \
#                 --library ${FASTQ_DIR2}/$@/Human_GeCKOv2_Library_A_3_mageck.csv \
#                 --output_prefix $@ \
#                 --output ${OUTPUT_DIR}
# 
# Wang_SARS-CoV2_library_B:
# 	nextflow run \
#                 olgabot/crispr-screen-nf \
#                 -r patch-2 \
#                 --treatment_fastq ${FASTQ_DIR2}/$@/'*treatment.fastq.gz' \
#                 --control_fastq ${FASTQ_DIR2}/$@/'*control.fastq.gz' \
#                 --library ${FASTQ_DIR2}/$@/Human_GeCKOv2_Library_B_1_mageck.csv \
#                 --output_prefix $@ \
#                 --output ${OUTPUT_DIR}
