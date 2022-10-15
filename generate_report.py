# built in python modules
import logging
import datetime as dt
from pathlib import Path

# 3rd party modules
import pandas as pd
import numpy as np
from jinja2 import Environment, FileSystemLoader
from utils.utils import bcolors



class Battery:
    """Class used to represent a battery"""
    def __init__(self, pack_num:int, cell_num:int, rated_cap:float, summary_fp:str, metadata_fp:str=None) -> None:
        try:
            self.summary_df = pd.read_csv(summary_fp)
        except FileNotFoundError:
            logging.error(f"File {summary_fp} not found")
            raise FileNotFoundError
        self.packnum = pack_num
        self.cell_num = cell_num
        self._rated_cap = rated_cap # rated capacity of the Nissan batteries
        self.metadata_df = pd.read_csv(metadata_fp) if metadata_fp else None
        self._cycles_record = self._calc_cycles()
        self._total_cycles = self.cycles_record[-1]
        self._last_test_name, self._start_date, self._end_date = self._get_test_metadata()

    def _calc_cycles(self) -> np.ndarray:
        """Calculate the number of cycles at the end of each test"""
        rows = self.summary_df.shape[0]
        dch1 = self.summary_df['DCH1']
        dch2 = self.summary_df['DCH2']

        cycles = np.zeros((rows,))
        cycles[0] = dch1[0]
        for i in range(rows-1):
            cycles[i+1] = cycles[i] + dch1[i+1] + dch2[i]
        return cycles / self.rated_cap

    def _get_test_metadata(self) -> tuple:
        """Extracts the test metadata from the progress tracker csv"""
        self.metadata_df.dropna(inplace=True, subset=['Cycle']) # drop empty rows
        last_row = self.metadata_df.iloc[-1, :]

        if last_row[:3].hasnans: # if any of the first 3 columns are NaN
            last_row = self.metadata_df.iloc[-2, :3] # if so, push back one test
        
        # extract data for the report
        test_name = last_row['Cycle']
        start_date = last_row['Date Started']
        end_date = last_row['Date Completed']
        return (test_name, start_date, end_date)

    @property
    def total_cycles(self):
        return self._total_cycles

    @property
    def rated_cap(self):
        return self._rated_cap

    @property
    def cycles_record(self):
        return self._cycles_record

    @property
    def last_test_name(self):
        return self._last_test_name

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date


def write_html(html: str, fp: str, mode: str = 'w') -> None:
    """Writes the html to a file"""
    with open(fp, mode) as f:
        f.write(html)


# TODO fix this
# def backup(fp: Path) -> None:
#     """Backs up the file by renaming it with a '.back' suffix"""
#     backup_fp = fp.with_suffix('.back.html')
#     if fp.exists():
#         fp.unlink()
#     fp.rename(backup_fp)


def main():
    """Main function"""
    # instantiate the battery objects, change the filepaths as needed
    NP_rated_cap = 56.3
    NP5 = Battery(5, 16, NP_rated_cap, 'input/summary_data/NP5_test_summary.csv', 'input\progress_trackers\Testing Progress Tracker - Nissan Pack 5 (B).csv')
    NP6 = Battery(6, 16, NP_rated_cap, 'input/summary_data/NP6_test_summary.csv', 'input\progress_trackers\Testing Progress Tracker - Nissan Pack 6 (A).csv')

    # jinja2 setup
    template_html = 'nissan.html' # modify this to change the template
    logging.info(f"Loading template from {'./templates/' + template_html}")
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template(template_html)

    # organize timeline data into a dictionary
    timeline_table = {}
    timeline_table[NP5.packnum] = NP5.last_test_name, NP5.start_date, NP5.end_date
    timeline_table[NP6.packnum] = NP6.last_test_name, NP6.start_date, NP6.end_date
    timeline_table = dict(sorted(timeline_table.items())) # sort dict by key value

    # render the template with variables, modify the variables as needed
    logging.info("Rendering template")
    html = template.render(page_title_text='Nissan Report',
                        date=dt.datetime.now().date(),
                        title_text='Nissan Cycle Aging Report',
                        name='Ben',
                        date_written=str(dt.datetime.now().date()),
                        timeline_table=timeline_table,
                        np5_cycle_count=round(NP5.total_cycles),
                        np6_cycle_count=round(NP6.total_cycles),
                        )

    # write the template to an HTML file
    generated_html_fp = Path('./nissan.html')
    # TODO: backup the file before writing 
    logging.info(f"Writing HTML to {generated_html_fp}")
    write_html(html, generated_html_fp)

if __name__ == '__main__':
    # set logging level and formatting
    logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s', level=logging.INFO)
    print(f'{bcolors.HEADER}Don\'t forget keep a record of the previous reports!{bcolors.ENDC}')
    if input(f"{bcolors.WARNING}OK to overwrite to the old report? (y/n): {bcolors.ENDC}") == 'y':
        logging.info('Starting report generation')
        main()
        logging.info('Done!')
    else:
        logging.info('Exiting')