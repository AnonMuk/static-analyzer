import glob
import re
from typing import List

search = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[&-_@.&+]|' +
                    '{!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                    flags=re.MULTILINE)


def find_smali(path: str) -> List[str]:
    filepath = f'{path}/**/*.smali'
    return glob.glob(filepath, recursive=True)


def find_urls(target_list: str) -> dict:
    list = {}
    for file in target_list:
        with open(file, encoding='utf-8') as target:
            all_lines = target.readlines()  # More memory intensive
            target = "".join(all_lines)  # in theory might be faster?
            res = search.findall(target)
            for match in res:  # No idea if it's like cached now or what
                list.setdefault(match, 0)
                list[match] += 1
    return list


def get_urls(path: str) -> dict:
    files = find_smali(path)
    urls = find_urls(files)
    return urls


def multicheck(file_list: List[str],
               targets: List[tuple]) -> bool:
    found = {
        'urls': {},
    }
    for target in targets:
        found.setdefault(target[0], {})
        for function in target[1]:
            found[target[0]].setdefault(function, 0)
    for file in file_list:
        with open(file, encoding='utf-8') as f:
            datafile = f.readlines()
            url_matching = "".join(datafile)
            url_regex = search.findall(url_matching)
            for line in datafile:
                for target in targets:
                    for function in target[1]:
                        if function in line:
                            found[target[0]][function] += 1
            for match in url_regex:  # No idea if it's like cached now or what
                found['urls'].setdefault(match, 0)
                found['urls'][match] += 1
    return found


def check_for_danger(file_list: List[str]) -> dict:
    danger_fns = ['sendTextMessage',
                  'getPackageInfo',
                  'getSimCountryInfo',
                  'Ljava/lang/Runtime;->exec',
                  'getDeviceId',
                  'getSimSerialNumber',
                  'getImei',
                  'getSubscriberId',
                  'setWifiEnabled',
                  'execHttpRequest',
                  'SendBroadcast',
                  'sendDataMessage',
                  'getLastKnownLocation',
                  'getLatitude',
                  'getLongitude',
                  'requestLocationUpdates',
                  'Runtime.exec',
                  'DexClassLoader.Loadclass',
                  'Cipher.getInstance']
    crypto_fns = ['Ljavax/crypto',
                  'AES/CBC/PKCS7PADDING',
                  'SHA1PRNG',
                  'RSA/ECB/OAEPPadding',
                  'AES/CBC/PKCS5PADDING',
                  'Ljavax/crypto/Cipher;->getInstance',
                  'Ljavax/crypto/Cipher;->init ',
                  'generateKey()']

    result = multicheck(file_list,
                        [('dangerous', danger_fns),
                         ('encryption', crypto_fns)])
    return result


def analyze(path: str) -> dict:
    files = find_smali(path)
    result = check_for_danger(files)
    # print(results)
    return result
