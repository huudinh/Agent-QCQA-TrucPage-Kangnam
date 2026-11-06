# 03 · Output mẫu

> ★ Đây **không phải** output bịa. Toàn bộ con số dưới đây lấy từ lần chạy thật trên
> `Bệnh viện thẩm mỹ Kangnam_20261103-20261105.txt` (2.086 hội thoại hợp lệ).
> Mọi mã `HT-xxxxxxxx` là mã thật, tra lại được trong `out/03-11_05-11-2026/ht.csv`.
>
> Phần nào do **code** làm và phần nào do **agent** làm được ghi rõ ở mỗi mục.

---

# BÁO CÁO SÁNG TRỰC PAGE · 06/11/2026 · 08:45

Cỡ mẫu: **2.086 / 2.087** hội thoại hợp lệ · kỳ 03/11 → 05/11/2026 · page *Bệnh viện thẩm mỹ Kangnam* · giờ trực 08:30–22:00

**Số CHỐT:** CR24 cho inbox **04/11** · CR48 cho inbox **03/11**
**Số TẠM:** mọi tỷ lệ của inbox 05/11 — chưa hội thoại nào đủ 24h → ⛔ không dùng để đánh giá nhân viên

⚠ Mọi mục tiêu còn ở trạng thái `demo` (`tools/muc-tieu.json`) — chưa ai chốt. Cờ 🟢🟡🔴 chỉ để tham khảo.

---

## 1 · Một dòng tình hình

> CR48 chốt của 03/11 là **25,9%** (mẫu 679) — thiếu **11,1 điểm** so mục tiêu demo 37%. Inbox không thiếu (695/ngày, vượt 24% mục tiêu); chỗ rơi nằm ở mắt xích **xin số**: **45,8%** hội thoại cả kỳ không có lượt xin số nào, và riêng **05/11 tỷ lệ đã xin số tụt từ 60,4% xuống 43,7%** — mất **16,7 điểm** trong một ngày.

*(mục này: agent viết, số lấy từ `bao-cao.md` mục 1 và mục 10)*

---

## 2 · Bảng chốt

*(mục này: copy nguyên từ `bao-cao.md` mục 1 — code tính)*

| Ngày | Inbox | SĐT thô | Tỷ lệ SĐT thô | CR24 (mẫu) | CR48 (mẫu) | Chưa đủ 24h | Chưa đủ 48h |
|---|---|---|---|---|---|---|---|
| 03/11 | 679 | 176 | 25,9% | 24,9% (679) | **25,9% (679)** ✅ | 0 | 0 |
| 04/11 | 748 | 157 | 21,0% | **19,5% (748)** ✅ | — (0) | 0 | 748 |
| 05/11 | 659 | 129 | 19,6% | — (0) tạm | — (0) tạm | 659 | 659 |
| **Toàn kỳ** | **2.086** | **462** | **22,1%** | 22,1% (1.427) | 25,9% (679) | 659 | 1.407 |

| So mục tiêu | Thực tế | Mục tiêu (⚠ demo) | Đạt? |
|---|---|---|---|
| CR24 toàn kỳ | 22,1% | 32,0% | 🔴 69,0% |
| CR48 toàn kỳ | 25,9% | 37,0% | 🔴 70,1% |
| Inbox/ngày | 695 | 560 | 🟢 124,2% |
| SĐT/ngày | 154 | 180 | 🟡 85,6% |

⛔ **Chi phí/SĐT**: không tính được — bản xuất hội thoại không có số chi quảng cáo.
⚠ **Cùng thứ tuần trước** và **7 ngày vs 7 ngày trước**: chưa có mốc so sánh (kỳ chỉ 3 ngày).

---

## 3 · Ba vấn đề lớn nhất

*(mục này: agent chẩn đoán — L3. Mỗi vấn đề đúng khuôn 6 ô của `TP-06 §1`)*

### 🔴 Vấn đề 1 · Ngày 05/11 team bỏ hẳn bước xin số

