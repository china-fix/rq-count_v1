import argparse
import pandas as pd

def eliminate_outliers(data):
    mu = data.mean()
    std = data.std()
    clean_data = data[(data > mu - 1.645 * std) & (data < mu + 1.645 * std)]
    return clean_data

def calculate_statistics(input_file, output_file):
    # Read the data from the file into a pandas DataFrame
    df_start = pd.read_csv(input_file, sep='\t', header=None, names=["ID", "Column2", "Column3"])
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


    # Save the results to the output file
    with open(output_file, 'w') as f:
        f.write(f"Name: {output_file}\n")
        f.write(f"Mean: {mean_value}\n")
        f.write(f"Median: {median_value}\n")
        f.write(f"Standard Deviation: {std_deviation}\n")
        f.write(f"Max: {max_value}\n")
        f.write(f"Min: {min_value}\n")
    
    # Save the results to the output file as a single tab-separated line
    output_file_2=str(output_file) +'.tsv'
    with open(output_file_2, 'w') as f:
        f.write(f"{output_file}\t{mean_value}\t{median_value}\t{std_deviation}\t{max_value}\t{min_value}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate statistics for the third column of a file.")
    parser.add_argument("--input", required=True, help="Input file path")
    parser.add_argument("--output", required=True, help="Output file path")

    args = parser.parse_args()
    calculate_statistics(args.input, args.output)

