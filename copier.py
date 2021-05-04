import glob
import os

from bs4 import BeautifulSoup as bs4


def bulkcopy(path: str, outfile: str) -> None:
    globpath = os.path.join(path, '*', '')
    dirs = glob.glob(globpath)
    target = os.path.join(path, '000_RESULTS', '')
    print(f'Copying results to {target}.')
    failures = 0
    try:
        os.mkdir(target)  # create directory if it doesn't exist
    except OSError:
        pass
    if target in dirs:
        dirs.remove(target)  # remove from list
    for dir in dirs:
        results_xml = os.path.join(dir, 'result.xml')
        new_name = dir[len(path) + 1:-1]
        try:
            with open(results_xml, encoding='utf-8') as file:
                soup = bs4(file, 'lxml')
                new_name = soup.find('package').string
                cp_result = os.path.join(target, f'{new_name}.xml')
                # print(f'Copying {results_xml} to {cp_result}')
                with (open(cp_result, encoding='utf-8', mode='w')) as output:
                    output.write(soup.prettify())
        except FileNotFoundError as fnfe:
            failures += 1
            print(fnfe)
    if failures > 0:
        print(f'{len(dirs)} directories found, {failures} errors.')
    else:
        print(f'Operation completed successfully on {len(dirs)} files.')
