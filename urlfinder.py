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
