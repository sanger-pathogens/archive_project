file_of_studies=$1
output_file=$2
sum=0
while read s
do	
    echo $s >> $output_file
    lanes_per_study=$(pf data -t study -i "$s" | wc -l)    
    echo $lanes_per_study >> $output_file
    sum=$((sum+lanes_per_study))
done < $file_of_studies
echo 'TOTAL:' >> $output_file
echo $sum >> $output_file
