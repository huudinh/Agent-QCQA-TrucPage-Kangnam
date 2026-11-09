# -*- coding: utf-8 -*-
"""Bộ dữ liệu đầy đủ cho từng lát cắt (toàn bộ · 8 dịch vụ · 6 thị trường).
Mỗi lát có: KPI đội, ma trận nhân viên, diễn biến theo ngày, SLA theo ngày,
tương quan FRT, số nhân viên/hội thoại, câu hỏi giá."""
import json, os, csv, collections, statistics as st

import ky as _ky

BASE = _ky.BASE
KY, SP = _ky.chon_ky()
ROWS = [r for r in json.load(open(SP + '/v2rows.json', encoding='utf-8')) if not r['cu']]
ALLROWS = json.load(open(SP + '/v2rows.json', encoding='utf-8'))
DAYS = _ky.sap_ngay(r['ngay'] for r in ALLROWS)
DVL = [('MAT', 'Mắt'), ('MUI', 'Mũi'), ('NGUC', 'Ngực'), ('HAM_MAT', 'Hàm mặt'),
       ('BODY', 'Body / Hút mỡ'), ('DA_TRE_HOA', 'Da / Trẻ hoá'), ('KHAC', 'Khác'),
       ('KHONG_XAC_DINH', 'Chưa xếp được')]
MKL = [('HA_NOI', 'Hà Nội'), ('HO_CHI_MINH', 'Hồ Chí Minh'), ('TINH_KHAC', 'Các tỉnh khác'),
       ('VIET_KIEU', 'Việt kiều'), ('QUOC_TE', 'Quốc tế'), ('CHUA_RO', 'Chưa xác định')]
SHORT = dict(DVL); SHORT.update({'KHONG_XAC_DINH': 'Chưa rõ', 'BODY': 'Béo/Hút mỡ',
                                 'DA_TRE_HOA': 'Da'})
import diem_ai as _ai
AI = _ai.AI
SONV = {}
for r in csv.DictReader(open(SP + '/ht.csv', encoding='utf-8-sig')):
    try:
        SONV[r['ma']] = int(r['so_nv'] or 0)
    except ValueError:
        SONV[r['ma']] = 0

def p(a, b, nd=1):
    return round(a / b * 100, nd) if b else None

def kpis(rs, allrs):
    """allrs = kể cả khách cũ, để đếm tổng hội thoại"""
    d6 = [r for r in rs if r['du6']]
    d24 = [r for r in rs if r['du24']]
    d48 = [r for r in rs if r['du48']]
    sla = [r for r in rs if r['n_wait'] > 0]
    sla1 = [r for r in rs if r['first_wait'] is not None]
    chua = [r for r in rs if not r['co_sdt']]
    # SLA theo LƯỢT
    waits = []
    for r in rs:
        if r['n_wait']:
            waits.append(r['worst_wait'])
    luot = sum(r['n_wait'] for r in rs)
    luot_ok = sum(r['n_wait_ok5'] for r in rs)
    luot_ok2 = sum(r['n_wait_ok2'] for r in rs)
    tong_wait = sum(r['sum_wait'] for r in rs)
    q8a = p(sum(1 for r in chua if r['cham_lai'] >= 1), len(chua))
    q8b = p(sum(1 for r in chua if r['n_xin'] >= 2), len(chua))
    q8c = p(sum(1 for r in rs if not r['treo']), len(rs))
    pr = [x for x in (q8a, q8b, q8c) if x is not None]
    tc = [r for r in rs if r['tu_choi']]
    return {
      'n': len(rs), 'tong_ht': len(allrs), 'khach_cu': len(allrs) - len(rs),
      'sdt': sum(1 for r in rs if r['co_sdt']),
      'q1': p(sum(1 for r in rs if r['co_sdt']), len(rs)),
      'q2': p(sum(1 for r in d6 if r['gio_sdt'] is not None and r['gio_sdt'] <= 6), len(d6)),
      'q2n': len(d6),
      'q3': p(sum(1 for r in d24 if r['gio_sdt'] is not None and r['gio_sdt'] <= 24), len(d24)),
      'q3n': len(d24),
      'q4': p(sum(1 for r in d48 if r['gio_sdt'] is not None and r['gio_sdt'] <= 48), len(d48)),
      'q4n': len(d48),
      'q5': p(sum(1 for r in sla if r['worst_wait'] <= 300), len(sla)), 'q5n': len(sla),
      'q5_2p': p(sum(1 for r in sla if r['worst_wait'] <= 120), len(sla)),
      'q5_dau': p(sum(1 for r in sla1 if r['first_wait'] <= 300), len(sla1)), 'q5_daun': len(sla1),
      'luot': luot, 'luot_pc': p(luot_ok, luot), 'luot_pc2': p(luot_ok2, luot),
      'phut_tb': round(tong_wait / luot / 60, 1) if luot else None,
      'q8': round(sum(pr) / len(pr), 1) if pr else None,
      'q8a': q8a, 'q8b': q8b, 'q8c': q8c, 'q8n': len(chua),
      'mot_cham': p(sum(1 for r in rs if r['kh_mot_cham']), len(rs)),
      'mot_chamn': sum(1 for r in rs if r['kh_mot_cham']),
      'nv_mot_cham': p(sum(1 for r in rs if r['mot_cham']), len(rs)),
      'treo': sum(1 for r in rs if r['treo']),
      'tu_choi': len(tc), 'tu_choi_cuu': p(sum(1 for r in tc if r['co_sdt']), len(tc)),
      'hot_chua': sum(1 for r in rs if r['nhiet'] == 'HOT' and not r['co_sdt']),
      'warm_chua': sum(1 for r in rs if r['nhiet'] == 'WARM' and not r['co_sdt']),
    }

