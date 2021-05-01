import glob
import subprocess
'''
Uses apktool to unpack all Android Packages (apks) in folder.
APKTOOL MUST BE ON THE PATH
'''
def unpacker(dir):
	apks = glob.glob(f'{dir}/*.apk')
	# return apks
	for apk in apks:
		subprocess.run(["apktool", apk], shell=True)
	print("all apks unpacked")