import argparse
from pathlib import Path

import bulkprocessing
import copier
import manifestanalysis
import unpacker


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
    commands.add_argument('-f', '--full',
                          help='Unpack and Process ONE APK. ')
    commands.add_argument('-b', '--bulk',
                          help="To bulk process, use the directory " +
                          "containing ALL target files/folders.")
    parser.add_argument('-o', '--outfile',
                        help='output file for bulk analysis, ' +
                        f'defaults to {results_file}',
                        default=results_file)
    parser.add_argument('-t', '--threads',
                        help='number of parallel threads for processing. ' +
                        'Default is 8',
                        default=8, type=int)
    parser.add_argument('--use-xml',
                        action='store_true',
                        help='Uses XML for analysis results.')
    args = parser.parse_args()
    print(args)
    if args.bulk is not None:
        print("Bulk Mode Enabled. Go cook a meal and come back.")
        out = Path(args.bulk) / args.outfile
        bulkprocessing.bulk_process(dir=args.bulk,
                                    outfile=str(out),
                                    threads=args.threads,
                                    use_xml=args.use_xml)
    elif args.unpack is not None:
        if args.unpack[-4:] != '.apk':
            parser.error(f'{args.unpack} is not a valid .apk file')
        unpacker.unpack(args.unpack)
    elif args.analyze is not None:
        analysis = manifestanalysis.analysis(args.analyze,
                                             write_xml=args.use_xml)
    elif args.full is not None:
        unpacker.unpack(args.full)
        manifestanalysis.analysis(args.full[:-4], write_xml=args.use_xml)
        parent = Path(args.full).parent
        out = parent / args.outfile
        copier.copy(path=args.full[:-4],
                    outfile=str(out), is_xml=args.use_xml, clever_naming=False)
