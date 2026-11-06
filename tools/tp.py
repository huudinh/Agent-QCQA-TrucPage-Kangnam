#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tp.py · Agent-QCQA-TrucPage-Kangnam

LỚP L0 + L1 của hệ: phần ĐẾM ĐƯỢC. ⛔ Script KHÔNG đọc hiểu.

    kiem     L0 · nạp & kiểm dữ liệu  → phiếu chất lượng dữ liệu
    tinh     L1 · máy tính chỉ số     → out/<ky>/ht.csv · so.json · lich-su.csv
    viec     L4 · hàng chờ ưu tiên    → out/<ky>/viec.csv  (P0–P6)
    mau      L2 · lấy mẫu phân tầng   → out/<ky>/mau-ai.md (cho AI đọc)
    bao-cao  gộp số đã tính thành báo cáo markdown có đủ 4 cột so kỳ

Luật của script:
  ① Một hội thoại tính đúng MỘT lần. Mọi bảng sau đọc lại từ out/<ky>/ht.csv.
  ② Mẫu số CR24/CR48 chỉ gồm inbox ĐÃ ĐỦ 24h/48h tính từ tin đầu của khách
     (so công bằng — note §0). Inbox chưa đủ giờ hiện riêng ở dòng "đang chạy".
  ③ Chưa đo được thì ghi "—", ⛔ không ghi 0. Chưa có mốc thì ghi
     "⚠ chưa có mốc so sánh", ⛔ không tự đặt mốc.
  ④ Ô < 30 hội thoại → gắn nhãn MẪU NHỎ, ⛔ không xếp hạng.
  ⑤ Mọi ngưỡng đọc từ tools/muc-tieu.json. Ngưỡng còn trang_thai="demo"
     in kèm ⚠ — ⛔ script không tự coi số demo là số chốt.

Cách dùng:
    python tools/tp.py kiem    "du-lieu/Kangnam_20261103-20261105.txt"
    python tools/tp.py tinh    "du-lieu/Kangnam_20261103-20261105.txt"
    python tools/tp.py viec    "du-lieu/Kangnam_20261103-20261105.txt" --ngay 05/11
    python tools/tp.py mau     "du-lieu/Kangnam_20261103-20261105.txt" --ngay 05/11 --n 120
    python tools/tp.py bao-cao --ky 03-05-11-2026 --ngay 05/11
