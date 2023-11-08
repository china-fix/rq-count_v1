#!/bin/bash

# Default values
MAPPING_REF=""
TARGETS=""
REPORT_DIR=""
SCRIPT=""
OUT_DIR="output_directory"
CUTLEN="5000"
FIXLEN=""

# Function to display usage information
display_help() {
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo "  --REPORT_DIR   Directory containing .tab files (example: '../report')"
    echo "  --TARGETS      Targets fasta file (example: 'targets.fasta')"
    echo "  --MAPPING_REF  Mapping reference fasta file (example: '../in/REF/28791.REF')"
    echo "  --SCRIPT       Path to the Python script (example: '~/xiao_bin/github/rq-count_v1/scripts/relative_mapping_caculation_V2.0.py')"
    echo "  --OUT_DIR      Output directory (default: 'output_directory')"
    echo "  --CUTLEN       The flanking seq length for target calculation (default: 5000)"
    echo "  --FIXLEN       Flanking seq length to drop near the deletion edge location (optional)"
    exit 1
}

# Parse command line options
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --REPORT_DIR) REPORT_DIR="$2"; shift 2 ;;
        --TARGETS) TARGETS="$2"; shift 2 ;;
        --MAPPING_REF) MAPPING_REF="$2"; shift 2 ;;
        --SCRIPT) SCRIPT="$2"; shift 2 ;;
        --OUT_DIR) OUT_DIR="$2"; shift 2 ;;
        --CUTLEN) CUTLEN="$2"; shift 2 ;;
        --FIXLEN) FIXLEN="$2"; shift 2 ;;
        -h|--help) display_help; exit 0 ;;
        *) echo "Unknown option: $1"; display_help; exit 1 ;;
    esac
done

# Check if mandatory options are provided
if [ -z "$REPORT_DIR" ] || [ -z "$TARGETS" ] || [ -z "$MAPPING_REF" ] || [ -z "$SCRIPT" ]; then
    echo "Error: Mandatory options not provided. Use --help for usage information."
    exit 1
fi

# Create the output directory if it doesn't exist
mkdir -p "$OUT_DIR"

# Loop through the files in the report directory
for name in "$REPORT_DIR"/*.tab; do
    if [ -f "$name" ]; then
        # Extract the filename without the path
        base_name="${name##*/}"_OUT

        # Define the output file path
        output_file="$OUT_DIR/$base_name"

        # Run the Python script with additional options
        echo "Processing $name..."
        python "$SCRIPT" \
            --MAPPING_REF "$MAPPING_REF" \
            --TARGETS "$TARGETS" \
            --DEPTH_TAB "$name" \
            --OUT "$output_file" \
            --CUTLEN "$CUTLEN" \
            ${FIXLEN:+--FIXLEN "$FIXLEN"}  # Include FIXLEN if it's provided by the user

        echo "Processing $name complete. Output saved to $output_file"
    fi
done

echo "All files processed."
