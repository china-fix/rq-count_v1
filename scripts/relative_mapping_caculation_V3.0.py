#!/usr/bin/env python3

'''
This script is designed to calculate the relative mapping rate change between start samples and end samples.
### Updates
- 20220512: Modify the linear model.
- 20220516: Add new machine-learning model.
- 20220601: Major revision.
- 20220604: Update the outlier dropping function.
- 20230507: Add multiprocessing and handle BLAST no match issues.
'''

import subprocess
import sys
import argparse
import io
from Bio.Blast import NCBIXML
import pandas as pd
import numpy as np
import multiprocessing
from functools import partial
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, explained_variance_score, mean_absolute_error, mean_absolute_percentage_error, median_absolute_error


def parse_args():
    parser = argparse.ArgumentParser(description="Welcome to use Xiao_Fei_Robot")
    parser.add_argument('--MAPPING_REF', required=True, type=str, metavar='FILENAME', help="The fasta filename you used for bwa mapping reference")
    parser.add_argument('--TARGETS', required=True, type=str, metavar='FILENAME', help="The fasta file includes all the tested gene sequences you want to measure")
    parser.add_argument('--DEPTH_TAB', required=True, type=str, metavar='FILENAME', help="The tab file describing the mapping depth of every base")
    parser.add_argument('--CUTLEN', default=5000, type=int, metavar='DEFAULT 5000', help="The flanking seq length for target calculation (extracted for model learning)")
    parser.add_argument('--CUTLEN_FROM', type=int, help="Starting value for CUTLEN (overrides --CUTLEN if used)")
    parser.add_argument('--CUTLEN_TO', type=int, help="Ending value for CUTLEN (overrides --CUTLEN if used)")
    parser.add_argument('--CUT_STEP', default=50, type=int, metavar='STEP', help="step size for CUTLEN range (default: 50)")
    parser.add_argument('--FIXLEN', type=int, help="Flanking seq length you want to drop near the deletion edge location (default is 0)")
    parser.add_argument('--OUT', default="report", type=str, metavar='FILENAME', help="Output file name, 'report' as default")
    parser.add_argument('--DEV', action='store_const', const=True, metavar='FOR DEVELOPING ONLY', help="For developing and testing only, normal users can ignore this")
    return parser.parse_args()


def get_learning_df(depth_tab, targets, mapping_ref, cutlen, fixlen=False):
    depth_tab_df = pd.read_csv(depth_tab, sep='\t', names=["reference", "1_index", "depth"])
    blast_run_xml = subprocess.run(["blastn", "-query", targets, "-subject", mapping_ref, "-outfmt", "5"], check=True, capture_output=True)
    xml = blast_run_xml.stdout
    xml_obj = io.BytesIO(xml)
    blast_records = NCBIXML.parse(xml_obj)

    masked_df_append = pd.DataFrame()
    flanking_df_append = pd.DataFrame()

    for blast_record in blast_records:
        try:
            alignment = blast_record.alignments[0]
        except IndexError:
            print(blast_record.query + " BLAST no match!")
            continue
        hsp = alignment.hsps[0]
        start_loc = hsp.sbjct_start
        end_loc = hsp.sbjct_end
        target_name = blast_record.query
        if start_loc > end_loc:
            start_loc, end_loc = end_loc, start_loc
        if fixlen:
            masked_df = depth_tab_df.query('(@start_loc) <= `1_index` <= (@end_loc)')
            masked_df = masked_df.assign(target_name=target_name)
            masked_df_append = pd.concat([masked_df_append, masked_df])
            flanking_df = depth_tab_df.query('((@end_loc + @cutlen) >= `1_index` > (@end_loc + @fixlen)) or ((@start_loc - @cutlen) <= `1_index` < (@start_loc - @fixlen))')
            flanking_df = flanking_df.assign(target_name=target_name)
            flanking_df_append = pd.concat([flanking_df_append, flanking_df])
        else:
            masked_df = depth_tab_df.query('@start_loc <= `1_index` <= @end_loc')
            masked_df = masked_df.assign(target_name=target_name)
            masked_df_append = pd.concat([masked_df_append, masked_df])
            flanking_df = depth_tab_df.query('((@end_loc + @cutlen) >= `1_index` > @end_loc) or ((@start_loc - @cutlen) <= `1_index` < @start_loc)')
            flanking_df = flanking_df.assign(target_name=target_name)
            flanking_df_append = pd.concat([flanking_df_append, flanking_df])

    return depth_tab_df, masked_df_append, flanking_df_append


