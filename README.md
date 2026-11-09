# 🩺 Agent-QCQA-TrucPage-Kangnam

> **Agent QC/QA trực page hằng ngày của Bệnh viện Thẩm mỹ Kangnam.**
> Project: **KANGNAM TPQ – Trực Page QC/QA**
>
> Mỗi ngày hai lần, đọc **bộ số do code tính 100%** cộng **một mẫu hội thoại do code chọn**, để trả lời ba câu: **hôm nay rò SĐT ở đâu · vì sao rò · ai phải làm gì trước 10h**.
>
> Đầu ra dùng được ngay: **Báo cáo Sáng · Nhịp Trưa · bảng Việc hôm nay có mã hội thoại và hạn giờ · trang riêng từng nhân viên · chu kỳ tuần WIN/Fail/coaching**.

`v1.0` · 06/11/2026 · Claude / ChatGPT / Gemini / Claude Code

### 📘 [**Hướng dẫn cài đặt & 26 prompt mẫu →**](https://claude.ai/artifact/GfkDRraeVwVoRtrSVcrvtj)

> Trang hướng dẫn có **nút Copy từng file**: 2 thẻ bộ não · 7 sổ tri thức · 5 prompt mẫu dạng file · 26 prompt mẫu lọc theo lệnh · 5 luật người đọc báo cáo phải biết · 9 khoản đang chặn.
> Người mới vào khối thì **mở trang này trước, đừng đọc README**.
> Sinh lại bằng `python tools/trang-huong-dan.py` — nội dung các file nhúng thật từ repo nên sửa sổ tri thức rồi chạy lại là trang tự khớp.

---

## Bài toán

★ **Không phải báo cáo, mà là "rò SĐT".** Mỗi inbox đã trả tiền quảng cáo. Inbox không ra số trong 48h gần như là mất chi phí. Tăng CR48 là đòn bẩy rẻ nhất trong toàn phễu: không thêm ngân sách, CP/SĐT giảm ngay.

```
Chỉ số gốc:  CR48 = SĐT thô mới xin được trong 48h ÷ inbox mới (đã đủ 48h)
Phân rã:     SĐT = Inbox mới × % phản hồi đúng SLA × Tỷ lệ xin số
                   + SĐT từ chăm sóc lại
```

Mọi chỉ số khác tồn tại để giải thích **vì sao CR48 tăng hay giảm**.

---

## Ba nguyên tắc thiết kế

| # | Nguyên tắc | Hệ quả trong code |
|---|---|---|
| ① | **Code đếm, AI đọc** | `tp.py` tính 100% chỉ số trên **toàn bộ** hội thoại. AI chỉ đọc **mẫu phân tầng do code chọn**. ⛔ AI không đếm, không tự chọn hội thoại |
| ② | **So người công bằng theo chất lượng inbox nhận được** | Chỉ số **CEI** = CR thực tế ÷ CR kỳ vọng, kỳ vọng tính theo từng ô `dịch vụ × nhiệt × khung giờ`. ⛔ Không xếp hạng bằng CR thô — "TOP A" khi đó chỉ là "TOP inbox ngon" |
| ③ | **Mỗi báo cáo phải ra việc cụ thể có mã hội thoại** | Hàng chờ `P0–P6`, mỗi dòng có mã hội thoại, người xử lý, hạn giờ, và cột *Kết quả* để đo *tỷ lệ cứu được* ở lần chạy sau |

---

## Năm lớp

```
L0 NẠP & KIỂM      code   tp.py kiem    → phiếu chất lượng dữ liệu, 3 ngưỡng DỪNG
L1 MÁY TÍNH SỐ     code   tp.py tinh    → ht.csv (75 cột) · so.json · lich-su.csv
                          tp.py bao-cao → 10 mục bảng số
──────────────────────────────────────────────────────────────────────────────
L2 CHẤM HỘI THOẠI  AI     KF-60 · KF-62 · rubric TP-05, trên mau-ai.md
L3 CHẨN ĐOÁN       AI     6 nhóm nguyên nhân → ĐÚNG 3 vấn đề lớn nhất
L4 DANH SÁCH VIỆC  code+AI  code xếp P0–P6 · AI viết câu gợi ý nhắn tiếp
L5 HỌC THEO TUẦN   AI     WIN · Fail · giáo án coaching (thứ 2)
```

---

## Đầu vào → Đầu ra

```
① Bản xuất hội thoại Caresoft (.txt)  ─┐          ┌─► BÁO CÁO SÁNG   (lệnh NGÀY)
② tools/muc-tieu.json  ⚠ còn 'demo'   ─┼─► AGENT ─┼─► NHỊP TRƯA      (lệnh TRƯA)
③ tools/master-nv.json 🔴 CHƯA CÓ     ─┤          ├─► VIỆC HÔM NAY   P0–P6
④ Số chi quảng cáo     🔴 CHƯA CÓ     ─┘          ├─► TRANG RIÊNG NV (lệnh NV)
                                                   └─► CHU KỲ TUẦN    (lệnh TUẦN)
```

---

## ★ Đã chạy thật — không phải demo

Kiểm chứng trên bản xuất **2.087 hội thoại · 03–05/11/2026** của page *Bệnh viện thẩm mỹ Kangnam*. Toàn bộ số trong [`doc/04-kiem-chung-du-lieu-that.md`](doc/04-kiem-chung-du-lieu-that.md).

Vài con số:

