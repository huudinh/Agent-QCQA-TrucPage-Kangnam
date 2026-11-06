# -*- coding: utf-8 -*-
import json, os, collections
SP = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/out/03-11_05-11-2026'
ROWS = json.load(open(SP+'/v2rows.json', encoding='utf-8'))
NEW = [r for r in ROWS if not r['cu']]

# điểm AI đã chấm khi đọc mẫu (thang 0-2) — Q6 xử lí từ chối, Q7 tuân thủ kịch bản
AI = {
 "NV-236425444": {"q6":1.9,"q7":1.7,"doc":7},  "NV-254668856": {"q6":1.0,"q7":1.5,"doc":7},
 "NV-238736928": {"q6":0.9,"q7":1.0,"doc":6},  "NV-232258930": {"q6":1.6,"q7":1.8,"doc":10},
 "NV-264113743": {"q6":1.2,"q7":1.3,"doc":6},  "NV-198843202": {"q6":1.4,"q7":1.8,"doc":8},
 "NV-205107209": {"q6":0.8,"q7":0.9,"doc":5},  "NV-258612608": {"q6":1.6,"q7":1.7,"doc":3},
 "NV-202194914": {"q6":0.7,"q7":1.0,"doc":3},  "NV-226199192": {"q6":1.3,"q7":1.4,"doc":2},
 "NV-240896987": {"q6":0.9,"q7":1.3,"doc":2},  "NV-262546406": {"q6":1.1,"q7":1.5,"doc":2},
 "NV-269001161": {"q6":1.2,"q7":1.7,"doc":3},  "NV-198842634": {"q6":0.9,"q7":1.1,"doc":2},
 "NV-198842558": {"q6":1.8,"q7":1.6,"doc":2},
 "NV-202193608": {"q6":None,"q7":None,"doc":0},"NV-262546620":{"q6":None,"q7":None,"doc":1},
}
LBL = {'MAT':'Mắt','BODY':'Béo/Hút mỡ','DA_TRE_HOA':'Da','MUI':'Mũi','NGUC':'Ngực',
       'HAM_MAT':'Hàm mặt','KHAC':'Khác','KHONG_XAC_DINH':'Chưa rõ'}
MKT = [('HA_NOI','Hà Nội'),('HO_CHI_MINH','Hồ Chí Minh'),('TINH_KHAC','Các tỉnh khác'),
       ('VIET_KIEU','Việt kiều'),('QUOC_TE','Quốc tế'),('CHUA_RO','Chưa xác định')]

def p(a, b, nd=1):
    return round(a/b*100, nd) if b else None

def block(rs):
    """bộ Q1-Q5 + Q8 cho một tập hội thoại (đã là inbox mới)"""
    d6 = [r for r in rs if r['du6']]
    d24 = [r for r in rs if r['du24']]
    d48 = [r for r in rs if r['du48']]
    sla = [r for r in rs if r['n_wait'] > 0]
    sla1 = [r for r in rs if r['first_wait'] is not None]
    chua = [r for r in rs if not r['co_sdt']]
    q8a = p(sum(1 for r in chua if r['cham_lai'] >= 1), len(chua))
    q8b = p(sum(1 for r in chua if r['n_xin'] >= 2), len(chua))
    q8c = p(sum(1 for r in rs if not r['treo']), len(rs))
    parts = [x for x in (q8a, q8b, q8c) if x is not None]
    tc = [r for r in rs if r['tu_choi']]
    return {
      'n': len(rs),
      'q1': p(sum(1 for r in rs if r['co_sdt']), len(rs)), 'q1n': len(rs),
      'q2': p(sum(1 for r in d6 if r['gio_sdt'] is not None and r['gio_sdt'] <= 6), len(d6)),
      'q2n': len(d6),
      'q3': p(sum(1 for r in d24 if r['gio_sdt'] is not None and r['gio_sdt'] <= 24), len(d24)),
      'q3n': len(d24),
      'q4': p(sum(1 for r in d48 if r['gio_sdt'] is not None and r['gio_sdt'] <= 48), len(d48)),
      'q4n': len(d48),
      'q5': p(sum(1 for r in sla if r['worst_wait'] <= 300), len(sla)), 'q5n': len(sla),
      'q5_2p': p(sum(1 for r in sla if r['worst_wait'] <= 120), len(sla)),
      'q5_dau': p(sum(1 for r in sla1 if r['first_wait'] <= 300), len(sla1)), 'q5_daun': len(sla1),
      'q8': round(sum(parts)/len(parts), 1) if parts else None,
      'q8a': q8a, 'q8b': q8b, 'q8c': q8c, 'q8n': len(chua),
      'sdt': sum(1 for r in rs if r['co_sdt']),
      'mot_cham': p(sum(1 for r in rs if r['mot_cham']), len(rs)),
      'mot_chamn': sum(1 for r in rs if r['mot_cham']),
      'treo': sum(1 for r in rs if r['treo']),
      'tu_choi': len(tc),
      'tu_choi_cuu': p(sum(1 for r in tc if r['co_sdt']), len(tc)),
      'hot_chua': sum(1 for r in rs if r['nhiet'] == 'HOT' and not r['co_sdt']),
      'warm_chua': sum(1 for r in rs if r['nhiet'] == 'WARM' and not r['co_sdt']),
    }

TEAM = block(NEW)
TEAM['tong_ht'] = len(ROWS)
TEAM['khach_cu'] = len(ROWS) - len(NEW)

