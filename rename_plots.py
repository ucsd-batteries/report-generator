from pathlib import Path 
import re

if __name__ == '__main__':
    print("\nRenaming plots...")
    root = Path('./input') # set where to look for image
    dest = Path('./assets/img')
    files = root.glob('*.jpg') # get all jpg files in plots folder

    # rename files
    for file in files:
        # if no npx in name, skip
        try: 
            NPname = re.findall("NP[0-9]+", file.name)[-1]
        except IndexError:
            # check if its gantt chart
            if file.name == 'Nissan Gantt Chart.jpg':
                gantt_dest = dest / 'gantt.jpg'
                print(f'Moving {file} to {gantt_dest}')
                file.rename(gantt_dest)
            print("No NP name found")
            continue

        if file.name.find('SOH') > 0:
            plot_type = 'SOH'
        if file.name.find('Internal Resistance') > 0:
            plot_type = 'IR'

        summary_plot_dest = dest / f'{NPname}_{plot_type}.jpg'
        print(f'Moving {file} to {summary_plot_dest}')
        file.rename(summary_plot_dest)
    print("Done\n")
        