| Ô | Nội dung |
|---|---|
| ① **Số** | % hội thoại có lượt xin số: 03/11 = **58,8%** → 04/11 = **60,4%** → 05/11 = **43,7%**. Mất **16,7 điểm** trong một ngày, mẫu 659 |
| ② **Nhóm** | ④ **Kịch bản** — ⛔ không phải SLA: FRT tin đầu 05/11 là **0,9 phút**, tốt nhất cả kỳ |
| ③ **Ai chịu** | QL trực page |
| ④ **Việc** | Họp đầu ca 06/11: chốt **mốc bắt buộc** — xin số **trước tin NV thứ 3**, dùng câu `W1`/`W2` của `TP-07 §2.1`. Dán 2 câu đó lên bảng ca |
| ⑤ **Bằng** | `HT-7f29907d179a` — Mũi · `NV-205107209` · **10 tin NV** · phiên 70,1 phút · khách đã hỏi giá · ⛔ **không có lượt xin số nào**<br>`HT-34fc47d7e94b` — Mắt · `NV-198843202` · **12 tin NV** · phiên 42,1 phút · ⛔ không xin số |
| ⑥ **Quy mô** | **17** hội thoại ngày 05/11 vừa HOT-chưa-số vừa **không xin số lần nào** / 659 inbox. Cả kỳ: **956 / 2.086 = 45,8%** |

### 🔴 Vấn đề 2 · Khung 18–22h: đông nhất, CR thấp nhất, và không phải vì thiếu người

| Ô | Nội dung |
|---|---|
| ① **Số** | Khung 18–22h: **554 inbox = 26,6%** cả kỳ — khung đông nhất. CR24 = **19,8%** (mẫu 398), thấp nhất trong giờ trực. So khung 14–18h: CR24 26,7% (mẫu 300), CR48 34,2%. Chênh **−6,9 điểm CR24** |
| ② **Nhóm** | ④ **Kịch bản** + ⑤ **Kỹ năng** — ⛔ không phải ③ quy trình: FRT 18–22h là **1,4 phút**, trong ngưỡng. Nhưng *≤ 1h ra số* tụt còn **16,8%** so 22,1% của khung chiều → đúng dấu hiệu *"FRT tốt mà ≤24h vẫn thấp = lỗi kịch bản/kỹ năng"* (`TP-02 §5`) |
| ③ **Ai chịu** | QL trực page + trực page ca tối |
| ④ **Việc** | Mini-training 15 phút đầu ca tối 06/11, đúng một nội dung: sau câu trao giá trị → **nối thẳng** câu xin số. Đo lại CR24 khung 18–22h ở báo cáo 08/11 |
| ⑤ **Bằng** | `HT-bb22fd7b7f55` — Hàm mặt · `NV-198843202` · phiên **49,6 phút** · ⛔ chưa xin số lần nào<br>`HT-30c0f1250fd8` — Mắt · `NV-236425444` · phiên 24,6 phút · khách đã hỏi giá · ⛔ chưa xin số |
| ⑥ **Quy mô** | **14** hội thoại khung 18–22h ngày 05/11 có phiên > 15 phút mà chưa xin số lần nào. Cả kỳ: **181** hội thoại |

### 🔧 Vấn đề 3 · Việc hệ thống: 296 inbox rơi vào khoảng không có người trực

| Ô | Nội dung |
|---|---|
| ① **Số** | 00–06h: **115 inbox** (CR48 21,4%, mẫu 28) · 22–24h: **181 inbox** (CR48 15,8%, mẫu 76) → **296 inbox = 14,2%** cả kỳ. FRT ngoài giờ trung vị **5,9 giờ** (mẫu 470). Khung 06–09h ngày 04/11 có FRT tin đầu trung vị **41,1 phút** — dấu vết "đào mess buổi sáng" |
| ② **Nhóm** | ③ **Quy trình / SLA** — ★ ⛔ **không trừ điểm người trực**: cả hai khung nằm ngoài 08:30–22:00 (`TP-02 §6`) |
| ③ **Ai chịu** | 🔧 Hệ thống + QL ca |
| ④ **Việc** | Hai lựa chọn, cần anh chọn: ① mở ca đêm 22–24h (khung này đông hơn 00–06h **1,6 lần**) ② bot chào + **2 nút hỏi nhanh** cho khung 22–06h. ⚠ Đo được: bot hiện chỉ xin số ở **8 hội thoại** trong 3 ngày — đòn bẩy này **chưa dùng** |
| ⑤ **Bằng** | `HT-8dfd849e3205` — FRT **87 phút** · `NV-262546406` · không ra số<br>`HT-c70c8d5a0182` — FRT **87 phút** · `NV-236425444` · không ra số |
| ⑥ **Quy mô** | 296 / 2.086 = **14,2%** inbox · 470 hội thoại có tin đầu ngoài giờ = **22,5%** |