| | |
|---|---|
| Parser | **2.087/2.087** hội thoại khớp header · **0** dòng lạ |
| CR48 chốt (03/11) | **25,9%** (mẫu 679) so mục tiêu demo 37% → 🔴 |
| Mắt xích rơi nặng nhất | **45,8%** hội thoại **không có lượt xin số nào** |
| Xin số lần đầu | trung vị **29,6 phút** so mục tiêu demo ≤ 5 phút |
| Khung giờ đáng sửa | **18–22h**: đông nhất (26,6% inbox), CR24 thấp nhất trong giờ trực (19,8%) |
| Ngoài giờ trực | **296 inbox (14,2%)** rơi vào 00–06h và 22–24h, FRT trung vị **5,9 giờ** |
| Bỏ sót | 15,0% — nhưng **157/313 là "vắt ca"** → 🔧 lỗi xếp ca, ⛔ không trừ điểm người |

### Ba thứ chỉ chạy thật mới lộ ra

| # | Vấn đề | Đã xử lý thế nào |
|---|---|---|
| ① | Giữ nguyên 5 tín hiệu KF-60 thì **"HOT chưa số" = 0** — vì tín hiệu ③ là *"đã cho SĐT"*, tức là *kết quả*. Mức ưu tiên `P1`, đúng cái việc đáng làm nhất, sẽ **rỗng** | Chạy **hai** thang: `nhiet_code` (5 tín hiệu, để so với agent khác) và `nhiet_loc` (4 tín hiệu, bỏ ③ — để xếp ưu tiên, chọn mẫu, làm ô cho CEI). Sau khi sửa: 0 → **156** |
| ② | *"Độ dài phiên chat"* ra **806,8 phút** vì phép đo lấy từ tin đầu tới tin cuối, mà nhiều hội thoại có nhân viên nhắn lại **hôm sau** | Cắt phiên theo luật note §0 (im > 30 phút là đóng phiên) → **7,8 phút**. Và mới lộ so sánh có nghĩa: hội thoại **ra số** có phiên 7,8 phút, hội thoại **chưa ra số** chỉ **1,8 phút** |
| ③ | Từ khóa tiếng Việt **bỏ dấu** trùng nghĩa: `kien` trùng *dự kiến* / *Kiên Giang* (38 `P0` sai) · `bao chi` trùng *bảo chị* · `sợ` → `so` trùng *số* trong "số điện thoại" · `nam`/`tham` trùng *năm* / *tham khảo* | Thay bằng cụm dài. Và `canh_bao_do` chia **hai tầng**: `chac` vào thẳng `P0`, `nghi` ⛔ không vào `P0` mà chỉ **buộc** vào mẫu AI đọc — vì *"có trường hợp nào biến chứng không ạ"* là **rào cản trước mổ**, không phải khiếu nại |

---

## Bảy sổ tri thức

| Sổ | Nội dung |
|---|---|
| [`TP-01`](knowledge/TP-01-chi-dan-lenh.md) | Vai trò · 7 lệnh · 12 luật bất biến · khi thiếu dữ liệu |
| [`TP-02`](knowledge/TP-02-core-chi-so.md) | ★★ CORE chỉ số · **hai thang nhiệt** · luật so công bằng · luật chốt/tạm · 6 nhóm nguyên nhân · điểm tuần |
| [`TP-03`](knowledge/TP-03-dac-ta-du-lieu.md) | ★ Đặc tả bản xuất Caresoft · giờ trực đang xung đột · **ba chỗ bộ che hở** · cột đang thiếu |
| [`TP-04`](knowledge/TP-04-master-data.md) | 🔴 Master data — **CHỜ QL**, đang chặn 4 đầu ra |
| [`TP-05`](knowledge/TP-05-rubric-qa-hoi-thoai.md) | ★★ Rubric QA `Q1–Q6` thang 100 · 6 lỗi nghiêm trọng `LN-1…6` |
| [`TP-06`](knowledge/TP-06-mau-bao-cao.md) | Mẫu báo cáo Sáng · Trưa · Tuần · trang riêng · giáo án |
| [`TP-07`](knowledge/TP-07-thu-vien-win-fail.md) | ⏳ Thư viện WIN/Fail — hạt giống từ kỳ đầu, mọi dòng `CHỜ DUYỆT` |

Dùng lại từ hệ: **KF-60** chấm nóng/lạnh · **KF-62** chân dung · **KF-11** tuân thủ.

---

## Cài & chạy

```bash
# ★ Cả chuỗi · từ file hội thoại ra thẳng dữ liệu cho dashboard
python tools/bao-cao.py    "du-lieu/<file>.txt"

# L0 · kiểm dữ liệu trước — 3 ngưỡng dừng
python tools/tp.py kiem    "du-lieu/<file>.txt"

# L1 · tính toàn bộ chỉ số → out/<ky>/
python tools/tp.py tinh    "du-lieu/<file>.txt"
python tools/tp.py bao-cao --ky <ky>

# L4 · hàng chờ ưu tiên P0–P6
python tools/tp.py viec    "du-lieu/<file>.txt" --ngay 05/11 --n 30

# L2 · mẫu phân tầng cho AI đọc
python tools/tp.py mau     "du-lieu/<file>.txt" --ngay 05/11 --n 120
```

Không cần cài gì — Python 3.9+, chỉ dùng thư viện chuẩn. Chi tiết: [`doc/01-cai-dat.md`](doc/01-cai-dat.md).

---

## 🔴 Chín khoản đang chặn

