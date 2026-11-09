# -*- coding: utf-8 -*-
"""Các khối bổ sung cho tab Sức khoẻ team: SLA theo ngày, tương quan FRT,
số nhân viên/hội thoại, mẫu tin dán chung chứa từ cấm."""
import json, os, re, csv, collections, datetime, statistics as st

import ky as _ky

BASE = _ky.BASE
KY, SP = _ky.chon_ky()
ROWS = json.load(open(SP + '/v2rows.json', encoding='utf-8'))
NEW = [r for r in ROWS if not r['cu']]
LBL = {'MAT': 'Mắt', 'BODY': 'Body / Hút mỡ', 'DA_TRE_HOA': 'Da / Trẻ hoá', 'MUI': 'Mũi',
       'NGUC': 'Ngực', 'HAM_MAT': 'Hàm mặt', 'KHAC': 'Khác', 'KHONG_XAC_DINH': 'Chưa xếp được'}
DAYS = _ky.sap_ngay(r['ngay'] for r in ROWS)

def p(a, b, nd=1):
    return round(a / b * 100, nd) if b else None

# ---------- số nhân viên riêng biệt / hội thoại ----------
sonv = {}
for r in csv.DictReader(open(SP + '/ht.csv', encoding='utf-8-sig')):
    try:
        sonv[r['ma']] = int(r['so_nv'] or 0)
    except ValueError:
        sonv[r['ma']] = 0

# ---------- 1. SLA theo ngày: nhân viên × ngày ----------
def sla_cell(rs):
    s = [r for r in rs if r['n_wait'] > 0]
    return {'v': p(sum(1 for r in s if r['worst_wait'] <= 300), len(s)), 'n': len(s)}

nv_list = [nv for nv, c in collections.Counter(
    r['nv'] for r in NEW if r['nv']).most_common() if c >= 30]
sla_nv = []
for nv in nv_list:
    rs = [r for r in NEW if r['nv'] == nv]
    row = {'k': nv, 'all': sla_cell(rs)}
    for d in DAYS:
        row[d] = sla_cell([r for r in rs if r['ngay'] == d])
    sla_nv.append(row)
sla_nv.sort(key=lambda x: -(x['all']['v'] or 0))

sla_dv = []
for key, lab in LBL.items():
    rs = [r for r in NEW if r['dv'] == key]
    if not rs:
        continue
    row = {'k': lab, 'all': sla_cell(rs)}
    for d in DAYS:
        row[d] = sla_cell([r for r in rs if r['ngay'] == d])
    sla_dv.append(row)
sla_dv.sort(key=lambda x: -(x['all']['v'] or 0))

sla_team = {'k': 'Toàn đội', 'all': sla_cell(NEW)}
for d in DAYS:
    sla_team[d] = sla_cell([r for r in NEW if r['ngay'] == d])

# ---------- 2. Diễn biến theo ngày ----------
trend = []
for d in DAYS:
    rs = [r for r in NEW if r['ngay'] == d]
    d6 = [r for r in rs if r['du6']]
    d24 = [r for r in rs if r['du24']]
    d48 = [r for r in rs if r['du48']]
    s = [r for r in rs if r['n_wait'] > 0]
    chua = [r for r in rs if not r['co_sdt']]
    trend.append({
        'k': d, 'n': len(rs), 'sdt': sum(1 for r in rs if r['co_sdt']),
        'q1': p(sum(1 for r in rs if r['co_sdt']), len(rs)),
        'q2': p(sum(1 for r in d6 if r['gio_sdt'] is not None and r['gio_sdt'] <= 6), len(d6)),
        'q2n': len(d6),
        'q3': p(sum(1 for r in d24 if r['gio_sdt'] is not None and r['gio_sdt'] <= 24), len(d24)),
        'q3n': len(d24),
        'q4': p(sum(1 for r in d48 if r['gio_sdt'] is not None and r['gio_sdt'] <= 48), len(d48)),
        'q4n': len(d48),
        'q5': p(sum(1 for r in s if r['worst_wait'] <= 300), len(s)), 'q5n': len(s),
        'mot_cham': p(sum(1 for r in rs if r['mot_cham']), len(rs)),
        'cham_lai': p(sum(1 for r in chua if r['cham_lai'] >= 1), len(chua)),
        'treo': sum(1 for r in rs if r['treo']),
    })

# ---------- 3. Tương quan FRT (chỉ khách mới, bỏ lượt ngoài giờ) ----------
BINS = [(0, 60, '< 1 phút'), (60, 300, '1–5 phút'), (300, 900, '5–15 phút'),
        (900, 1800, '15–30 phút'), (1800, 10 ** 9, '> 30 phút')]
resp_eng, resp_rs = [], []
for lo, hi, lab in BINS:
    sub = [r for r in NEW if r['first_wait'] is not None and lo <= r['first_wait'] < hi]
    resp_eng.append({'k': lab, 'v': p(sum(1 for r in sub if r['n_kh'] >= 2), len(sub)),
                     'n': len(sub)})
    s48 = [r for r in sub if r['du48']]
    resp_rs.append({'k': lab,
                    'v': p(sum(1 for r in s48 if r['gio_sdt'] is not None and r['gio_sdt'] <= 48),
                           len(s48)), 'n': len(s48)})

