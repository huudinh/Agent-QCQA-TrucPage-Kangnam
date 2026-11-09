# -*- coding: utf-8 -*-
"""Một lệnh: file hội thoại .txt → tools/data/v2.js cho dashboard trực page.

  python tools/bao-cao.py "du-lieu/<file>.txt"            cả chuỗi từ file gốc
  python tools/bao-cao.py "du-lieu/<file>.txt" --kiem      chạy L0 trước khi tính
  python tools/bao-cao.py --ky 03-11_05-11-2026           chạy lại từ ht.csv đã có

Chuỗi: tp.py tinh → v2calc → v2agg → v2extra → v2slices → v2bundle.

⛔ File này KHÔNG tự tính con số nào. Mọi chỉ số vẫn do đúng các script cũ
tính ra — đây chỉ là người nối dây và truyền tên kỳ, để luật ① còn đứng:
một hội thoại chấm đúng một lần, mọi bảng sau đọc lại từ out/<ky>/ht.csv.
"""
import os
import subprocess
import sys
import time

TOOLS = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(TOOLS).replace('\\', '/') + '/'
sys.path.insert(0, TOOLS)

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

BUOC = [('v2calc',   'v2rows.json'),
        ('v2agg',    'v2.json'),
        ('v2extra',  'v2extra.json'),
        ('v2slices', 'v2slices.json'),
        ('v2pack',   'tools/data/rows.js'),
        ('v2bundle', 'tools/data/v2.js')]


def chay(nhan, args, env):
    print('\n── ' + nhan + ' ' + '─' * max(3, 56 - len(nhan)))
    t0 = time.time()
    r = subprocess.run([sys.executable] + args, cwd=BASE, env=env)
    if r.returncode != 0:
        raise SystemExit(f'\n⛔ Dừng ở "{nhan}" (mã {r.returncode}). '
                         'Các bước sau không chạy, nên data/v2.js vẫn là bản cũ.')
    print(f'   ✓ {time.time() - t0:.1f}s')


def main():
    av = sys.argv[1:]
    kiem = '--kiem' in av
    av = [a for a in av if a != '--kiem']

    ky, txt = None, None
    if '--ky' in av:
        i = av.index('--ky')
        if len(av) <= i + 1:
            raise SystemExit('--ky cần tên kỳ, ví dụ: --ky 03-11_05-11-2026')
        ky = av[i + 1]
    else:
        if not av:
            raise SystemExit(__doc__)
        p = av[0] if os.path.isabs(av[0]) else BASE + av[0]
        if not os.path.isfile(p):
            import glob as _g
            co = sorted(os.path.basename(x) for x in _g.glob(BASE + 'du-lieu/*.txt'))
            ds = '\n'.join('    du-lieu/' + x for x in co) or '    (du-lieu/ chưa có file .txt nào)'
            raise SystemExit(f'không thấy file: {p}\n\n  du-lieu/ đang có:\n{ds}\n\n  Chép bản xuất vào du-lieu/ rồi chạy lại.')
        txt = p.replace('\\', '/')
        # Tên kỳ lấy bằng chính hàm của tp.py, không tự đặt lại quy ước
        import tp
        _, meta = tp.doc_file(txt)
        ky = tp._ten_ky(meta)
        print(f'file : {os.path.basename(txt)}')
        print(f'kỳ   : {ky}   ({meta["ky_dau"]:%d/%m} → {meta["ky_cuoi"]:%d/%m/%Y})')
        print(f'hội thoại trong file: {len(_):,}'.replace(',', '.'))

    env = dict(os.environ, TP_KY=ky, PYTHONIOENCODING='utf-8')
    if txt:
        env['TP_TXT'] = os.path.relpath(txt, BASE).replace('\\', '/')
        if kiem:
            chay('L0 · tp.py kiem', ['tools/tp.py', 'kiem', env['TP_TXT']], env)
        chay('L1 · tp.py tinh → ht.csv', ['tools/tp.py', 'tinh', env['TP_TXT']], env)
    elif not os.path.isfile(f'{BASE}out/{ky}/ht.csv'):
        raise SystemExit(f'chưa có out/{ky}/ht.csv\n'
                         '  chạy với file .txt thay vì --ky để tạo nó.')

    for ten, ra in BUOC:
        chay(f'{ten} → {ra}', [f'tools/{ten}.py', ky], env)

    js = BASE + 'tools/data/v2.js'
    n = os.path.getsize(js) if os.path.isfile(js) else 0
    print('\n' + '═' * 60)
    print(f'✓ Xong. tools/data/v2.js — {n / 1024:,.0f} KB'.replace(',', '.'))
    print('\nSoát lại trước khi đăng:  tools/chot-so.html (kéo tools/data/v2.js vào)')
    print('\nRồi đưa câu này cho Claude Code:')
    print('  publish tools/truc-page.html lên '
          'https://claude.ai/artifact/NjRqQFQ1XYZwLNcrg8k1JD,')
    print('  kèm files = {"data/v2.js": "tools/data/v2.js", "data/rows.js": "tools/data/rows.js"}')


if __name__ == '__main__':
    main()
