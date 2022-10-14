from pathlib import Path 
import re
import logging
import shutil

# TODO: improve logging
# TODO: catch file not found error


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s', level=logging.INFO) # set logging level and formatting
    
    root = Path('./input/images') # set where to look for image
    dest = Path('./assets/img')

    logging.info(f'Starting rename of images in {root} and moving to {dest}')

    files = root.glob('*.jpg') # get all jpg files in plots folder
    for file in files:
        logging.info(f'Renaming {file.name}')
        # if no npx in name, skip
        try: 
            NPname = re.findall("NP[0-9]+", file.name)[-1]
        except IndexError:
            # check if its gantt chart
            if file.name == 'Nissan Gantt Chart.jpg':
                gantt_dest = dest / 'gantt.jpg'
                logging.info(f'Copying {file} to {gantt_dest}')
                shutil.copy(file, gantt_dest)  # use copy instead of move to avoid deleting original

            
            continue

        plot_type = None
        if file.name.find('SOH') > 0:
            plot_type = 'SOH'
        if file.name.find('IR') > 0:
            plot_type = 'IR'
        try: 
            summary_plot_dest = dest / f'{NPname}_{plot_type}.jpg'
            logging.info(f'Copying {file} to {summary_plot_dest}')
            shutil.copy(file, summary_plot_dest)  # use copy instead of move to avoid deleting original
        except:
            logging.error(f'Could not rename {file}')
    
    logging.info('Finished renaming images')
        
