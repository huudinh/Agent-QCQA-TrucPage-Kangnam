# -*- coding: utf-8 -*-
"""Chọn kỳ, tìm file hội thoại gốc, liệt kê ngày trong kỳ.

Dùng chung cho v2calc · v2agg · v2extra · v2slices · v2bundle để tên kỳ chỉ nằm
ở MỘT chỗ. Trước đây mỗi script tự ghi 'out/03-11_05-11-2026' và tên file .txt,
nên đổi kỳ là phải sửa 11 dòng rải trong 4 file.

Thứ tự ưu tiên khi chọn kỳ: tham số dòng lệnh → biến môi trường TP_KY →
kỳ mới nhất trong out/.
"""
import datetime
import glob
import os
import re
import sys

# Console Windows mặc định cp1252 nên mọi dòng print tiếng Việt đều nổ
# UnicodeEncodeError — sau khi file JSON đã ghi xong, nên lỗi rất dễ hiểu sai.
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
THU = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'Chủ nhật']


def chon_ky(argv=None):
    """→ (ten_ky, duong_dan_out). Sai thì dừng kèm câu phải làm gì tiếp."""
    av = sys.argv[1:] if argv is None else list(argv)
    ky = next((a for a in av if not a.startswith('-')), None) or os.environ.get('TP_KY')
    out = BASE + 'out/'
    if not ky:
        ds = sorted(d for d in os.listdir(out) if os.path.isdir(out + d)) if os.path.isdir(out) else []
        if not ds:
            raise SystemExit('out/ chưa có kỳ nào.\n'
                             '  chạy trước: python tools/tp.py tinh "du-lieu/<file>.txt"')
        ky = ds[-1]
    sp = out + ky
    if not os.path.isdir(sp):
        co = ', '.join(sorted(d for d in os.listdir(out) if os.path.isdir(out + d)))
        raise SystemExit(f'không thấy out/{ky}/\n  kỳ đang có: {co or "(chưa có kỳ nào)"}')
    return ky, sp


def nguon_txt(ky):
    """File .txt gốc của kỳ: biến TP_TXT, hoặc dò theo khoảng ngày trong tên kỳ."""
    p = os.environ.get('TP_TXT')
    if p:
        p = p if os.path.isabs(p) else BASE + p
        if not os.path.isfile(p):
            raise SystemExit(f'TP_TXT trỏ vào file không có: {p}')
        return p
    m = re.match(r'(\d\d)-(\d\d)_(\d\d)-(\d\d)-(\d{4})$', ky)
    if m:
        d1, m1, d2, m2, y = m.groups()
        hit = glob.glob(f'{BASE}du-lieu/*{y}{m1}{d1}-{y}{m2}{d2}*.txt')
        if len(hit) == 1:
            return hit[0]
    hit = glob.glob(BASE + 'du-lieu/*.txt')
    if len(hit) == 1:
        return hit[0]
    raise SystemExit(f'không đoán được file .txt của kỳ {ky} — du-lieu/ có {len(hit)} file .txt.\n'
                     '  chỉ rõ bằng: TP_TXT="du-lieu/<file>.txt"')


def moc_quan_sat(ky):
    """00:00 ngày sau ngày cuối kỳ — mốc hết quan sát.

    Sau mốc này trong file không còn tin của khách nữa, nên inbox chưa đủ
    6h/24h/48h tính tới mốc thì ⛔ không được vào mẫu số Q2–Q4.
    """
    m = re.match(r'(\d\d)-(\d\d)_(\d\d)-(\d\d)-(\d{4})$', ky)
    if not m:
        raise SystemExit(f'không đọc được ngày cuối từ tên kỳ: {ky}')
    d2, m2, y = m.group(3), m.group(4), m.group(5)
    return datetime.datetime(int(y), int(m2), int(d2)) + datetime.timedelta(days=1)


def sap_ngay(it):
    """Các ngày dd/mm đúng thứ tự thời gian → ['03/11', '04/11', ...]."""
    ds = {str(d).strip() for d in it if str(d).strip()}
    def khoa(d):
        try:
            dd, mm = (int(x) for x in d.split('/'))
            return (mm, dd)
        except Exception:
            return (99, 99)
    return sorted(ds, key=khoa)


def nhan_ngay(ky, days):
    """[('03/11', '03/11 · Thứ 3'), ...] — năm lấy từ tên kỳ để biết thứ."""
    m = re.search(r'-(\d{4})$', ky)
    nam = int(m.group(1)) if m else datetime.date.today().year
    out = []
    for d in days:
        try:
            dd, mm = (int(x) for x in d.split('/'))
            out.append((d, f'{d} · {THU[datetime.date(nam, mm, dd).weekday()]}'))
        except Exception:
            out.append((d, d))
    return out
