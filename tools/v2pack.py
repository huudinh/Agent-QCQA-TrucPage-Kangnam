# -*- coding: utf-8 -*-
"""Nén bảng hội thoại thành dạng cột để trang tự lọc mọi chiều.

Cột phân loại đổi thành chỉ số vào từ điển, cờ thành 0/1, bỏ những trường
trang không dùng tới. Khoảng 71 B/dòng — nhẹ hơn chính file lát cắt.

⛔ Không tính lại gì. Mọi con số vẫn do v2calc.py chấm; đây chỉ là đổi cách
   đóng gói để trang lọc được theo ngày, page, khung giờ, nguồn.
"""
import json
import os

import ky as _ky

KY, SP = _ky.chon_ky()

# đúng những trường mà phần tổng hợp của trang cần, không hơn
CAT = ['ngay', 'nv', 'dv', 'kg', 'nguon', 'tt', 'page', 'nhiet']
CO = ['cu', 'co_sdt', 'du6', 'du24', 'du48', 'treo', 'tu_choi', 'mot_cham', 'kh_mot_cham']
SO = ['gio_sdt', 'n_wait', 'first_wait', 'worst_wait', 'n_kh', 'n_xin', 'cham_lai', 'so_nv',
      'n_wait_ok5', 'n_wait_ok2', 'sum_wait']


def lam():
    rows = json.load(open(SP + '/v2rows.json', encoding='utf-8'))
    tu = {c: sorted({str(r.get(c) or '') for r in rows}) for c in CAT}
    idx = {c: {v: i for i, v in enumerate(tu[c])} for c in CAT}

    cot = {}
    for c in CAT:
        cot[c] = [idx[c][str(r.get(c) or '')] for r in rows]
    for c in CO:
        cot[c] = [1 if r.get(c) else 0 for r in rows]
    for c in SO:
        v = []
        for r in rows:
            x = r.get(c)
            v.append(None if x is None else (round(x, 2) if isinstance(x, float) else x))
        cot[c] = v
    return {'ky': KY, 'n': len(rows), 'tu': tu, 'cot': cot}


if __name__ == '__main__':
    pack = lam()
    s = json.dumps(pack, ensure_ascii=False, separators=(',', ':'))
    dest = _ky.BASE + 'tools/data/rows.js'
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('var ROWS = ' + s + ';\n')
    goc = os.path.getsize(SP + '/v2rows.json')
    print(f'kỳ          : {KY}')
    print(f'dòng        : {pack["n"]:,}'.replace(',', '.'))
    print(f'gốc         : {goc:,} B'.replace(',', '.'))
    print(f'→ rows.js   : {len(s.encode()):,} B'.replace(',', '.')
          + f'  ({len(s.encode()) // max(1, pack["n"])} B/dòng)')