### 👁 Theo dõi — chưa đủ để thành vấn đề

- **Hàm mặt** (dịch vụ giá trị cao): CR48 **14,6%** (mẫu 41 → ⚠ MẪU NHỎ) và % đã xin số **40,8%** — cả hai thấp nhất. Gộp 7 ngày rồi xem lại.
- **Chạm lại** chỉ **61,7%** (mục tiêu demo 95%) và **% SĐT thêm ở cửa sổ 24–48h chỉ 1,0%** → chăm sóc lại gần như không đem thêm số. Đưa vào `TUẦN`.
- Khách đã từ chối mà **vẫn ra số 47,5%** (mẫu 40) — ★ đang làm **tốt** hơn mục tiêu demo 25%. Lấy câu từ nhóm này vào `TP-07`.

---

## 4 · Việc hôm nay — 05/11 · 63 dòng, trích 5 dòng P1 + tổng hợp P2–P4

*(cột `P` → `Hạn`: code xếp, ở `viec-0511.csv`. Cột **Câu gợi ý nhắn tiếp**: agent viết)*

| P | Mã hội thoại | Dịch vụ | NV | Tình trạng | Câu gợi ý nhắn tiếp | Hạn | Kết quả |
|---|---|---|---|---|---|---|---|
| P1 | `HT-7f29907d179a` | Mũi | `NV-205107209` | 10 tin NV, phiên 70 phút, khách hỏi giá, chưa xin số lần nào | *"Để bác sĩ đánh giá đúng nền mũi và báo chi phí sát với mình, anh/chị cho em xin số điện thoại để trợ lý bác sĩ gọi tư vấn kỹ nhé"* | 10:00 | |
| P1 | `HT-34fc47d7e94b` | Mắt | `NV-198843202` | 12 tin NV, phiên 42 phút, rào cản giá, chưa xin số | *"Em gửi hội chẩn bác sĩ cho tình trạng mí của chị. Chị cho em xin SĐT để khi có kết quả trợ lý bác sĩ liên hệ lại ạ"* | 10:00 | |
| P1 | `HT-f1406ea93e2f` | Body | `NV-198843202` | 8 tin NV, phiên 31 phút, rào cản giá, chưa xin số | *"Chi phí body phụ thuộc vùng và lượng mỡ, em xin SĐT để bên em gọi báo đúng cho mình trong 2–3 phút nha"* | 10:00 | |
| P1 | `HT-f426bc7bb886` | Da / Trẻ hóa | `NV-264113743` | 5 tin NV, phiên 31 phút, chưa nêu rào cản, chưa xin số | *"Em xin 1–2 ảnh vùng da chị đang lo để bác sĩ xem, và xin SĐT để gửi kết quả hội chẩn tới mình ạ"* | 10:00 | |
| P1 | `HT-c2911fb4f64b` | Ngực | `NV-264113743` | cửa sổ 24h còn 22,0h | *(agent viết theo rào cản của hội thoại)* | 10:00 | |
| P2 | — 19 hội thoại ngày 05/11 khách nhắn cuối, chưa ai trả lời > 15 phút | | | | **xử lý ngay**, trước mọi việc khác | ngay | |
| P3 | — 8 hội thoại WARM chưa số, cửa sổ 24h còn < 6h | | | | | trước khi hết 24h | |
| P4 | — 2 hội thoại khách đã từ chối, NV chưa thử cách xin thứ 2 | | | | lấy câu từ nhóm 47,5% từ chối-vẫn-ra-số | trong ca | |

⚠ **P5** (có SĐT mà chưa bàn giao Sale) 🔴 không xuất được: bản xuất Caresoft không có tag bàn giao / lead.
⚠ **P0** = **0** trong cả 3 ngày. Đây là số đúng — tầng `chac` của `canh_bao_do` được làm rất hẹp để tránh dương tính giả (`TP-03`, `doc/04 §5.3`). Cột `canh_bao_nghi` vẫn buộc các hội thoại nghi vấn vào mẫu AI đọc.

