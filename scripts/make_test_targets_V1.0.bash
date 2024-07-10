#!/bin/bash

function usage() {
    echo "Usage: $0 --input_file <input_file> --output_file <output_file> --seq_length_from <seq_length_from> --seq_length_to <seq_length_to> --sub_seq_num <sub_seq_num>"
    echo ""
    echo "Parameters:"
    echo "  --input_file      Path to the input FASTA file"
    echo "  --output_file     Path to the output FASTA file"
    echo "  --seq_length_from Starting sequence length (in bp)"
    echo "  --seq_length_to   Ending sequence length (in bp)"
    echo "  --sub_seq_num     Number of sub-sequences to extract per sequence length"
    echo "  -h                Display this help message"
    exit 1
}

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --input_file) input_file="$2"; shift ;;
        --output_file) output_file="$2"; shift ;;
        --seq_length_from) seq_length_from="$2"; shift ;;
        --seq_length_to) seq_length_to="$2"; shift ;;
        --sub_seq_num) sub_seq_num="$2"; shift ;;
        -h|--help) usage ;;
        *) echo "Unknown parameter passed: $1"; usage ;;
    esac
    shift
done

# Validate input parameters
if [ -z "$input_file" ] || [ -z "$output_file" ] || [ -z "$seq_length_from" ] || [ -z "$seq_length_to" ] || [ -z "$sub_seq_num" ]; then
    echo "Missing required parameters."
    usage
fi

# Remove the output file if it already exists
rm -f $output_file

# Loop through the sequence lengths from seq_length_from to seq_length_to with a step of 50bp
for (( size=$seq_length_from; size<=$seq_length_to; size+=50 ))
do
  # Create a temporary file for the sliding sequences
  temp_file="temp_${size}.fa"
  filtered_temp_file="filtered_temp_${size}.fa"

  # Run seqkit sliding with the current window size and store in a temporary file
  seqkit sliding -s $((size/2)) -W $size -S :${size}bp $input_file |
  
  # Use the seqkit grep command to exclude sequences that contain the character "K"
  seqkit grep -s -v -p K > $temp_file
  
  # Remove the top 1000 and bottom 1000 sequences
  # Count the number of remaining sequences
  num_sequences=$(grep -c '^>' $temp_file)
  num_sequences=$((num_sequences - 1001))
  seqkit range -r 1001:$num_sequences $temp_file > $filtered_temp_file

  # Shuffle the sequences in the filtered temporary file
  seqkit shuffle $filtered_temp_file |
  # Use awk to print each sequence until reaching sub_seq_num sequences
  awk -v sub_seq_num="$sub_seq_num" 'BEGIN {count=0} /^>/ {if (++count > sub_seq_num) exit} {print}' >> $output_file

  # Remove the temporary files
  rm -f $temp_file $filtered_temp_file
done

echo "Extraction complete. Results are in $output_file"
