import glob
import os
import subprocess
from threading import Thread
from typing import List


def unpack(file: str) -> None:
    '''
    Decompiles a file using APKtool
    '''
    subprocess.run(["apktool", 'd', '-o', f'{file[:-4]}', file],
                   shell=True,
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.STDOUT)


def unpacker(dir, num_threads):
    '''
    Uses apktool to unpack all APKS in folder
    APKTOOL MUST BE ON PATH
    '''
    globpath = os.path.join(dir, '*.apk')
    apks = glob.glob(globpath)
    unpackers: List[Unpacker] = []
    for i in range(num_threads):
        unpacker = Unpacker(apk_list=apks[i::num_threads])
        unpacker.thread.start()
        unpackers.append(unpacker)
    for unpacker in unpackers:
        if unpacker.thread.is_alive:
            unpacker.thread.join(60)
    print(f"all apks in directory {dir} unpacked")


class Unpacker:
    def __init__(self, apk_list):
        self.apk_list = apk_list
        self.total_value = len(apk_list)
        self.thread = Thread(target=self.bulk_unpack)

    def bulk_unpack(self):
        current_apk = 1
        for apk in self.apk_list:
            print(f'{self.thread.name}: Unpacking APK {current_apk} ' +
                  f'of {self.total_value}')
            unpack(apk)
            current_apk += 1
