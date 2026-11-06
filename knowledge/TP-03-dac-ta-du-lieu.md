# TP-03 · Đặc tả dữ liệu

> Sổ đầu vào. Mở rộng từ `KF-67-03` chế độ B.
> ★ Sổ này viết **sau khi đã đọc bản xuất thật** `Bệnh viện thẩm mỹ Kangnam_20261103-20261105.txt`
> (2.087 hội thoại · 03–05/11/2026 · 4,4 MB · 39.717 dòng). Mọi con số dưới đây là số đo được, ⛔ không phải giả định.

---

## 1 · Quy ước tên file & nhịp xuất

```
<Tên page>_<YYYYMMDD bắt đầu>-<YYYYMMDD kết thúc>.txt
ví dụ: Bệnh viện thẩm mỹ Kangnam_20261103-20261105.txt
```

Đặt vào `du-lieu/`. ⛔ **Không commit** — xem `.gitignore`.

| Giờ | Việc | Ai |
|---|---|---|
| Trước **8:15** | Xuất toàn bộ tin D-1 từ Caresoft, bỏ vào folder đúng tên | Code / QL |
| **8:45** | `tp.py kiem` → `tinh` → `mau` → agent chạy `NGÀY` | Hệ |
| **9:00** | QL giao việc, họp đầu ca 10 phút (1 vấn đề + 1 câu mẫu của ngày) | QL trực page |
| Trước **13:05** | Xuất tin từ 0h đến 13:00 hôm nay | Code / QL |
| **13:30** | Agent chạy `TRƯA` | Hệ |
| **17:00** | QL chốt cột *Kết quả*, bàn giao ca tối | QL trực page |

⚠ File 13h và file 8:30 hôm sau **trùng tin nhau**. `tp.py` khử trùng bằng **mã hội thoại + mốc giây**, nhưng chỉ trong **một lần chạy**. Chạy hai file cùng kỳ thì ghi đè nhau theo cặp `(ngày, kỳ)` trong `out/lich-su.csv`.

---

## 2 · Cấu trúc bản xuất

### 2.1 Phần đầu file — ★ bắt buộc

```
# <Tên page>_<kỳ>

- Kỳ: 03/11/2026 → 05/11/2026
- Hội thoại: 2087

---

# Page: Bệnh viện thẩm mỹ Kangnam
```

⛔ Thiếu dòng `- Kỳ:` thì `tp.py` **dừng**: bản xuất không ghi năm ở từng tin, năm được suy từ dòng này.
Dòng `- Hội thoại:` dùng để **đối chiếu** — lệch là dấu hiệu bản xuất bị cắt → 🔴 dừng, kiểm lại.

### 2.2 Một hội thoại

```
## 1. HT-a434a80c6334

[03/11 00:06:25] **HT:** [tên KH] đã trả lời một quảng cáo.
[03/11 00:06:25] **QC:** Inbox từ quảng cáo <tên quảng cáo> — <mô tả>
[03/11 00:06:26] **BOT (Bệnh viện thẩm mỹ Kangnam):** <lời chào tự động>
[03/11 00:06:29] **KH:** Mở da nhiều
[03/11 08:32:34] **NV (NV-198843202) ⏱ ngoài giờ:** Em chào chị ...
[03/11 14:51:07] **NV (NV-198843202) ⏱ 14 giây ✓:** Dạ, ... Chị cho em xin SĐT nhé!
*(lượt cuối được NV-264113743 trả lời lúc 06/11 08:34:13 ⏱ ngoài giờ — sau kỳ)*
```

| Vai | Nghĩa | Đo được gì |
|---|---|---|
| `HT` | sự kiện hệ thống (*"đã trả lời một quảng cáo"*, *"Tin nhắn phản hồi bình luận"*) | nguồn inbox |
| `QC` | tên quảng cáo kéo inbox về | → **dịch vụ** (nguồn ưu tiên số 1) |
| `BOT` | tin tự động. Hai bot: lời chào page, và `CareSoft Workflow 2.1` | ⛔ **không** vào FRT, ⛔ không tính là "đã xin số" của người |
| `KH` | khách | tin đầu · SĐT · rào cản · tín hiệu nóng |
| `NV (NV-nnnnnnnnn)` | người trực | FRT · xin số · chạm lại |

**Hậu tố `⏱` của Caresoft** (tiện, nhưng ⛔ không phải nguồn tính):

| Hậu tố | Nghĩa | Số lượt trong bản thật |
|---|---|---|
| `⏱ N giây ✓` | trả lời trong ngưỡng | 3.088 |
| `⏱ NpN ✓` | ≤ ~2 phút | 1.029 |
| `⏱ NpN ✗` · `⏱ NgNp ✗` | quá ngưỡng | 1.057 + 100 |
| `⏱ ngoài giờ` | tin của khách rơi ngoài giờ trực → Caresoft **không chấm** | 578 |
| `… — sau kỳ)*` | lượt trả lời rơi **sau** ngày cuối kỳ | 108 hội thoại |

★ `tp.py` **tự tính lại FRT từ mốc giây**, ⛔ không đọc hậu tố `⏱`. Hậu tố chỉ dùng để **đối chiếu** ở `tp.py kiem`.

★ Dòng `*(… — sau kỳ)*` được nạp **như một lượt trả lời** để biết hội thoại có bị bỏ hẳn hay không, nhưng ⛔ **không vào FRT của kỳ**.

### 2.3 ⚠ Giờ trực — ba con số đang xung đột

| Nguồn | Giờ trực |
|---|---|
| Phương án §1 | 08:00 – 21:30 |
| note §0 / §6 | 08 – 22h |
| **Cờ `ngoài giờ` của chính bản xuất Caresoft** | **08:30 – 22:00** |

