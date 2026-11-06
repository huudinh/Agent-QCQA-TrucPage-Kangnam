# 01 · Cài đặt

> 📘 **Trang hướng dẫn có nút Copy từng file:** https://claude.ai/artifact/GfkDRraeVwVoRtrSVcrvtj
> Người mới vào khối thì mở trang đó trước — nó có sẵn 2 thẻ bộ não, 7 sổ tri thức và 26 prompt mẫu,
> bấm Copy là dán được ngay, không cần tải repo.
> Sinh lại trang: `python tools/trang-huong-dan.py` → `tools/huong-dan.html`.

## 1 · Yêu cầu

- **Python 3.9+** — chỉ dùng thư viện chuẩn, ⛔ không cần `pip install` gì.
- Windows: chạy trong PowerShell hoặc Git Bash. Nếu màn hình hiện `?` thay cho tiếng Việt:
  ```bash
  set PYTHONIOENCODING=utf-8      # cmd
  $env:PYTHONIOENCODING="utf-8"   # PowerShell
  export PYTHONIOENCODING=utf-8   # Git Bash
  ```

## 2 · Cây thư mục

```
Agent-QCQA-TrucPage-Kangnam/
├─ SYSTEM-PROMPT.md          ← dán vào Custom instructions của Claude Project / Gem
├─ SYSTEM-PROMPT-NGAN.md     ← bản ≤ 8.000 ký tự cho ChatGPT Custom GPT
├─ knowledge/TP-01 … TP-07   ← 7 sổ tri thức, nạp hết vào Project
├─ prompts/                  ← 5 prompt mẫu: ngay · trua · nv · tuan · coach
├─ tools/
│  ├─ tp.py                  ← L0 + L1, phần đếm được
│  ├─ tu_dien.json           ← từ khóa: dịch vụ · xin số · rào cản · cảnh báo
│  ├─ muc-tieu.json          ← ⚠ mọi mục tiêu còn 'demo', chưa ai chốt
│  ├─ master-nv.mau.json     ← bản mẫu TP-04 (commit được)
│  └─ master-nv.json         ← 🔴 bản thật, CÓ TÊN NHÂN VIÊN, ⛔ không commit
├─ du-lieu/                  ← ⛔ không commit. Bỏ bản xuất Caresoft vào đây
├─ out/                      ← ⛔ không commit. Kết quả chạy
│  ├─ trang-huong-dan.py     ← sinh trang hướng dẫn + prompt mẫu (nhúng thật nội dung file)
│  └─ huong-dan.html         ← trang đã sinh; publish file này làm artifact
├─ template/MAU_hoi-thoai.md ← khuôn bản xuất, để đối chiếu khi Caresoft đổi cú pháp
└─ doc/                      ← tài liệu + hai file nguồn (phương án, note chốt mục tiêu)
```

## 3 · Dựng Project trên Claude / Gemini / ChatGPT

1. Tạo Project mới, tên **KANGNAM TPQ – Trực Page QC/QA**.
2. Dán toàn bộ `SYSTEM-PROMPT.md` vào ô **Custom instructions / Chỉ dẫn**.
   ChatGPT Custom GPT giới hạn 8.000 ký tự → dùng `SYSTEM-PROMPT-NGAN.md` (6.373 ký tự).
3. Nạp **7 file** `knowledge/TP-01 … TP-07` làm knowledge file.
4. ⛔ **Không** nạp bản xuất Caresoft gốc vào Project. Mỗi lần chạy mới đính kèm
   `out/<ky>/bao-cao.md` + `out/<ky>/mau-ai.md` + `out/<ky>/viec-<ngày>.csv`.
   Lý do: bản gốc còn tên thật lọt qua bộ che (`TP-03 §3`), và AI đọc 2.000 hội thoại
   sẽ đếm sai (`TP-01 §7` luật ②).

## 4 · Chạy lần đầu

```bash
# ① bỏ bản xuất vào du-lieu/
# ② kiểm trước — 3 ngưỡng dừng
python tools/tp.py kiem "du-lieu/Bệnh viện thẩm mỹ Kangnam_20261103-20261105.txt"

# ③ tính
python tools/tp.py tinh "du-lieu/Bệnh viện thẩm mỹ Kangnam_20261103-20261105.txt"

# ④ ba file để đưa cho agent
python tools/tp.py bao-cao --ky 03-11_05-11-2026
python tools/tp.py viec    "du-lieu/...txt" --ngay 05/11
python tools/tp.py mau     "du-lieu/...txt" --n 120

# ⑤ mở Project, gõ: NGÀY 05/11   (kèm 3 file ở out/03-11_05-11-2026/)
```

## 5 · Việc phải làm trước khi dùng thật

- [ ] Điền `tools/master-nv.json` — 40 mã NV → tên · nhóm · hạng (`TP-04 §2`)
- [ ] Chốt **giờ trực** ở `tools/muc-tieu.json › dinh_nghia.gio_truc`
- [ ] Đổi `trang_thai` từ `"demo"` sang `"chot"` cho các mục tiêu đã duyệt
- [ ] Dựng Google Sheet cho bảng *Việc hôm nay* với cột **Kết quả** (`Đã có số` / `Không phản hồi` / `Từ chối`)

⛔ Chưa làm 3 việc đầu thì agent vẫn chạy được, nhưng ⛔ không xếp hạng A/B/C và mọi cờ RAG chỉ để tham khảo.

## 6 · Lịch tự động (PA2)

Hai Scheduled Task, 8:45 và 13:15:

```bash
cd /d E:\Dinh_code\Project\Agent\Agent-QCQA-TrucPage-Kangnam
for %%f in (du-lieu\*.txt) do (
  python tools\tp.py kiem    "%%f" > out\phieu-du-lieu.md
  python tools\tp.py tinh    "%%f"
  python tools\tp.py mau     "%%f" --n 120
)
```

Phần gọi agent (L2–L5) vẫn làm tay cho tới khi `TP-04` xong — ⛔ không nên tự động hoá một bảng điểm mà chưa biết mã nào là ai.
