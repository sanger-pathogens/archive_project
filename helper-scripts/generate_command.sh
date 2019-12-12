studies_file=$1
echo "bsub -o prokaryotes/$studies_file.o -e prokaryotes/$studies_file.e -q long -M2000 -R "\'"select[mem>2000] rusage[mem=2000]"\'" "\""archive_2S3 -i prokaryotes/$studies_file -d prokaryotes -b prokaryotes -r /lustre/scratch118/infgen/pathogen/pathpipe/prokaryotes/seq-pipelines/ -o prokaryotes/${studies_file}_output -m sync"\"""
