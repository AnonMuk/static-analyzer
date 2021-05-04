import argparse

import copier
import manifestanalysis
import unpacker

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
    results_file = "00_AnalysisResults"
    parser = argparse.ArgumentParser()
    commands = parser.add_mutually_exclusive_group()
    commands.add_argument('-a', '--analyze', type=str,
                          help="analyze decompiled APKs. " +
                          "Point this to the folder " +
                          "produced by apktool or the -u flag.")
    commands.add_argument('-u', '--unpack',
                          help="Unpack APKs.")
    parser.add_argument('-b', '--bulk',
                        help="To bulk process, use the directory containing " +
                        "ALL target files/folders.",
                        action="store_true")
    parser.add_argument('-t', '--threads',
                        help='Specifies the number of threads. Defaults to 1.',
                        type=int, default=1)
    parser.add_argument('-o', '--outfile',
                        help='output file for bulk analysis, ' +
                        f'defaults to {results_file}',
                        default=results_file)
    args = parser.parse_args()
    # print(args)
    if args.bulk:
        print("Bulk Mode Enabled. Go cook a meal and come back.")
        if args.unpack is not None:
            print("Unpacking APKs...")
            unpacker.unpacker(args.unpack, args.threads)
        if args.analyze is not None:
            print("Analyzing Files:")
            manifestanalysis.bulk_handler(args.analyze, args.threads)
            copier.bulkcopy(args.analyze, args.outfile)
    else:
        if args.unpack is not None:
            if args.unpack[-4:] != '.apk':
                parser.error(f'{args.unpack} is not a valid .apk file')
            unpacker.unpack(args.unpack)
        if args.analyze is not None:
            analysis = manifestanalysis.analysis(args.analyze)
