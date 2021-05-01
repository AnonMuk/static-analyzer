from bs4 import BeautifulSoup as bs
import glob
import argparse
import unpacker

'''
takes files and does analysis.
'''
def analyze(f):
	try: 
		count = 0
		soup = bs(f, "lxml")
		permissions_dict = []
		package_name = ""
		manifests = soup.find_all('manifest')  # Should only be one...
		for manifest in manifests:
			package_name = manifest.get('package')
			for permission in manifest.find_all('uses-permission'):
				count += 1
				permissions_dict.append(permission.get('android:name'))
		return [package_name, count, permissions_dict]
	except:  # if bs4/lxml can't parse, it errors out (generally based on charset)
		return ["err", "x", "Could not process"]

'''
Batch analysis for multiple APK folders
'''
def processor(filepath, csv):
	locations = glob.glob(f'{filepath}/*/AndroidManifest.xml')
	with open(csv, 'w+') as list:
		for location in locations:
			print(f'File: {location}')
			with open(location, encoding='utf-8') as manifest:
				results = analyze(manifest)
				if(results[0] == "err"):
					print(f"Error on {location}")
				list.write(f'{results[0]}, {results[1]}, {results[2]}\n')

'''
Argument parser
'''
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('path', type=str, help='The path for unpacking and processing APKs')
	parser.add_argument('--outfile', '-o', default="results.csv", help="results file")
	args = parser.parse_args()
	# print(args)
	unpacker.unpacker(args.path)
	processor(args.path, args.outfile)

