# -*- coding: utf-8 -*-
"""Gộp nhiều bản xuất Caresoft thành MỘT file của một kỳ dài hơn.

  python tools/gop.py "du-lieu/a.txt" "du-lieu/b.txt" [-o du-lieu/ten.txt]

Vì sao cần: Caresoft xuất theo cửa sổ ngày, nên một hội thoại kéo dài qua
nhiều cửa sổ bị cắt làm đôi — mỗi file giữ một khúc tin của chính nó. Chạy
riêng từng file thì khúc sau vô hình với kỳ trước và ngược lại; ngày gắn cho
hội thoại cũng sai vì tin đầu của khách nằm ở file kia.

Gộp theo MÃ hội thoại rồi xếp tin theo thời gian là dựng lại đúng hội thoại
thật. ⛔ Không sửa, không bịa, không bỏ tin nào — chỉ nối và xếp.
"""
import os
import re
import sys
from datetime import datetime

RE_KY = re.compile(r'^-\s*Kỳ:\s*(\d{2})/(\d{2})/(\d{4})\s*→\s*(\d{2})/(\d{2})/(\d{4})')
RE_PAGE = re.compile(r'^#\s+Page:\s*(.+?)\s*$')
RE_HT = re.compile(r'^##\s+(\d+)\.\s+(HT-[0-9a-fA-F]+)\s*$')
RE_TIN = re.compile(r'^\[(\d{2})/(\d{2})\s+(\d{2}):(\d{2}):(\d{2})\]\s+\*\*')
RE_SAU = re.compile(r'^\*\(lượt cuối được\s+NV-\d+')


def doc(path):
    """→ (ky_dau, ky_cuoi, [(page, ma, [khối tin])]) giữ nguyên thứ tự gặp."""
    txt = open(path, encoding='utf-8-sig').read()
    dong = txt.split('\n')
    ky = None
    for ln in dong[:40]:
        m = RE_KY.match(ln)
        if m:
            a = [int(x) for x in m.groups()]
            ky = (datetime(a[2], a[1], a[0]), datetime(a[5], a[4], a[3]))
            break
    if not ky:
        raise SystemExit(f'⛔ {os.path.basename(path)}: không thấy dòng "- Kỳ: ..." ở đầu file.')

    ra, page, ma, khoi = [], None, None, None

    def dong_lai():
        if ma:
            ra.append((page, ma, khoi))

    for ln in dong:
        m = RE_PAGE.match(ln)
        if m:
            dong_lai()
            page, ma, khoi = m.group(1), None, None
            continue
        m = RE_HT.match(ln)
        if m:
            dong_lai()
            ma, khoi = m.group(2), []
            continue
        if ma is None:
            continue
        if RE_TIN.match(ln.strip()):
            khoi.append([ln.rstrip()])
        elif khoi:
            khoi[-1].append(ln.rstrip())          # dòng tiếp của tin nhiều dòng
        elif ln.strip():
            khoi.append([ln.rstrip()])            # dòng lạ trước tin đầu — vẫn giữ
    dong_lai()
    return ky[0], ky[1], ra


def khoa(kh):
    """Mốc thời gian của một khối tin, để xếp lại cho đúng thứ tự."""
    m = RE_TIN.match(kh[0].strip())
    if not m:
        return (99, 99, 99, 99, 99)
    d, mo, H, M, S = (int(x) for x in m.groups())
    return (mo, d, H, M, S)


