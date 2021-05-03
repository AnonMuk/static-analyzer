# static-analyzer

Static Analyzer for Smartphone Security

This is a static analysis tool and that's honestly kinda cool of us. It has the capability to unpack APKs and run analysis in bulk and speeds itself up using threading.

This uses **Python 3**, I haven't checked for Python 2 compatibility.

To install needed packages: `pip install -r requirements.txt`

## Usage

```txt
python staticanalyzer.py -h
usage: staticanalyzer.py [-h] [-a ANALYZE | -u UNPACK] [-b] [-t THREADS]

optional arguments:
  -h, --help            show this help message and exit
  -a ANALYZE, --analyze ANALYZE
                        analyze decompiled APKs. Point this to the folder produced by apktool or the -u flag.
  -u UNPACK, --unpack UNPACK
                        Unpack APKs.
  -b, --bulk            To bulk process, use the directory containing ALL target files/folders.
  -t THREADS, --threads THREADS
                        Specifies the number of threads. Defaults to 1.
```
