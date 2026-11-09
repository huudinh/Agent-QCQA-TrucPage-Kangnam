# -*- coding: utf-8 -*-
"""Gói 3 file JSON chỉ số thành 1 file JS cho artifact nạp rời.

Dùng: python tools/v2bundle.py [ten-ky]
  ten-ky  tên thư mục trong out/ (mặc định: thư mục mới nhất)

Ra: tools/data/v2.js  ->  publish kèm artifact bằng tham so `files`.
"""
import json, os
import ky as _ky

BASE = _ky.BASE
ky, SP = _ky.chon_ky()

# bien trong page  <-  file JSON sinh boi v2agg / v2extra / v2slices
NGUON = [('V2', 'v2.json'), ('EX', 'v2extra.json'), ('SLICES', 'v2slices.json')]

def nen(f):
    """Doc JSON roi serialize lai dang nen — giong het chuoi nhung trong page."""
    with open(f'{SP}/{f}', encoding='utf-8') as fh:
        return json.dumps(json.load(fh), ensure_ascii=False, separators=(',', ':'))

js = ''.join(f'var {bien} = {nen(f)};\n' for bien, f in NGUON)

dest = BASE + 'tools/data/v2.js'
os.makedirs(os.path.dirname(dest), exist_ok=True)
with open(dest, 'w', encoding='utf-8', newline='\n') as fh:
    fh.write(js)

print(f'ky           : {ky}')
for bien, f in NGUON:
    print(f'  {bien:7s} <- {f:16s} {os.path.getsize(f"{SP}/{f}"):>9,} B')
print(f'-> tools/data/v2.js  {len(js.encode("utf-8")):,} B')
