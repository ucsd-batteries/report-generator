from pathlib import Path 
import re
import logging

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s', level=logging.INFO) # set logging level and formatting
    
    root = Path('./input/images') # set where to look for image
    dest = Path('./assets/img')

    logging.info(f'Starting rename of images in {root} and moving to {dest}')

    files = root.glob('*.jpg') # get all jpg files in plots folder
    for file in files:
        # if no npx in name, skip
        try: 
            NPname = re.findall("NP[0-9]+", file.name)[-1]
        except IndexError:
            # check if its gantt chart
            if file.name == 'Nissan Gantt Chart.jpg':
                gantt_dest = dest / 'gantt.jpg'
                logging.info(f'Moving {file} to {gantt_dest}')
                file.rename(gantt_dest)
            
            continue

        if file.name.find('SOH') > 0:
            plot_type = 'SOH'
        if file.name.find('Internal Resistance') > 0:
            plot_type = 'IR'

        summary_plot_dest = dest / f'{NPname}_{plot_type}.jpg'
        logging.info(f'Moving {file} to {summary_plot_dest}')
        file.rename(summary_plot_dest)
    
    logging.info('Finished renaming images')
        
