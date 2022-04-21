"""
Author: Tom Norman

The script reads the results from a RORB model and plots an ensemble and line of AEP vs Duration. This script provides a convenient way of visualising the results to determine the citical storm duration for each AEP.
The script will handle mutliple AEP within the same '_batch.out' file, so a single RORB model can be run for multiple AEPs. 
The script is to be placed in the '../_output' RORB file.

"""

from pathlib import Path
import re
from unittest import skip
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def main():
    #read the batch file, extract results data and convert to a CSV
    file = ''
    csv_table = []
    p = list(Path('./_output/').glob('*_batch.out'))
    if len(p) == 1:
        file = p[0]
    if len(p) > 1:
        print('multiple batch files')
        print(p)
        file = p[int(input('select batch file index\n'))]
    else:
        print('no batch file found, existing...')
        exit(1)
    with file.open('r') as f:
        flag = 0
        lines = f.readlines()
        for line in lines:
            if line[1:4] == 'Run':
                flag += 1
            if flag == 1:
                new_line = re.sub("\s+", ",", line.strip()) + '\n'
                #convert min to hours
                if new_line.find('min') >= 0:
                    new_line = new_line.replace('min,', '')
                    pos = new_line.find(',') + 1
                    min = new_line[pos:pos+2]
                    try:
                        hour = int(min) / 60
                        new_line = new_line.replace(',{},'.format(min), ',{},'.format(hour), 1)
                    except:
                        print('error: converting minutes to hours on line: {}'.format(line))
                        exit(2)
                else:
                    new_line = new_line.replace('hour,', '')
                new_line = new_line.replace('%', '')
                csv_table.append(new_line)
    results_csv = open('./results.csv', 'w')
    results_csv.writelines(csv_table)
    results_csv.close()
    #Use pandas and seaborn to plot as a ensemble
    df = pd.read_csv('./results.csv')
    df = df.set_index(['AEP', 'Duration']).sort_index()
    means = df.groupby(['AEP', 'Duration'])['Peak0001'].mean()
    means = means.reset_index()
    df_plot = df.copy()
    df_plot = df_plot.drop(axis=1, columns=['Run', 'TPat', 'Rain(mm)', 'ARF'])
    df_plot = df_plot.reset_index()
    fig, axes = plt.subplots(2, 2)
    sns.boxplot(x='Duration', y='Peak0001', hue='AEP', data=df_plot, ax=axes[0, 0])
    LP = sns.lineplot(x='Duration', y='Peak0001', hue='AEP', data=means, ax=axes[0, 1])

    # label points on the plot
    for x, y in zip(means['Duration'], means['Peak0001']):
        LP.annotate(str(round(y, 2)), xy=(x, y), horizontalalignment = 'center') 
    plt.show()

if __name__ == "__main__":
    main()