⛔ Cột **Kết quả** để trống — NV điền trên Google Sheet. Lần chạy sau đọc lại để đo *tỷ lệ cứu được*.

---

## 5 · 🔧 Việc hệ thống — ⛔ không trừ điểm người

| Việc | Số | Ghi chú |
|---|---|---|
| Inbox có tin đầu **ngoài giờ trực** | 470 (22,5%) | FRT ghi `—`, ⛔ không chấm `Q1.1` |
| Bỏ sót **vắt ca** — khách nhắn còn trong giờ, trả lời chỉ đến sau khi ca đóng | 157 / 313 bỏ sót | lỗi **xếp ca** |
| Hội thoại **1 chiều** — khách nhắn 1 tin rồi im | 661 (31,7%) | chỉ số của **Ads**, ⛔ không trừ điểm NV |
| BOT xin số | chỉ **8** hội thoại / 3 ngày | đòn bẩy chưa dùng |

★ Phần **quy được cho người trực** trong "bỏ sót" chỉ là **111 hội thoại = 5,3%**, không phải 15,0%.

### Và một việc cho Ads

| Quảng cáo (≥ 30 inbox) | Inbox | CR48 | % hội thoại 1 chiều |
|---|---|---|---|
| `thương hiệu_Banner đẹp hàn quốc_page bv` | 77 | **62,5%** | 10,4% |
| `QC_Cắt mí_Video cắt mí nam 7,2Tr tối ưu` | 84 | 37,1% | 23,8% |
| `QC_Cắt mí_Banner bọng mỡ 23-10 - Bản sao_Group_1` | 51 | **13,6%** | 29,4% |
| `Nâng mũi_Video top 5_page bv` | 33 | **10,0%** | 36,4% |
| `Banner chị Loan cấy mỡ_dungnx_caymo - Bản sao` | 36 | **9,1%** | 38,9% |

Chênh **62,5% vs 9,1%** trong cùng 3 ngày, và **% 1 chiều đi cùng hướng**. → chuyển Performance: ba quảng cáo cuối đang kéo inbox lạnh. ⛔ Không quy lỗi nhân viên trực page.

---

## 6 · Câu mẫu của ngày

> *"Dạ, với tình trạng của mình hiện tại em sẽ gửi hội chẩn bác sỹ về phương pháp cũng như chi phí cho mình chị nha. Chị cho em xin Số Điện Thoại để em lưu thông tin, khi có kết quả trợ lý bác sỹ sẽ liên hệ tới chị ạ"*

Nguyên văn từ một hội thoại thắng của kỳ (`TP-07 §2.1` mã `W1`). Đặt **ngay sau** khi trả lời câu đầu của khách, ⛔ không để đến tin thứ 10.

⏳ Trạng thái: **CHỜ DUYỆT** — chưa đủ 10 lần dùng để vào kịch bản chuẩn.

---

## 7 · ⚠ Thứ đang chặn

| # | Chặn gì | Chặn đầu ra nào |
|---|---|---|
| 1 | `TP-04` — bản đồ **40 mã NV → tên · nhóm · hạng** | bảng Nhóm · xếp hạng A/B/C · luật chia inbox |
| 2 | **Bảng phân ca** | cột *Số NV* của ma trận cohort · trần tải/ca |
| 3 | **Giờ trực chính thức** — 3 con số đang xung đột | mẫu số của toàn bộ SLA |
| 4 | **Số chi quảng cáo** | Chi phí/SĐT · mốc realtime 13h |
| 5 | **Trường thị trường** | toàn bộ mục 4 của note — phủ 10,4% |
| 6 | **Tag bàn giao / lead** | mức ưu tiên `P5` |
| 7 | **62 inbox nhóm `KHAC`** | mục tiêu CR của nhóm này |
| 8 | **Bản xuất nhiều page** | chiều cắt theo Page |
| 9 | Đóng dấu **chốt** cho `muc-tieu.json` | mọi cờ RAG |

> *Điểm dùng để phân việc kèm cặp. Không phải căn cứ kỷ luật hay xếp hạng công khai.*