| # | Chặn gì | Chặn đầu ra nào | Ai mở |
|---|---|---|---|
| 1 | Bản đồ **40 mã NV → tên · nhóm · hạng** | bảng Nhóm · xếp hạng A/B/C · luật chia inbox · giáo án theo nhóm | QL trực page |
| 2 | **Bảng phân ca** theo khung giờ | cột *Số NV* của ma trận cohort · trần tải/ca | QL ca |
| 3 | **Giờ trực chính thức** — 3 con số đang xung đột (08:00–21:30 · 08–22h · 08:30–22:00) | mẫu số của **toàn bộ** SLA | Anh / QL |
| 4 | **Số chi quảng cáo** | Chi phí/SĐT · mốc realtime 13h | Performance |
| 5 | **Trường thị trường** | toàn bộ mục 4 của note — hiện phủ 10,4% | Caresoft / QL |
| 6 | **Tag bàn giao / lead** | mức ưu tiên `P5` | Caresoft / Sale |
| 7 | **62 inbox nhóm `KHAC`** chưa có trong danh sách dịch vụ chốt | mục tiêu CR của nhóm này | QL |
| 8 | **Bản xuất nhiều page** | chiều cắt theo Page | Caresoft |
| 9 | Đóng dấu **chốt** cho `tools/muc-tieu.json` | mọi cờ 🟢🟡🔴 hiện chỉ để tham khảo | Anh / QL |

Hai khoản **không mở được bằng dữ liệu**, phải đổi cách xuất: SĐT đã bị che `[SĐT ẩn]` → ⛔ không đo được *tỷ lệ SĐT hợp lệ* · chưa có lịch sử 30 ngày → ⛔ không tách *khách cũ quay lại*.

---

## 🔒 Dữ liệu cá nhân — đọc trước khi commit

**Repo này public.** `.gitignore` chặn `du-lieu/` · `out/` · `tools/master-nv.json`.

⚠ Bộ che của Caresoft **hở ở ba chỗ** (chi tiết [`TP-03 §3`](knowledge/TP-03-dac-ta-du-lieu.md)):

1. **21 tên khách thật lọt qua** ở dòng `**HT:** <tên> đã trả lời một quảng cáo.`
2. Có chỗ tên **khách** bị che thành `[tên NV]` → ⛔ không dùng nhãn này để suy ai là nhân viên.
3. **60 hội thoại** có nhân viên nhắc lại SĐT mà khách chưa từng gửi trong hội thoại → số đến từ kênh khác, ⛔ không tính vào SĐT thô.

⛔ Không đưa bản xuất gốc cho AI đọc — dùng `out/<ky>/mau-ai.md`.

---

## ⛔ Đây KHÔNG phải agent nào

| Việc | Của agent khác |
|---|---|
| Chấm **cuộc gọi điện thoại** | `Agent-QC-Telesale` |
| Chân dung khách · ngân hàng hook · dashboard insight kỳ 7 ngày | `Agent-InsightDashboard-Kangnam` |
| 30 mã cảnh báo ads · phân bổ ngân sách | `Agent-AdsReport-Kangnam` |
| Nội dung ads theo bác sĩ · kế hoạch quay | `Agent-SeedingPlant-Kangnam` |
| Gộp 4 nguồn telesale | `Agent-TongHopBaoCao-Telesale` |

⚠ Khác `Agent-InsightDashboard-Kangnam` ở **nhịp** và **đơn vị việc**: agent kia đọc theo kỳ 7 ngày và ra chân dung + hook. Agent này chạy **2 lần/ngày** và ra **một bảng việc có mã hội thoại, có hạn giờ**.

---

## 📊 Ba mẫu báo cáo đã dựng

Cả hai chạy trên cùng một bản xuất `du-lieu/Bệnh viện thẩm mỹ Kangnam_20261103-20261105.txt`
(2.087 hội thoại đọc được · 2.086 hợp lệ · kỳ 03–05/11/2026).
Khác nhau ở **bộ tiêu chí** và **người đọc chính**, không phải ở dữ liệu.

