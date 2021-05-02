import argparse
import unpacker
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

def is_an_apk(filename: str):
    '''
    Typing to verify that the file is an APK
    '''
    if filename[-4:] != '.apk':
        raise argparse.ArgumentTypeError('File must be a .apk')
    return filename


'''
Argument parser
'''
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    commands = parser.add_mutually_exclusive_group()
    commands.add_argument('-a', '--analyze', type=str,
                          help="analyze decompiled APKs. " +
                          "Point this to the folder " +
                          "produced by apktool or the -u flag.")
    commands.add_argument('-u', '--unpack', type=is_an_apk,
                          help="Unpack APKs.")
    parser.add_argument('-b', '--bulk',
                        help="To bulk process, use the directory containing " +
                        "ALL target files/folders.",
                        action="store_true")
    # parser.add_argument('path', type=str,
    # help='The path for unpacking and processing APKs')
    # parser.add_argument('--outfile', '-o',
    # default="results.csv", help="results file")
    args = parser.parse_args()
    # print(args)
    if args.bulk:
        print("bulk processing")
        if args.unpack is not None:
            unpacker.unpacker(args.unpack)
    else:
        if args.unpack is not None:
            unpacker.unpack(args.unpack)
        if args.analyze is not None:
            analysis = manifestanalysis.analysis(args.analyze)
            xml = dicttoxml(analysis)
            dom = parseString(xml)
            print(dom.toprettyxml())
    # unpacker.unpacker(args.path)
    # processor(args.path, args.outfile)
