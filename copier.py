import glob
import os
import shutil

from bs4 import BeautifulSoup as bs4


def copy_driver(path, outfile):
    results_xml = os.path.join(path, 'result.xml')
    new_name = path[:-4]  # extracts filename from XML just in case
    with open(results_xml, encoding='utf-8') as file:
        soup = bs4(file, 'lxml')
        new_name = soup.find('package').string
        cp_result = os.path.join(outfile, f'{new_name}.xml')
        print(f'Copying {results_xml} to {cp_result}')
    shutil.copyfile(results_xml, cp_result)


def copy(path: str, outfile: str):
    if not os.path.isdir(outfile):
        try:
            os.mkdir(outfile)
        except OSError:
            pass
    copy_driver(path, outfile)


def bulkcopy(path: str, outfile: str) -> None:
    globpath = os.path.join(path, '*', '')
    dirs = glob.glob(globpath)
    target = os.path.join(path, outfile, '')
    print(f'Copying results to {target}.')
    failures = 0
    if not os.path.isdir(target):
        try:
            os.mkdir(target)  # create directory if it doesn't exist
        except OSError:
            # print(f'error creating {target}')
            pass
    if target in dirs:
        dirs.remove(target)  # remove from list
    # print(dirs)
    for dir in dirs:
        try:
            copy_driver(dir, outfile)
        except FileNotFoundError as fnfe:
            failures += 1
            print(fnfe)
    if failures > 0:
        print(f'{len(dirs)} directories found, {failures} errors.')
    else:
        print(f'Operation completed successfully on {len(dirs)} files.')
