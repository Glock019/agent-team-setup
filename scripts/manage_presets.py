"""Maintain reusable team presets in a caller-owned, persistent JSON registry."""
import argparse
import json
import os
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path


def normalize(source):
    if source.get('schema_version') != 1:
        raise ValueError('Unsupported schema version')
    members = source.get('members')
    if not isinstance(members, list) or not 1 <= len(members) <= 30:
        raise ValueError('Expected 1–30 members')
    result = []
    ids = set()
    for m in members:
        import re
        if not isinstance(m, dict) or not re.fullmatch(r'M[1-9][0-9]*', str(m.get('id', ''))) or m['id'] in ids:
            raise ValueError('Invalid or duplicate member ID')
        ids.add(m['id'])
        for k in ('role', 'model', 'effort'):
            if not isinstance(m.get(k), str) or not m[k].strip():
                raise ValueError('Missing member ' + k)
        deps = m.get('dependencies', [])
        if not isinstance(deps, list) or not all(isinstance(x, str) for x in deps):
            raise ValueError('Invalid dependencies')
        result.append({k:m[k] for k in ('id','role','model','effort')} | {
            'scope':m.get('scope','只读') if isinstance(m.get('scope','只读'),str) else '只读',
            'task':'', 'dependencies':list(dict.fromkeys(deps))})
    links = {m['id']:m['dependencies'] for m in result}
    visiting, done = set(), set()
    def visit(i):
        if i in visiting: raise ValueError('Cyclic dependencies')
        if i in done: return
        visiting.add(i)
        for d in links[i]:
            if d not in links: raise ValueError('Unknown dependency')
            visit(d)
        visiting.remove(i); done.add(i)
    for i in links: visit(i)
    n = source.get('max_concurrency')
    if type(n) is not int or n < 1: raise ValueError('Invalid concurrency')
    assignment = source.get('assignment')
    if assignment not in ('auto','manual'): raise ValueError('Choose assignment mode')
    return {'schema_version':1, 'kind':'agent_team_preset', 'assignment':assignment,
            'start_mode':'wait_for_start', 'max_concurrency':n, 'members':result}


def read_store(path):
    if not path.exists(): return {'schema_version':1,'presets':[]}
    data=json.loads(path.read_text(encoding='utf-8'))
    if data.get('schema_version')!=1 or not isinstance(data.get('presets'),list):
        raise ValueError('Invalid preset registry; will not overwrite')
    return data


def save(path, source, name, replace=False, expected_version=None):
    name=name.strip()
    if not name or len(name)>80: raise ValueError('Name must be 1–80 characters')
    normalized=normalize(source)
    path.parent.mkdir(parents=True,exist_ok=True)
    lock=path.with_name(path.name+'.lock')
    fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
    try:
        os.close(fd)
        data=read_store(path)
        matches=[x for x in data['presets'] if x['name'].casefold()==name.casefold()]
        if len(matches)>1: raise ValueError('Ambiguous duplicate names')
        old=matches[0] if matches else None
        if old and (not replace or expected_version!=old['preset_version']):
            raise ValueError('Name already exists; explicit replacement and matching expected version required')
        if not old and replace: raise ValueError('Cannot replace a missing preset')
        item=normalized | {'preset_id':old['preset_id'] if old else str(uuid.uuid4()),
            'name':name,'preset_version':old['preset_version']+1 if old else 1,
            'updated_at':datetime.now(timezone.utc).isoformat()}
        if old: data['presets'][data['presets'].index(old)]=item
        else: data['presets'].append(item)
        temp=None
        try:
            with tempfile.NamedTemporaryFile(mode='w',dir=path.parent,encoding='utf-8',delete=False) as f:
                temp=f.name;json.dump(data,f,ensure_ascii=False,indent=2);f.flush();os.fsync(f.fileno())
            os.replace(temp,path)
        finally:
            if temp and os.path.exists(temp): os.unlink(temp)
        return item
    finally:
        lock.unlink()


def main():
    p=argparse.ArgumentParser();p.add_argument('--store',type=Path,required=True)
    sub=p.add_subparsers(dest='command',required=True)
    s=sub.add_parser('save');s.add_argument('--input',type=Path,required=True);s.add_argument('--name',required=True)
    s.add_argument('--replace',action='store_true');s.add_argument('--expected-version',type=int)
    sub.add_parser('list')
    g=sub.add_parser('get');g.add_argument('--name',required=True)
    a=p.parse_args()
    if a.command=='save': result=save(a.store,json.loads(a.input.read_text(encoding='utf-8')),a.name,a.replace,a.expected_version)
    else:
        items=read_store(a.store)['presets']
        if a.command=='list': result=items
        else:
            found=[x for x in items if x['name'].casefold()==a.name.strip().casefold()]
            if len(found)!=1: raise ValueError('Preset missing or ambiguous')
            result=found[0]
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__': main()
