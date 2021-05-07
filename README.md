# static-analyzer

Static Analyzer for Smartphone Security

This is a static analysis tool and that's honestly kinda cool of us. It has the capability to unpack APKs and run analysis in bulk and speeds itself up using threading. The default file output is JSON, though the `--use-xml` flag can be used to provide XMLs so that it works with our ML system.

This uses **Python 3**, I haven't checked for Python 2 compatibility.

To install needed packages: `pip install -r requirements.txt`

## Usage

```txt
usage: staticanalyzer.py [-h] [-a ANALYZE | -u UNPACK | -f FULL | -b BULK] [-o OUTFILE] [-t THREADS] [--use-xml]

optional arguments:
  -h, --help            show this help message and exit
  -a ANALYZE, --analyze ANALYZE
                        analyze decompiled APKs. Point this to the folder produced by apktool or the -u flag.
  -u UNPACK, --unpack UNPACK
                        Unpack APKs.
  -f FULL, --full FULL  Unpack and Process ONE APK.
  -b BULK, --bulk BULK  To bulk process, use the directory containing ALL target files/folders.
  -o OUTFILE, --outfile OUTFILE
                        output file for bulk analysis, defaults to 00_AnalysisResults
  -t THREADS, --threads THREADS
                        number of parallel threads for processing. Default is 8
  --use-xml             Uses XML for analysis results.
```
