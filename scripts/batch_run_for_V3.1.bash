#!/bin/bash

# Default values
MAPPING_REF=""
TARGETS=""
REPORT_DIR=""
SCRIPT=""
OUT_DIR="output_directory"
CUTLEN_FROM=""
CUTLEN_TO=""
CUT_STEP=50
FIXLEN=""

# Function to display usage information
display_help() {
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo "  --REPORT_DIR   Directory containing .tab files (example: '../report')"
    echo "  --TARGETS      Targets fasta file (example: 'targets.fasta')"
    echo "  --MAPPING_REF  Mapping reference fasta file (example: '../in/REF/28791.REF')"
    echo "  --SCRIPT       Path to the Python script (example: '~/xiao_bin/github/rq-count_v1/scripts/relative_mapping_caculation_V3.0.py')"
    echo "  --OUT_DIR      Output directory (default: 'output_directory')"
    echo "  --CUTLEN_FROM  Start value for CUTLEN range"
    echo "  --CUTLEN_TO    End value for CUTLEN range"
    echo "  --CUT_STEP     Step size for CUTLEN range (default: 50)"
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
        --CUTLEN_FROM) CUTLEN_FROM="$2"; shift 2 ;;
        --CUTLEN_TO) CUTLEN_TO="$2"; shift 2 ;;
        --CUT_STEP) CUT_STEP="$2"; shift 2 ;;
        --FIXLEN) FIXLEN="$2"; shift 2 ;;
        -h|--help) display_help; exit 0 ;;
        *) echo "Unknown option: $1"; display_help; exit 1 ;;
    esac
done

# Check if mandatory options are provided
if [ -z "$REPORT_DIR" ] || [ -z "$TARGETS" ] || [ -z "$MAPPING_REF" ] || [ -z "$SCRIPT" ] || [ -z "$CUTLEN_FROM" ] || [ -z "$CUTLEN_TO" ]; then
    echo "Error: Mandatory options not provided. Use --help for usage information."
    exit 1
fi

# Create the output directory if it doesn't exist
mkdir -p "$OUT_DIR"

# Export necessary variables for GNU Parallel
export MAPPING_REF TARGETS SCRIPT OUT_DIR CUTLEN_FROM CUTLEN_TO CUT_STEP FIXLEN

# Function to process each file
process_file() {
    local name="$1"
    local base_name="${name##*/}"
    local output_file="$OUT_DIR/${base_name}_OUT"
    
    echo "Processing $name..."
    python "$SCRIPT" \
        --MAPPING_REF "$MAPPING_REF" \
        --TARGETS "$TARGETS" \
        --DEPTH_TAB "$name" \
        --OUT "$output_file" \
        --CUTLEN_FROM "$CUTLEN_FROM" \
        --CUTLEN_TO "$CUTLEN_TO" \
        --CUT_STEP "$CUT_STEP" \
        ${FIXLEN:+--FIXLEN "$FIXLEN"}  # Include FIXLEN if it's provided by the user
    
    echo "Processing $name complete. Output saved to $output_file"
}

export -f process_file

# Find .tab files and process them in parallel
find "$REPORT_DIR" -name "*.tab" | parallel process_file {}

echo "All files processed."
