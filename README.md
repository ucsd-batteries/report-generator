# Report Generator

This is a simple report generator that takes a html template, plot images, and data files and generates a report.

- [Report Generator](#report-generator)
  - [First time setup](#first-time-setup)
  - [Usage](#usage)
  - [TODO](#todo)

## First time setup

If you would like to setup only for the report generator, you can run the following commands:

```bash
conda env create -f environment.yml
```

## Usage

1. Place plots in the [`./input/images`] directory to be parsed and moved to the `./assets/img` directory.
2. Similarly, place summary data files (ex: `NP5_test_summary.csv`) in `./input/summary_data` for the script to calculate cycle count.
3. Place downloaded [Testing Progress Tracker](https://docs.google.com/spreadsheets/d/1nAmstAEzmYJce6Vif8Z6ur3eQHhDitz8AH5MXsRy5Yo/edit?usp=sharing) from google sheets to `./input/progress_tracker` directory.
4. Run the script with `python generate_report.py`.
5. The resulting html report `generated_report.html` will be placed in the root directory.
6. Lastly, run the following commands to generate the pdf report:

```bash
conda activate report-generator
python rename_plots.py # rename and place plots in the right directory for the report
python generate_report.py # generate the report with the correct data
```

## TODO

- [x] Allow data files to be parsed
- [ ] Standardize all test progress tracker sheets
- [ ] Allow for generalization with other tests
- [ ] Create a template for compiled reports
- [ ] Create a template for monthly reports
- [ ] Integrate better with bootstrap studio? (maybe)
