from glob import glob
import os
from pathlib import Path
from threading import Thread
from typing import List

import manifestanalysis
import unpacker
import copier


def bulk_process(dir: str, outfile: str, num_threads: int):
    globpath = os.path.join(dir, '*.apk')
    files = glob(globpath)
    processors: List[BulkAnalyzer] = []
    for i in range(num_threads):
        processor = BulkAnalyzer(target_filepaths=files[i::num_threads],
                                 outfile=outfile)
        processor.thread.start()
        processors.append(processor)
    for processor in processors:
        if processor.thread.is_alive():
            processor.thread.join(60)
    # Doing it again, just in case
    for processor in processors:
        if processor.thread.is_alive():
            processor.thread.join(100)
    print("All APKs processed.")


class BulkAnalyzer:
    def __init__(self, target_filepaths, outfile):
        self.paths = target_filepaths
        self.total_paths = len(target_filepaths)
        self.thread = Thread(target=self.do_everything_but_smarter)
        self.outfile = outfile

    def do_everything_but_smarter(self):
        count = 0
        # print(f'{self.thread.name}: {count} of {self.total_paths}')
        for apk in self.paths:
            apk_path = Path(apk)
            try:
                print(f'{self.thread.name}: unpacking {apk_path.name}')
                unpacker.unpack(apk)
            except Exception:
                print("Unpacker error. Continuing.")
            try:
                print(f'{self.thread.name}: analyzing APK')
                manifestanalysis.analysis(apk[:-4])
            except Exception:
                print('Analysis error. Continuing.')
            try:
                print(f'{self.thread.name}: Copying Results')
                copier.copy(path=apk[:-4],
                            outfile=self.outfile,
                            clever_naming=False)
            except Exception:
                print('Copy Error. Continuing.')
            count += 1
            print(f'{self.thread.name}: {count} of {self.total_paths} ' +
                  f'({round(100 * count/self.total_paths, 3)}% processed)')
        print(f'{self.thread.name} analyzed assigned files.')
