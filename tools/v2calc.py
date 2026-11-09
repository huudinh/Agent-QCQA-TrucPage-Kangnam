# -*- coding: utf-8 -*-
"""Bộ chỉ số Q1-Q8 bản 2 — tính lại từ file hội thoại gốc.
SLA khung 8:15-21:30 · tách khách cũ · thị trường 6 nhóm."""
import re, json, os, csv, collections, datetime, statistics as st
import ky as _ky

BASE = _ky.BASE
KY, SP = _ky.chon_ky()
SRC = _ky.nguon_txt(KY)

txt = open(SRC, encoding='utf-8-sig').read()
parts = re.split(r'\n## \d+\. (HT-[0-9a-f]+)\n', txt)
CONV = {parts[i]: parts[i+1] for i in range(1, len(parts), 2)}

LINE = re.compile(r'^\[(\d\d)/(\d\d) (\d\d):(\d\d):(\d\d)\] \*\*'
                  r'(KH|BOT|HT|QC|NV \((NV-\d+)\)[^:]*)\:\*\* (.*)$')
SDT = re.compile(r'\[SĐT ẩn\]')
OBS = _ky.moc_quan_sat(KY)                              # mốc hết quan sát
SLA_FROM, SLA_TO = datetime.time(8, 15), datetime.time(21, 30)

def parse(t):
    out = []
    for ln in t.split('\n'):
        m = LINE.match(ln.strip())
        if not m:
            continue
        d, mo, H, M, S, role, nv, msg = m.groups()
        ts = datetime.datetime(2026, int(mo), int(d), int(H), int(M), int(S))
        r = 'NV' if role.startswith('NV') else role
        out.append({'ts': ts, 'r': r, 'nv': nv, 'm': msg})
    return out

def in_sla(ts):
    return SLA_FROM <= ts.time() <= SLA_TO

# ---------- bộ nhận diện ----------
CU = re.compile(r'(làm (dịch vụ )?(ở |tại |bên )?(em|mình|kangnam)( rồi| r\b)'
                r'|đã làm (ở |tại |bên )?(kangnam|bên em|bên mình)'
                r'|tái khám|bảo hành|làm bên em (được|hơn|cách đây)'
                r'|mổ (ở |tại |bên )?(kangnam|bên em)'
                r'|khách (hàng )?cũ|thông tin cũ của (chị|anh|mình)'
                r'|(chị|anh|em|mình) (đã )?(cắt|nâng|hút|tiêm|cấy|phẫu thuật) (ở |tại |bên )?'
                r'(em|mình|kangnam))', re.I)
HN = re.compile(r'(hà nội|hanoi|\bhn\b|trường chinh|cầu giấy|thanh xuân|hoàng mai|long biên'
                r'|đống đa|ba đình|hai bà trưng|hà đông|mỹ đình)', re.I)
HCM = re.compile(r'(hồ chí minh|\bhcm\b|tphcm|tp hcm|sài gòn|saigon|\bsg\b|gò vấp|tân bình'
                 r'|bình thạnh|thủ đức|phú nhuận|tân phú|tân sơn nhất|quận \d)', re.I)
QT = re.compile(r'(hàn quốc|\bhq\b|đài loan|nhật bản|nhật|úc|\bmỹ\b|canada|đức|pháp|anh quốc'
                r'|singapore|malaysia|thái lan|nga\b|séc|ba lan|angola|lào|campuchia'
                r'|nước ngoài|hải ngoại|việt kiều|kiều bào)', re.I)
VK = re.compile(r'(việt kiều|kiều bào|về việt nam|khi nào (mình |chị |anh )?về|đang ở nước ngoài'
                r'|số điện thoại nước ngoài)', re.I)
