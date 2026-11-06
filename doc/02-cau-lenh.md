# 02 · Câu lệnh

## 1 · Lệnh của agent (gõ trong Project)

| Lệnh | Khi nào | Cần kèm file nào | Mẫu đầu ra |
|---|---|---|---|
| `NGÀY <dd/mm>` | 8:45 | `bao-cao.md` · `mau-ai.md` · `viec-<ngày>.csv` | `TP-06 §1` |
| `TRƯA <dd/mm>` | 13:30 | `bao-cao.md` bản trưa · `viec-<ngày>.csv` **đã có cột Kết quả** | `TP-06 §2` |
| `NV <mã>` | khi cần kèm cặp | `bao-cao.md` · `ht.csv` · phần `mau-ai.md` của người đó | `TP-06 §4` |
| `TUẦN <từ> → <đến>` | thứ 2 | `bao-cao.md` · `lich-su.csv` · kết quả chấm rubric · `viec-*.csv` | `TP-06 §3` |
| `COACH <nhóm\|mã>` | sau `TUẦN` | kết quả chấm rubric · `TP-07` | `TP-06 §5` |
| `HT <mã>` | khi cần soi 1 hội thoại | `mau-ai.md` | `TP-05 §4` |
| `KIỂM` | khi nghi dữ liệu lệch | — | phiếu chất lượng dữ liệu |

Prompt mẫu đầy đủ cho từng lệnh nằm ở `prompts/`.

## 2 · Lệnh của script

```bash
python tools/tp.py kiem    <file>                      # L0
python tools/tp.py tinh    <file>                      # L1
python tools/tp.py bao-cao --ky <ky> [--in]            # gộp số thành báo cáo
python tools/tp.py viec    <file> [--ngay dd/mm] [--n 30]
python tools/tp.py mau     <file> [--ngay dd/mm] [--n 120]
```

### Tham số dùng chung

| Tham số | Mặc định | Nghĩa |
|---|---|---|
| `--gio-mo` | `08:30` | giờ mở ca trực. Đổi là đổi mẫu số của **toàn bộ** SLA |
| `--gio-dong` | `22:00` | giờ đóng ca |
| `--khung` | `note` | bộ khung giờ. `note` = 7 khung của note §5 · `pa` = 9 khung của phương án §4.3 |

### Tham số riêng

| Lệnh | Tham số | Nghĩa |
|---|---|---|
| `bao-cao` | `--ky` | tên kỳ, chính là tên thư mục trong `out/` (ví dụ `03-11_05-11-2026`) |
| `bao-cao` | `--in` | in ra màn hình, không chỉ ghi file |
| `viec` · `mau` | `--ngay dd/mm` | chỉ lọc hội thoại có **tin đầu của khách** trong ngày đó |
| `viec` | `--n` | số dòng in ra màn hình. File CSV luôn đầy đủ |
| `mau` | `--n` | cỡ mẫu mục tiêu. Tầng nào không đủ thì hạn mức **dồn** sang tầng sau |

## 3 · File ra

| File | Nội dung | Ai đọc |
|---|---|---|
| `out/<ky>/ht.csv` | ★ **bảng chấm một lần** — 1 dòng/hội thoại × 75 cột. Mọi bảng sau đọc lại từ đây | code · người soi số |
| `out/<ky>/so.json` | toàn bộ chỉ số đã gộp theo 8 chiều cắt | code · agent |
| `out/<ky>/bao-cao.md` | 10 mục bảng số, đã so mục tiêu, có cờ RAG | **agent** |
| `out/<ky>/viec-<ngày>.csv` | hàng chờ `P0–P6`, đã xếp thứ tự | **agent** · QL |
| `out/<ky>/mau-ai.md` | mẫu phân tầng, có nguyên văn hội thoại | **agent** (L2) |
| `out/lich-su.csv` | 1 dòng/ngày, cộng dồn qua các kỳ → để so kỳ | code |

## 4 · Ba ngưỡng DỪNG của `tp.py kiem`

| Kiểm | 🔴 Dừng khi |
|---|---|
| Hội thoại đọc được vs dòng `- Hội thoại:` ở header | **lệch bất kỳ** → bản xuất bị cắt |
| Dòng lạ không gắn được vào hội thoại nào | **> 0** → cú pháp bản xuất đã đổi |
| Dòng `- Kỳ: dd/mm/yyyy → dd/mm/yyyy` | **thiếu** → không suy được năm |

Ba ngưỡng ⚠ cảnh báo (vẫn chạy): phủ dịch vụ < 85% · phủ nhân viên < 95% · hội thoại treo > 5%.

## 5 · Lỗi thường gặp

| Hiện tượng | Nguyên nhân | Cách sửa |
|---|---|---|
| `⛔ Không tìm thấy dòng '- Kỳ:'` | bản xuất thiếu phần đầu, hoặc bị copy thiếu | xuất lại từ Caresoft, giữ nguyên 6 dòng đầu |
| `🔴 LỆCH — dừng, kiểm lại bản xuất` | file bị cắt giữa | xuất lại |
| Tiếng Việt ra `?` trên màn hình | codepage Windows | `set PYTHONIOENCODING=utf-8` |
| `⛔ Chưa có out/<ky>/so.json` | chưa chạy `tinh` | chạy `tinh` trước `bao-cao` |
| Cột Nhóm/Hạng toàn `⚠ thiếu TP-04` | chưa điền `master-nv.json` | `TP-04 §2` |
| CR48 của ngày cuối kỳ là `—` | **đúng** — chưa hội thoại nào đủ 48h | ⛔ không sửa. Đó là luật so công bằng |
| `P0 = 0` | **đúng** — tầng `chac` của `canh_bao_do` rất hẹp để tránh dương tính giả | xem cột `canh_bao_nghi` |
