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

1. Place plots in the `input` directory to be parsed and moved to the `assets/img` directory.
2. Similarly, place data files in the `input` for the script to calculate cycle count and end dates.
3. Run the script with `python generate_report.py`.
4. The resulting html report `generated_report.html` will be placed in the root directory.

```bash
conda activate report-generator
python generate_report.py
```

## TODO

- [ ] Allow data files to be parsed
- [ ] Allow for generalization with other tests
- [ ] Create a template for compiled reports
- [ ] Create a template for monthly reports
- [ ] Integrate better with bootstrap studio? (maybe)