TINH = re.compile(r'(nghệ an|đà nẵng|hải phòng|cần thơ|huế|quảng ninh|thanh hoá|thanh hóa'
                  r'|nam định|thái bình|bắc ninh|bắc giang|hưng yên|hải dương|vĩnh phúc|phú thọ'
                  r'|quảng nam|quảng ngãi|bình định|khánh hoà|khánh hòa|nha trang|đắk lắk'
                  r'|đăk nông|đắk nông|gia lai|kon tum|lâm đồng|đà lạt|bình dương|đồng nai'
                  r'|vũng tàu|long an|tiền giang|an giang|kiên giang|cà mau|sóc trăng|trà vinh'
                  r'|bến tre|vĩnh long|đồng tháp|tây ninh|bình phước|ninh bình|hà tĩnh'
                  r'|quảng bình|quảng trị|lào cai|yên bái|tuyên quang|thái nguyên|hoà bình'
                  r'|hòa bình|sơn la|điện biên|lạng sơn|cao bằng|hà giang|bắc kạn|hậu giang'
                  r'|bạc liêu|ninh thuận|bình thuận|phú yên|gia lâm|vt\b)', re.I)
XINSO = re.compile(r'(xin|cho em|để lại|gửi em|chia sẻ)[^.?!]{0,40}'
                   r'(số điện thoại|sđt|sdt|số đt|số zalo|số của (mình|chị|anh))', re.I)
TUCHOI = re.compile(r'(không tiện|ko tiện|k tiện|chưa tiện|không muốn|ko muốn|không cho|ko cho'
                    r'|không để lại|vui lòng (không|ko) gọi|đừng gọi|để (tôi|chị|anh|a|c|e) '
                    r'(nghiên cứu|suy nghĩ|xem|tham khảo)|tham khảo (thêm|rồi)|nhắn (tin )?qua đây'
                    r'|cứ (tư vấn|nhắn) (qua )?đây|báo giá qua đây)', re.I)

def market(msgs):
    kh = ' '.join(m['m'] for m in msgs if m['r'] == 'KH')
    allt = ' '.join(m['m'] for m in msgs)
    if VK.search(kh) or (QT.search(kh) and re.search(r'về việt nam|khi nào.*về', allt, re.I)):
        return 'VIET_KIEU'
    if QT.search(kh):
        return 'QUOC_TE'
    if HN.search(kh):
        return 'HA_NOI'
    if HCM.search(kh):
        return 'HO_CHI_MINH'
    if TINH.search(kh):
        return 'TINH_KHAC'
    if VK.search(allt) and not kh.strip():
        return 'CHUA_RO'
    return 'CHUA_RO'

# ---------- gắn dịch vụ / khung giờ từ ht.csv ----------
meta = {}
for r in csv.DictReader(open(SP+'/ht.csv', encoding='utf-8-sig')):
    meta[r['ma']] = r