def main():
    av = [a for a in sys.argv[1:] if a != '-o']
    ra = None
    if '-o' in sys.argv[1:]:
        i = sys.argv[1:].index('-o')
        ra = sys.argv[1:][i + 1]
        av = [a for a in av if a != ra]
    if len(av) < 2:
        raise SystemExit(__doc__)

    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
    bo_trung = [0]
    dau, cuoi = None, None
    trang = []                 # thứ tự page gặp đầu tiên
    hoi = {}                   # ma → {'page':…, 'khoi':[…]}
    thu_tu = []                # thứ tự mã gặp đầu tiên
    nguon = []

    for p in av:
        pp = p if os.path.isabs(p) else base + p
        if not os.path.isfile(pp):
            raise SystemExit(f'⛔ không thấy file: {pp}')
        d, c, ds = doc(pp)
        dau = d if dau is None or d < dau else dau
        cuoi = c if cuoi is None or c > cuoi else cuoi
        nguon.append((os.path.basename(pp), len(ds), d, c))
        rieng = {}
        for page, ma, khoi in ds:
            if page not in trang:
                trang.append(page)
            if ma not in hoi:
                hoi[ma] = {'page': page, 'khoi': [], 'da': set()}
                thu_tu.append(ma)
            rieng.setdefault(ma, []).extend(khoi)

        # Chặn đếm trùng CHỈ GIỮA CÁC FILE: lỡ đưa vào một file GỘP cùng với
        # chính nguồn của nó thì mọi khối tin là bản sao y hệt.
        # ⛔ Trong CÙNG một file, tin lặp y hệt là dữ liệu thật (nhân viên gửi
        #    lại đúng câu đó) — phải giữ, nếu không số sẽ lệch với đường ống gốc.
        for ma, khoi in rieng.items():
            h = hoi[ma]
            for k in khoi:
                if '\n'.join(k) in h['da']:
                    bo_trung[0] += 1
                    continue
                h['khoi'].append(k)
            h['da'].update('\n'.join(k) for k in khoi)

    # xếp lại tin trong từng hội thoại; dòng "lượt cuối được…" luôn ở cuối
    for ma in thu_tu:
        kh = hoi[ma]['khoi']
        sau = [k for k in kh if RE_SAU.match(k[0].strip())]
        tin = [k for k in kh if not RE_SAU.match(k[0].strip())]
        tin.sort(key=khoa)
        hoi[ma]['khoi'] = tin + sau[-1:]

    ten = ra or f'du-lieu/GOP_{dau:%Y%m%d}-{cuoi:%Y%m%d}.txt'
    dest = ten if os.path.isabs(ten) else base + ten

    out = [f'# {os.path.splitext(os.path.basename(dest))[0]}', '',
           f'- Kỳ: {dau:%d/%m/%Y} → {cuoi:%d/%m/%Y}',
           f'- Hội thoại: {len(thu_tu)}', '', '---', '']
    for page in trang:
        mas = [m for m in thu_tu if hoi[m]['page'] == page]
        if not mas:
            continue
        out += [f'# Page: {page}', '']
        for i, ma in enumerate(mas, 1):
            out += [f'## {i}. {ma}', '']
            for kh in hoi[ma]['khoi']:
                out += kh
            out += ['']
    with open(dest, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(out))

    tong_vao = sum(n for _, n, _, _ in nguon)
    print('Nguồn:')
    for ten_f, n, d, c in nguon:
        print(f'   {ten_f}  —  {n:,} hội thoại  ·  {d:%d/%m} → {c:%d/%m}'.replace(',', '.'))
    print(f'\nGộp: {tong_vao:,} → {len(thu_tu):,} hội thoại '
          f'({tong_vao - len(thu_tu):,} mã trùng được nối lại)'.replace(',', '.'))
    if bo_trung[0]:
        print(f'\n⚠️  Bỏ {bo_trung[0]:,} khối tin trùng y hệt.'.replace(',', '.'))
        print('    Số lớn nghĩa là bạn đã đưa vào một file GỘP cùng với chính nguồn của nó —')
        print('    chỉ gộp các bản xuất GỐC từ Caresoft.')
    print(f'Kỳ : {dau:%d/%m/%Y} → {cuoi:%d/%m/%Y}  ·  {len(trang)} page')
    print(f'→ {os.path.relpath(dest, base)}  ({os.path.getsize(dest):,} B)'.replace(',', '.'))


if __name__ == '__main__':
    main()