"""

import argparse
import csv
import json
import os
import re
import statistics
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timedelta

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(GOC, "tools")
RA = os.path.join(GOC, "out")
F_TU_DIEN = os.path.join(TOOLS, "tu_dien.json")
F_MUC_TIEU = os.path.join(TOOLS, "muc-tieu.json")
F_MASTER = os.path.join(TOOLS, "master-nv.json")
F_LICH_SU = os.path.join(RA, "lich-su.csv")

KHONG_DO_DUOC = "—"

KHUNG = {
    "note": [(0, 6), (6, 9), (9, 12), (12, 14), (14, 18), (18, 22), (22, 24)],
    "pa":   [(0, 7), (7, 9), (9, 11), (11, 13), (13, 15), (15, 17), (17, 19), (19, 21), (21, 24)],
}


# ═══════════════════════════ tiện ích ═══════════════════════════

def kd(s):
    """Bỏ dấu, chữ thường — để khớp từ khóa."""
    s = unicodedata.normalize("NFD", s or "")
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower()


_RE_TU = {}


def _re_tu(tu):
    """Khớp theo RANH GIỚI TỪ. Không có nó thì 'mi' khớp nhầm trong 'minh'."""
    k = kd(tu)
    if k not in _RE_TU:
        _RE_TU[k] = re.compile(r'(?<![0-9a-zđ])' + re.escape(k).replace(r'\ ', r'\s+') + r'(?![0-9a-zđ])')
    return _RE_TU[k]


def co_tu(text_kd, ds):
    return any(_re_tu(t).search(text_kd) for t in ds)


def tu_trung(text_kd, ds):
    return [t for t in ds if _re_tu(t).search(text_kd)]


def nap_json(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def pct(n, d):
    return None if not d else n / d


def f_pct(x, so_le=1):
    return KHONG_DO_DUOC if x is None else f"{x * 100:.{so_le}f}%".replace(".", ",")


def f_so(x, so_le=1):
    if x is None:
        return KHONG_DO_DUOC
    return f"{x:.{so_le}f}".replace(".", ",") if so_le else f"{x:,.0f}".replace(",", ".")


def trung_vi(xs):
    xs = [x for x in xs if x is not None]
    return statistics.median(xs) if xs else None


def p75(xs):
    xs = sorted(x for x in xs if x is not None)
    if not xs:
        return None
    if len(xs) == 1:
        return xs[0]
    return statistics.quantiles(xs, n=4)[2]


def f_phut(giay):
    if giay is None:
        return KHONG_DO_DUOC
    if giay < 60:
        return f"{giay:.0f} giây"
    if giay < 3600:
        return f"{giay / 60:.1f} phút".replace(".", ",")
    return f"{giay / 3600:.1f} giờ".replace(".", ",")


# ═══════════════════════════ L0 · ĐỌC FILE ═══════════════════════════

RE_PAGE = re.compile(r'^#\s+Page:\s*(.+?)\s*$')
RE_HT = re.compile(r'^##\s+(\d+)\.\s+(HT-[0-9a-fA-F]+)\s*$')
RE_MSG = re.compile(r'^\[(\d{2})/(\d{2})\s+(\d{2}):(\d{2}):(\d{2})\]\s+\*\*(HT|QC|KH|BOT|NV)(.*?):\*\*\s?(.*)$')
RE_SAU_KY = re.compile(r'^\*\(lượt cuối được\s+(NV-\d+)\s+trả lời lúc\s+(\d{2})/(\d{2})\s+(\d{2}):(\d{2}):(\d{2})(.*?)\)\*\s*$')
RE_KY = re.compile(r'^-\s*Kỳ:\s*(\d{2})/(\d{2})/(\d{4})\s*→\s*(\d{2})/(\d{2})/(\d{4})')
RE_TONG_HT = re.compile(r'^-\s*Hội thoại:\s*([\d.,]+)')
RE_NV = re.compile(r'(NV-\d+)')
RE_QC_AD = re.compile(r'^Inbox từ quảng cáo\s+(.*?)(?:\s+—\s|\s*$)', re.S)


class TinNhan:
    __slots__ = ("t", "ai", "nv", "chu", "co_sdt", "ngoai_gio_co", "sau_ky")

    def __init__(self, t, ai, nv, chu, sau_ky=False):
        self.t = t
        self.ai = ai            # HT | QC | KH | BOT | NV
        self.nv = nv            # mã NV-xxxxx hoặc None
        self.chu = chu
        self.co_sdt = "[SĐT ẩn]" in chu
        self.ngoai_gio_co = False
        self.sau_ky = sau_ky


class HoiThoai:
    def __init__(self, stt, ma, page):
        self.stt = stt
        self.ma = ma
        self.page = page
        self.tin = []
        self.loi = []


def _nam_cua(dd, mm, ky_dau, ky_cuoi):
    """Bản xuất không ghi năm. Suy từ kỳ ở header; xử lý cả trường hợp vắt tháng/năm."""
    for nam in (ky_dau.year, ky_dau.year + 1):
        try:
            d = datetime(nam, mm, dd)
        except ValueError:
            continue
        if ky_dau - timedelta(days=2) <= d <= ky_cuoi + timedelta(days=5):
            return nam
    return ky_dau.year


def doc_file(duong_dan):
    """Đọc bản xuất Caresoft dạng markdown → (danh sách HoiThoai, meta)."""
    with open(duong_dan, encoding="utf-8-sig") as f:
        dong = f.read().split("\n")

    meta = {"file": os.path.basename(duong_dan), "page": None, "ky_dau": None,
            "ky_cuoi": None, "tong_ht_header": None, "dong_la": 0, "dong_tong": len(dong)}

    for ln in dong[:40]:
        m = RE_KY.match(ln)
        if m:
            d1, m1, y1, d2, m2, y2 = (int(x) for x in m.groups())
            meta["ky_dau"] = datetime(y1, m1, d1)
            meta["ky_cuoi"] = datetime(y2, m2, d2)
        m = RE_TONG_HT.match(ln)
        if m:
            meta["tong_ht_header"] = int(re.sub(r'[.,]', '', m.group(1)))

    if not meta["ky_dau"]:
        raise SystemExit("⛔ Không tìm thấy dòng '- Kỳ: dd/mm/yyyy → dd/mm/yyyy' ở đầu file. Xem TP-03 §1.")

    ky_dau, ky_cuoi = meta["ky_dau"], meta["ky_cuoi"]
    ds, page, ht = [], None, None

    for i, ln in enumerate(dong, 1):
        if not ln.strip():
            continue
        m = RE_PAGE.match(ln)
        if m:
            page = m.group(1)
            if meta["page"] is None:
                meta["page"] = page
            continue
        m = RE_HT.match(ln)
        if m:
            ht = HoiThoai(int(m.group(1)), m.group(2), page)
            ds.append(ht)
            continue
        m = RE_MSG.match(ln)
        if m:
            dd, mm, hh, mi, ss, ai, hau_to, chu = m.groups()
            dd, mm, hh, mi, ss = int(dd), int(mm), int(hh), int(mi), int(ss)
            t = datetime(_nam_cua(dd, mm, ky_dau, ky_cuoi), mm, dd, hh, mi, ss)
            nv = RE_NV.search(hau_to).group(1) if ai == "NV" else None
            tn = TinNhan(t, ai, nv, chu)
            tn.ngoai_gio_co = "ngoài giờ" in hau_to
            if ht is None:
                meta["dong_la"] += 1
                continue
            ht.tin.append(tn)
            continue
        m = RE_SAU_KY.match(ln)
        if m and ht is not None:
            nv, dd, mm, hh, mi, ss, _ = m.group(1), *(int(x) for x in m.groups()[1:6]), m.group(7)
            t = datetime(_nam_cua(dd, mm, ky_dau, ky_cuoi), mm, dd, hh, mi, ss)
            ht.tin.append(TinNhan(t, "NV", nv, "", sau_ky=True))
            continue
        # dòng tiếp của tin nhiều dòng
        if ht is not None and ht.tin:
            ht.tin[-1].chu += "\n" + ln
            if "[SĐT ẩn]" in ln:
                ht.tin[-1].co_sdt = True
        elif ht is None and not ln.startswith(("#", "-", "*", "﻿")):
            meta["dong_la"] += 1

    for h in ds:
        h.tin.sort(key=lambda x: (x.t, x.sau_ky))
    return ds, meta


# ═══════════════════════════ L1 · CHẤM MỘT HỘI THOẠI ═══════════════════════════

class May:
    def __init__(self, gio_mo="08:30", gio_dong="22:00", khung="note"):
        self.td = nap_json(F_TU_DIEN)
        self.mt = nap_json(F_MUC_TIEU)
        self.master = nap_json(F_MASTER) if os.path.exists(F_MASTER) else {"nv": {}}
        h, m = gio_mo.split(":")
        self.mo = int(h) * 60 + int(m)
        h, m = gio_dong.split(":")
        self.dong = int(h) * 60 + int(m)
        self.khung = KHUNG[khung]
        self.ten_khung = khung

    # ── trong giờ trực? ──
    def trong_gio(self, t):
        p = t.hour * 60 + t.minute
        return self.mo <= p < self.dong

    def o_khung(self, t):
        for a, b in self.khung:
            if a <= t.hour < b:
                return f"{a:02d}-{b:02d}"
        return f"{self.khung[-1][0]:02d}-{self.khung[-1][1]:02d}"

    # ── dịch vụ ──
    def xep_dich_vu(self, qc_ad, bot_chu, kh_chu):
        dv = self.td["dich_vu"]
        for nguon, nhan in ((qc_ad, "qc"), (bot_chu, "bot"), (kh_chu, "kh")):
            if not nguon:
                continue
            k = kd(nguon)
            for ma in dv["_thu_tu"]:
                if co_tu(k, dv[ma]):
                    return ma, nhan
        return "KHONG_XAC_DINH", None

    def xep_thi_truong(self, kh_chu):
        k = kd(kh_chu)
        for ma, ds in self.td["thi_truong"].items():
            if ma.startswith("_"):
                continue
            if co_tu(k, ds):
                return ma
        return "KHONG_XAC_DINH"

    # ── chấm ──
    def cham(self, h, moc_quan_sat):
        r = {"ma": h.ma, "stt": h.stt, "page": h.page}

        tin_kh = [t for t in h.tin if t.ai == "KH"]
        tin_nv = [t for t in h.tin if t.ai == "NV" and not t.sau_ky]
        tin_nv_ky = [t for t in h.tin if t.ai == "NV"]           # gồm cả lượt sau kỳ
        tin_bot = [t for t in h.tin if t.ai == "BOT"]
        qc = next((t for t in h.tin if t.ai == "QC"), None)
        ht_evt = [t for t in h.tin if t.ai == "HT"]

        kh_chu = "\n".join(t.chu for t in tin_kh)
        nv_chu = "\n".join(t.chu for t in tin_nv)
        kh_chu_sach = re.sub(r'\[[^\]]*\]', ' ', kh_chu)
        kh_kd = kd(kh_chu)

        r["so_tin_kh"] = len(tin_kh)
        r["so_tin_nv"] = len(tin_nv)
        r["so_tin_bot"] = len(tin_bot)
        r["so_tin_2_chieu"] = len(tin_kh) + len(tin_nv)
        r["so_ky_tu_kh"] = len(kh_chu_sach.strip())

        # ── nguồn inbox ──
        if qc:
            r["nguon"] = "QC"
            m = RE_QC_AD.match(qc.chu.strip())
            r["qc_ad"] = (m.group(1).strip() if m else qc.chu.strip())[:120]
        elif any("phản hồi bình luận" in t.chu for t in ht_evt):
            r["nguon"], r["qc_ad"] = "COMMENT", ""
        else:
            r["nguon"], r["qc_ad"] = "TRUC_TIEP", ""

        # ── loại trừ L0 ──
        loai = None
        if not tin_kh:
            loai = "KHONG_CO_TIN_KH"
        else:
            for ma, ds in self.td["spam_loai_tru"].items():
                if ma.startswith("_"):
                    continue
                if co_tu(kh_kd, ds):
                    loai = ma
                    break
        r["loai_tru"] = loai or ""
        if not tin_kh:
            r.update({k: None for k in ("t_dau", "phut_den_sdt")})
            r["hop_le"] = 0
            return r
        r["hop_le"] = 0 if loai else 1

        # ── mốc thời gian ──
        t_dau = tin_kh[0].t
        r["t_dau"] = t_dau.strftime("%Y-%m-%d %H:%M:%S")
        r["ngay"] = t_dau.strftime("%d/%m")
        r["khung_gio"] = self.o_khung(t_dau)
        r["t_dau_trong_gio"] = int(self.trong_gio(t_dau))
        r["t_cuoi_kh"] = tin_kh[-1].t.strftime("%Y-%m-%d %H:%M:%S")

        # ── dịch vụ · thị trường ──
        dv, nguon_dv = self.xep_dich_vu(r["qc_ad"], "\n".join(t.chu for t in tin_bot), kh_chu)
        r["dich_vu"], r["dich_vu_tu"] = dv, nguon_dv or ""
        r["gia_tri_don"] = "cao" if dv in self.td["dich_vu_gia_tri_cao"] else ("thuong" if dv not in ("KHAC", "KHONG_XAC_DINH") else "")
        r["thi_truong"] = self.xep_thi_truong(kh_chu)

        # ── nhân viên ──
        dem_nv = Counter(t.nv for t in tin_nv_ky if t.nv)
        r["nv_chinh"] = dem_nv.most_common(1)[0][0] if dem_nv else ""
        r["so_nv"] = len(dem_nv)
        r["nv_tat_ca"] = "|".join(sorted(dem_nv))
        mas = self.master.get("nv", {}).get(r["nv_chinh"], {})
        r["nhom"] = mas.get("nhom", "") or ""
        r["hang"] = mas.get("hang", "") or ""

        # ── SĐT ──
        t_sdt = next((t.t for t in tin_kh if t.co_sdt), None)
        r["co_sdt"] = int(bool(t_sdt))
        r["t_sdt"] = t_sdt.strftime("%Y-%m-%d %H:%M:%S") if t_sdt else ""
        r["phut_den_sdt"] = round((t_sdt - t_dau).total_seconds() / 60, 1) if t_sdt else None
        # NV nhắc lại số mà KH chưa từng gửi trong hội thoại → nghi lấy số ngoài kênh
        r["nv_co_sdt_ma_kh_khong"] = int(bool(not t_sdt and any(t.co_sdt for t in tin_nv)))

        # mẫu số so công bằng
        r["du_24h"] = int(t_dau + timedelta(hours=24) <= moc_quan_sat)
        r["du_48h"] = int(t_dau + timedelta(hours=48) <= moc_quan_sat)
        gio = (t_sdt - t_dau).total_seconds() / 3600 if t_sdt else None
        for n in (1, 4, 24, 48):
            r[f"sdt_{n}h"] = int(gio is not None and gio <= n)

        # ── FRT: đi từng khối tin KH chưa được trả lời ──
        cho = None          # tin KH đầu của khối đang chờ
        frt_dau = frt_dau_ng = None
        frt_giua, frt_giua_ng, bo_sot_phut = [], [], []
        vat_ca = 0
        so_khoi = 0
        for t in h.tin:
            if t.ai == "KH":
                if cho is None:
                    cho = t
            elif t.ai == "NV":
                if cho is not None:
                    giay = (t.t - cho.t).total_seconds()
                    trong = self.trong_gio(cho.t)
                    so_khoi += 1
                    if so_khoi == 1:
                        if trong:
                            frt_dau = giay
                        else:
                            frt_dau_ng = giay
                    else:
                        (frt_giua if trong else frt_giua_ng).append(giay)
                    if trong and giay > 30 * 60:
                        bo_sot_phut.append(giay / 60)
                        # vắt ca = khách nhắn lúc còn trong giờ nhưng câu trả lời
                        # chỉ đến sau khi ca đã đóng → lỗi XẾP CA, ⛔ không phải lỗi người
                        if t.t.date() != cho.t.date() or not self.trong_gio(t.t):
                            vat_ca += 1
                    cho = None
        r["frt_dau_giay"] = round(frt_dau) if frt_dau is not None else None
        r["frt_dau_ngoai_gio_giay"] = round(frt_dau_ng) if frt_dau_ng is not None else None
        r["frt_giua_tv_giay"] = round(trung_vi(frt_giua)) if frt_giua else None
        r["frt_giua_ngoai_gio_tv_giay"] = round(trung_vi(frt_giua_ng)) if frt_giua_ng else None
        r["so_luot_cho"] = so_khoi
        # còn treo đến hết kỳ = chưa ai trả lời
        r["treo_chua_tra_loi"] = int(cho is not None)
        r["treo_tu_phut"] = round((moc_quan_sat - cho.t).total_seconds() / 60) if cho is not None else None
        r["bo_sot"] = int(bool(bo_sot_phut) or (cho is not None and self.trong_gio(cho.t)))
        r["bo_sot_vat_ca"] = int(vat_ca > 0)
        r["bo_sot_trong_ca"] = int(bool(bo_sot_phut) and vat_ca == 0)
        r["tra_loi_sau_ky"] = int(any(t.sau_ky for t in h.tin))

        # ── xin số ──
        xs = self.td["xin_so"]
        xin = []
        for i, t in enumerate(tin_nv, 1):
            k = kd(t.chu)
            if co_tu(k, xs["co"]) and not co_tu(k, xs["loai_tru"]):
                xin.append((i, t.t))
        r["da_xin_so"] = int(bool(xin))
        r["so_lan_xin"] = len(xin)
        r["luot_nv_xin_dau"] = xin[0][0] if xin else None
        r["phut_den_xin_dau"] = round((xin[0][1] - t_dau).total_seconds() / 60, 1) if xin else None
        r["xin_truoc_luot_5"] = int(bool(xin) and xin[0][0] <= 4)
        # BOT cũng xin số — tách riêng, note §6 còn để ngỏ ☐ tính ☐ không tính
        r["bot_xin_so"] = int(any(co_tu(kd(t.chu), xs["co"]) for t in tin_bot))
        if xin and t_sdt:
            r["so_lan_xin_den_khi_cho"] = sum(1 for _, tx in xin if tx <= t_sdt)
        else:
            r["so_lan_xin_den_khi_cho"] = None
        if t_sdt:
            r["so_tin_nv_den_sdt"] = sum(1 for t in tin_nv if t.t <= t_sdt)
            r["so_tin_2_chieu_den_sdt"] = sum(1 for t in h.tin if t.ai in ("KH", "NV") and t.t <= t_sdt)
        else:
            r["so_tin_nv_den_sdt"] = None
            r["so_tin_2_chieu_den_sdt"] = None

        # ── phiên chat ── phiên đóng khi cả hai phía im > 30 phút (note §0)
        hai_chieu = [t for t in h.tin if t.ai in ("KH", "NV") and not t.sau_ky]
        im_lang = self.mt["dinh_nghia"]["phien_chat_ket_thuc_sau_phut"]["gia_tri"] * 60
        phien = []
        for t in hai_chieu:
            if phien and (t.t - phien[-1][-1].t).total_seconds() <= im_lang:
                phien[-1].append(t)
            else:
                phien.append([t])
        def dai(p):
            return (p[-1].t - p[0].t).total_seconds() / 60
        r["so_phien"] = len(phien)
        # phiên đầu = phiên đi xin số; đây là phiên mà mốc "≤ 20 phút" của note §5b nói tới
        r["phien_phut"] = round(dai(phien[0]), 1) if phien else 0.0
        r["phien_dai_nhat_phut"] = round(max((dai(p) for p in phien), default=0.0), 1)
        r["phien_tong_phut"] = round(sum(dai(p) for p in phien), 1)
        nguong_dai = self.mt["hanh_trinh"]["phien_dai_chua_xin_so_phut"]["gia_tri"]
        r["phien_dai_chua_xin"] = int(r["phien_dai_nhat_phut"] > nguong_dai and not xin)
        r["mot_chieu"] = int(len(tin_kh) == 1 and len(tin_nv) >= 1)
        tin_nv_dau = tin_nv[0].t if tin_nv else None
        r["kh_phan_hoi_sau_tin_nv_dau"] = int(bool(tin_nv_dau and any(t.t > tin_nv_dau for t in tin_kh))) if tin_nv_dau else None

        # ── chạm lại (NV chủ động nhắn khi KH đang im) ──
        cham = []
        for i, t in enumerate(h.tin):
            if t.ai != "NV" or t.sau_ky:
                continue
            kh_truoc = [x for x in h.tin[:i] if x.ai == "KH"]
            if not kh_truoc:
                continue
            gap = (t.t - kh_truoc[-1].t).total_seconds() / 60
            truoc_do_la_nv = any(x.ai == "NV" for x in h.tin[:i] if x.t > kh_truoc[-1].t)
            if gap > 30 and truoc_do_la_nv:
                cham.append((t.t - kh_truoc[-1].t).total_seconds() / 3600)
        r["so_lan_cham_lai"] = len(cham)
        r["cham_lai_24h"] = int(any(g <= 24 for g in cham))
        r["cham_lai_lan_2_48h"] = int(len([g for g in cham if g <= 48]) >= 2)

        # ── 5 tín hiệu nóng (KF-60-lite · chỉ để LỌC, ⛔ không phải điểm KF-60) ──
        th = self.td["tin_hieu_nong"]
        dv_dict = self.td["dich_vu"]
        th1 = any(co_tu(kh_kd, dv_dict[ma]) for ma in dv_dict["_thu_tu"])
        th2 = co_tu(kh_kd, th["TH2_MOC_THOI_GIAN"])
        th3 = bool(t_sdt)
        th4 = co_tu(kh_kd, th["TH4_DIEU_KIEN_THUC_HIEN"])
        th5 = co_tu(kh_kd, th["TH5_DONG_Y_GOI"])
        n = sum((th1, th2, th3, th4, th5))
        r["tin_hieu"] = "".join("①②③④⑤"[i] for i, v in enumerate((th1, th2, th3, th4, th5)) if v)
        r["so_tin_hieu"] = n
        # bộ 5 tín hiệu — giữ đúng KF-60 để so được với agent khác
        ng = self.mt["nhiet"]
        r["nhiet_code"] = ("HOT" if n >= ng["kf60_hot_tu"]
                           else ("WARM" if n >= ng["kf60_warm_tu"] else "COLD"))
        # ★ bộ LỌC VẬN HÀNH — bỏ tín hiệu ③ "đã cho SĐT" ra khỏi phép tính.
        # ⛔ Không bỏ thì "HOT chưa số" gần như KHÔNG TỒN TẠI (vì muốn HOT phải có
        # 4/5 tín hiệu, mà thiếu ③ thì phải đủ cả 4 cái còn lại) — đúng mức ưu tiên
        # P1 của phương án §6.1 sẽ rỗng. Bộ này mới là bộ dùng để xếp P1/P3 và lấy mẫu.
        n_loc = sum((th1, th2, th4, th5))
        r["so_tin_hieu_loc"] = n_loc
        r["nhiet_loc"] = ("HOT" if n_loc >= ng["loc_hot_tu"]
                          else ("WARM" if n_loc >= ng["loc_warm_tu"] else "COLD"))

        # ── rào cản · từ chối · cảnh báo đỏ ──
        rc = [ma for ma, ds in self.td["rao_can"].items() if not ma.startswith("_") and co_tu(kh_kd, ds)]
        r["rao_can"] = "|".join(rc)
        r["tu_choi_cho_so"] = int(co_tu(kh_kd, self.td["tu_choi_cho_so"]["co"]))
        # hai tầng: `chac` → thẳng P0 · `nghi` → ⛔ KHÔNG vào P0, chỉ buộc vào mẫu AI đọc
        r["canh_bao_do"] = "|".join(tu_trung(kh_kd, self.td["canh_bao_do"]["chac"]))
        r["canh_bao_nghi"] = "|".join(tu_trung(kh_kd, self.td["canh_bao_do"]["nghi"]))
        return r


# ═══════════════════════════ GỘP SỐ ═══════════════════════════

def _cr(rows, n_gio):
    """CR so công bằng: mẫu số = inbox đã đủ n giờ."""
    du = [r for r in rows if r.get(f"du_{n_gio}h")]
    if not du:
        return None, 0, 0
    co = sum(r[f"sdt_{n_gio}h"] for r in du)
    return co / len(du), co, len(du)


def _khoi(rows):
    """Bộ chỉ số cho một ô (toàn kỳ / một ngày / một NV / một dịch vụ…)."""
    o = {}
    o["inbox"] = len(rows)
    o["sdt"] = sum(r["co_sdt"] for r in rows)
    o["ty_le_sdt_tho"] = pct(o["sdt"], o["inbox"])
    for n in (24, 48):
        cr, co, d = _cr(rows, n)
        o[f"cr{n}"] = cr
        o[f"cr{n}_sdt"] = co
        o[f"cr{n}_mau"] = d
    o["dang_chay_24h"] = sum(1 for r in rows if not r["du_24h"])
    o["dang_chay_48h"] = sum(1 for r in rows if not r["du_48h"])
    o["sdt_1h"] = sum(r["sdt_1h"] for r in rows)
    o["sdt_4h"] = sum(r["sdt_4h"] for r in rows)

    frt = [r["frt_dau_giay"] for r in rows if r["frt_dau_giay"] is not None]
    o["frt_dau_tv"] = trung_vi(frt)
    o["frt_dau_p75"] = p75(frt)
    o["frt_dau_mau"] = len(frt)
    o["frt_duoi_2p"] = pct(sum(1 for x in frt if x <= 120), len(frt))
    o["frt_duoi_5p"] = pct(sum(1 for x in frt if x <= 300), len(frt))
    o["frt_duoi_15p"] = pct(sum(1 for x in frt if x <= 900), len(frt))
    ng = [r["frt_dau_ngoai_gio_giay"] for r in rows if r["frt_dau_ngoai_gio_giay"] is not None]
    o["frt_ngoai_gio_tv"] = trung_vi(ng)
    o["frt_ngoai_gio_mau"] = len(ng)
    giua = [r["frt_giua_tv_giay"] for r in rows if r["frt_giua_tv_giay"] is not None]
    o["frt_giua_tv"] = trung_vi(giua)
    o["frt_giua_mau"] = len(giua)

    o["bo_sot"] = sum(r["bo_sot"] for r in rows)
    o["ty_le_bo_sot"] = pct(o["bo_sot"], o["inbox"])
    o["bo_sot_vat_ca"] = sum(r["bo_sot_vat_ca"] for r in rows)
    o["bo_sot_trong_ca"] = sum(r["bo_sot_trong_ca"] for r in rows)
    o["ty_le_bo_sot_trong_ca"] = pct(o["bo_sot_trong_ca"], o["inbox"])
    o["treo_chua_tra_loi"] = sum(r["treo_chua_tra_loi"] for r in rows)

    o["da_xin_so"] = sum(r["da_xin_so"] for r in rows)
    o["ty_le_da_xin_so"] = pct(o["da_xin_so"], o["inbox"])
    xin = [r for r in rows if r["da_xin_so"]]
    o["ty_le_xin_duoc"] = pct(sum(r["co_sdt"] for r in xin), len(xin))
    o["xin_truoc_luot_5"] = pct(sum(r["xin_truoc_luot_5"] for r in xin), len(xin))
    o["luot_nv_xin_dau_tv"] = trung_vi([r["luot_nv_xin_dau"] for r in rows])
    o["phut_den_xin_dau_tv"] = trung_vi([r["phut_den_xin_dau"] for r in rows])
    o["so_lan_xin_tv_ht_chua_so"] = trung_vi([r["so_lan_xin"] for r in rows if not r["co_sdt"]])
    o["phien_dai_chua_xin"] = sum(r["phien_dai_chua_xin"] for r in rows)

    ra = [r for r in rows if r["co_sdt"]]
    o["phut_den_sdt_tv"] = trung_vi([r["phut_den_sdt"] for r in ra])
    o["phut_den_sdt_p75"] = p75([r["phut_den_sdt"] for r in ra])
    o["tin_2_chieu_den_sdt_tv"] = trung_vi([r["so_tin_2_chieu_den_sdt"] for r in ra])
    o["tin_2_chieu_den_sdt_p75"] = p75([r["so_tin_2_chieu_den_sdt"] for r in ra])
    o["tin_nv_den_sdt_tv"] = trung_vi([r["so_tin_nv_den_sdt"] for r in ra])
    o["so_lan_xin_den_khi_cho_tv"] = trung_vi([r["so_lan_xin_den_khi_cho"] for r in ra])
    o["phien_phut_tv_ra_so"] = trung_vi([r["phien_phut"] for r in ra])
    o["phien_phut_tv_khong_ra_so"] = trung_vi([r["phien_phut"] for r in rows if not r["co_sdt"]])
    o["so_phien_tv"] = trung_vi([r["so_phien"] for r in rows])
    o["phien_tong_phut_tv"] = trung_vi([r["phien_tong_phut"] for r in rows])

    n24 = [r for r in rows if r["du_24h"] and r["sdt_24h"]]
    o["sdt_trong_1h_tren_24h"] = pct(sum(r["sdt_1h"] for r in n24), len(n24))
    n48 = [r for r in rows if r["du_48h"]]
    o["sdt_24_48h"] = pct(sum(1 for r in n48 if r["sdt_48h"] and not r["sdt_24h"]), len(n48))

    o["mot_chieu"] = sum(r["mot_chieu"] for r in rows)
    o["ty_le_mot_chieu"] = pct(o["mot_chieu"], o["inbox"])
    ph = [r["kh_phan_hoi_sau_tin_nv_dau"] for r in rows if r["kh_phan_hoi_sau_tin_nv_dau"] is not None]
    o["kh_phan_hoi_sau_tin_nv_dau"] = pct(sum(ph), len(ph))

    chua = [r for r in rows if not r["co_sdt"]]
    o["cham_lai_24h"] = pct(sum(r["cham_lai_24h"] for r in chua), len(chua))
    o["cham_lai_lan_2_48h"] = pct(sum(r["cham_lai_lan_2_48h"] for r in chua), len(chua))

    tc = [r for r in rows if r["tu_choi_cho_so"]]
    o["tu_choi"] = len(tc)
    o["tu_choi_van_ra_sdt"] = pct(sum(r["co_sdt"] for r in tc), len(tc))

    for nh in ("HOT", "WARM", "COLD"):
        s = [r for r in rows if r["nhiet_code"] == nh]
        o[f"n_{nh.lower()}"] = len(s)
        o[f"cr_{nh.lower()}"] = pct(sum(r["co_sdt"] for r in s), len(s))
        sl = [r for r in rows if r["nhiet_loc"] == nh]
        o[f"loc_n_{nh.lower()}"] = len(sl)
        o[f"loc_cr_{nh.lower()}"] = pct(sum(r["co_sdt"] for r in sl), len(sl))
        o[f"loc_chua_so_{nh.lower()}"] = sum(1 for r in sl if not r["co_sdt"])
    # ★ ô nguy hiểm nhất — tính trên bộ LỌC (đã bỏ tín hiệu "đã cho SĐT")
    o["hot_chua_so"] = o["loc_chua_so_hot"]
    o["warm_chua_so"] = o["loc_chua_so_warm"]
    o["canh_bao_do"] = sum(1 for r in rows if r["canh_bao_do"])
    o["canh_bao_nghi"] = sum(1 for r in rows if r["canh_bao_nghi"])
    return o


def cei(rows, n_gio=48, khoa_o=("dich_vu", "nhiet_loc", "khung_gio")):
    """CEI = CR thực tế ÷ CR kỳ vọng. Kỳ vọng = CR team của từng ô,
    cộng theo số inbox NV nhận ở mỗi ô (phương án §4.1).

    ⚠ Ô được định nghĩa bằng `nhiet_loc`, ⛔ KHÔNG bằng `nhiet_code`: `nhiet_code`
    có tín hiệu ③ "đã cho SĐT" nên lấy nó làm ô là **đưa kết quả vào mẫu số kỳ vọng**
    — CEI sẽ luôn xấp xỉ 1 và mất hết ý nghĩa.
    """
    cot_du, cot_sdt = f"du_{n_gio}h", f"sdt_{n_gio}h"
    du = [r for r in rows if r[cot_du]]
    team = defaultdict(lambda: [0, 0])
    for r in du:
        k = tuple(r[c] for c in khoa_o)
        team[k][0] += r[cot_sdt]
        team[k][1] += 1
    cr_team = pct(sum(r[cot_sdt] for r in du), len(du))
    ra = {}
    for nv, g in _nhom(du, "nv_chinh").items():
        if not nv:
            continue
        thuc = sum(r[cot_sdt] for r in g)
        ky_vong = 0.0
        for r in g:
            k = tuple(r[c] for c in khoa_o)
            co, d = team[k]
            # ô chỉ có đúng NV này thì không có mốc để so → rơi về CR team chung
            ky_vong += (co / d) if d >= 3 else (cr_team or 0)
        ra[nv] = {
            "mau": len(g),
            "sdt_thuc": thuc,
            "cr_thuc": pct(thuc, len(g)),
            "cr_ky_vong": pct(ky_vong, len(g)),
            "cei": (thuc / ky_vong) if ky_vong > 0 else None,
            "mau_nho": len(g) < 30,
        }
    return ra, cr_team


def _nhom(rows, cot):
    g = defaultdict(list)
    for r in rows:
        g[r.get(cot) or ""].append(r)
    return g


# ═══════════════════════════ LỆNH ═══════════════════════════

def _moc_quan_sat(meta):
    """Thời điểm hết quan sát = 00:00 ngày sau ngày cuối kỳ. Sau mốc này
    không còn tin của khách trong file, nên ⛔ không được tính vào mẫu số."""
    return meta["ky_cuoi"] + timedelta(days=1)


def _ten_ky(meta):
    return f"{meta['ky_dau']:%d-%m}_{meta['ky_cuoi']:%d-%m-%Y}"


def _chay(duong_dan, args):
    ds, meta = doc_file(duong_dan)
    may = May(args.gio_mo, args.gio_dong, args.khung)
    moc = _moc_quan_sat(meta)
    rows = [may.cham(h, moc) for h in ds]
    return ds, meta, may, rows, moc


def lenh_kiem(args):
    ds, meta, may, rows, moc = _chay(args.file, args)
    hl = [r for r in rows if r["hop_le"]]
    print(f"\n# PHIẾU CHẤT LƯỢNG DỮ LIỆU · L0\n")
    print(f"- File: `{meta['file']}`")
    print(f"- Kỳ: **{meta['ky_dau']:%d/%m/%Y} → {meta['ky_cuoi']:%d/%m/%Y}** "
          f"({(meta['ky_cuoi'] - meta['ky_dau']).days + 1} ngày)")
    print(f"- Mốc hết quan sát: **{moc:%d/%m/%Y %H:%M}** — mọi mẫu số 24h/48h chặn ở mốc này")
    print(f"- Page: **{meta['page']}** — ⚠ bản xuất chỉ có **1 page**, "
          f"⛔ không chạy được chiều cắt theo Page")
    print(f"- Giờ trực dùng để chấm SLA: **{args.gio_mo}–{args.gio_dong}** · khung giờ: `{may.ten_khung}`\n")

    print("| Kiểm | Số | Ghi chú |\n|---|---|---|")
    print(f"| Hội thoại khai báo ở header | {meta['tong_ht_header']} | |")
    print(f"| Hội thoại đọc được | {len(ds)} | "
          f"{'✅ khớp' if len(ds) == meta['tong_ht_header'] else '🔴 LỆCH — dừng, kiểm lại bản xuất'} |")
    print(f"| Dòng lạ không gắn được vào hội thoại nào | {meta['dong_la']} | "
          f"{'✅' if meta['dong_la'] == 0 else '⚠ kiểm tay'} |")
    print(f"| Hội thoại hợp lệ (vào mẫu tính) | {len(hl)} | {f_pct(pct(len(hl), len(ds)))} |")
    for ma, n in Counter(r["loai_tru"] for r in rows if r["loai_tru"]).most_common():
        print(f"| ⤷ loại: {ma} | {n} | |")
    print(f"| Có lượt trả lời **sau kỳ** (06/11…) | {sum(r['tra_loi_sau_ky'] for r in rows)} | "
          f"lượt này KHÔNG tính vào FRT của kỳ |")
    print(f"| Còn treo, chưa ai trả lời đến hết kỳ | {sum(r['treo_chua_tra_loi'] for r in rows)} | |")

    print(f"\n## Độ phủ từng trường\n")
    print("| Trường | Phủ | Trạng thái |\n|---|---|---|")
    def phu(ten, n, note=""):
        print(f"| {ten} | {n}/{len(hl)} · {f_pct(pct(n, len(hl)))} | {note} |")
    phu("Nguồn quảng cáo (dòng `QC:`)", sum(1 for r in hl if r["nguon"] == "QC"))
    phu("Xếp được dịch vụ", sum(1 for r in hl if r["dich_vu"] != "KHONG_XAC_DINH"))
    phu("Xác định được nhân viên chính", sum(1 for r in hl if r["nv_chinh"]))
    phu("Suy ra được thị trường", sum(1 for r in hl if r["thi_truong"] != "KHONG_XAC_DINH"),
        "🔴 **bản xuất KHÔNG có trường thị trường** — suy từ chữ khách, độ phủ thấp")
    phu("Đo được FRT tin đầu (trong giờ)", sum(1 for r in hl if r["frt_dau_giay"] is not None))

    thieu = []
    if not os.path.exists(F_MASTER) or not nap_json(F_MASTER).get("nv"):
        thieu.append("`tools/master-nv.json` chưa có bản đồ **NV-code → tên · nhóm · hạng** "
                     "→ ⛔ không chạy được bảng Nhóm, không xếp hạng A/B/C (TP-04)")
    else:
        mas = nap_json(F_MASTER)["nv"]
        trong = [c for c in sorted({r["nv_chinh"] for r in hl if r["nv_chinh"]}) if not mas.get(c, {}).get("hang")]
        if trong:
            thieu.append(f"{len(trong)} mã NV chưa có hạng trong `master-nv.json`: "
                         f"{', '.join(trong[:8])}{'…' if len(trong) > 8 else ''}")
    thieu.append("Bản xuất **không có số chi quảng cáo** → ⛔ không tính được **Chi phí/SĐT** (note §1)")
    thieu.append("SĐT đã bị che thành `[SĐT ẩn]` → ⛔ không kiểm được **đầu số hợp lệ** (note §6)")
    thieu.append("Chưa có **lịch sử 30 ngày** → ⛔ không tách được *inbox mới* vs *khách cũ quay lại*, "
                 "không đo được *tái khai thác inbox cũ 3–30 ngày*")
    if (meta["ky_cuoi"] - meta["ky_dau"]).days + 1 < 14:
        thieu.append(f"Kỳ chỉ {(meta['ky_cuoi'] - meta['ky_dau']).days + 1} ngày → "
                     "⛔ không có *cùng thứ tuần trước*, không có *7 ngày vs 7 ngày trước*")
    print(f"\n## 🔴 Thiếu gì — {len(thieu)} khoản\n")
    for i, t in enumerate(thieu, 1):
        print(f"{i}. {t}")

    # đối chiếu cờ ⏱ của Caresoft với FRT do code tự tính
    tong_co, khop = 0, 0
    for h in ds:
        for t in h.tin:
            if t.ai == "NV" and t.ngoai_gio_co:
                tong_co += 1
    print(f"\n## Đối chiếu cờ `⏱ ngoài giờ` của Caresoft\n")
    print(f"- Caresoft gắn cờ *ngoài giờ* cho **{tong_co}** lượt trả lời.")
    print(f"- Code tự tính và thấy **{sum(1 for r in hl if r['frt_dau_ngoai_gio_giay'] is not None)}** "
          f"hội thoại có tin đầu của khách rơi ngoài **{args.gio_mo}–{args.gio_dong}**.")
    print(f"- ⚠ Hai số này không phải một: Caresoft đếm **lượt**, code đếm **hội thoại**. "
          f"Khớp về khung giờ là đủ.\n")


def _ghi_csv(path, rows):
    if not rows:
        return
    cot = list(rows[0].keys())
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cot, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in cot})


def lenh_tinh(args):
    ds, meta, may, rows, moc = _chay(args.file, args)
    hl = [r for r in rows if r["hop_le"]]
    ky = _ten_ky(meta)
    thu_muc = os.path.join(RA, ky)
    os.makedirs(thu_muc, exist_ok=True)

    _ghi_csv(os.path.join(thu_muc, "ht.csv"), rows)

    cei48, cr48_team = cei(hl, 48)
    cei24, cr24_team = cei(hl, 24)
    so = {
        "ky": ky,
        "file": meta["file"],
        "page": meta["page"],
        "ky_dau": meta["ky_dau"].strftime("%Y-%m-%d"),
        "ky_cuoi": meta["ky_cuoi"].strftime("%Y-%m-%d"),
        "moc_quan_sat": moc.strftime("%Y-%m-%d %H:%M:%S"),
        "gio_truc": f"{args.gio_mo}-{args.gio_dong}",
        "khung_gio": may.ten_khung,
        "tong_doc_duoc": len(ds),
        "hop_le": len(hl),
        "loai_tru": dict(Counter(r["loai_tru"] for r in rows if r["loai_tru"])),
        "toan_ky": _khoi(hl),
        "theo_ngay": {k: _khoi(v) for k, v in sorted(_nhom(hl, "ngay").items())},
        "theo_khung_gio": {k: _khoi(v) for k, v in sorted(_nhom(hl, "khung_gio").items())},
        "theo_dich_vu": {k: _khoi(v) for k, v in sorted(_nhom(hl, "dich_vu").items(),
                                                        key=lambda x: -len(x[1]))},
        "theo_nhiet": {k: _khoi(v) for k, v in _nhom(hl, "nhiet_code").items()},
        "theo_nhiet_loc": {k: _khoi(v) for k, v in _nhom(hl, "nhiet_loc").items()},
        "theo_nguon": {k: _khoi(v) for k, v in _nhom(hl, "nguon").items()},
        "theo_thi_truong": {k: _khoi(v) for k, v in sorted(_nhom(hl, "thi_truong").items(),
                                                           key=lambda x: -len(x[1]))},
        "theo_nv": {k: _khoi(v) for k, v in sorted(_nhom(hl, "nv_chinh").items(),
                                                   key=lambda x: -len(x[1])) if k},
        "theo_nhom": {k: _khoi(v) for k, v in _nhom(hl, "nhom").items() if k},
        "cei48": cei48,
        "cei24": cei24,
        "cr48_team": cr48_team,
        "cr24_team": cr24_team,
        "rao_can": dict(Counter(x for r in hl for x in r["rao_can"].split("|") if x).most_common()),
        "qc_ad_top": dict(Counter(r["qc_ad"] for r in hl if r["qc_ad"]).most_common(30)),
    }
    with open(os.path.join(thu_muc, "so.json"), "w", encoding="utf-8") as f:
        json.dump(so, f, ensure_ascii=False, indent=1, default=str)

    # lịch sử — một dòng mỗi ngày, để các kỳ sau so được
    moi = []
    for ngay, g in sorted(_nhom(hl, "ngay").items()):
        o = _khoi(g)
        moi.append({"ngay": ngay, "ky": ky, "file": meta["file"], "inbox": o["inbox"],
                    "sdt": o["sdt"], "cr24": o["cr24"], "cr24_mau": o["cr24_mau"],
                    "cr48": o["cr48"], "cr48_mau": o["cr48_mau"],
                    "frt_dau_tv_giay": o["frt_dau_tv"], "frt_duoi_5p": o["frt_duoi_5p"],
                    "ty_le_da_xin_so": o["ty_le_da_xin_so"], "ty_le_bo_sot": o["ty_le_bo_sot"],
                    "hot_chua_so": o["hot_chua_so"]})
    cu = []
    if os.path.exists(F_LICH_SU):
        with open(F_LICH_SU, encoding="utf-8-sig") as f:
            cu = [r for r in csv.DictReader(f) if (r["ngay"], r["ky"]) not in
                  {(m["ngay"], m["ky"]) for m in moi}]
    _ghi_csv(F_LICH_SU, cu + moi)

    print(f"✅ L1 xong · kỳ `{ky}` · {len(hl)}/{len(ds)} hội thoại hợp lệ")
    print(f"   {os.path.join('out', ky, 'ht.csv')}   ← bảng chấm một lần, mọi bảng sau đọc lại từ đây")
    print(f"   {os.path.join('out', ky, 'so.json')}  ← toàn bộ chỉ số đã gộp")
    print(f"   {os.path.join('out', 'lich-su.csv')}  ← {len(moi)} dòng ngày, để kỳ sau so kỳ")
    print(f"\n👉 Bước tiếp: `python tools/tp.py bao-cao --ky {ky}`")


# ─────────────────── L4 · hàng chờ ưu tiên ───────────────────

def _uu_tien(r, moc, mt):
    """P0…P6 theo phương án §6.1. Trả (mã, lý do, hạn)."""
    t_cuoi_kh = datetime.strptime(r["t_cuoi_kh"], "%Y-%m-%d %H:%M:%S") if r.get("t_cuoi_kh") else None
    con_24h = (t_cuoi_kh + timedelta(hours=24) - moc).total_seconds() / 3600 if t_cuoi_kh else None
    if r["canh_bao_do"]:
        return "P0", f"Cảnh báo đỏ: {r['canh_bao_do'].replace('|', ', ')}", "≤ 30 phút"
    if r["nhiet_loc"] == "HOT" and not r["co_sdt"] and con_24h is not None and con_24h > 0:
        return "P1", f"HOT chưa số, cửa sổ 24h còn {con_24h:.1f}h", "trước 10:00"
    if r["treo_chua_tra_loi"] and (r["treo_tu_phut"] or 0) > 15:
        return "P2", f"Khách nhắn cuối, chưa ai trả lời {r['treo_tu_phut']:.0f} phút", "ngay"
    if r["nhiet_loc"] == "WARM" and not r["co_sdt"] and con_24h is not None and 0 < con_24h < 6:
        return "P3", f"WARM chưa số, cửa sổ 24h còn {con_24h:.1f}h", "trước khi hết 24h"
    if r["tu_choi_cho_so"] and not r["co_sdt"] and r["so_lan_xin"] <= 1:
        return "P4", "Khách từ chối, NV chưa thử cách xin thứ 2", "trong ca"
    if r["co_sdt"]:
        return "P5", "Có SĐT — ⚠ không kiểm được đã bàn giao Sale chưa (bản xuất thiếu tag lead)", "trong ca"
    if r["nhiet_loc"] == "COLD" and con_24h is not None and con_24h <= 0:
        return "P6", "Inbox lạnh quá 24h", "tự động → remarketing"
    return "", "", ""


def lenh_viec(args):
    ds, meta, may, rows, moc = _chay(args.file, args)
    hl = [r for r in rows if r["hop_le"]]
    if args.ngay:
        hl = [r for r in hl if r["ngay"] == args.ngay]
    mt = may.mt
    ra = []
    for r in hl:
        p, ly_do, han = _uu_tien(r, moc, mt)
        if not p or p == "P5":
            continue
        ra.append({**r, "P": p, "ly_do": ly_do, "han": han})
    thu_tu = {f"P{i}": i for i in range(7)}
    gtri = {"cao": 0, "thuong": 1, "": 2}
    ra.sort(key=lambda r: (thu_tu[r["P"]], -r["so_tin_hieu_loc"], gtri.get(r["gia_tri_don"], 2),
                           r["phut_den_xin_dau"] if r["phut_den_xin_dau"] is not None else 9e9))
    ky = _ten_ky(meta)
    thu_muc = os.path.join(RA, ky)
    os.makedirs(thu_muc, exist_ok=True)
    cot = ["P", "ma", "ngay", "khung_gio", "dich_vu", "gia_tri_don", "nv_chinh", "nhom", "hang",
           "nhiet_loc", "nhiet_code", "tin_hieu", "rao_can", "so_tin_nv", "so_lan_xin", "phut_den_xin_dau",
           "treo_tu_phut", "ly_do", "han"]
    ten = f"viec{('-' + args.ngay.replace('/', '')) if args.ngay else ''}.csv"
    _ghi_csv(os.path.join(thu_muc, ten), [{k: r.get(k) for k in cot} for r in ra])

    print(f"\n# HÀNG CHỜ ƯU TIÊN · L4{(' · ngày ' + args.ngay) if args.ngay else ''}\n")
    print("| Mức | Số hội thoại | Nghĩa |\n|---|---|---|")
    ngh = {"P0": "Cảnh báo đỏ — QL chi nhánh + CSKH", "P1": "HOT chưa số, còn cửa sổ 24h",
           "P2": "Khách nhắn cuối, chưa ai trả lời", "P3": "WARM chưa số, cửa sổ sắp đóng",
           "P4": "Đã từ chối, chưa thử cách xin thứ 2", "P6": "Inbox lạnh quá 24h → remarketing"}
    d = Counter(r["P"] for r in ra)
    for p in ("P0", "P1", "P2", "P3", "P4", "P6"):
        if d[p]:
            print(f"| **{p}** | {d[p]} | {ngh[p]} |")
    print(f"\n⚠ **P5 (có SĐT, chưa rõ đã bàn giao Sale)** không xuất được: bản xuất Caresoft "
          f"không có tag bàn giao / lead. Xem TP-03 §4.\n")
    gioi_han = args.n or 30
    print(f"## Bảng \"Việc hôm nay\" — {min(gioi_han, len(ra))} dòng đầu "
          f"(tổng {len(ra)}; phương án §6 chốt trần 30 dòng)\n")
    print("| P | Mã hội thoại | Dịch vụ | NV | Nhiệt lọc / KF-60-lite | Tình trạng | Hạn |")
    print("|---|---|---|---|---|---|---|")
    for r in ra[:gioi_han]:
        dv = may.mt["dich_vu"].get(r["dich_vu"], {}).get("ten", r["dich_vu"])
        nv = r["nv_chinh"] or "⚠ chưa có NV"
        print(f"| {r['P']} | `{r['ma']}` | {dv} | {nv} "
              f"| **{r['nhiet_loc']}** / {r['nhiet_code']} {r['tin_hieu']} "
              f"| {r['ly_do']} | {r['han']} |")
    print(f"\n⛔ Cột **Câu gợi ý nhắn tiếp** để trống — đó là việc của AI (L4), "
          f"⛔ script không viết câu. Xem `prompts/prompt-ngay.md`.")
    print(f"\n📄 Đầy đủ: `{os.path.join('out', ky, ten)}`\n")


# ─────────────────── L2 · lấy mẫu phân tầng ───────────────────

def lenh_mau(args):
    ds, meta, may, rows, moc = _chay(args.file, args)
    hl = [r for r in rows if r["hop_le"]]
    if args.ngay:
        hl = [r for r in hl if r["ngay"] == args.ngay]
    theo_ma = {h.ma: h for h in ds}

    # tầng: ô (nhiệt × ra số) — ô nguy hiểm nhất lấy dày nhất
    tang = {
        "HOT_CHUA_SO":   [r for r in hl if r["nhiet_loc"] == "HOT" and not r["co_sdt"]],
        "WARM_CHUA_SO":  [r for r in hl if r["nhiet_loc"] == "WARM" and not r["co_sdt"]],
        "HOT_RA_SO":     [r for r in hl if r["nhiet_loc"] == "HOT" and r["co_sdt"]],
        "WARM_RA_SO":    [r for r in hl if r["nhiet_loc"] == "WARM" and r["co_sdt"]],
        "COLD_RA_SO":    [r for r in hl if r["nhiet_loc"] == "COLD" and r["co_sdt"]],
        "COLD_CHUA_SO":  [r for r in hl if r["nhiet_loc"] == "COLD" and not r["co_sdt"]],
    }
    ty_le = {"HOT_CHUA_SO": .30, "WARM_CHUA_SO": .25, "HOT_RA_SO": .15,
             "WARM_RA_SO": .15, "COLD_RA_SO": .10, "COLD_CHUA_SO": .05}
    n = args.n or 120
    chon = []
    # hạn mức tầng nào không dùng hết thì DỒN sang tầng sau, ⛔ không bỏ phí cỡ mẫu
    du_ra = 0
    for ma, ds_t in tang.items():
        if not ds_t:
            du_ra += round(n * ty_le[ma])
            continue
        k = min(len(ds_t), max(1, round(n * ty_le[ma])) + du_ra)
        du_ra = max(0, round(n * ty_le[ma]) + du_ra - k)
        # trải đều theo dịch vụ rồi theo khung giờ, ⛔ không để AI tự chọn
        ds_t = sorted(ds_t, key=lambda r: (r["dich_vu"], r["khung_gio"], r["ma"]))
        buoc = max(1, len(ds_t) // k) if k else 1
        chon += [{**r, "tang": ma} for r in ds_t[::buoc][:k]]

    # ★ hội thoại có cờ cảnh báo — BUỘC vào mẫu, ⛔ không để phép lấy mẫu bỏ sót
    da = {r["ma"] for r in chon}
    buoc = [r for r in hl if (r["canh_bao_do"] or r["canh_bao_nghi"]) and r["ma"] not in da]
    chon += [{**r, "tang": "CO_CANH_BAO"} for r in buoc]

    ky = _ten_ky(meta)
    thu_muc = os.path.join(RA, ky)
    os.makedirs(thu_muc, exist_ok=True)
    ten = f"mau-ai{('-' + args.ngay.replace('/', '')) if args.ngay else ''}.md"
    p = os.path.join(thu_muc, ten)
    with open(p, "w", encoding="utf-8") as f:
        f.write(f"# MẪU CHO AI ĐỌC · L2 · kỳ {meta['ky_dau']:%d/%m} → {meta['ky_cuoi']:%d/%m/%Y}"
                f"{(' · ngày ' + args.ngay) if args.ngay else ''}\n\n")
        f.write(f"> {len(chon)} hội thoại, chọn bằng **code** theo tầng (ô nguy hiểm lấy dày nhất), "
                f"⛔ không để AI tự chọn.\n> Trong mỗi tầng: trải đều theo dịch vụ × khung giờ.\n"
                f"> Tổng mẫu hợp lệ của kỳ: {len(hl)} hội thoại.\n\n")
        f.write("| Tầng | Có trong kỳ | Vào mẫu |\n|---|---|---|\n")
        d = Counter(r["tang"] for r in chon)
        for ma, ds_t in tang.items():
            f.write(f"| {ma} | {len(ds_t)} | {d[ma]} |\n")
        f.write(f"| ★ CO_CANH_BAO (buộc thêm vào) | "
                f"{sum(1 for r in hl if r['canh_bao_do'] or r['canh_bao_nghi'])} "
                f"| {d['CO_CANH_BAO']} |\n")
        f.write("\n---\n")
        for r in chon:
            h = theo_ma[r["ma"]]
            f.write(f"\n## {r['ma']} · {r['tang']}\n\n")
            f.write(f"- Ngày {r['ngay']} · khung {r['khung_gio']} · dịch vụ `{r['dich_vu']}` "
                    f"· NV `{r['nv_chinh'] or '—'}`\n")
            f.write(f"- Nhiệt (code, chỉ để lọc): **{r['nhiet_loc']}** (KF-60-lite 5 tín hiệu: {r['nhiet_code']}) {r['tin_hieu']} "
                    f"· rào cản: `{r['rao_can'] or '—'}`\n")
            f.write(f"- Ra số: {'**CÓ** sau ' + f_phut((r['phut_den_sdt'] or 0) * 60) if r['co_sdt'] else '**CHƯA**'}"
                    f" · NV xin số {r['so_lan_xin']} lần"
                    f"{' (lần đầu ở lượt NV thứ ' + str(r['luot_nv_xin_dau']) + ')' if r['luot_nv_xin_dau'] else ''}\n")
            f.write(f"- FRT tin đầu: {f_phut(r['frt_dau_giay']) if r['frt_dau_giay'] is not None else '— (ngoài giờ)'}"
                    f" · phiên {f_so(r['phien_phut'])} phút\n\n")
            for t in h.tin:
                if t.sau_ky:
                    f.write(f"  *(lượt cuối sau kỳ — {t.nv} lúc {t.t:%d/%m %H:%M})*\n")
                    continue
                ai = t.ai if t.ai != "NV" else f"NV {t.nv}"
                chu = t.chu.replace("\n", " ⏎ ")
                f.write(f"  [{t.t:%d/%m %H:%M:%S}] **{ai}:** {chu}\n")
    print(f"✅ L2 · {len(chon)} hội thoại vào mẫu → `{os.path.join('out', ky, ten)}`")
    print(f"   Tầng: " + " · ".join(f"{k}={Counter(r['tang'] for r in chon)[k]}" for k in tang))
    print(f"\n👉 Đưa file này cho AI kèm `prompts/prompt-ngay.md`. "
          f"⛔ Không đưa cả bản xuất gốc — AI đếm tay sẽ sai (phương án §1).")


# ─────────────────── BÁO CÁO ───────────────────

def _so_ky(cur, truoc, cung_ky, khoa):
    """4 cột so kỳ. Thiếu mốc thì ⚠, ⛔ không tự đặt mốc."""
    def d(a, b):
        if a is None or b is None:
            return "⚠ chưa có mốc"
        if isinstance(a, float) and 0 <= a <= 1 and isinstance(b, float) and 0 <= b <= 1:
            diem = (a - b) * 100
            return f"{'▲' if diem >= 0 else '▼'} {abs(diem):.1f} điểm".replace(".", ",")
        if b == 0:
            return "⚠ mốc = 0"
        return f"{'▲' if a >= b else '▼'} {abs(a - b) / abs(b) * 100:.1f}%".replace(".", ",")
    return d(cur.get(khoa), (truoc or {}).get(khoa)), d(cur.get(khoa), (cung_ky or {}).get(khoa))


def lenh_bao_cao(args):
    thu_muc = os.path.join(RA, args.ky)
    f_so_json = os.path.join(thu_muc, "so.json")
    if not os.path.exists(f_so_json):
        raise SystemExit(f"⛔ Chưa có `{f_so_json}`. Chạy `tp.py tinh <file>` trước.")
    so = nap_json(f_so_json)
    mt = nap_json(F_MUC_TIEU)
    dvt = mt["dich_vu"]
    tk = so["toan_ky"]
    ngays = sorted(so["theo_ngay"])
    out = []
    w = out.append

    w(f"# BÁO CÁO TRỰC PAGE QC/QA · kỳ {so['ky_dau']} → {so['ky_cuoi']}\n")
    w(f"> Cỡ mẫu: **{so['hop_le']}/{so['tong_doc_duoc']}** hội thoại hợp lệ · page **{so['page']}** "
      f"· giờ trực **{so['gio_truc']}** · mốc hết quan sát **{so['moc_quan_sat']}**")
    w(f"> ⚠ Mọi mục tiêu dưới đây còn ở trạng thái **demo** (`tools/muc-tieu.json`), "
      f"chưa ai chốt → cột *Đạt?* chỉ để tham khảo.\n")

    # ── 1 · chốt vs tạm ──
    w("## 1 · Chỉ số chốt & chỉ số tạm\n")
    w("Mẫu số **so công bằng**: chỉ inbox đã đủ 24h/48h tính từ tin đầu của khách.\n")
    w("| Ngày | Inbox | SĐT thô | Tỷ lệ SĐT thô | CR24 (mẫu) | CR48 (mẫu) | Chưa đủ 24h | Chưa đủ 48h |")
    w("|---|---|---|---|---|---|---|---|")
    for n in ngays:
        o = so["theo_ngay"][n]
        w(f"| {n} | {o['inbox']} | {o['sdt']} | {f_pct(o['ty_le_sdt_tho'])} "
          f"| {f_pct(o['cr24'])} ({o['cr24_mau']}) | {f_pct(o['cr48'])} ({o['cr48_mau']}) "
          f"| {o['dang_chay_24h']} | {o['dang_chay_48h']} |")
    w(f"| **Toàn kỳ** | **{tk['inbox']}** | **{tk['sdt']}** | **{f_pct(tk['ty_le_sdt_tho'])}** "
      f"| **{f_pct(tk['cr24'])}** ({tk['cr24_mau']}) | **{f_pct(tk['cr48'])}** ({tk['cr48_mau']}) "
      f"| {tk['dang_chay_24h']} | {tk['dang_chay_48h']} |")
    w(f"\n**Đọc bảng:** ngày cuối kỳ chưa có hội thoại nào đủ 24h → CR24/CR48 của ngày đó là **—**, "
      f"⛔ không phải 0 và ⛔ không dùng để đánh giá nhân viên (phương án §4.1).\n")
    w(f"| So mục tiêu | Thực tế | Mục tiêu (⚠ demo) | Đạt? |\n|---|---|---|---|")
    for ten, tt, mtg in (("CR24 toàn kỳ", tk["cr24"], mt["tong"]["cr24"]["gia_tri"]),
                         ("CR48 toàn kỳ", tk["cr48"], mt["tong"]["cr48"]["gia_tri"]),
                         ("Inbox/ngày", tk["inbox"] / max(1, len(ngays)), mt["tong"]["inbox_ngay"]["gia_tri"]),
                         ("SĐT/ngày", tk["sdt"] / max(1, len(ngays)), mt["tong"]["sdt_ngay"]["gia_tri"])):
        if tt is None:
            w(f"| {ten} | — | {mtg} | — |")
            continue
        tl = tt / mtg
        cờ = "🟢" if tl >= 1 else ("🟡" if tl >= .85 else "🔴")
        v = f_pct(tt) if tt <= 1 else f_so(tt, 0)
        m = f_pct(mtg) if mtg <= 1 else f_so(mtg, 0)
        w(f"| {ten} | {v} | {m} | {cờ} {f_pct(tl)} |")
    w(f"\n⛔ **Chi phí/SĐT**: không tính được — bản xuất hội thoại không có số chi quảng cáo.")
    w(f"⛔ **Cùng thứ tuần trước / 7 ngày vs 7 ngày trước**: ⚠ chưa có mốc so sánh "
      f"(kỳ chỉ {len(ngays)} ngày). Nạp thêm bản xuất rồi chạy lại là có.\n")

    # ── 2 · cohort khung giờ ──
    w("## 2 · Ma trận cohort khung giờ (inbox → SĐT thô)\n")
    w(f"Khung giờ theo bộ `{so['khung_gio']}` "
      f"({'7 khung của note §5' if so['khung_gio'] == 'note' else '9 khung của phương án §4.3'}). "
      f"FRT chỉ tính tin đầu **trong giờ trực** — khung nào nằm trọn ngoài giờ thì ghi `—`.\n")
    w("| Khung giờ inbox | Inbox | % inbox | FRT tin đầu (trung vị) | ≤ 2p | ≤ 5p | ≤ 1h ra số | ≤ 24h (mẫu) | ≤ 48h (mẫu) | Số NV |")
    w("|---|---|---|---|---|---|---|---|---|---|")
    for k in sorted(so["theo_khung_gio"]):
        o = so["theo_khung_gio"][k]
        nho = " ⚠MẪU NHỎ" if o["inbox"] < mt["rag"]["o_mau_nho_duoi"]["gia_tri"] else ""
        w(f"| {k}h{nho} | {o['inbox']} | {f_pct(pct(o['inbox'], tk['inbox']))} "
          f"| {f_phut(o['frt_dau_tv'])} | {f_pct(o['frt_duoi_2p'])} | {f_pct(o['frt_duoi_5p'])} "
          f"| {f_pct(pct(o['sdt_1h'], o['inbox']))} "
          f"| {f_pct(o['cr24'])} ({o['cr24_mau']}) | {f_pct(o['cr48'])} ({o['cr48_mau']}) "
          f"| — |")
    w(f"\n⚠ Cột **Số NV** để trống: bản xuất không có bảng phân ca, "
      f"code không biết ai trực khung nào. Cần TP-04.\n")
    w("**Cách đọc** (phương án §4.3): FRT cao + *≤1h ra số* thấp = **thiếu người ca đó**. "
      "FRT tốt mà *≤24h* vẫn thấp = **lỗi kịch bản/kỹ năng**. "
      "Khoảng cách *≤24h → ≤48h* lớn = **chăm sóc lại đang có tác dụng**.\n")

    # ── 3 · SLA ──
    w("## 3 · SLA & quy trình (note §6)\n")
    sla = mt["sla"]
    w("| Chỉ số | Thực tế | Mục tiêu (⚠ demo) | Cờ | Mẫu |\n|---|---|---|---|---|")
    def dong(ten, tt, mtg, nguoc=False, fmt=f_phut, mau=""):
        if tt is None:
            w(f"| {ten} | — | {mtg} | — | {mau} |")
            return
        dat = (tt <= mtg) if not nguoc else (tt >= mtg)
        w(f"| {ten} | {fmt(tt)} | {fmt(mtg) if fmt is not f_pct else f_pct(mtg)} "
          f"| {'🟢' if dat else '🔴'} | {mau} |")
    dong("Phản hồi đầu, trong giờ (trung vị)", tk["frt_dau_tv"], sla["phan_hoi_dau_trong_gio_phut"]["gia_tri"] * 60,
         mau=tk["frt_dau_mau"])
    w(f"| ⤷ P75 | {f_phut(tk['frt_dau_p75'])} | — | — | {tk['frt_dau_mau']} |")
    dong("% phản hồi đầu ≤ 5 phút", tk["frt_duoi_5p"], sla["ty_le_phan_hoi_dau_duoi_5p"]["gia_tri"],
         nguoc=True, fmt=f_pct, mau=tk["frt_dau_mau"])
    dong("Phản hồi đầu, ngoài giờ (trung vị)", tk["frt_ngoai_gio_tv"],
         sla["phan_hoi_dau_ngoai_gio_phut"]["gia_tri"] * 60, mau=tk["frt_ngoai_gio_mau"])
    dong("Phản hồi giữa hội thoại (trung vị)", tk["frt_giua_tv"],
         sla["phan_hoi_giua_hoi_thoai_phut"]["gia_tri"] * 60, mau=tk["frt_giua_mau"])
    dong("Hội thoại bị bỏ sót (> 30 phút)", tk["ty_le_bo_sot"], sla["hoi_thoai_bo_sot"]["gia_tri"],
         fmt=f_pct, mau=f"{tk['bo_sot']} HT")
    w(f"| ⤷ trong đó **vắt ca** (khách nhắn còn trong giờ, câu trả lời chỉ đến sau khi ca đóng) "
      f"| {tk['bo_sot_vat_ca']} HT | — | 🔧 lỗi **xếp ca**, ⛔ không trừ điểm người | |")
    w(f"| ⤷ trong đó **trong cùng ca** | {tk['bo_sot_trong_ca']} HT · {f_pct(tk['ty_le_bo_sot_trong_ca'])} "
      f"| {f_pct(sla['hoi_thoai_bo_sot']['gia_tri'])} "
      f"| {'🟢' if (tk['ty_le_bo_sot_trong_ca'] or 1) <= sla['hoi_thoai_bo_sot']['gia_tri'] else '🔴'} "
      f"| đây mới là phần **quy được cho người trực** |")
    w(f"| ⤷ còn treo, chưa ai trả lời đến hết kỳ | {tk['treo_chua_tra_loi']} HT | 0 "
      f"| {'🟢' if not tk['treo_chua_tra_loi'] else '🔴'} | |")
    dong("% hội thoại đã có lượt xin số", tk["ty_le_da_xin_so"], 0.70, nguoc=True, fmt=f_pct)
    dong("Xin số lần đầu trước tin NV thứ 5", tk["xin_truoc_luot_5"],
         sla["xin_so_truoc_tin_nv_thu_5"]["gia_tri"], nguoc=True, fmt=f_pct, mau=f"{tk['da_xin_so']} HT đã xin")
    dong("Số lần xin ở HT chưa ra số (trung vị)", tk["so_lan_xin_tv_ht_chua_so"],
         sla["so_lan_xin_o_ht_chua_ra_so"]["gia_tri"], nguoc=True, fmt=lambda x: f_so(x, 1) + " lần")
    dong("Chạm lại trong 24h (HT chưa ra số)", tk["cham_lai_24h"],
         sla["cham_lai_trong_24h"]["gia_tri"], nguoc=True, fmt=f_pct)
    dong("Chạm lại lần 2 trong 48h", tk["cham_lai_lan_2_48h"],
         sla["cham_lai_lan_2_trong_48h"]["gia_tri"], nguoc=True, fmt=f_pct)
    dong("Khách đã từ chối nhưng vẫn ra SĐT", tk["tu_choi_van_ra_sdt"],
         sla["tu_choi_nhung_van_ra_sdt"]["gia_tri"], nguoc=True, fmt=f_pct, mau=f"{tk['tu_choi']} HT từ chối")
    w(f"| Tỷ lệ SĐT hợp lệ | — | {f_pct(sla['ty_le_sdt_hop_le']['gia_tri'])} | — "
      f"| ⛔ số đã bị che `[SĐT ẩn]` |")
    w(f"| Tái khai thác inbox cũ 3–30 ngày | — | {f_pct(sla['inbox_cu_3_30_ngay_ra_sdt']['gia_tri'])} | — "
      f"| ⛔ chưa có lịch sử 30 ngày |\n")

    # ── 4 · hành trình đến SĐT ──
    w("## 4 · Hành trình đến SĐT (note §5b)\n")
    hj = mt["hanh_trinh"]
    w("| Chỉ số | Trung vị | P75 | Mục tiêu (⚠ demo) | Cờ |\n|---|---|---|---|---|")
    w(f"| Số tin 2 chiều đến khi KH cho số | {f_so(tk['tin_2_chieu_den_sdt_tv'],1)} "
      f"| {f_so(tk['tin_2_chieu_den_sdt_p75'],1)} | ≤ {hj['tin_2_chieu_den_sdt_trung_vi']['gia_tri']} "
      f"(P75 ≤ {hj['tin_2_chieu_den_sdt_trung_vi']['p75']}) "
      f"| {'🟢' if (tk['tin_2_chieu_den_sdt_tv'] or 99) <= hj['tin_2_chieu_den_sdt_trung_vi']['gia_tri'] else '🔴'} |")
    w(f"| Thời gian đến khi KH cho số (phút) | {f_so(tk['phut_den_sdt_tv'],1)} "
      f"| {f_so(tk['phut_den_sdt_p75'],1)} | ≤ {hj['phut_den_sdt_trung_vi']['gia_tri']} "
      f"(P75 ≤ {hj['phut_den_sdt_trung_vi']['p75']}) "
      f"| {'🟢' if (tk['phut_den_sdt_tv'] or 999) <= hj['phut_den_sdt_trung_vi']['gia_tri'] else '🔴'} |")
    w(f"| Số tin NV đến khi KH cho số | {f_so(tk['tin_nv_den_sdt_tv'],1)} | — "
      f"| ≤ {hj['tin_nv_den_sdt_trung_vi']['gia_tri']} "
      f"| {'🟢' if (tk['tin_nv_den_sdt_tv'] or 99) <= hj['tin_nv_den_sdt_trung_vi']['gia_tri'] else '🔴'} |")
    w(f"| Thời gian đến lần xin SĐT đầu (phút) | {f_so(tk['phut_den_xin_dau_tv'],1)} | — "
      f"| ≤ {hj['phut_den_xin_so_dau_trung_vi']['gia_tri']} "
      f"| {'🟢' if (tk['phut_den_xin_dau_tv'] or 999) <= hj['phut_den_xin_so_dau_trung_vi']['gia_tri'] else '🔴'} |")
    w(f"| Số lần xin đến khi KH cho số | {f_so(tk['so_lan_xin_den_khi_cho_tv'],1)} | — "
      f"| ≤ {hj['so_lan_xin_den_khi_cho_so']['gia_tri']} "
      f"| {'🟢' if (tk['so_lan_xin_den_khi_cho_tv'] or 9) <= hj['so_lan_xin_den_khi_cho_so']['gia_tri'] else '🔴'} |")
    w(f"| Độ dài **phiên đầu** — HT **ra số** (phút) | {f_so(tk['phien_phut_tv_ra_so'],1)} | — | ≤ 20 "
      f"| {'🟢' if (tk['phien_phut_tv_ra_so'] or 999) <= 20 else '🔴'} |")
    w(f"| Độ dài **phiên đầu** — HT **chưa ra số** (phút) | {f_so(tk['phien_phut_tv_khong_ra_so'],1)} | — "
      f"| chỉ theo dõi | 👁 |")
    w(f"| Số phiên / hội thoại (trung vị) | {f_so(tk['so_phien_tv'],1)} | — | — | 👁 |")
    w(f"| Tổng thời gian trao đổi, cộng mọi phiên (trung vị, phút) | {f_so(tk['phien_tong_phut_tv'],1)} "
      f"| — | — | 👁 |")
    w(f"| Phiên > {hj['phien_dai_chua_xin_so_phut']['gia_tri']} phút mà **chưa xin số** "
      f"| {tk['phien_dai_chua_xin']} HT | — | cờ đỏ | "
      f"{'🔴' if tk['phien_dai_chua_xin'] else '🟢'} |")
    w(f"| % SĐT ra ≤ 1h (trong số ra ≤ 24h) | {f_pct(tk['sdt_trong_1h_tren_24h'])} | — | 57% "
      f"| 👁 |")
    w(f"| % thêm ở cửa sổ 24–48h | {f_pct(tk['sdt_24_48h'])} | — | +5 điểm % | 👁 |")
    w(f"| KH phản hồi sau tin đầu của NV | {f_pct(tk['kh_phan_hoi_sau_tin_nv_dau'])} | — "
      f"| ≥ {f_pct(hj['kh_phan_hoi_sau_tin_nv_dau']['gia_tri'])} "
      f"| {'🟢' if (tk['kh_phan_hoi_sau_tin_nv_dau'] or 0) >= hj['kh_phan_hoi_sau_tin_nv_dau']['gia_tri'] else '🔴'} |")
    w(f"| Hội thoại 1 chiều (KH nhắn 1 tin rồi im) | {f_pct(tk['ty_le_mot_chieu'])} | — "
      f"| ≤ {f_pct(hj['hoi_thoai_mot_chieu']['gia_tri'])} "
      f"| {'🟢' if (tk['ty_le_mot_chieu'] or 1) <= hj['hoi_thoai_mot_chieu']['gia_tri'] else '🔴'} "
      f"— chỉ số của **Ads**, ⛔ không trừ điểm NV |\n")

    # ── 5 · dịch vụ ──
    w("## 5 · Theo dịch vụ\n")
    w("| Dịch vụ | Giá trị | Inbox | SĐT | Tỷ lệ SĐT | CR24 (mẫu) | CR48 (mẫu) | Mục tiêu CR48 | FRT tin đầu | % đã xin số |")
    w("|---|---|---|---|---|---|---|---|---|---|")
    for k, o in so["theo_dich_vu"].items():
        c = dvt.get(k, {})
        nho = " ⚠MẪU NHỎ" if o["inbox"] < mt["rag"]["o_mau_nho_duoi"]["gia_tri"] else ""
        mtg = c.get("cr48")
        w(f"| {c.get('ten', k)}{nho} | {c.get('gia_tri_don') or '—'} | {o['inbox']} | {o['sdt']} "
          f"| {f_pct(o['ty_le_sdt_tho'])} | {f_pct(o['cr24'])} ({o['cr24_mau']}) "
          f"| {f_pct(o['cr48'])} ({o['cr48_mau']}) | {f_pct(mtg) if mtg else '⚠ chưa có'} "
          f"| {f_phut(o['frt_dau_tv'])} | {f_pct(o['ty_le_da_xin_so'])} |")
    w("")

    # ── 6 · nhiệt & nguồn ──
    w("## 6 · Nhiệt độ (bộ lọc code, ⛔ không phải KF-60) & nguồn inbox\n")
    w("Code chạy **hai** thang nhiệt, cố ý:\n")
    w("| Thang | Tín hiệu | Dùng để |\n|---|---|---|")
    ngn = mt["nhiet"]
    w(f"| `nhiet_code` | đủ 5 tín hiệu KF-60 (có cả ③ *đã cho SĐT*) · HOT ≥ {ngn['kf60_hot_tu']} "
      f"| so với các agent khác dùng KF-60 |")
    w(f"| `nhiet_loc` ★ | 4 tín hiệu, **bỏ ③** · HOT ≥ {ngn['loc_hot_tu']} "
      f"| xếp ưu tiên P1/P3 và lấy mẫu |")
    w("\n⛔ Vì sao phải bỏ ③: giữ nó thì *“HOT chưa số”* gần như không tồn tại — muốn HOT phải "
      "có 4/5 tín hiệu, thiếu ③ là phải đủ cả 4 cái còn lại. Mức ưu tiên **P1** của phương án §6.1 "
      "sẽ rỗng, tức là hệ **mất đúng cái việc đáng làm nhất**.\n")
    w("| Nhiệt | Inbox | % | Ra số | CR | Chưa số |\n|---|---|---|---|---|---|")
    for ten, khoa in (("nhiet_code (5 tín hiệu)", "theo_nhiet"), ("★ nhiet_loc (4 tín hiệu)", "theo_nhiet_loc")):
        w(f"| **{ten}** | | | | | |")
        for k in ("HOT", "WARM", "COLD"):
            o = so.get(khoa, {}).get(k)
            if not o:
                continue
            w(f"| ⤷ {k} | {o['inbox']} | {f_pct(pct(o['inbox'], tk['inbox']))} | {o['sdt']} "
              f"| {f_pct(o['ty_le_sdt_tho'])} | {o['inbox'] - o['sdt']} |")
    w(f"\n★ **Ô nguy hiểm nhất** (theo `nhiet_loc`): HOT chưa số = **{tk['hot_chua_so']}** · "
      f"WARM chưa số = **{tk['warm_chua_so']}**\n")
    w("| Nguồn inbox | Inbox | Tỷ lệ SĐT | CR48 (mẫu) | % 1 chiều |\n|---|---|---|---|---|")
    for k, o in sorted(so["theo_nguon"].items(), key=lambda x: -x[1]["inbox"]):
        w(f"| {k} | {o['inbox']} | {f_pct(o['ty_le_sdt_tho'])} | {f_pct(o['cr48'])} ({o['cr48_mau']}) "
          f"| {f_pct(o['ty_le_mot_chieu'])} |")
    w("")

    # ── 7 · nhân viên + CEI ──
    w("## 7 · Nhân viên — CEI (so công bằng theo chất lượng inbox nhận được)\n")
    w("CEI = CR thực tế ÷ CR kỳ vọng. Kỳ vọng = CR của **team** ở từng ô "
      "`dịch vụ × nhiệt(lọc) × khung giờ`, cộng theo số inbox người đó nhận ở mỗi ô. "
      "CEI ≥ 1,1 là giỏi thật, ⛔ không phải nhờ inbox ngon.\n")
    w(f"CR team toàn kỳ: **CR24 = {f_pct(so['cr24_team'])}** (mẫu {tk['cr24_mau']}) · "
      f"**CR48 = {f_pct(so['cr48_team'])}** (mẫu {tk['cr48_mau']}).\n")
    w(f"★ **Cột để đọc trong kỳ này là CEI24**, không phải CEI48: kỳ chỉ 3 ngày nên chỉ "
      f"{tk['cr48_mau']} inbox đủ 48h, trong khi {tk['cr24_mau']} inbox đủ 24h. "
      f"Mẫu < {mt['xep_hang']['mau_toi_thieu_moi_nv']} HT → ⛔ không phân loại, ô để `—`.\n")
    tt = mt["xep_hang"]["mau_toi_thieu_moi_nv"]
    w("| NV | Nhóm | Hạng QL | Inbox | SĐT | Mẫu 24h | CR24 thực | CR24 kỳ vọng | **CEI24** | Mẫu 48h | CEI48 | FRT tin đầu | % đã xin số | Nhãn |")
    w("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for nv, o in so["theo_nv"].items():
        c24 = so["cei24"].get(nv, {})
        c48 = so["cei48"].get(nv, {})
        m24, m48 = c24.get("mau", 0), c48.get("mau", 0)
        if m24 < tt:
            nhan, hien24 = "⛔ chưa đủ mẫu", False
        elif m24 < mt["rag"]["o_mau_nho_duoi"]["gia_tri"]:
            nhan, hien24 = "⚠ MẪU NHỎ", True
        else:
            ce = c24.get("cei")
            hien24 = True
            nhan = "—" if ce is None else ("🟢 CEI ≥ 1,1" if ce >= 1.1 else
                                           ("🔴 CEI < 0,9" if ce < 0.9 else "🟡 quanh 1,0"))
        g24 = (f_pct(c24.get("cr_thuc")), f_pct(c24.get("cr_ky_vong")), f_so(c24.get("cei"), 2)) \
            if hien24 else (KHONG_DO_DUOC,) * 3
        g48 = f_so(c48.get("cei"), 2) if m48 >= tt else KHONG_DO_DUOC
        w(f"| `{nv}` | {o.get('nhom') or '⚠ thiếu TP-04'} | ⚠ thiếu TP-04 "
          f"| {o['inbox']} | {o['sdt']} | {m24} | {g24[0]} | {g24[1]} | **{g24[2]}** "
          f"| {m48} | {g48} "
          f"| {f_phut(o['frt_dau_tv'])} | {f_pct(o['ty_le_da_xin_so'])} | {nhan} |")
    w(f"\n> *Điểm dùng để phân việc kèm cặp. Không phải căn cứ kỷ luật hay xếp hạng công khai.*\n")
    w(f"⛔ **Bảng điểm tuần thang 100 và xếp hạng A/B/C chưa chạy được**: thiếu "
      f"① bản đồ `NV-code → tên · nhóm · hạng` (TP-04) ② điểm rubric TP-05 (việc của AI, lớp L2) "
      f"③ cột *Kết quả* của bảng việc hôm qua để tính *tỷ lệ cứu được*.\n")

    # ── 8 · thị trường ──
    w("## 8 · Theo thị trường — ⚠ suy luận, không phải trường dữ liệu\n")
    w("| Thị trường | Inbox | % | SĐT | Tỷ lệ SĐT | CR48 (mẫu) |\n|---|---|---|---|---|---|")
    for k, o in so["theo_thi_truong"].items():
        c = mt["thi_truong"].get(k, {})
        nho = " ⚠MẪU NHỎ" if o["inbox"] < mt["rag"]["o_mau_nho_duoi"]["gia_tri"] else ""
        w(f"| {c.get('ten', k)}{nho} | {o['inbox']} | {f_pct(pct(o['inbox'], tk['inbox']))} | {o['sdt']} "
          f"| {f_pct(o['ty_le_sdt_tho'])} | {f_pct(o['cr48'])} ({o['cr48_mau']}) |")
    w(f"\n🔴 Bản xuất Caresoft **không có trường thị trường**. Số trên suy từ chữ khách tự nói "
      f"→ độ phủ thấp, ⛔ không dùng để đánh giá. Chốt cách xác định ở note §4.\n")

    # ── 9 · rào cản ──
    w("## 9 · Rào cản khách nêu (đếm bằng từ khóa, trên chữ của khách)\n")
    w("| Rào cản | Số HT | % mẫu | CR48 trong nhóm này |\n|---|---|---|---|")
    f_ht = os.path.join(thu_muc, "ht.csv")
    with open(f_ht, encoding="utf-8-sig") as f:
        hts = [r for r in csv.DictReader(f) if r["hop_le"] == "1"]
    for rc, n in so["rao_can"].items():
        g = [r for r in hts if rc in (r["rao_can"] or "").split("|")]
        du = [r for r in g if r["du_48h"] == "1"]
        cr = pct(sum(1 for r in du if r["sdt_48h"] == "1"), len(du))
        w(f"| {rc} | {n} | {f_pct(pct(n, so['hop_le']))} | {f_pct(cr)} ({len(du)}) |")
    w(f"\n⚠ Đây là **đếm từ khóa**, ⛔ không phải chẩn đoán. Việc đọc *NV đã xử lý rào cản đúng "
      f"mẫu chưa* là của AI (rubric TP-05, lớp L2).\n")

    # ── 10 · phân rã ──
    w("## 10 · Phân rã SĐT — về nào đang rơi\n")
    w("```\nSĐT = Inbox mới × % phản hồi đúng SLA × Tỷ lệ xin số + SĐT từ chăm sóc lại\n```\n")
    w("| Mắt xích | Số kỳ này | Mục tiêu (⚠ demo) | Nhận xét của code |\n|---|---|---|---|")
    w(f"| Inbox mới | {tk['inbox']} ({f_so(tk['inbox']/max(1,len(ngays)),0)}/ngày) "
      f"| {mt['tong']['inbox_ngay']['gia_tri']}/ngày | |")
    w(f"| % phản hồi đầu ≤ 5p (trong giờ) | {f_pct(tk['frt_duoi_5p'])} "
      f"| {f_pct(mt['sla']['ty_le_phan_hoi_dau_duoi_5p']['gia_tri'])} | |")
    w(f"| % hội thoại đã có lượt xin số | {f_pct(tk['ty_le_da_xin_so'])} | ≥ 70% | |")
    w(f"| Tỷ lệ xin được (ra số ÷ đã xin) | {f_pct(tk['ty_le_xin_duoc'])} | ≥ 50% | |")
    w(f"| SĐT ra ở cửa sổ 24–48h (nhờ chăm sóc) | {f_pct(tk['sdt_24_48h'])} | +5 điểm % | |")
    w(f"\n⛔ Dòng **Nhận xét** để trống — chẩn đoán là việc của AI (L3). "
      f"Code chỉ chỉ ra *về nào rơi*, ⛔ không nói *vì sao*.\n")

    w("---\n")
    w("## ⛔ Phần script KHÔNG làm\n")
    w("| Lớp | Việc | Ai làm |\n|---|---|---|")
    w("| L2 | Chấm KF-60 chính thức, gán chân dung KF-62, chấm rubric TP-05 | AI, trên `mau-ai.md` |")
    w("| L3 | Cây nguyên nhân 6 nhóm · 3 vấn đề lớn nhất trong ngày | AI |")
    w("| L4 | Câu gợi ý nhắn tiếp cho từng hội thoại | AI, dùng TP-07 |")
    w("| L5 | Công thức WIN, bài học Fail, giáo án coaching | AI, thứ 2 hàng tuần |")
    w(f"\n*Cột `nhiet_code` trong `ht.csv` là **bộ lọc trước** bằng 5 tín hiệu từ khóa, "
      f"⛔ KHÔNG phải điểm KF-60. Nó chỉ dùng để chọn mẫu và xếp ưu tiên.*\n")

    noi_dung = "\n".join(out)
    p = os.path.join(thu_muc, "bao-cao.md")
    with open(p, "w", encoding="utf-8") as f:
        f.write(noi_dung)
    if args.in_ra:
        print(noi_dung)
    else:
        print(f"✅ Báo cáo → `{os.path.join('out', args.ky, 'bao-cao.md')}` ({len(noi_dung):,} ký tự)")


# ═══════════════════════════ CLI ═══════════════════════════

def main():
    ap = argparse.ArgumentParser(description="tp.py · L0+L1 của Agent-QCQA-TrucPage-Kangnam")
    sub = ap.add_subparsers(dest="lenh", required=True)

    def chung(p, co_file=True):
        if co_file:
            p.add_argument("file")
        p.add_argument("--gio-mo", default="08:30", dest="gio_mo")
        p.add_argument("--gio-dong", default="22:00", dest="gio_dong")
        p.add_argument("--khung", default="note", choices=list(KHUNG))

    chung(sub.add_parser("kiem", help="L0 · phiếu chất lượng dữ liệu"))
    chung(sub.add_parser("tinh", help="L1 · tính toàn bộ chỉ số"))
    p = sub.add_parser("viec", help="L4 · hàng chờ ưu tiên P0–P6")
    chung(p); p.add_argument("--ngay"); p.add_argument("--n", type=int)
    p = sub.add_parser("mau", help="L2 · lấy mẫu phân tầng cho AI đọc")
    chung(p); p.add_argument("--ngay"); p.add_argument("--n", type=int)
    p = sub.add_parser("bao-cao", help="gộp số đã tính thành báo cáo markdown")
    p.add_argument("--ky", required=True)
    p.add_argument("--in", dest="in_ra", action="store_true", help="in ra màn hình thay vì chỉ ghi file")

    a = ap.parse_args()
    {"kiem": lenh_kiem, "tinh": lenh_tinh, "viec": lenh_viec,
     "mau": lenh_mau, "bao-cao": lenh_bao_cao}[a.lenh](a)


if __name__ == "__main__":
    main()