OUT = []
for ma, t in CONV.items():
    md = meta.get(ma)
    if not md or md['hop_le'] != '1':
        continue
    msgs = parse(t)
    kh = [m for m in msgs if m['r'] == 'KH']
    nvm = [m for m in msgs if m['r'] == 'NV']
    if not kh:
        continue
    t0 = kh[0]['ts']
    alltxt = ' '.join(m['m'] for m in msgs)
    khtxt = ' '.join(m['m'] for m in kh)

    # --- khách cũ ---
    cu = bool(CU.search(alltxt))

    # --- SĐT ---
    sdt_ts = None
    for m in kh:
        if SDT.search(m['m']):
            sdt_ts = m['ts']
            break
    gio = (sdt_ts - t0).total_seconds()/3600 if sdt_ts else None

    # --- SLA: mọi lượt khách chờ, chỉ tính lượt bắt đầu trong khung 8:15-21:30 ---
    waits = []
    pending = None
    for m in msgs:
        if m['r'] == 'KH':
            if pending is None:
                pending = m['ts']
        elif m['r'] == 'NV' and pending is not None:
            if in_sla(pending):
                waits.append((m['ts'] - pending).total_seconds())
            pending = None
    first_wait = waits[0] if waits else None
    worst = max(waits) if waits else None
    n_ok5 = sum(1 for w in waits if w <= 300)
    n_ok2 = sum(1 for w in waits if w <= 120)
    sum_wait = sum(waits)

    # --- bám đuổi / chăm sóc ---
    n_xin = sum(1 for m in nvm if XINSO.search(m['m']))
    cham_lai = 0          # lượt NV chủ động nhắn khi tin cuối là của NV
    last_role = None
    for m in msgs:
        if m['r'] in ('KH', 'NV'):
            if m['r'] == 'NV' and last_role == 'NV':
                cham_lai += 1
            last_role = m['r']
    treo = (msgs[-1]['r'] == 'KH') if msgs else False
    tu_choi = bool(TUCHOI.search(khtxt))

    OUT.append({
        'ma': ma, 'nv': md['nv_chinh'], 'dv': md['dich_vu'], 'kg': md['khung_gio'],
        'ngay': md['ngay'], 'page': md.get('page', ''), 'nhiet': md['nhiet_loc'],
        'nguon': md['nguon'], 'so_nv': int(md['so_nv'] or 0) if (md.get('so_nv') or '').strip().isdigit() else 0,
        'cu': cu, 'tt': market(msgs),
        'co_sdt': sdt_ts is not None, 'gio_sdt': gio,
        'du6': (OBS - t0).total_seconds()/3600 >= 6,
        'du24': (OBS - t0).total_seconds()/3600 >= 24,
        'du48': (OBS - t0).total_seconds()/3600 >= 48,
        'n_wait': len(waits), 'first_wait': first_wait, 'worst_wait': worst,
        'n_wait_ok5': n_ok5, 'n_wait_ok2': n_ok2, 'sum_wait': sum_wait,
        'kh_mot_cham': len(kh) <= 1,
        'n_kh': len(kh), 'n_nv': len(nvm), 'n_xin': n_xin, 'cham_lai': cham_lai,
        'treo': treo, 'tu_choi': tu_choi,
        'mot_cham': len(nvm) <= 1,
    })

json.dump(OUT, open(SP+'/v2rows.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('hội thoại hợp lệ :', len(OUT))
print('khách cũ         :', sum(1 for r in OUT if r['cu']),
      ' → inbox mới:', sum(1 for r in OUT if not r['cu']))
print('có SĐT           :', sum(1 for r in OUT if r['co_sdt']))
print('đo được SLA      :', sum(1 for r in OUT if r['n_wait']))
print()
mk = collections.Counter(r['tt'] for r in OUT)
print('thị trường:', dict(mk))
print()
new = [r for r in OUT if not r['cu']]
def q(sel, cond):
    base = [r for r in new if sel(r)]
    hit = [r for r in base if cond(r)]
    return (len(hit), len(base), round(len(hit)/len(base)*100, 1) if base else None)
print('Q1 SĐT/inbox mới :', q(lambda r: True, lambda r: r['co_sdt']))
print('Q2 ≤6h           :', q(lambda r: r['du6'], lambda r: r['gio_sdt'] is not None and r['gio_sdt'] <= 6))
print('Q3 ≤24h          :', q(lambda r: r['du24'], lambda r: r['gio_sdt'] is not None and r['gio_sdt'] <= 24))
print('Q4 ≤48h          :', q(lambda r: r['du48'], lambda r: r['gio_sdt'] is not None and r['gio_sdt'] <= 48))
print('Q5a SLA đầu <5p  :', q(lambda r: r['first_wait'] is not None, lambda r: r['first_wait'] <= 300))
print('Q5b SLA toàn <5p :', q(lambda r: r['n_wait'] > 0, lambda r: r['worst_wait'] <= 300))
print('Q5c SLA toàn <2p :', q(lambda r: r['n_wait'] > 0, lambda r: r['worst_wait'] <= 120))
print('1 chạm           :', q(lambda r: True, lambda r: r['mot_cham']))
print('khách từ chối số :', sum(1 for r in new if r['tu_choi']))
