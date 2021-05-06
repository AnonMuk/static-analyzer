import glob
import os
import shutil
from pathlib import Path

from bs4 import BeautifulSoup as bs4


def copy_driver(path, outfile, clever_naming=True):
    results_xml = os.path.join(path, 'result.xml')
    res_obj = Path(results_xml)
    # res_path = res_obj.name
    new_name = res_obj.parts[-2]  # extracts filename from XML just in case
    if clever_naming:
        with open(results_xml, encoding='utf-8') as file:
            soup = bs4(file, 'lxml')
            new_name = soup.find('package').string
    cp_result = os.path.join(outfile, f'{new_name}.xml')
    # cp_path = Path(cp_result)
    # print(f'Copying {res_path} to {cp_path}')
    shutil.copyfile(results_xml, cp_result)


def copy(path: str, outfile: str, clever_naming=True):
    if not os.path.isdir(outfile):
        try:
            os.mkdir(outfile)
        except OSError:
            pass
    copy_driver(path, outfile, clever_naming=clever_naming)


def bulkcopy(path: str, outfile: str, clever_naming=True) -> None:
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
            copy_driver(dir, outfile, clever_naming=clever_naming)
        except FileNotFoundError as fnfe:
            failures += 1
            print(fnfe)
    if failures > 0:
        print(f'{len(dirs)} directories found, {failures} errors.')
    else:
        print(f'Operation completed successfully on {len(dirs)} files.')
