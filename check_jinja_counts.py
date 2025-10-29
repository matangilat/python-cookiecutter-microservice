#!/usr/bin/env python3
import os,re
root='.'
def remove_raw_blocks(s):
    # remove content between {% raw %} and {% endraw %} (including the tags)
    return re.sub(r"{%\\s*raw\\s*%}.*?{%\\s*endraw\\s*%}", "", s, flags=re.S)

for dirpath,_,files in os.walk(root):
    for f in files:
        path=os.path.join(dirpath,f)
        # skip the checker itself
        if path.endswith('check_jinja_counts.py'):
            continue
        try:
            with open(path,'r',encoding='utf-8') as fh:
                s=fh.read()
        except Exception:
            continue
        s2 = remove_raw_blocks(s)
        a=len(re.findall(r'{%\\s*if\\b',s2))
        b=len(re.findall(r'{%\\s*endif\\b',s2))
        if a!=b:
            print(f'{path}: if={a} endif={b}')
