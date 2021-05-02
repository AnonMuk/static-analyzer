import argparse
# from . import unpacker
import manifestanalysis
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString


# '''
# Batch analysis for multiple APK folders
# '''
# def processor(filepath, csv):
# 	locations = glob.glob(f'{filepath}/*/AndroidManifest.xml')
# 	with open(csv, 'w+') as list:
# 		for location in locations:
# 			print(f'File: {location}')
# 			with open(location, encoding='utf-8') as manifest:
# 				results = manifestanalysis.analyze(manifest)
# 				if(results[0] == "err"):
# 					print(f"Error on {location}")
# 				list.write(f'{results[0]}, {results[1]}, {results[2]}\n')

'''
Argument parser
'''
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    analysis = parser.add_mutually_exclusive_group()
    analysis.add_argument('-a', '--analyze', type=str,
                          help="analyze decompiled APK")
    analysis.add_argument('-ba', '--batch-analyze', type=str,
                          help='Analyze a folder of decompiled APKs')
    unpack = parser.add_mutually_exclusive_group()
    unpack.add_argument('-u', '--unpack', type=str,
                        help="Unpack a single APK")
    unpack.add_argument('-bu', '--batch-unpack', type=str,
                        help='Unpack a folder with APKs')
    # parser.add_argument('path', type=str,
    # help='The path for unpacking and processing APKs')
    # parser.add_argument('--outfile', '-o',
    # default="results.csv", help="results file")
    args = parser.parse_args()
    # print(args)
    if args.analyze is not None:
        analysis = manifestanalysis.analysis(args.analyze)
        xml = dicttoxml(analysis)
        dom = parseString(xml)
        print(dom.toprettyxml())
    # unpacker.unpacker(args.path)
    # processor(args.path, args.outfile)