| | Mẫu 1 · Trực page QC/QA | Mẫu 2 · Sức khoẻ team |
|---|---|---|
| Link | [claude.ai/artifact/5LTvbByV2SUN5TwGwAT5yX](https://claude.ai/artifact/5LTvbByV2SUN5TwGwAT5yX) | [claude.ai/artifact/SUfxsHxkvTjxYYCtdAzneG](https://claude.ai/artifact/SUfxsHxkvTjxYYCtdAzneG) |
| Mẫu 3 | [claude.ai/artifact/NjRqQFQ1XYZwLNcrg8k1JD](https://claude.ai/artifact/NjRqQFQ1XYZwLNcrg8k1JD) — bám sát biểu mẫu đối tác, có thanh lọc 14 lát cắt ||
| Người đọc chính | QL trực page, dùng hằng ngày | Trưởng nhóm / BGĐ, đọc theo kỳ |
| Bộ tiêu chí | 11 tiêu chí (Q1–Q11) | **8 tiêu chí (Q1–Q8)** |
| Mẫu số chính | inbox hợp lệ (2.086) | **inbox mới** (1.977, đã trừ 109 khách cũ) |
| SLA | FRT tin đầu, khung 08:30–22:00 | **SLA lần đầu + SLA toàn hội thoại**, khung 08:15–21:30 |
| Xếp hạng | CEI24, không chia A/B/C | **A/B/C tính lại từ dữ liệu kỳ** |
| Lọc | theo dịch vụ, 9 lát cắt | 5 lát cắt trong tab, không lọc toàn trang |
| Lưu trạng thái | có — đánh dấu việc đã xử lý, form kiến nghị | không |
| Thiết kế | hệ riêng, có chế độ tối | theo biểu mẫu đối tác, Be Vietnam Pro, một chế độ sáng |

### Mẫu 1 — 7 tab
`Việc cần làm` · `Thẻ điểm của tôi` · `Cả đội` · `Chẩn đoán` · `Kịch bản` · `Kiến nghị QC/QA` · `Cách tính & luật`

Q1–Q7 máy đếm, Q8–Q11 AI chấm trên mẫu đã đọc.
Bộ lọc Dịch vụ tính lại thật 9 lát cắt; CEI và điểm AI giữ ở mức toàn kỳ vì cắt tiếp sẽ hết mẫu.
Dùng capability `db` + `user`: trạng thái việc dùng chung giữa mọi người mở link, mục Kiến nghị
giới hạn ở quyền Editor.

### Mẫu 2 — 5 tab
`Sức khoẻ team` · `Thẻ điểm nhân viên` · `Kịch bản` · `Việc cần làm` · `Cách tính & luật`

| Mã | Tiêu chí | Mục tiêu | Đo bằng |
|---|---|---|---|
| Q1 | Tỉ lệ xin số | ≥ 32% | Máy · SĐT thô ÷ inbox mới phát sinh trong kỳ |
| Q2 | Ra số trong 6h | ≥ 24% | Máy · tính từ tin đầu của khách |
| Q3 | Ra số trong 24h | ≥ 32% | Máy |
| Q4 | Ra số trong 48h | ≥ 37% | Máy |
| Q5 | SLA toàn hội thoại ≤ 5 phút | ≥ 85% | Máy · mọi lượt khách chờ, khung 08:15–21:30 |
| Q6 | Xử lí từ chối | ≥ 1,5/2 | AI · trên mẫu hội thoại đã đọc |
| Q7 | Tuân thủ kịch bản | ≥ 1,5/2 | AI |
| Q8 | Tuân thủ quy trình | ≥ 80 | Máy · chạm lại · xin ≥ 2 lần · không treo |

**Điểm tổng = tỉ lệ so với trung bình đội** (đội = 100):
Q1 30% · Q3 15% · Q5 20% · Q8 15% · Q6 10% · Q7 10%.
Hạng **A ≥ 110 · B 92–109 · C < 92**. Ô dưới 20 hội thoại để trống và bị loại khỏi điểm tổng.

**Thị trường** (6 nhóm): Hà Nội · Hồ Chí Minh · Các tỉnh khác · Việt kiều · Quốc tế · Chưa xác định.
Suy từ lời khách vì bản xuất không có trường này — độ phủ 21%, chỉ dùng để chia kịch bản,
⛔ không dùng để so hiệu quả.


### Mẫu 3 — Truy soát trực page (bám sát biểu mẫu đối tác)

[claude.ai/artifact/NjRqQFQ1XYZwLNcrg8k1JD](https://claude.ai/artifact/NjRqQFQ1XYZwLNcrg8k1JD) · 6 tab,
cùng bộ Q1–Q8 với mẫu 2 nhưng dựng đúng bố cục biểu mẫu:

- **Thanh lọc toàn cục**: Kỳ truy soát · So với kỳ · Page · Khối · Dịch vụ · Thị trường.
  Bốn ô đầu khoá kèm tooltip vì chưa có dữ liệu; Dịch vụ và Thị trường lọc thật, **một chiều**
  (chọn chiều này thì chiều kia về Tất cả).
- **14 lát cắt tính riêng** ([tools/v2slices.py](tools/v2slices.py)) — mỗi lát có đủ KPI đội, ma trận
  nhân viên, xếp hạng, diễn biến theo ngày, SLA theo ngày, tương quan FRT. ⛔ Không chia tỉ lệ từ số tổng.
- **Tab Sức khoẻ team đủ 8 khối** như biểu mẫu: Chỉ số toàn đội · Ma trận NV × Q1–Q8 (bấm dòng mở thẻ
  điểm) · Nhận xét nhanh · Diễn biến · SLA theo ngày + theo dịch vụ · Vì sao mất số · Mẫu tin dán chung
  chứa từ cấm · Tương quan FRT và số người cùng trả lời.

**Hai định nghĩa sửa lại cho khớp biểu mẫu** (khác mẫu 2):

| | Mẫu 2 | Mẫu 3 |
|---|---|---|
| Q5 trên ô KPI | 73,8% — tỉ lệ **hội thoại** giữ mọi lượt ≤ 5p | **13,7 phút TB · 90,6% lượt ≤ 5p** trên 4.806 lượt |
| % tin nhắn 1 chạm | 10,3% — **nhân viên** chỉ gửi 1 tin | **36,6% — khách** chỉ nhắn ≤ 1 tin rồi im |

Ô KPI có mũi tên ▲▼ so **mục tiêu** (chưa có kỳ trước để so kỳ).
Ba khối tính trên toàn kỳ và ghi rõ trên trang: *Vì sao mất số* · *Mẫu tin dán chung* · *Câu hỏi giá*.

```bash
python tools/v2calc.py    # thêm SLA theo lượt + cờ khách nhắn ≤1 tin
python tools/v2slices.py  # → v2slices.json: 14 lát cắt đầy đủ
python tools/v2extra.py   # → v2extra.json: mẫu tin từ cấm, câu hỏi giá
```

### Script sinh số

Thường chỉ cần `python tools/bao-cao.py "du-lieu/<file>.txt"` là chạy hết. Gọi lẻ khi cần soi
một bước — mọi script đều nhận tên kỳ làm tham số, mặc định lấy kỳ mới nhất trong `out/`:

```bash
python tools/v2calc.py  [<ky>]  # đọc file gốc + ht.csv → v2rows.json: SLA khung mới, khách cũ, thị trường
python tools/v2agg.py   [<ky>]  # → v2.json: Q1-Q8 theo người · dịch vụ · thị trường · khung giờ · ngày
python tools/v2bundle.py [<ky>] # → tools/data/v2.js
```

Tên kỳ, tên file `.txt` và **mốc hết quan sát** chỉ còn nằm ở [`tools/ky.py`](tools/ky.py) — trước
đây chúng bị ghi cứng ở **12 dòng** rải trong 4 script, nên đổi kỳ là phải sửa code. Ghi đè bằng
`TP_KY` và `TP_TXT` nếu cần trỏ tay.

Tiêu đề trang cũng **tự sinh từ dữ liệu**: `v2agg.py` ghi thêm `ky` và `pages` vào `v2.json`, và
`truc-page.html` dựng câu "Khách nhắn đầu … · N hội thoại · N inbox mới · N nhân viên · N page" từ
đó. Trước đây 13 chỗ trong shell ghi cứng kỳ 03–05/11, nên đổi dữ liệu là tiêu đề nói sai.

⚠️ Chỗ nguy hiểm nhất trong 12 chỗ đó là `OBS` ở `v2calc.py`: nó ghi cứng `2026-11-06`. Chạy kỳ khác
mà không sửa thì mốc hết quan sát rơi *trước* dữ liệu, và **Q2/Q3/Q4 rỗng sạch mà không báo lỗi gì**.
Nay mốc suy từ tên kỳ: 00:00 ngày sau ngày cuối.

### Gộp nhiều bản xuất thành một kỳ

Caresoft xuất theo cửa sổ ngày, nên **một hội thoại kéo dài qua nhiều cửa sổ bị cắt làm đôi** — mỗi
file chỉ giữ khúc tin của chính nó. Chạy riêng từng file thì khúc sau vô hình với kỳ trước, và ngày
gắn cho hội thoại cũng sai vì tin đầu của khách nằm ở file kia.

```bash
python tools/gop.py "du-lieu/a.txt" "du-lieu/b.txt"   # → du-lieu/GOP_<từ>-<đến>.txt
python tools/bao-cao.py "du-lieu/GOP_<từ>-<đến>.txt"
```

[tools/gop.py](tools/gop.py) gộp theo **mã hội thoại** rồi xếp tin theo thời gian. Không sửa, không
bịa, không bỏ tin nào.

Kết quả trên ba bản xuất 03–05/11, 06/11 và 08/11:

```
8.052 → 6.128 hội thoại  (1.924 mã trùng được nối lại)
62.659 tin vào → 62.659 tin ra · khớp từng ngày · 0 hội thoại sai thứ tự thời gian
2.152 hội thoại trải nhiều ngày — trước khi gộp, mỗi cái bị đếm thành hai
```

⛔ **Chỉ gộp bản xuất GỐC.** Đưa một file `GOP_*` vào cùng chính nguồn của nó là nhân đôi tin;
`gop.py` chặn bằng cách bỏ khối tin trùng **giữa các file** và báo số lượng ra màn hình.
Trong *cùng* một file thì tin lặp y hệt là dữ liệu thật (nhân viên gửi lại đúng câu đó) nên
được giữ — ba bản xuất này có 318 khối như vậy, bỏ đi là lệch với đường ống gốc.

⚠️ **Mỗi bản xuất một phạm vi page khác nhau** — kỳ 03–08/11 có `1 · 1 · 1 · 29 · 26` page theo
ngày. Gộp xong thì "Tất cả page" nhảy vọt ở ngày đổi phạm vi, trông y như đội đổi.

Trang **tự phát hiện** điều này: khi số page đổi giữa các ngày đã chọn, khối *Diễn biến theo ngày*
và *SLA theo ngày* hiện cảnh báo đỏ kèm nút **lọc về page có mặt đủ mọi ngày**. Ô chọn Page cũng
ghi rõ page nào chỉ phủ được mấy ngày (`3/5 ngày`).

Chênh lệch thật sự rất lớn:

| Ngày | Tất cả page · inbox | Q1 | Chỉ page chung · inbox | Q1 |
|---|---|---|---|---|
| 03/11 | 629 | 25,9 | 629 | 25,9 |
| 05/11 | 625 | 21,9 | 625 | 21,9 |
| 06/11 | **1.265** | 20,9 | **697** | 21,7 |
| 08/11 | **1.137** | 19,0 | **667** | 19,6 |

Đọc "Tất cả page" thì tưởng lưu lượng tăng gấp đôi từ 06/11 và Q1 rơi mạnh. Lọc về page chung thì
lưu lượng **đứng yên** (629 → 697 → 667) — cú tăng kia hoàn toàn là do bản xuất rộng hơn. Q1 vẫn
giảm thật, nhưng êm hơn nhiều: 25,9 → 22,3 → 21,9 → 21,7 → 19,6.

### Lọc mọi chiều ngay trên trang

Trang không còn đọc lát cắt dựng sẵn. Nó nhận **bảng hội thoại đã chấm** và tự cộng lại theo bộ lọc
đang chọn, nên lọc được **khoảng ngày · page · khung giờ · nguồn · dịch vụ · thị trường** và mọi
tổ hợp của chúng.

| File | Vai trò |
|---|---|
| `data/rows.js` ← [tools/v2pack.py](tools/v2pack.py) | bảng hội thoại nén theo cột, **71 B/dòng** |
| `agg.js` ← [tools/agg.js](tools/agg.js) | bản JS của công thức trong `v2slices.py` |
| [tools/kiem-agg.js](tools/kiem-agg.js) | đối chiếu từng ô JS với số Python |

Nén theo cột + từ điển nên bảng thô **nhẹ hơn chính file lát cắt nó thay thế** (105 KB so với
152 KB). Dự phóng: 2 tháng ≈ 2 MB, 6 tháng ≈ 6 MB.

### Kỳ đang chạy · 01–08/11

Một bản xuất liền mạch cả 8 ngày (`KN_ALL_20261101-20261108.txt`, 25 MB) thay cho việc gộp nhiều
bản. **Không còn lệch phạm vi page** — 25–30 page mỗi ngày, dao động tự nhiên vì có page hôm đó
không ai nhắn.

```
9.716 hợp lệ · 9.071 inbox mới · 38 page · 20 nhân viên · độ phủ trọng số 100% cho cả 20
Q1 23,8 · Q2 19,3 · Q3 22,7 · Q4 23,7 · Q5 69,4 · Q8 65,7   ·   hạng A 2 · B 14 · C 4
```

⛔ Ngưỡng cảnh báo phạm vi page đã nâng: chỉ kêu khi chênh **từ gấp đôi trở lên** (bản gộp cũ là
1 so với 29). Chênh vài đơn vị trong một bản xuất là bình thường — cảnh báo bật cả lúc bình thường
thì người đọc quen tay bỏ qua.

### Kết quả chấm lại Q6/Q7 · kỳ 03–08/11

AI đọc **204 hội thoại** lấy mẫu phân tầng, phủ đủ 17 nhân viên (5–23 hội thoại mỗi người,
126 hội thoại có rào cản). Lần đầu **cả 17 người có độ phủ trọng số 100%** — trước đó luôn có
người thiếu Q6/Q7 nên hạng tính trên 80–85% thước đo.

```
Q6 xử lí từ chối     trung bình 1,39 / 2   (thấp nhất 0,9 · cao nhất 1,9)
Q7 tuân thủ kịch bản trung bình 1,52 / 2   (thấp nhất 1,0 · cao nhất 1,8)
hạng: A 5 · B 10 · C 2
```

Ba điều rút ra khi đọc:

- **Người điểm Q6 cao không phải người nói nhiều hơn, mà người đổi được lý do.** Người cao nhất
  nói thẳng nỗi sợ của khách — *"em hiểu để lại số có thể khiến mình ngại bị gọi nhiều... em xin
  phép chỉ gọi một cuộc 2 phút, đúng khung giờ mình chọn"* — rồi mới xin lại.
- **Mở kênh thay thế là ranh giới rõ nhất.** Khách nói "không nghe máy được": người khá chuyển
  sang Zalo/Viber ngay; người yếu lặp lại đúng câu xin số cũ. Có ca khách nói *"sim đang khoá, nhắn
  tin giúp em"* ba lần mà vẫn bị mời nghe máy.
- **Q7 rơi ở nhịp giữa, không ở nhịp đầu.** Gần như ai cũng hỏi câu phân loại và xin ảnh. Khác
  nhau ở chỗ *trao giá trị thật*: đọc ảnh cụ thể, tính BMI, nêu khoảng giá — hay dán khối ưu đãi.

⚠️ Từ khi có `rows.js`, lệnh publish phải mang **cả hai** file dữ liệu. Đăng mỗi `data/v2.js` thì
tiêu đề trang nói kỳ mới trong khi mọi bảng vẫn là kỳ cũ — trang không báo lỗi, chỉ lặng lẽ sai.

⛔ **`agg.js` và `v2slices.py` là hai bản của cùng một công thức.** Sửa một bên là phải sửa bên kia,
rồi chạy `node tools/kiem-agg.js <ky>` — nó so từng ô của mọi lát:

```
kỳ 01-11_08-11-2026 · 17 lát · 28.556 ô  → ✓ khớp toàn bộ   ← kỳ đang chạy
kỳ 03-11_08-11-2026 · 15 lát · 22.228 ô  → ✓ khớp toàn bộ
kỳ 03-11_06-11-2026 · 15 lát · 19.295 ô  → ✓ khớp toàn bộ
kỳ 03-11_05-11-2026 · 14 lát · 15.642 ô  → ✓ khớp toàn bộ
kỳ 06-11_06-11-2026 · 11 lát ·  9.885 ô  → ✓ khớp toàn bộ
```

Ba chỗ bản JS suýt sai, và vì sao test bắt được:

1. **Làm tròn mốc hoà.** `round()` của Python làm tròn về số chẵn (81,25 → 81,2), JS làm tròn lên
   (81,3). Mẫu số hay là luỹ thừa của 2 nên mốc hoà xảy ra thật — 25 ô lệch.
2. **Thứ tự khi đồng hạng.** `Counter.most_common()` giữ thứ tự gặp đầu tiên; duyệt `for (k in obj)`
   trong JS trả khoá số theo thứ tự tăng dần — 6 ô lệch ở top-3 dịch vụ/thị trường của nhân viên.
3. **Mốc hoà giả.** `8109/53/60` trông là 2,55 nhưng double gần nhất là 2,5499… nên Python cho 2,5.
   Bản JS đầu nhân với 10 trước khi xét, phép nhân đó "sửa" sai số thành đúng 25,5 rồi tạo ra một
   mốc hoà không có thật → 2,6. Phải xét trên giá trị thật của double. Đúng **1 ô** trong 19.295 —
   không có bộ đối chiếu thì không đời nào thấy.

### Chạy một kỳ mới — ba điều phải biết

1. **Chấm lại Q6/Q7.** Điểm AI nằm ở [tools/diem_ai.py](tools/diem_ai.py), gắn với đúng kỳ
   `AI_KY`. Chạy kỳ khác, script cảnh báo và vẫn chạy, nhưng `diem`/`hang` lúc đó dựa trên điểm
   của kỳ trước. Cách chấm lại:

   ```bash
   python tools/tp.py mau "du-lieu/<file>.txt" --n 170   # → out/<ky>/mau-ai.md
   ```

   AI đọc mẫu rồi thay bảng trong `diem_ai.py` + đổi `AI_KY`. Bảng này trước đây **bị chép hai
   bản** — dict trong `v2agg.py` và tuple trong `v2slices.py` — nên sửa một bên là hai nơi nói hai
   điểm khác nhau mà không ai biết. Nay cả hai cùng import từ một chỗ.
2. **Kỳ ngắn thì Q3/Q4 rỗng.** Mẫu số chỉ nhận inbox đã đủ 24h/48h trước mốc. Kỳ một ngày ⇒ Q3 và Q4
   không có mẫu số nào; kỳ hai ngày ⇒ Q4 rất mỏng.
3. **Bản xuất nhiều page có nhiều thread không có tin khách.** Kỳ 06/11 xuất cả 29 page:
   1.974/3.445 hội thoại bị loại vì `KHONG_CO_TIN_KH` (bài đăng, thread bot). Đúng luật L0, không
   phải lỗi — nhưng đừng đọc tỉ lệ hợp lệ của bản nhiều page như của bản một page.

### Cập nhật dữ liệu lên artifact — AI không đọc số

Mẫu 3 **tách dữ liệu khỏi trang**. Artifact gồm hai file:

| File trong artifact | Nguồn trong repo | Vai trò |
|---|---|---|
| `index.html` · 103 KB | [tools/truc-page.html](tools/truc-page.html) | giao diện + mã — **không chứa số nào** |
| `data/v2.js` · 236 KB | `tools/data/v2.js` — sinh tự động | `var V2` · `var EX` · `var SLICES` |

Trang nạp số bằng `<script src="data/v2.js"></script>` đặt ngay trước mã ứng dụng, nên ba biến vẫn
là biến toàn cục y như hồi nhúng cứng — **mã ứng dụng không phải sửa một dòng**.

**Quy trình cập nhật kỳ mới — một lệnh rồi một lệnh:**

```bash
# 1 · từ file hội thoại gốc ra thẳng file dữ liệu
python tools/bao-cao.py "du-lieu/<file>.txt"
#    chuỗi: tp.py tinh → v2calc → v2agg → v2extra → v2slices → v2bundle
#    thêm --kiem để chạy phiếu chất lượng L0 trước
#    hoặc --ky <ky> để chạy lại từ ht.csv đã có, không tính lại
```

2 · nhờ Claude Code publish — một lệnh, không đọc dữ liệu:

> publish `tools/truc-page.html` lên `https://claude.ai/artifact/NjRqQFQ1XYZwLNcrg8k1JD`,
> kèm `files = {"data/v2.js": "tools/data/v2.js", "data/rows.js": "tools/data/rows.js"}`

Muốn tự động hẳn thì bọc bước 2 vào `.bat` + Task Scheduler gọi `claude -p "<câu trên>"`.

**Cách trực quan — tool [Chốt Số Trực Page](https://claude.ai/artifact/W3DLV4N1KdGJesrAktXszg)**
([tools/chot-so.html](tools/chot-so.html)) soát bằng mắt ở hai đầu của quy trình.

**Chế độ A — kéo file hội thoại gốc `.txt`/`.md` vào** (soát *trước* khi tính):

- **4 phép kiểm trên bản xuất** — đọc được bao nhiêu hội thoại · có lọt số điện thoại hay email
  chưa che (quét **toàn bộ** văn bản, không chỉ phần khớp khuôn) · vai nhân viên có đủ mã
  `NV-<số>` · hội thoại nào không đọc được tin nào.
- **Xem file có gì** — hội thoại, tin nhắn, tin khách, người trực, phân bố vai, và bảng theo ngày.
- **Trả về đúng lệnh cần chạy**, kèm nút copy. Tool **không tự tính** — xem phần *Vì sao không port
  sang JS* bên dưới.

**Chế độ B — kéo bộ số hoặc `data/v2.js` vào** (soát *sau* khi tính):

- **Chạy 10 ngưỡng** — 4 ngưỡng chặn (đủ bộ · đủ khoá · mã NV đúng dạng `NV-<số>` · không lọt
  SĐT/email) và 6 cảnh báo (kỳ khớp · tổng inbox khớp tổng theo người · lát *Tất cả* khớp `v2.json`
  · số nhân viên khớp cả ba bộ · mẫu tin dán chung · dung lượng). **Còn ngưỡng chặn thì khoá nút
  xuất** — không đăng được số bẩn.
- **Xem trước** 10 ô chỉ số đội kèm so với mục tiêu, số người hạng A/B/C, và bảng 17 nhân viên
  xếp theo điểm.
- **So với bản đang chạy** — kéo thêm `tools/data/v2.js` của kỳ trước vào bước 2 thì mọi chỉ số và
  mọi nhân viên có cột lệch, kèm ai mới vào bảng và ai đổi hạng.
- **Gói ra `v2.js`** để copy hoặc tải, kèm nút copy sẵn câu lệnh publish.

Tool giữ **nguyên văn bản JSON gốc** thay vì serialize lại, nên file nó xuất có thể lớn hơn file của
`v2bundle.py` — đổi lại `19.0` không bao giờ bị biến thành `19`. Nó **không tự đăng được**: một trang
artifact không có quyền ghi lên artifact khác, nên bước publish vẫn là một lệnh của Claude Code.
Artifact đang ở chế độ riêng tư — mở Share trên trang nếu muốn người khác dùng.

⚠️ Trên bộ số kỳ 03–05/11 tool chạy sạch 4 ngưỡng chặn, còn 2 cảnh báo, trong đó một cái là phát hiện
thật: `team.n` ghi **1.977** nhưng cộng 17 nhân viên chỉ ra **1.939** — **38 inbox không gán được cho
nhân viên nào**. Ma trận nhân viên vì thế luôn hụt 38 hội thoại so với KPI đội.

### Vì sao tool không tự tính từ `.txt`

Vì sẽ thành **hai bộ máy chấm điểm nhân sự song song**. Luật ① của repo là *một hội thoại chấm đúng
một lần, mọi bảng sau đọc lại từ `out/<ky>/ht.csv`* — một bản JS tính lại trong trình duyệt là phá
đúng luật đó: lệch một con số thì không ai biết tin bản nào. Thêm hai lẽ nữa:

- **`q6` và `q7` code không chấm được.** Chúng là điểm AI chấm khi đọc mẫu, dán cứng ở
  [`v2agg.py`](tools/v2agg.py) dòng 9–17. Hai tiêu chí này chiếm **20% trọng số hạng**, nên thiếu
  chúng là `diem` và `hang` của cả 17 người đều khác (trường `phu` tụt từ 100 xuống 80).
- **`.txt` một mình không đủ.** Cả bốn script v2 đều đọc thêm `ht.csv` — bảng 75 cột do `tp.py` chấm.

Nên tool giữ vai **cửa soát hai đầu**, còn `bao-cao.py` nối một đường ống duy nhất.

### ⚠️ Hai điều lộ ra khi dựng đường ống này

**1. `tp.py` và `v2calc.py` đọc tin nhiều dòng khác nhau.** `tp.py` nối dòng tiếp vào tin
(`ht.tin[-1].chu += "
" + ln`), còn [`v2calc.py`](tools/v2calc.py) thì `if not m: continue` — bỏ
thẳng. Trên kỳ 03–05/11 có **4.368 / 32.507 dòng (13,4%)** là dòng tiếp. Hệ quả: `ht.csv` đọc đủ
tin, nhưng **Q1–Q8 chỉ đọc dòng đầu của mỗi tin** — câu xin số hay câu từ chối nằm ở dòng thứ hai
không được tính. ⛔ Chưa sửa, vì sửa là đổi điểm và hạng của nhân sự.

**2. File gốc có 40 mã nhân viên, bảng xếp hạng chỉ 17 người.** Bảng chỉ tính người được gán là
*nhân viên chính* của hội thoại; 11 người có dưới 10 tin trong cả kỳ. Không phải lỗi, nhưng đọc hạng
của nhóm mẫu nhỏ thì phải dè dặt.

**Vì sao làm vậy** — trước đây 232 KB trong 339 KB của artifact là số nhúng cứng, nên mỗi lần đổi kỳ
hay chỉ sửa một màu nền cũng phải kéo cả khối số qua context của AI. Giờ số đi đường riêng: AI chỉ
chuyển file, **không đọc và không có cơ hội chép sai một chữ số nào**.

**Bốn điều đừng làm:**

- ⛔ Đừng nhúng số trở lại `tools/truc-page.html` — mất toàn bộ lợi ích.
- ⛔ Đừng sửa tay `tools/data/v2.js` — nó bị ghi đè mỗi lần chạy; sửa ở script sinh số.
- ⛔ Đừng truyền `capabilities` khi publish. Bỏ trống thì artifact giữ nguyên `db` (sổ kiến nghị
  `kiennghi`) và `user`; truyền thiếu một cái là **xoá** cái đó.
- ⛔ Đừng đổi tên `data/v2.js` một phía — tên này nằm trong cả `truc-page.html` và lệnh publish.

`tools/data/v2.js` **bị `.gitignore` bắt** (quy tắc `data/`) — cố ý, vì repo này public. Ai clone về
phải chạy lại `v2bundle.py` để có file dữ liệu. Ngược lại `tools/truc-page.html` commit được, vì
tách xong thì nó không còn số liệu khách nào.

⚠️ Artifact **không có capability mạng ngoài** (bộ capability khả dụng: `artifact · assets ·
comments · db · downloads · files · mcp · room · sample · self · user`), nên hướng "trang tự tải
JSON từ GitHub hay Google Sheets" là bất khả thi. File rời publish kèm artifact là cách gần nhất.

### Kết quả kỳ đầu 03–05/11/2026 — giữ làm mốc so sánh
```
inbox mới 1.977 (trừ 109 khách cũ) · Q1 21,5% · Q2 19,0% · Q3 21,8% · Q4 25,3%
Q5 SLA toàn hội thoại 73,8% (tin đầu 80,1% · ngưỡng 2 phút 50,4%) · Q8 64,5 · một chạm 10,3%
hạng: A 2 người · B 9 · C 6
```

**Ba điều chỉ lộ ra ở bộ Q mới:**
1. SLA tụt từ 80,1% xuống 73,8% khi tính cả hội thoại thay vì chỉ tin đầu — chỗ rơi nằm ở *giữa*.
2. Nhóm C không chậm: `NV-202194914` SLA 88,5% mà Q1 chỉ 13,1%. Lỗi nằm ở kịch bản, không ở tốc độ.
3. Hàm mặt có SLA cao nhất (80,3%) mà Q1 thấp nhất (17,8%) — dịch vụ giá trị cao đang rơi ở bước chốt.

---

## Luật quan trọng nhất

```
① CODE ĐẾM, AI ĐỌC
   ⛔ Không đếm hội thoại bằng tay. ⛔ Không nêu số không có trong so.json.

② SO CÔNG BẰNG
   Mẫu số CR24/CR48 chỉ gồm inbox ĐÃ ĐỦ 24h/48h kể từ tin đầu của khách.
   Chưa đủ giờ → dòng "đang chạy", ⛔ không nhập vào tỷ lệ.

③ LỖI HỆ KHÔNG TRỪ ĐIỂM NGƯỜI
   Inbox ngoài giờ · bỏ sót VẮT CA · hội thoại 1 chiều → "—" + 🔧 việc hệ thống.

④ ĐIỂM ĐỂ KÈM CẶP, KHÔNG ĐỂ KỶ LUẬT
   ⛔ Không có bảng xếp hạng cá nhân ngoài trang riêng của chính người đó.
```
"# Agent-QCQA-TrucPage-Kangnam" 