def get_ML_model(learning_df):
    X = learning_df[["1_index"]].to_numpy(dtype=float)
    y = learning_df["depth"].to_numpy(dtype=float)
    regr = SVR(kernel="rbf", C=50, gamma=0.1, epsilon=0.1, cache_size=5000)
    regr.fit(X, y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
    regr_metrics = SVR(kernel="rbf", C=50, gamma=0.1, epsilon=0.1, cache_size=5000)
    regr_metrics.fit(X_train, y_train)
    R2 = r2_score(y_test, regr_metrics.predict(X_test))
    VAR = explained_variance_score(y_test, regr_metrics.predict(X_test))
    ABS = mean_absolute_error(y_test, regr_metrics.predict(X_test))
    ABS_MEDIAN = median_absolute_error(y_test, regr_metrics.predict(X_test))
    ABS_PER = mean_absolute_percentage_error(y_test, regr_metrics.predict(X_test))
    print("R2:", R2)
    print("variance:", VAR)
    print("mean absolute error:", ABS)
    print("median absolute error:", ABS_MEDIAN)
    print("mean absolute percentage error: ", ABS_PER)
    return regr, ABS, R2, ABS_MEDIAN


def elimate_outliters(data):
    mu = data.mean()
    std = data.std()
    clean_data = data[(data > mu - 1.645 * std) & (data < mu + 1.645 * std)]
    return clean_data


def ratio_caculate(model, targets_df, mean_abs_er, R2, median_abs_er):
    predict_X = targets_df[["1_index"]].to_numpy(dtype=float)
    predict_y = model.predict(predict_X)
    targets_df = targets_df.assign(predict_depth=predict_y.tolist())
    targets_df['DEL_depth'] = targets_df.predict_depth - targets_df.depth
    targets_df['target_rate'] = (targets_df.predict_depth - targets_df.depth) / targets_df.predict_depth
    clean_df = targets_df[["target_name", "depth", "predict_depth", "DEL_depth", "target_rate"]]
    df = clean_df.groupby("target_name").median()
    series_depth_clean = elimate_outliters(clean_df["depth"])
    series_predict_depth_clean = elimate_outliters(clean_df["predict_depth"])
    series_DEL_depth_clean = elimate_outliters(clean_df["DEL_depth"])
    series_target_rate_clean = elimate_outliters(clean_df["target_rate"])
    df = df.assign(depth_c=series_depth_clean.median())
    df = df.assign(depth_c_std=series_depth_clean.std())
    df = df.assign(predict_depth_c=series_predict_depth_clean.median())
    df = df.assign(predict_depth_c_std=series_predict_depth_clean.std())
    df = df.assign(DEL_depth_c=series_DEL_depth_clean.median())
    df = df.assign(DEL_depth_c_std=series_DEL_depth_clean.std())
    df = df.assign(target_rate_c=series_target_rate_clean.median())
    df = df.assign(target_rate_c_std=series_target_rate_clean.std())
    df = df.assign(ML_median_abs_er=median_abs_er)
    df = df.assign(ML_mean_abs_er=mean_abs_er)
    df = df.assign(ML_R2=R2)
    return targets_df, df


def process_target(name, flanking_df, targets_df):
    try:
        flanking_df_i = flanking_df.query('`target_name` == @name')
        trained_model, mean_abs_er, R2, median_abs_er = get_ML_model(flanking_df_i)
        targets_df_i = targets_df.query('`target_name` == @name')
        new_df, new_df_summary = ratio_caculate(trained_model, targets_df_i, mean_abs_er, R2, median_abs_er)
        flanking_df_i['target_name'] = 'flanking_' + name
        new_df = pd.concat([new_df, flanking_df_i])
        return new_df, new_df_summary
    except Exception as e:
        print(f"Error processing target {name}: {e}")
        return None, None


def main():
    args = parse_args()
    new_df_append = pd.DataFrame()
    new_df_summary_append = pd.DataFrame()

    cutlen_values = [args.CUTLEN]
    if args.CUTLEN_FROM is not None and args.CUTLEN_TO is not None:
        cutlen_values = range(args.CUTLEN_FROM, args.CUTLEN_TO + 1, args.CUT_STEP)

    for cutlen in cutlen_values:
        print(f"Processing with CUTLEN={cutlen}")
        depth_tab_df, targets_df, flanking_df = get_learning_df(args.DEPTH_TAB, args.TARGETS, args.MAPPING_REF, cutlen, args.FIXLEN)
        process_func = partial(process_target, flanking_df=flanking_df, targets_df=targets_df)

        with multiprocessing.Pool() as pool:
            results = pool.map(process_func, targets_df.target_name.unique())
        
        for result in results:
            if result is not None:
                new_df, new_df_summary = result
                new_df_append = pd.concat([new_df_append, new_df])
                new_df_summary_append = pd.concat([new_df_summary_append, new_df_summary])

    new_df_summary_append_sub = new_df_summary_append.reset_index()[['target_name','target_rate','target_rate_c']]
    # Assuming your DataFrame is named new_df_summary_append_sub
    grouped_df = new_df_summary_append_sub.groupby('target_name').agg({
        'target_rate_c': ['median', 'mean', 'std'],
        'target_rate': ['median', 'mean', 'std']
        })

    # Rename the columns for clarity
    grouped_df.columns = [
        'target_rate_c_median', 'target_rate_c_mean', 'target_rate_c_std',
        'target_rate_median', 'target_rate_mean', 'target_rate_std'
        ]

    
    grouped_df.to_csv(args.OUT + "_summary_cal.csv")
    # new_df_append.to_csv(args.OUT + ".csv")
    new_df_summary_append.to_csv(args.OUT + "_summary_full.csv")


if __name__ == "__main__":
    main()
