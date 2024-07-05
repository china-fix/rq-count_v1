import argparse
import pandas as pd
import os

def eliminate_outliers(data):
    mu = data.mean()
    std = data.std()
    clean_data = data[(data > mu - 1.645 * std) & (data < mu + 1.645 * std)]
    return clean_data

def calculate_statistics(input_file, output_file, output_folder):
    # Read the data from the file into a pandas DataFrame
    df_start = pd.read_csv(input_file, sep='\t', names=['Column1','Column2','Column3'])
    if 'Column3' not in df_start.columns:
        print("The file does not have 'Column3'. Assuming it's in the second column.")
        df = eliminate_outliers(df_start["Column2"])
    else:
        df = eliminate_outliers(df_start["Column3"])

    # Calculate the requested statistics
    mean_value = df.mean()
    median_value = df.median()
    std_deviation = df.std()
    max_value = df.max()
    min_value = df.min()
    
    # Format the values to two decimal places
    mean_value = "{:.2f}".format(mean_value)
    median_value = "{:.2f}".format(median_value)
    std_deviation = "{:.2f}".format(std_deviation)

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Write the statistics to the output file
    output_path = os.path.join(output_folder, output_file)
    with open(output_path, 'w') as f:
        f.write(f"Name: {output_file}\n")
        f.write(f"Mean: {mean_value}\n")
        f.write(f"Median: {median_value}\n")
        f.write(f"Standard Deviation: {std_deviation}\n")
        f.write(f"Max: {max_value}\n")
        f.write(f"Min: {min_value}\n")

    # Create the output file with .tsv extension
    output_file_2 = os.path.splitext(output_file)[0] + '.tsv'
    output_path_2 = os.path.join(output_folder, output_file_2)
    with open(output_path_2, 'w') as f:
        f.write(f"{output_file}\t{mean_value}\t{median_value}\t{std_deviation}\t{max_value}\t{min_value}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate statistics for specific columns in multiple files.")
    parser.add_argument("--input-folder", required=False, help="Path to a folder containing input files")
    parser.add_argument("--output-folder", required=True, help="Path to the output folder")

    args = parser.parse_args()

    if args.input_folder:
        input_files = [os.path.join(args.input_folder, file) for file in os.listdir(args.input_folder)]
        for file in input_files:
            output_file = os.path.splitext(os.path.basename(file))[0] + '.txt'
            calculate_statistics(file, output_file, args.output_folder)
    else:
        parser.print_help()
