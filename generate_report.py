# built in python modules
import logging
import datetime as dt
from pathlib import Path

# 3rd party modules
import pandas as pd
import numpy as np
from jinja2 import Environment, FileSystemLoader


def get_test_metadata(fp: Path) -> tuple:
    """Extracts the test metadata from the file name"""
    df = pd.read_csv(fp)
    df.dropna(inplace=True, subset=['Cycle']) # drop empty rows
    last_row = df.iloc[-1, :]

    if last_row[:3].hasnans: # if any of the first 3 columns are NaN
        # if so, push back one test
        last_row = df.iloc[-2, :3]
    
    # extract needed data for the report
    test_name = last_row['Cycle']
    start_date = last_row['Date Started']
    end_date = last_row['Date Completed']
    return (test_name, start_date, end_date)


def calc_cycles(df):
    """Calculate the number of cycles that the battery has gone through"""
    rated_cap = 56.3 # rated capacity of the Nissan batteries 
    rows = df.shape[0]
    dch1 = df['DCH1']
    dch2 = df['DCH2']

    cycles = np.zeros((rows,))
    cycles[0] = dch1[0]
    for i in range(rows-1):
        cycles[i+1] = cycles[i] + dch1[i+1] + dch2[i]
    return cycles / rated_cap


def write_html(html: str, fp: str, mode: str = 'w') -> None:
    """Writes the html to a file"""
    with open(fp, mode) as f:
        f.write(html)


def main():
    """Main function"""
    # extract cycle count from summmary csvs
    cycle_counts = []
    summary_data_root = Path('./input/summary_data/')
    for fp in summary_data_root.glob('*.csv'):
        logging.info(f'Calculating cycle count from {fp.name}')
        df = pd.read_csv(fp)
        cycle_counts.append(round(calc_cycles(df)[-1]))

    # jinja2 setup
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('./index.html')

    timeline_table = dict()
    progress_tracker_root = Path('./input/progress_trackers/')
    for fp in progress_tracker_root.glob('*.csv'):
        logging.info(f'Generating timeline table data from {fp.name}')
        pack_num = fp.name.split(" ")[6]
        timeline_table[pack_num] = get_test_metadata(fp)

    timeline_table = dict(sorted(timeline_table.items())) # sort dict by key value

    # render the template with variables
    html = template.render(page_title_text='Report',
                        date=dt.datetime.now().date(),
                        title_text='Nissan Cycle Aging Report',
                        name='Ben',
                        date_written=str(dt.datetime.now().date()),
                        timeline_table=timeline_table,
                        np5_cycle_count=cycle_counts[0],
                        np6_cycle_count=cycle_counts[1],
                        )


    # write the template to an HTML file
    write_html(html, 'nissan.html')

if __name__ == '__main__':
    # set logging level and formatting
    logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s', level=logging.INFO)
    if input("Are you sure you want to generate the report? (y/n): ") == 'y':
        logging.info('Starting report generation')
        main()