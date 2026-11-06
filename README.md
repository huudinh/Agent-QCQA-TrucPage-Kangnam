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
```bash
python tools/v2calc.py   # đọc file gốc → v2rows.json: SLA khung mới, khách cũ, thị trường
python tools/v2agg.py    # → v2.json: Q1-Q8 theo người · dịch vụ · thị trường · khung giờ · ngày
```

### Kết quả kỳ 03–05/11/2026 (bộ Q mới)
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