def sla_cell(rs):
    s = [r for r in rs if r['n_wait'] > 0]
    return {'v': p(sum(1 for r in s if r['worst_wait'] <= 300), len(s)), 'n': len(s)}

BINS = [(0, 60, '< 1 phút'), (60, 300, '1–5 phút'), (300, 900, '5–15 phút'),
        (900, 1800, '15–30 phút'), (1800, 10 ** 9, '> 30 phút')]

def build(rs, allrs, label):
    T = kpis(rs, allrs)
    nvs = []
    for nv, c in collections.Counter(r['nv'] for r in rs if r['nv']).most_common():
        if c < 20:
            continue
        sub = [r for r in rs if r['nv'] == nv]
        b = kpis(sub, sub)
        for k, nk in (('q2', 'q2n'), ('q3', 'q3n'), ('q4', 'q4n'), ('q5', 'q5n'), ('q8', 'q8n')):
            if (b.get(nk) or 0) < 20:
                b[k] = None
        b['nv'] = nv
        a = AI.get(nv)
        b['q6'], b['q7'], b['doc'] = (a[0], a[1], a[2]) if a else (None, None, 0)
        mix = collections.Counter(SHORT.get(r['dv'], r['dv']) for r in sub)
        b['mix'] = [[k, round(v / len(sub) * 100)] for k, v in mix.most_common(3)]
        mk = collections.Counter(dict(MKL)[r['tt']] for r in sub)
        b['mkt'] = [[k, round(v / len(sub) * 100)] for k, v in mk.most_common(3)]
        nvs.append(b)
    W = [('q1', .30), ('q3', .15), ('q5', .20), ('q8', .15), ('q6', .10), ('q7', .10)]
    ai6 = [x['q6'] for x in nvs if x['q6'] is not None]
    ai7 = [x['q7'] for x in nvs if x['q7'] is not None]
    avg = {'q6': sum(ai6) / len(ai6) if ai6 else None, 'q7': sum(ai7) / len(ai7) if ai7 else None}
    for b in nvs:
        tot = wsum = 0.0
        for k, w in W:
            v = b.get(k)
            tv = avg[k] if k in avg else T.get(k)
            if v is None or not tv:
                continue
            tot += w * min(v / tv * 100, 160); wsum += w
        b['diem'] = round(tot / wsum, 1) if wsum else None
        d = b['diem']
        b['hang'] = 'A' if d is not None and d >= 110 else ('B' if d is not None and d >= 92 else 'C')
    nvs.sort(key=lambda x: (-(x['diem'] or 0)))
    trend = []
    for d in DAYS:
        sub = [r for r in rs if r['ngay'] == d]
        if not sub:
            continue
        t = kpis(sub, sub); t['k'] = d
        t['cham_lai'] = t['q8a']
        trend.append(t)
    slaNv = []
    for nv, c in collections.Counter(r['nv'] for r in rs if r['nv']).most_common():
        if c < 20:
            continue
        sub = [r for r in rs if r['nv'] == nv]
        row = {'k': nv, 'all': sla_cell(sub)}
        for d in DAYS:
            row[d] = sla_cell([r for r in sub if r['ngay'] == d])
        slaNv.append(row)
    slaNv.sort(key=lambda x: -(x['all']['v'] or 0))
    slaDv = []
    for key, lab in DVL:
        sub = [r for r in rs if r['dv'] == key]
        if len(sub) < 20:
            continue
        row = {'k': lab, 'all': sla_cell(sub)}
        for d in DAYS:
            row[d] = sla_cell([r for r in sub if r['ngay'] == d])
        slaDv.append(row)
    slaDv.sort(key=lambda x: -(x['all']['v'] or 0))
    slaTeam = {'k': 'Toàn đội', 'all': sla_cell(rs)}
    for d in DAYS:
        slaTeam[d] = sla_cell([r for r in rs if r['ngay'] == d])
    eng, rsp = [], []
    for lo, hi, lab in BINS:
        sub = [r for r in rs if r['first_wait'] is not None and lo <= r['first_wait'] < hi]
        eng.append({'k': lab, 'v': p(sum(1 for r in sub if r['n_kh'] >= 2), len(sub)), 'n': len(sub)})
        s48 = [r for r in sub if r['du48']]
        rsp.append({'k': lab, 'v': p(sum(1 for r in s48
                    if r['gio_sdt'] is not None and r['gio_sdt'] <= 48), len(s48)), 'n': len(s48)})
    hand = []
    for k, lab in [(1, '1 người'), (2, '2 người'), (3, '3 người'), (4, '4 người trở lên')]:
        sub = [r for r in rs if (SONV.get(r['ma'], 0) == k if k < 4 else SONV.get(r['ma'], 0) >= 4)]
        s48 = [r for r in sub if r['du48']]
        hand.append({'k': lab, 'v': p(sum(1 for r in s48
                     if r['gio_sdt'] is not None and r['gio_sdt'] <= 48), len(s48)),
                     'n': len(s48), 'ht': len(sub)})
    slices = {}
    for dim, pairs, fn in (('dv', DVL, lambda r: r['dv']), ('mkt', MKL, lambda r: r['tt']),
                           ('kg', [(k, k.replace('-', '–') + 'h') for k in
                                   ['00-06', '06-09', '09-12', '12-14', '14-18', '18-22', '22-24']],
                            lambda r: r['kg']),
                           ('nguon', [('QC', 'Từ quảng cáo'), ('TRUC_TIEP', 'Nhắn thẳng page'),
                                      ('COMMENT', 'Từ bình luận')], lambda r: r['nguon']),
                           ('ngay', [(d, d) for d in DAYS], lambda r: r['ngay'])):
        out = []
        for key, lab in pairs:
            sub = [r for r in rs if fn(r) == key]
            if not sub:
                continue
            b = kpis(sub, sub); b['key'] = key; b['label'] = lab
            out.append(b)
        slices[dim] = out
    return {'label': label, 'team': T, 'nv': nvs, 'trend': trend, 'slaNv': slaNv,
            'slaDv': slaDv, 'slaTeam': slaTeam, 'respEng': eng, 'respRs': rsp,
            'handoff': hand, 'sl': slices}

