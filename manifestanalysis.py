import os
from glob import glob
from threading import Thread
from xml.dom.minidom import parseString

import yaml
from bs4 import BeautifulSoup as bs
from dicttoxml import dicttoxml

import smalianalysis

'''
# decompile apk (APKTool)
- get smali files
'''


def meta_constructor(loader, node):
    '''
    function to make yaml play nice
    '''
    value = loader.construct_mapping(node)
    return value


yaml.add_constructor(u'tag:yaml.org,2002:brut.androlib.meta.MetaInfo',
                     meta_constructor)  # This makes sure yaml doesn't break


def bulk_handler(path: str, num_threads: int):
    globpath = os.path.join(path, '*', '')
    dirs = glob(globpath)
    analyzers = []
    for i in range(num_threads):
        analyzer = Analysis(target_filepaths=dirs[i::num_threads])
        analyzer.thread.start()
        analyzers.append(analyzer)
    for analyzer in analyzers:
        if analyzer.thread.is_alive():
            analyzer.thread.join(60)
    print("All APKs analyzed.")


def manifest_name(soup: bs) -> list:
    '''
    analyzes a soup file to locate the manifest name
    '''
    manifest = soup.find('manifest')
    return manifest.get('package')


def analyze_permissions(soup: bs) -> list:
    '''
    Analyzes a soup file to locate app permissions
    '''
    permissions = []
    manifests = soup.find_all('manifest')  # Should be one, catching edges
    for manifest in manifests:
        for permission in manifest.find_all('uses-permission'):
            permissions.append(permission.get('android:name'))
    return permissions


def analyze_intents(soup: bs) -> list:
    intents = []
    manifests = soup.find_all('manifest')  # should only be one manifest
    for manifest in manifests:
        for intent_filter in manifest.find_all('intent-filter'):
            for action in intent_filter.find_all('action'):
                intents.append(action.get('android:name'))
    return intents


def analyze_services(soup: bs) -> list:
    services = []
    manifests = soup.find_all('manifest')  # should only be one manifest
    for manifest in manifests:
        for service in manifest.find_all('service'):
            services.append(service.get('android:name'))
    return services


def analyze_receivers(soup: bs) -> list:
    receivers = []
    manifests = soup.find_all('manifest')  # just in case there's > 1
    for manifest in manifests:
        for receiver in manifest.find_all('receiver'):
            receivers.append(receiver.get('android:name'))
    return receivers


def analysis(path: str) -> None:
    '''
    takes filepath and does analysis.
    '''
    dict = {}
    filepath = os.path.join(path, 'AndroidManifest.xml')
    apkt_yaml = os.path.join(path, 'apktool.yml')
    results = os.path.join(path, 'result.xml')
    # print(f'Processing {filepath} and {apkt_yaml}, results to {results}.')
    with open(filepath, encoding='utf-8') as manifest:  # using UTF-8
        soup = bs(manifest, "lxml")
        dict['package'] = manifest_name(soup)
        manifest = {
            'permissions': analyze_permissions(soup),
            'intents': analyze_intents(soup),
            'services': analyze_services(soup),
            'receivers': analyze_receivers(soup)
        }
        dict['manifest'] = manifest
    with open(apkt_yaml, encoding='utf-8') as apktool_info:
        apkinfo = yaml.load(apktool_info, Loader=yaml.FullLoader)
        dict['sdkInfo'] = apkinfo['sdkInfo']  # no methods, a dict
    smali_results = smalianalysis.analyze(path)
    dict['urls'] = smali_results['urls']
    dict['dangerous_functions'] = smali_results['dangerous']
    dict['encryption_text'] = smali_results['encryption']
    write_results(results, dict)
    # print(f'{path} processed.')


def write_results(results, dict):
    with open(results, 'w', encoding='utf-8') as outfile:
        xml = dicttoxml(dict)
        dom = parseString(xml)
        outfile.write(dom.toprettyxml())


class Analysis:
    def __init__(self, target_filepaths):
        self.paths = target_filepaths
        self.total_paths = len(target_filepaths)
        self.thread = Thread(target=self.bulk_analyze)

    def bulk_analyze(self):
        current_file = 1
        for path in self.paths:
            print(f'{self.thread.name}: ' +
                  f'File {current_file} of {self.total_paths}: {path}')
            try:
                analysis(path)
            except Exception as e:
                print(f'Error {e} on {path}, continuing.')
            current_file += 1
        print(f'{self.thread.name} analyzed assigned files.')
