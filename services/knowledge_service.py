"""Small curated OFFLINE medical reference snippets. No web access at runtime.

These short notes are intentionally not a diagnosis or clinical database. They are
packaged with bibliographic URLs to help the user trace the original source later.
"""
import json
import re
from functools import lru_cache
from config.settings import ROOT

@lru_cache(maxsize=1)
def catalog():
    data=json.loads((ROOT/'data'/'medical_knowledge.json').read_text(encoding='utf-8'))
    entries=data.get('entries',[])
    if not isinstance(entries,list):
        raise ValueError('Offline knowledge catalog is malformed')
    return tuple(entries)


def search_knowledge(question: str, limit: int = 3):
    """Rank only exact phrase/word matches; never fabricate a match."""
    content=' '.join(str(question).casefold().split())[:2400]
    scored=[]
    for item in catalog():
        score=0
        for alias in item['aliases']:
            alias=alias.casefold()
            if re.search(r'(?<!\w)'+re.escape(alias)+r'(?!\w)',content):
                score+=2+min(len(alias.split()),3)
        if score:
            scored.append((score,item['id'],item))
    scored.sort(key=lambda t:(-t[0],t[1]))
    return [it for _,_,it in scored[:max(0,min(limit,4))]]


def for_lab_names(labs: list[dict], limit: int = 3):
    """Retrieve notes by recognized lab names, never raw untrusted PDF directives."""
    names='; '.join(x.get('name','') for x in labs[:45])
    return search_knowledge(names,limit)


def grounding_message(entries: list[dict]) -> str:
    if not entries:
        return ''
    lines=[]
    for i,item in enumerate(entries,1):
        lines.append(f'[{i}] {item["title"]} — {item["summary"]}\nSource: {item["source_title"]} ({item["source_url"]})')
    return ('CURATED OFFLINE REFERENCE NOTES (not patient data, not complete guidelines):\n' +
            '\n'.join(lines) + '\nUse these only if relevant; never invent a source or more specific facts. '
            'Where applicable, add a short References section naming only the provided sources with [1], [2]. '
            'The notes are educational context and cannot confirm a diagnosis.\n')