# ---------- từng nhân viên ----------
by = collections.defaultdict(list)
for r in NEW:
    if r['nv']:
        by[r['nv']].append(r)
NVS = []
for nv, rs in by.items():
    if len(rs) < 30:
        continue
    b = block(rs)
    # chặn ô cỡ mẫu nhỏ: dưới 20 hội thoại thì không công bố tỷ lệ
    for k, nk in (('q2','q2n'), ('q3','q3n'), ('q4','q4n'), ('q5','q5n'), ('q8','q8n')):
        if (b.get(nk) or 0) < 20:
            b[k] = None
    b['nv'] = nv
    b['q6'] = AI.get(nv, {}).get('q6')
    b['q7'] = AI.get(nv, {}).get('q7')
    b['doc'] = AI.get(nv, {}).get('doc', 0)
    mix = collections.Counter(LBL.get(r['dv'], r['dv']) for r in rs)
    b['mix'] = [[k, round(v/len(rs)*100)] for k, v in mix.most_common(3)]
    mk = collections.Counter(r['tt'] for r in rs)
    b['mkt'] = [[dict(MKT)[k], round(v/len(rs)*100)] for k, v in mk.most_common(3)]
    NVS.append(b)

# ---------- điểm tổng & hạng: so với trung bình đội ----------
W = [('q1', .30), ('q3', .15), ('q5', .20), ('q8', .15), ('q6', .10), ('q7', .10)]
for b in NVS:
    tot, wsum = 0.0, 0.0
    for k, w in W:
        v, tv = b.get(k), (TEAM.get(k) if k not in ('q6', 'q7') else None)
        if k in ('q6', 'q7'):
            vals = [x[k] for x in NVS if x.get(k) is not None]
            tv = sum(vals)/len(vals) if vals else None
        if v is None or not tv:
            continue
        tot += w * min(v/tv*100, 160)
        wsum += w
    b['diem'] = round(tot/wsum, 1) if wsum else None
    b['phu'] = round(wsum/sum(w for _, w in W)*100)
NVS.sort(key=lambda x: -(x['diem'] or 0))
for b in NVS:
    d = b['diem']
    b['hang'] = 'A' if d is not None and d >= 110 else ('B' if d is not None and d >= 92 else 'C')

# ---------- lát cắt ----------
def slices(keyfn, labels):
    out = []
    for k, lab in labels:
        rs = [r for r in NEW if keyfn(r) == k]
        if not rs:
            continue
        b = block(rs); b['key'] = k; b['label'] = lab
        out.append(b)
    return out

DVS = slices(lambda r: r['dv'], [('MAT','Mắt'),('MUI','Mũi'),('NGUC','Ngực'),
      ('HAM_MAT','Hàm mặt'),('BODY','Body / Hút mỡ'),('DA_TRE_HOA','Da / Trẻ hoá'),
      ('KHAC','Khác'),('KHONG_XAC_DINH','Chưa xếp được')])
MKTS = slices(lambda r: r['tt'], MKT)
KGS = slices(lambda r: r['kg'], [(k, k.replace('-', '–')+'h') for k in
      ['00-06','06-09','09-12','12-14','14-18','18-22','22-24']])
NGS = slices(lambda r: r['nguon'], [('QC','Từ quảng cáo'),('TRUC_TIEP','Nhắn thẳng page'),
      ('COMMENT','Từ bình luận')])
NGAY = slices(lambda r: r['ngay'], [('03/11','03/11 · Thứ 3'),('04/11','04/11 · Thứ 4'),
      ('05/11','05/11 · Thứ 5')])

json.dump({'team': TEAM, 'nv': NVS, 'dv': DVS, 'mkt': MKTS, 'kg': KGS,
           'nguon': NGS, 'ngay': NGAY},
          open(SP+'/v2.json', 'w', encoding='utf-8'), ensure_ascii=False)

print('TEAM  tổng %d · inbox mới %d · khách cũ %d' % (TEAM['tong_ht'], TEAM['n'], TEAM['khach_cu']))
print('  Q1 %s%% · Q2 %s%% · Q3 %s%% · Q4 %s%% · Q5 %s%% (2p %s%%) · Q8 %s · 1 chạm %s%%'
      % (TEAM['q1'], TEAM['q2'], TEAM['q3'], TEAM['q4'], TEAM['q5'], TEAM['q5_2p'],
         TEAM['q8'], TEAM['mot_cham']))
print()
hdr = ('NV', 'n', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'điểm', 'hạng')
print('{:<16}{:>5}{:>7}{:>7}{:>7}{:>7}{:>7}{:>6}{:>6}{:>7}{:>7}{:>6}'.format(*hdr))
for b in NVS:
    print('{:<16}{:>5}{:>7}{:>7}{:>7}{:>7}{:>7}{:>6}{:>6}{:>7}{:>7}{:>6}'.format(
        *[('—' if v is None else v) for v in (b['nv'], b['n'], b['q1'], b['q2'], b['q3'],
          b['q4'], b['q5'], b['q6'], b['q7'], b['q8'], b['diem'], b['hang'])]))
print()
print('thị trường:')
for m in MKTS:
    print('  {:<16}{:>5} ht · Q1 {}% · Q5 {}% · HOT chưa số {}'.format(
        m['label'], m['n'], m['q1'], m['q5'], m['hot_chua']))
print('dịch vụ:')
for m in DVS:
    print('  {:<16}{:>5} ht · Q1 {}% · Q5 {}% · Q8 {}'.format(
        m['label'], m['n'], m['q1'], m['q5'], m['q8']))
