import os
import re
import requests

API_BASE = os.getenv('API_BASE_URL', 'https://twitch-miner-api.vercel.app')
TOKEN = os.environ['API_PUBLISH_TOKEN']
version = os.environ['VERSION']


def extract_section(md, v):
    pat = re.compile(r'^##\s+\[?v?' + re.escape(v) + r'\]?.*?$(.*?)(?=^##\s|\Z)', re.M | re.S)
    m = pat.search(md)
    return (m.group(0).strip() if m else '')


def bullets(section):
    out = []
    for line in section.splitlines():
        s = line.strip()
        if s.startswith(('- ', '* ')):
            t = s[2:]
            t = re.sub(r'\s*\(\[.*?\]\(.*?\)\)\s*$', '', t)   # remove link do commit
            t = re.sub(r'^\*\*(.+?)\*\*:\s*', '', t)          # remove **scope**:
            out.append(t.strip())
    return out


with open('CHANGELOG.md', encoding='utf-8') as f:
    md = f.read()

section = extract_section(md, version)
payload = {
    'version': version,
    'description': bullets(section),
    'url': f'https://github.com/nthnunes/twitch-miner/releases/download/v{version}/TwitchMiner.zip',
    'changelog': section,
}

r = requests.post(
    f'{API_BASE}/publish-version',
    json=payload,
    headers={'Authorization': f'Bearer {TOKEN}'},
    timeout=30,
)
r.raise_for_status()
print('Publicado:', version)