---

---

# Phụ lục · Hai mẫu khác

## A · Mẫu `mau-ai.md` — file agent đọc ở L2

```
# MẪU CHO AI ĐỌC · L2 · kỳ 03/11 → 05/11/2026

> 135 hội thoại, chọn bằng code theo tầng (ô nguy hiểm lấy dày nhất),
> ⛔ không để AI tự chọn. Trong mỗi tầng: trải đều theo dịch vụ × khung giờ.
> Tổng mẫu hợp lệ của kỳ: 2086 hội thoại.

| Tầng | Có trong kỳ | Vào mẫu |
|---|---|---|
| HOT_CHUA_SO   | 140 | 36 |
| WARM_CHUA_SO  | 749 | 30 |
| HOT_RA_SO     |  68 | 18 |
| WARM_RA_SO    | 269 | 18 |
| COLD_RA_SO    | 125 | 12 |
| COLD_CHUA_SO  | 735 |  6 |
| ★ CO_CANH_BAO (buộc thêm vào) | 16 | 15 |

---

## HT-41f1208b3519 · HOT_CHUA_SO

- Ngày 04/11 · khung 09-12 · dịch vụ `BODY` · NV `NV-254668856`
- Nhiệt (code, chỉ để lọc): **HOT** (KF-60-lite 5 tín hiệu: WARM) ①④ · rào cản: `GIA`
- Ra số: **CHƯA** · NV xin số 2 lần (lần đầu ở lượt NV thứ 4)
- FRT tin đầu: 43 giây · phiên 28,5 phút

  [04/11 11:27:55] **HT:** [tên KH] đã trả lời một quảng cáo.
  [04/11 11:27:55] **QC:** Inbox từ quảng cáo thương hiệu_Video sale kỷ lục_page bv_Group_1
  [04/11 11:28:00] **KH:** Hút mỡ bắp tay giá bao nhiêu vậy ạ
  [04/11 11:28:43] **NV NV-254668856:** Em chào chị ạ
  [04/11 11:28:57] **NV NV-254668856:** Trước đây mình đã từng sử dụng biện pháp giảm mỡ vùng bắp tay chưa ạ?
  [04/11 11:29:11] **KH:** Chưa ạ
  ...
```

## B · Mẫu `NV <mã>` — trang riêng một người

```
# TRANG RIÊNG · NV-202194914 · kỳ 03–05/11/2026

Cỡ mẫu của bạn: 136 hội thoại · 71 đủ 24h · 1 đủ 48h

## Số của bạn
| Chỉ số | Bạn | Team | |
|---|---|---|---|
| Inbox nhận | 136 | — | |
| SĐT thô | 19 | — | |
| CR24 thực tế | 14,1% | 22,1% | |
| CR24 kỳ vọng (theo đúng loại inbox bạn nhận) | 20,8% | — | |
| **CEI24** | **0,68** | 1,00 | 🔴 |
| FRT tin đầu (trung vị) | **37 giây** | 1,1 phút | 🟢 |
| % hội thoại đã xin số | **76,5%** | 54,2% | 🟢 |

Nghĩa: với đúng loại inbox bạn nhận, team làm được 20,8%; bạn làm được 14,1%.

★ Hai con số của bạn ĐỀU tốt hơn người đứng đầu: phản hồi 37 giây, và xin số ở
76,5% hội thoại — cao nhất team. Nhưng CEI24 là 0,68. Nghĩa là bạn xin ĐÚNG GIỜ
và xin NHIỀU, nhưng khách vẫn không cho. Vấn đề không ở SLA, ở NỘI DUNG CÂU XIN.

⚠ Kỳ này chỉ 3 ngày nên chỉ 1 hội thoại của bạn đủ 48h → ⛔ không đọc CEI48.

## Ba hội thoại làm bằng
... (2 hội thoại mất số + 1 thắng, có trích nguyên văn, mỗi cái chỉ ra ĐÚNG MỘT mã Q)

## Việc của bạn — 1 việc
... (hành động + câu mẫu dùng được ngay + đo thế nào kỳ sau)

> Điểm dùng để phân việc kèm cặp. Không phải căn cứ kỷ luật hay xếp hạng công khai.
```