# ---------- 4. Số nhân viên cùng trả lời ----------
handoff = []
for k, lab in [(1, '1 người'), (2, '2 người'), (3, '3 người'), (4, '4 người trở lên')]:
    if k < 4:
        sub = [r for r in NEW if sonv.get(r['ma'], 0) == k]
    else:
        sub = [r for r in NEW if sonv.get(r['ma'], 0) >= 4]
    s48 = [r for r in sub if r['du48']]
    handoff.append({'k': lab,
                    'v': p(sum(1 for r in s48 if r['gio_sdt'] is not None and r['gio_sdt'] <= 48),
                           len(s48)),
                    'n': len(s48), 'ht': len(sub)})

# ---------- 5. Mẫu tin dán chung chứa từ cấm ----------
txt = open(_ky.nguon_txt(KY), encoding='utf-8-sig').read()
parts = re.split(r'\n## \d+\. (HT-[0-9a-f]+)\n', txt)
CONV = {parts[i]: parts[i + 1] for i in range(1, len(parts), 2)}
NVLINE = re.compile(r'\*\*NV \((NV-\d+)\)[^:]*:\*\* (.*)')
BANW = [('an toàn tuyệt đối', r'an toàn tuyệt đối|tuyệt đối an toàn'),
        ('không đau', r'không đau'), ('không để lại sẹo', r'không để lại sẹo|không có sẹo'),
        ('hoàn toàn yên tâm', r'hoàn toàn yên tâm'), ('vĩnh viễn', r'vĩnh viễn'),
        ('trọn đời', r'trọn đời'),
        ('không biến chứng', r'(không|ko)\s+(lo\s+)?(có\s+)?biến chứng'),
        ('chắc chắn', r'chắc chắn (giảm|khỏi|được|hết)')]
norm = lambda s: re.sub(r'\s+', ' ', re.sub(r'\[[^\]]*\]', '', s)).strip()
tmpl = collections.defaultdict(lambda: {'ht': set(), 'nv': set(), 'full': '', 'w': set()})
for ma, t in CONV.items():
    for m in NVLINE.finditer(t):
        nv, msg = m.group(1), m.group(2)
        hits = [w for w, rx in BANW if re.search(rx, msg, re.I)]
        if not hits:
            continue
        k = norm(msg).lower()[:70]
        e = tmpl[k]
        e['ht'].add(ma); e['nv'].add(nv); e['w'].update(hits)
        if not e['full']:
            e['full'] = norm(msg)[:260]
tmpl_out = sorted(
    [{'n': len(v['ht']), 'nv': len(v['nv']), 'w': sorted(v['w']), 'full': v['full']}
     for v in tmpl.values()], key=lambda x: -x['n'])[:8]

# ---------- 6. Câu hỏi giá ----------
GIA = re.compile(r'(bao nhiêu|bao nhiu|giá|chi phí|hết nhiêu|nhiêu tiền|bn tiền|bnhiêu)', re.I)
gia_rs = []
for r in NEW:
    t = CONV.get(r['ma'], '')
    kh = ' '.join(m for m in re.findall(r'\*\*KH:\*\* (.*)', t))
    if GIA.search(kh):
        gia_rs.append(r)
g48 = [r for r in gia_rs if r['du48']]
n48 = [r for r in NEW if r['du48'] and r not in gia_rs]
gia = {'n': len(gia_rs), 'pc': p(len(gia_rs), len(NEW)),
       'q1': p(sum(1 for r in gia_rs if r['co_sdt']), len(gia_rs)),
       'q4': p(sum(1 for r in g48 if r['gio_sdt'] is not None and r['gio_sdt'] <= 48), len(g48)),
       'q4n': len(g48),
       'q4_khac': p(sum(1 for r in n48 if r['gio_sdt'] is not None and r['gio_sdt'] <= 48),
                    len(n48)), 'q4_khacn': len(n48)}

json.dump({'slaNv': sla_nv, 'slaDv': sla_dv, 'slaTeam': sla_team, 'trend': trend,
           'respEng': resp_eng, 'respRs': resp_rs, 'handoff': handoff,
           'tmpl': tmpl_out, 'gia': gia, 'days': DAYS},
          open(SP + '/v2extra.json', 'w', encoding='utf-8'), ensure_ascii=False)

print('SLA toàn đội theo ngày:', {d: sla_team[d] for d in DAYS})
print('\nDiễn biến:')
for t in trend:
    print('  {k}  n={n:4d}  Q1 {q1}%  Q3 {q3}% ({q3n})  Q5 {q5}%  1chạm {mot_cham}%  treo {treo}'
          .format(**t))
print('\nFRT → khách trò chuyện tiếp:')
for b in resp_eng:
    print('  {k:<12} {v}%  (n={n})'.format(**b))
print('FRT → ra số 48h:')
for b in resp_rs:
    print('  {k:<12} {v}%  (n={n})'.format(**b))
print('\nSố nhân viên cùng trả lời → ra số 48h:')
for b in handoff:
    print('  {k:<16} {v}%  (mẫu 48h {n} · tổng {ht})'.format(**b))
print('\nCâu hỏi giá:', gia)
print('\nMẫu tin chứa từ cấm:')
for t in tmpl_out:
    print('  %3d HT · %d NV · %s | %s' % (t['n'], t['nv'], '/'.join(t['w']), t['full'][:90]))