OUT = {'all': build(ROWS, ALLROWS, 'Tất cả')}
for key, lab in DVL:
    sub = [r for r in ROWS if r['dv'] == key]
    allsub = [r for r in ALLROWS if r['dv'] == key]
    if len(sub) >= 40:
        OUT['dv:' + key] = build(sub, allsub, lab)
for key, lab in MKL:
    sub = [r for r in ROWS if r['tt'] == key]
    allsub = [r for r in ALLROWS if r['tt'] == key]
    if len(sub) >= 40:
        OUT['mkt:' + key] = build(sub, allsub, lab)

json.dump({'slices': OUT, 'days': DAYS, 'ai': AI,
           'dvOpts': [[k, l] for k, l in DVL], 'mktOpts': [[k, l] for k, l in MKL]},
          open(SP + '/v2slices.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('số lát cắt:', len(OUT))
T = OUT['all']['team']
print('toàn bộ · tổng %d · inbox mới %d · Q1 %s%% · lượt %d · phút TB %s · %% lượt ≤5p %s%%'
      % (T['tong_ht'], T['n'], T['q1'], T['luot'], T['phut_tb'], T['luot_pc']))
print('   1 chạm (khách ≤1 tin) %s%% · 1 chạm (NV ≤1 tin) %s%%' % (T['mot_cham'], T['nv_mot_cham']))
for k in list(OUT)[1:]:
    t = OUT[k]['team']
    print('  %-22s n=%4d · Q1 %s%% · %%lượt≤5p %s%% · NV đủ mẫu %d'
          % (k, t['n'], t['q1'], t['luot_pc'], len(OUT[k]['nv'])))
