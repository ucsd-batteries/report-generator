from itertools import cycle
from jinja2 import Environment, FileSystemLoader
import datetime as dt

cycle_counts = [1119, 1425]
# for pack_name in ('NP5', 'NP6'):
#     cycle_count = input(f'Enter cycle count for {pack_name}:')
#     cycle_counts.append(cycle_count)


# 2. Create a template Environment
env = Environment(loader=FileSystemLoader('templates'))

# 3. Load the template from the Environment
template = env.get_template('./index.html')


date_test = [{'pack_num': 5, 'test_name': 'Aging 61', 'start': dt.datetime.now().date(), 'end': dt.datetime.now().date()},
             {'pack_num': 6, 'test_name': 'Aging 32', 'start': dt.datetime.now().date(), 'end': '2022-12-23'},]

# 4. Render the template with variables
html = template.render(page_title_text='Report',
                       date=dt.datetime.now().date(),
                       title_text='Nissan Cycle Aging Report',
                       name='Ben',
                       date_written=str(dt.datetime.now().date()),
                       tests=date_test,
                       np5_cycle_count=cycle_counts[0],
                       np6_cycle_count=cycle_counts[1],
                       )

# 5. Write the template to an HTML file
with open('generated_report.html', 'w') as f:
    f.write(html)