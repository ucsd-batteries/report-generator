# Report-generator

This is a simple report generator for the battery of tests. It is a simple python script that takes the output of the tests and various metadata and generates a report in the form of a HTML file. These generated HTML files are then deployed this repo's [github pages](https://ucsd-batteries.github.io/report-generator/).

- [Report-generator](#report-generator)
  - [Dependencies](#dependencies)
  - [Usage](#usage)
    - [Behavior of each script](#behavior-of-each-script)
      - [`generate_report.py`:](#generate_reportpy)
      - [`rename_plots.py`:](#rename_plotspy)
  - [Todos](#todos)

## Dependencies

The report generator requires the following python packages:

1. [pandas](https://pandas.pydata.org/)
2. [numpy](https://numpy.org/)
3. [jinja2](https://pypi.org/project/Jinja2/)

You can manually install these packages using `pip` or `conda` or you can use the provided conda compatible `environment.yml` file to install them using `conda` as follows:

```bash
conda env create -f environment.yml
conda activate report-generator
```

This will create a conda environment called `report-generator` with all the required dependencies installed.

## Usage

Before running the report generator, you need to have the following files present in the `input` directory:

1. Plots that you want to include in the report
2. Summary csv file(s)
3. Progress tracker csv file(s)

There are directories already created with example files in there. You can use those as a template to get started or you can modify the file paths in `generate_report.py` to point to your own files.

Then, you can run the report generator using the following command:

```bash
python rename_plots.py
python generate_report.py
```

See [here](#behavior-of-each-script) for a more detailed description of what each script does.

**_IMPORTANT NOTE_**
Currently, only Nissan progress trackers and image renaming is fully tested. If you are using a different battery, you will need to modify the `generate_report.py` file to point to the correct progress tracker file and modify `rename_plots.py` or manually rename the images correctly. **Support for other batteries tests will be coming soon**

### Behavior of each script

#### `generate_report.py`: 
This script takes in the summary csv file(s) and progress tracker csv file(s) and generates a HTML file with the report.

#### `rename_plots.py`: 
This script takes in the plots and renames them to the format that the template HTML expects. This is necessary because the plots are generated by the tests and the names are not consistent with the image path coded in the template HTMLs. This script renames the plots to the format `NP[]_[SOH/IR].png` and moves them to the `./assets/img` directory.

## Todos

- [ ] Add support for other battery tests
- [ ] OOP-ify the code
- [ ] organize assets into corresponding pages