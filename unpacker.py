import glob
import subprocess


def unpack(file: str) -> None:
    '''
    Decompiles a file using APKtool
    '''
    subprocess.run(["apktool", 'd', '-o', f'{file[:-4]}', file], shell=True)


def unpacker(dir):
    '''
    Uses apktool to unpack all APKS in folder
    APKTOOL MUST BE ON PATH
    '''
    apks = glob.glob(f'{dir}/*.apk')
    # return apks
    for apk in apks:
        unpack(apk)
    print(f"all apks in directory {dir} unpacked")
