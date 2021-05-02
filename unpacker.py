import glob
import subprocess


def unpacker(dir):
    '''
    Uses apktool to unpack all APKS in folder
    APKTOOL MUST BE ON PATH
    '''
    apks = glob.glob(f'{dir}/*.apk')
    # return apks
    for apk in apks:
        subprocess.run(["apktool", apk], shell=True)
    print(f"all apks in directory {dir} unpacked")
