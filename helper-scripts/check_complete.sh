output_file=$1
expected_lanes_uploaded=$2

lanes_uploaded=$(grep "Done. Uploaded" $output_file | wc -l)
if [[ "$lanes_uploaded" -ne "$expected_lanes_uploaded" ]]
then
	echo Some lanes did not complete upload. $lanes_uploaded out of $expected_lanes_uploaded were uploaded
	failures=$(grep ERROR $output_file  -B 3 | grep upload | uniq)
	echo $failures
else 
	echo All expected lanes were uploaded. $lanes_uploaded out of $expected_lanes_uploaded were uploaded 
fi