`tp.py` mặc định **08:30–22:00** để khớp với cờ của Caresoft (đo được: tin khách ở hour 22–23 và 00–08:29 đều bị gắn `ngoài giờ`; tin ở 21:00–21:59 thì không). Đổi bằng `--gio-mo` / `--gio-dong`, hoặc chốt lại ở `tools/muc-tieu.json › dinh_nghia.gio_truc`.

★ Hệ quả đo được trên bản thật: **470/2.086** hội thoại có tin đầu rơi ngoài giờ trực → 23% inbox **không có FRT**, và FRT ngoài giờ trung vị là **5,9 giờ**. Đây là con số 🔧 **việc hệ thống** lớn nhất của kỳ, ⛔ không phải lỗi người trực.

---

## 3 · 🔴 Ẩn danh — bộ che của Caresoft và ba chỗ nó hở

Bản xuất đã che sẵn:

| Mã che | Số lần | Nghĩa |
|---|---|---|
| `[Số ẩn]` | 3.575 | dãy số **không phải** SĐT (chiều cao, cân nặng, giá, id facebook) |
| `[tên KH]` | 2.807 | tên khách |
| `[Hình ảnh/Video/Đính kèm]` | 2.018 | tệp đính kèm |
| `[SĐT ẩn]` | 1.862 | **SĐT hợp lệ** |
| `[tên NV]` | 469 | tên nhân viên |
| `[Mẫu]` | 155 | tin theo mẫu |

### Ba chỗ bộ che hở — ⚠ phải biết trước khi đưa file đi đâu

1. **21 tên khách thật lọt qua** ở dòng `**HT:** <tên> đã trả lời một quảng cáo.` (21/1.847 ≈ 1,1%). ⛔ `tp.py` không đọc trường này nên không vào đầu ra, nhưng **file gốc vẫn chứa tên thật** → ⛔ không commit, ⛔ không gửi ra ngoài khối.
2. **Nhầm nhãn**: có chỗ tên **khách** bị che thành `[tên NV]` (*"Em chào chị [tên NV] Nguyên"*) → ⛔ không dùng `[tên NV]` để suy ra ai là nhân viên.
3. **SĐT không còn chữ số** → ⛔ không kiểm được *"đúng đầu số 03/05/07/08/09"*, ⛔ không khử trùng khách theo số, ⛔ không đo *tỷ lệ SĐT hợp lệ ≥ 92%* của note §6.

### Luật ẩn danh của agent

- Nhân viên: gọi bằng **mã `NV-nnnnnnnnn`** ở mọi đầu ra có thể ra khỏi nhóm QL. Tên thật chỉ xuất hiện trong trang riêng gửi đúng người đó.
- Khách: ⛔ không bao giờ nêu tên, SĐT, ảnh, link. Trích câu khách thì **trích đúng chữ, bỏ mọi phần nhận dạng**.
- `out/` và `du-lieu/` ⛔ không commit. `tools/master-nv.json` (có tên thật) ⛔ không commit.

---

## 4 · Cột bắt buộc vs cột đang thiếu

### ✅ Có và dùng được

`mã hội thoại` · `page` · `mốc giây từng tin` · `vai (HT/QC/KH/BOT/NV)` · `mã NV` · `tên quảng cáo` · `nội dung tin` · `cờ ngoài giờ`

### 🔴 Thiếu — mỗi dòng là một chỉ số không chạy được

| Thiếu | Chặn chỉ số nào |
|---|---|
| **Số chi quảng cáo** | Chi phí/SĐT · mốc realtime 13h theo % mục tiêu ngày |
| **Trường thị trường / tỉnh thành** | Toàn bộ mục 4 của note. Suy từ chữ khách chỉ phủ **217/2.086 ≈ 10,4%** |
| **Tag bàn giao / lead** | Mức ưu tiên **P5** (có SĐT mà chưa bàn giao Sale) |
| **Bảng phân ca** | Cột *Số NV* của ma trận cohort · trần tải/ca · luật chia inbox |
| **Lịch sử 30 ngày của khách** | Tách *inbox mới* vs *khách cũ quay lại* · tái khai thác inbox cũ 3–30 ngày |
| **Nhiều page** | Chiều cắt theo Page — bản xuất chỉ có **1 page** |
| **Trường dịch vụ của Caresoft** | Hiện phải suy: 1.616 từ tên quảng cáo (77,5%) · 212 từ lời chào BOT · 145 từ chữ khách · **113 không xếp được (5,4%)** |

⛔ Thiếu cột nào thì ghi `—` kèm lý do. ⛔ Không ước lượng, ⛔ không lấy số của chiều khác gán sang.

---

## 5 · Phiếu chất lượng dữ liệu — ngưỡng dừng

`tp.py kiem` in phiếu này trước mỗi lần chạy. Ba ngưỡng **dừng hẳn**:

| Kiểm | Ngưỡng 🔴 dừng |
|---|---|
| Hội thoại đọc được vs dòng `- Hội thoại:` ở header | **lệch bất kỳ** → bản xuất bị cắt |
| Dòng lạ không gắn được vào hội thoại nào | > 0 → cú pháp bản xuất đã đổi |
| Thiếu dòng `- Kỳ:` | → không suy được năm |

Ba ngưỡng ⚠ **cảnh báo, vẫn chạy**: độ phủ dịch vụ < 85% · độ phủ nhân viên < 95% · số hội thoại treo chưa trả lời > 5% mẫu.

★ Kết quả chạy thật trên bản 03–05/11/2026: 2.087/2.087 khớp · 0 dòng lạ · phủ dịch vụ 94,6% · phủ nhân viên 99,4% · 52 hội thoại treo (2,5%). Chi tiết ở `doc/04-kiem-chung-du-lieu-that.md`.
