# 04 · Kiểm chứng trên dữ liệu thật

> Bản xuất: `Bệnh viện thẩm mỹ Kangnam_20261103-20261105.txt`
> **2.087 hội thoại · 03–05/11/2026 · 1 page · 4,4 MB · 39.717 dòng**
> Chạy ngày 06/11/2026 bằng `tools/tp.py` · giờ trực 08:30–22:00 · khung giờ `note`.
>
> ★ Tài liệu này ghi **những gì bản xuất thật đã nói ra**, gồm cả những chỗ nó **không nói được**. Đây là lớp L0+L1 (code). ⛔ Phần chẩn đoán (L3) chưa có trong file này — đó là việc của agent.

---

## 1 · Parser đọc được hết, không mất dòng nào

| Kiểm | Kết quả |
|---|---|
| Hội thoại khai báo ở header vs đọc được | 2.087 / 2.087 — ✅ khớp |
| Dòng lạ không gắn được vào hội thoại nào | 0 — ✅ |
| Hội thoại hợp lệ vào mẫu tính | 2.086 (99,95%) — 1 bị loại: đối tác chào hàng |
| Có lượt trả lời **sau kỳ** (06/11) | 108 hội thoại — nạp để biết có bị bỏ hẳn hay không, ⛔ không vào FRT |
| Còn treo, chưa ai trả lời đến hết kỳ | 52 (2,5%) |

**Độ phủ từng trường:** nguồn quảng cáo 93,7% · xếp được dịch vụ 94,6% · xác định được nhân viên 99,4% · đo được FRT tin đầu trong giờ 76,9% · **suy ra được thị trường 10,4% 🔴**.

---

## 2 · Ba chỗ bản xuất tự khai ra giờ trực — và ba con số đang xung đột

Bản xuất gắn cờ `⏱ ngoài giờ` cho 578 lượt. Đối chiếu mốc giây của tin khách đứng trước mỗi cờ:

- Tin khách ở **22:00–08:29** → luôn bị gắn `ngoài giờ`.
- Tin khách ở **08:30–21:59** → không bị gắn.

→ Caresoft đang chạy giờ trực **08:30 – 22:00**. Trong khi đó phương án §1 ghi **08:00–21:30** và note §0/§6 ghi **08–22h**.

`tp.py` mặc định theo Caresoft (08:30–22:00) để số của hệ khớp với số nhân viên nhìn thấy trên Caresoft. 🔴 **Cần chốt** ở `tools/muc-tieu.json › dinh_nghia.gio_truc` — đổi giờ trực là đổi mẫu số của toàn bộ SLA.

---

## 3 · Bộ số chính — kỳ 03–05/11/2026

### 3.1 Chốt / tạm

| Ngày | Inbox | SĐT thô | Tỷ lệ SĐT thô | CR24 (mẫu) | CR48 (mẫu) |
|---|---|---|---|---|---|
| 03/11 | 679 | 176 | 25,9% | 24,9% (679) | **25,9% (679)** ✅ chốt |
| 04/11 | 748 | 157 | 21,0% | **19,5% (748)** ✅ chốt | — (0) |
| 05/11 | 659 | 129 | 19,6% | — (0) | — (0) |
| **Toàn kỳ** | **2.086** | **462** | **22,1%** | 22,1% (1.427) | 25,9% (679) |

★ Luật so công bằng chạy đúng: 05/11 chưa hội thoại nào đủ 24h → CR24 ghi `—`, ⛔ không ghi 0. Với kỳ 3 ngày, **CR48 chốt chỉ có cho đúng một ngày**.

| So mục tiêu demo | Thực tế | Mục tiêu | Cờ |
|---|---|---|---|
| CR24 | 22,1% | ≥ 32% | 🔴 69,0% mục tiêu |
| CR48 | 25,9% | ≥ 37% | 🔴 70,1% mục tiêu |
| Inbox/ngày | 695 | 560 | 🟢 124,2% |
| SĐT/ngày | 154 | 180 | 🟡 85,6% |

⚠ Mọi mục tiêu còn ở trạng thái `demo` trong `tools/muc-tieu.json`. **Chưa ai chốt** → cột Cờ chỉ để tham khảo.

### 3.2 Phân rã — về nào đang rơi

```
SĐT = Inbox mới × % phản hồi đúng SLA × Tỷ lệ xin số + SĐT từ chăm sóc lại
```

| Mắt xích | Kỳ này | Mục tiêu demo | Khoảng cách |
|---|---|---|---|
| Inbox mới | 695/ngày | 560/ngày | 🟢 vượt 24% |
| % phản hồi đầu ≤ 5 phút (trong giờ) | 76,6% | ≥ 90% | 🔴 −13,4 điểm |
| **% hội thoại từng có lượt xin số** | **54,2%** | ≥ 70% | 🔴 **−15,8 điểm** |
| Tỷ lệ xin được (ra số ÷ đã xin) | 29,5% | ≥ 50% | 🔴 −20,5 điểm |
| SĐT ra ở cửa sổ 24–48h (nhờ chăm sóc) | 1,0% | +5 điểm % | 🔴 |

★ **Inbox không thiếu. Chỗ rơi nằm ở hai mắt xích giữa.** Và mắt xích rẻ nhất để sửa là *% hội thoại có lượt xin số*: nó không cần thêm người, chỉ cần một mốc bắt buộc trong kịch bản.

### 3.3 Nhóm chỉ số xin số — yếu nhất của kỳ

| Chỉ số | Kỳ này | Mục tiêu demo |
|---|---|---|
| Hội thoại **không có lượt xin số nào** | **956 / 2.086 = 45,8%** | — |
| Xin số lần đầu trước tin NV thứ 5 | 49,2% | ≥ 80% 🔴 |
| Thời gian đến lần xin số đầu (trung vị) | **29,6 phút** | ≤ 5 phút 🔴 |
| Phiên > 15 phút mà **chưa xin số lần nào** | **181 hội thoại** | cờ đỏ 🔴 |
| Số lần xin ở hội thoại chưa ra số (trung vị) | **0,0 lần** | ≥ 2 lần 🔴 |
| Số tin NV đến khi khách cho số (trung vị) | 5,0 tin | ≤ 4 tin 🔴 |

⚠ Một con số đáng để ý: **126 hội thoại ra số mà nhân viên chưa từng xin** — khách tự cho. Nghĩa là tỷ lệ 29,5% *"xin được"* chưa phải toàn bộ năng lực; nhưng cũng nghĩa là có một lượng SĐT đang đến **nhờ may**, không nhờ kịch bản.

⚠ **BOT chỉ xin số ở 8 hội thoại** trong 3 ngày (4 ra số). Lời chào bot hiện gần như không làm việc xin số — đây là một đòn bẩy 🔧 hệ thống chưa dùng.

### 3.4 SLA

| Chỉ số | Kỳ này | Mục tiêu demo | Mẫu |
|---|---|---|---|
| Phản hồi đầu, trong giờ (trung vị) | **1,1 phút** · P75 4,1 phút | ≤ 2 phút | 1.604 🟢 |
| % phản hồi đầu ≤ 5 phút | 76,6% | ≥ 90% | 1.604 🔴 |
| Phản hồi đầu, **ngoài giờ** (trung vị) | **5,9 giờ** | ≤ 15 phút | 470 🔴 |
| Phản hồi giữa hội thoại (trung vị) | 47 giây | ≤ 3 phút | 1.137 🟢 |
| Hội thoại bị bỏ sót (> 30 phút) | 15,0% · 313 HT | ≤ 2% | 🔴 |
| ⤷ **vắt ca** — trả lời chỉ đến sau khi ca đóng | 157 HT | — | 🔧 lỗi xếp ca |
| ⤷ **trong cùng ca** | 111 HT · **5,3%** | ≤ 2% | 🔴 phần quy được cho người trực |
| Chạm lại trong 24h (HT chưa ra số) | 61,7% | ≥ 95% | 🔴 |
| Chạm lại lần 2 trong 48h | 49,1% | ≥ 80% | 🔴 |
| Khách đã từ chối nhưng vẫn ra SĐT | **47,5%** | ≥ 25% | 🟢 (mẫu 40) |

★ **Tách "vắt ca" ra khỏi "bỏ sót" là thay đổi đáng kể**: 15,0% nhìn như thảm họa của người trực, nhưng một nửa (157/313) là khách nhắn lúc gần đóng ca và câu trả lời chỉ đến sáng hôm sau. Đó là việc 🔧 xếp ca, ⛔ không trừ điểm người (`TP-02 §6`).

### 3.5 Ma trận cohort khung giờ

| Khung | Inbox | % | FRT tin đầu (trung vị) | ≤ 2p | ≤ 5p | ≤ 1h ra số | CR24 (mẫu) | CR48 (mẫu) |
|---|---|---|---|---|---|---|---|---|
| 00–06h | 115 | 5,5% | — ngoài giờ | — | — | 2,6% | 16,9% (83) | 21,4% (28) |
| 06–09h | 235 | 11,3% | 3,6 phút | 39,7% | 51,7% | 13,6% | 21,7% (166) | 25,0% (68) |
| 09–12h | 345 | 16,5% | 1,0 phút | 63,8% | 79,6% | 20,3% | 23,2% (224) | 25,0% (80) |
| 12–14h | 212 | 10,2% | 2,0 phút | 50,2% | 65,4% | 20,8% | 25,4% (130) | 27,1% (59) |
| **14–18h** | 444 | 21,3% | **39 giây** | **84,9%** | **98,0%** | **22,1%** | **26,7% (300)** | **34,2% (146)** |
| **18–22h** | **554** | **26,6%** | 1,4 phút | 55,4% | 64,5% | 16,8% | **19,8% (398)** | 24,8% (222) |
| 22–24h | 181 | 8,7% | — ngoài giờ | — | — | 1,7% | 16,7% (126) | 15,8% (76) |

★ **Hai phát hiện rõ nhất của kỳ:**

1. **Khung 18–22h là khung đông nhất (26,6% inbox) nhưng CR24 thấp nhất trong giờ trực (19,8%)**, trong khi khung 14–18h có FRT 39 giây và CR48 34,2%. Chênh **−6,9 điểm CR24** giữa hai khung liền nhau, cùng ngày, cùng page. Theo cách đọc ở `TP-02 §5`: FRT 18–22h vẫn ổn (1,4 phút) nhưng `≤ 1h ra số` tụt xuống 16,8% → **không phải thiếu người, mà là kịch bản/kỹ năng ca tối**.
2. **296 inbox (14,2%) rơi vào 00–06h và 22–24h — khoảng không có người trực**, FRT ngoài giờ trung vị 5,9 giờ, CR48 chỉ 15,8–21,4%. Đây là việc 🔧 hệ thống: xếp ca đêm, hay bot chào + 2 nút hỏi nhanh.

### 3.6 Theo dịch vụ

| Dịch vụ | Giá trị | Inbox | CR48 (mẫu) | Mục tiêu CR48 | % đã xin số |
|---|---|---|---|---|---|
| Mắt | thường | 516 | 29,4% (194) | 40% | 53,1% |
| Da / Trẻ hóa | thường | 516 | 29,8% (141) | 44% | 55,2% |
| Body / Hút mỡ | thường | 349 | **19,3% (114)** | 36% | 59,6% |
| Mũi | thường | 248 | 28,4% (88) | 38% | 62,5% |
| **Hàm mặt** | **cao** | 142 | **14,6% (41)** | 32% | **40,8%** |
| Ngực | cao | 140 | 28,9% (45) | 34% | 54,3% |
| Chưa xếp được | — | 113 | 17,1% (35) | ⚠ chưa có | 37,2% |
| 🔴 **Khác** — chưa có trong danh sách chốt | — | **62** | 23,8% (21) | ⚠ chưa có | 51,6% |

★ **Hàm mặt** là dịch vụ **giá trị cao** mà có **CR48 thấp nhất (14,6%)** và **% đã xin số thấp nhất (40,8%)**. Mẫu 41 nên chỉ ở mức ⚠ *MẪU NHỎ* — nhưng hai con số cùng thấp một hướng thì đáng đưa vào `TUẦN` để xem lại kịch bản, ⛔ chưa đủ để kết luận.

★ **62 inbox nhóm `KHAC`** (tạo hình môi · hút tuyến mồ hôi · vùng kín · triệt lông) không có trong 6 dịch vụ note §3 chốt → 🔴 chặn, xem `TP-04 §4.2`.

### 3.7 Nhân viên — CEI

CR48 team toàn kỳ 25,9% (mẫu 679) · CR24 team 22,1% (mẫu 1.427) → **kỳ ngắn thì đọc CEI24**.

| NV | Inbox | Mẫu 24h | CR24 thực | CR24 kỳ vọng | CEI24 | FRT tin đầu | % đã xin số | Nhãn |
|---|---|---|---|---|---|---|---|---|
| `NV-236425444` | 212 | 159 | 28,3% | 21,8% | **1,30** | 1,2 phút | 53,3% | 🟢 |
| `NV-232258930` | 181 | 120 | 30,0% | 23,1% | **1,30** | 48 giây | 53,6% | 🟢 |
| `NV-262546406` | 61 | 61 | 23,0% | 18,4% | **1,25** | 28,5 phút | 49,2% | 🟢 |
| `NV-264113743` | 163 | 107 | 25,2% | 20,8% | **1,21** | 38 giây | 64,4% | 🟢 |
| `NV-198842558` | 50 | 39 | 25,6% | 22,1% | **1,16** | 5,7 phút | 30,0% | 🟢 |
| … | | | | | | | | |
| `NV-226199192` | 125 | 58 | 10,3% | 21,3% | **0,48** | 2,0 phút | 63,2% | 🔴 |
| `NV-238736928` | 182 | 132 | 14,4% | 23,4% | **0,61** | 1,2 phút | 38,5% | 🔴 |
| `NV-202194914` | 136 | 71 | 14,1% | 20,8% | **0,68** | 37 giây | 76,5% | 🔴 |
| `NV-205107209` | 148 | 109 | 19,3% | 22,7% | **0,85** | 1,3 phút | 35,1% | 🔴 |

★ **CEI làm đúng việc của nó.** Ví dụ rõ nhất: `NV-202194914` có FRT **37 giây** và **76,5% hội thoại đã xin số** — cả hai đều tốt hơn người đứng đầu — nhưng CEI24 chỉ **0,68**. Nghĩa là xin **đúng giờ** và xin **nhiều** nhưng vẫn không ra số → vấn đề nằm ở **nội dung câu xin**, không ở SLA, và đây chính là loại ô mà AI phải đọc ở L2. Ngược lại `NV-262546406` có FRT 28,5 phút (tệ) mà CEI24 = 1,25.

⛔ Bảng này in theo **mã NV**. Cột Nhóm / Hạng QL đều ghi `⚠ thiếu TP-04`. **Không xếp hạng A/B/C** cho tới khi có bản đồ mã → tên → hạng.

### 3.8 Nguồn inbox và quảng cáo

| Nguồn | Inbox | Tỷ lệ SĐT | CR48 (mẫu) | % 1 chiều |
|---|---|---|---|---|
| Từ quảng cáo (`QC`) | 1.954 | 22,7% | 26,7% (643) | 30,2% |
| Vào trực tiếp | 128 | 13,3% | 11,1% (36) | 52,3% |
| Từ bình luận | 4 | 50,0% | — (0) | 100,0% |

Cắt theo **tên quảng cáo** (chỉ quảng cáo có ≥ 30 inbox) — đây là chiều thay cho *Page* mà phương án §4.3 hỏi:

| Quảng cáo | Inbox | CR48 | % 1 chiều |
|---|---|---|---|
| `thương hiệu_Banner đẹp hàn quốc_page bv` | 77 | **62,5%** | 10,4% |
| `QC_Cắt mí_Video cắt mí nam 7,2Tr tối ưu` | 84 | 37,1% | 23,8% |
| `QC_Cắt mí_Banner feedback c Thảo AI` | 86 | 33,3% | 23,3% |
| `nhungtt_lamday_Video Trần Ny…` | 35 | 23,5% | 54,3% |
| `Hut tuyen_Hot hơn hè` | 66 | 22,2% | 40,9% |
| `QC_Cắt mí_Banner bọng mỡ 23-10 - Bản sao_Group_1` | 51 | **13,6%** | 29,4% |
| `Nâng mũi_Video top 5_page bv` | 33 | **10,0%** | 36,4% |
| `Banner chị Loan cấy mỡ_dungnx_caymo - Bản sao` | 36 | **9,1%** | 38,9% |

★ Chênh **62,5% vs 9,1%** giữa hai quảng cáo trong cùng 3 ngày. Và **% hội thoại 1 chiều** đi cùng hướng: quảng cáo CR cao có 10,4% khách nhắn-1-tin-rồi-im, quảng cáo CR thấp có 38–54%. Theo `TP-02 §6` nhóm ①, đây là **chất lượng inbox** → việc của **Performance/Ads**, ⛔ không quy lỗi nhân viên trực page.

### 3.9 Hành trình đến SĐT

| Chỉ số | Trung vị | P75 | Mục tiêu demo |
|---|---|---|---|
| Số tin 2 chiều đến khi khách cho số | 10,0 | 14,0 | ≤ 8 (P75 ≤ 14) 🔴 |
| Thời gian đến khi khách cho số (phút) | **11,1** | 68,4 | ≤ 20 (P75 ≤ 60) 🟢 |
| Độ dài **phiên đầu** — HT ra số | 7,8 phút | — | ≤ 20 🟢 |
| Độ dài **phiên đầu** — HT chưa ra số | 1,8 phút | — | 👁 |
| Số phiên / hội thoại | 2,0 | — | 👁 |
| % SĐT ra ≤ 1h (trong số ra ≤ 24h) | **74,9%** | — | 57% 👁 |
| % thêm ở cửa sổ 24–48h | **1,0%** | — | +5 điểm % 🔴 |
| Khách phản hồi sau tin đầu của NV | 60,6% | — | ≥ 70% 🔴 |
| Hội thoại 1 chiều | **31,7%** | — | ≤ 15% 🔴 (chỉ số của **Ads**) |

★ **Hai con số nói chung một câu:** phiên của hội thoại **ra số** dài 7,8 phút; phiên của hội thoại **chưa ra số** chỉ 1,8 phút. Khách không bỏ đi vì bị tư vấn lâu — khách bỏ đi **trước khi cuộc trò chuyện kịp bắt đầu**. Cộng với *khách phản hồi sau tin đầu của NV = 60,6%*, chỗ rơi lớn nhất là **câu mở đầu + câu thứ hai**.

★ **% thêm ở cửa sổ 24–48h chỉ 1,0%** → chăm sóc lại hiện gần như không đem thêm số nào. Khớp với *chạm lại trong 24h = 61,7%* so mục tiêu 95%.

---

## 4 · Hàng chờ ưu tiên — chạy thật

| Mức | Toàn kỳ | Riêng 05/11 |
|---|---|---|
| `P0` cảnh báo đỏ | 0 | 0 |
| `P1` HOT chưa số, còn cửa sổ 24h | 44 | 34 |
| `P2` khách nhắn cuối, chưa ai trả lời | 51 | 19 |
| `P3` WARM chưa số, cửa sổ còn < 6h | 9 | 8 |
| `P4` đã từ chối, chưa thử cách xin thứ 2 | 14 | 2 |
| `P5` có SĐT, chưa bàn giao Sale | 🔴 **không xuất được** — thiếu tag lead | |
| `P6` inbox lạnh quá 24h | 446 | — |

★ `P0 = 0` là con số **thật**, không phải lỗi. Xem §5.3 về vì sao.

---

## 5 · Ba thứ phải sửa trong code vì dữ liệu thật lộ ra

Ba lỗi này không thấy được khi thiết kế trên giấy; chỉ chạy thật mới lộ.

### 5.1 "HOT chưa số" bằng 0 nếu giữ nguyên 5 tín hiệu KF-60

Tín hiệu ③ của KF-60 là **"đã cho SĐT"**. Nó là *kết quả*, không phải *tín hiệu quan tâm*. Giữ nó trong phép tính thì muốn HOT (≥ 4/5) mà chưa có số là phải đủ **cả 4 tín hiệu còn lại** — gần như không xảy ra.

| Thang | HOT | HOT **chưa số** |
|---|---|---|
| `nhiet_code` — 5 tín hiệu, HOT ≥ 4 | 11 | **0** 🔴 |
| `nhiet_loc` — 4 tín hiệu (bỏ ③), HOT ≥ 2 | 233 | **156** ✅ |

→ Mức ưu tiên `P1` — **đúng cái việc đáng làm nhất của cả hệ** — sẽ rỗng. Code giờ chạy **hai** thang: giữ `nhiet_code` để so với các agent khác dùng KF-60, và dùng `nhiet_loc` để xếp `P1`/`P3`, chọn mẫu, và làm ô cho CEI.

Ngưỡng của `nhiet_loc` chọn theo **độ phân biệt đo được**, ⛔ không chọn cho đẹp:

| Số tín hiệu (bỏ ③) | Inbox | Tỷ lệ SĐT thô |
|---|---|---|
| 0 | 811 | 14,9% |
| 1 | 1.042 | 25,3% |
| 2 | 213 | 31,0% |
| 3 | 20 | 55,0% |

### 5.2 "Độ dài phiên chat" sai 100 lần nếu không cắt phiên

Lần chạy đầu cho *độ dài phiên của hội thoại ra số = **806,8 phút*** (13,4 giờ). Vì phép đo lấy từ tin hai chiều đầu tới tin hai chiều cuối — mà nhiều hội thoại có nhân viên nhắn lại **hôm sau**.

note §0 đã chốt: *phiên đóng khi cả hai phía im > 30 phút*. Sau khi cắt phiên: **7,8 phút** — và mới lộ ra so sánh có nghĩa ở §3.9 (ra số 7,8 phút vs chưa ra số 1,8 phút).

### 5.3 Từ khóa tiếng Việt bỏ dấu — bốn bẫy đã sập

Code khớp từ khóa trên bản **bỏ dấu**, nên nhiều từ khác nghĩa trùng nhau. Bốn trường hợp đo được:

| Từ khóa ban đầu | Trùng với | Hậu quả | Đã xử lý |
|---|---|---|---|
| `kien` (kiện) | **dự kiến** · **Kiên Giang** | 38 hội thoại bị gắn `P0` sai — 100% dương tính giả | bỏ, thay bằng `khoi kien` · `di kien` · `kien ra toa` · `lam don kien` |
| `bao chi` (báo chí) | **bảo chị** · **bảo chỉ** | 3 `P0` sai | bỏ, thay bằng `len bao chi` · `dang bao` |
| `sợ` | bỏ dấu thành `so`, trùng **số** trong *"số điện thoại"* | rào cản `SO_BIEN_CHUNG` bị phồng | bỏ, thay bằng `so dau` · `so bi` · `so hong` · `so xau` |
| `nam` (nám) · `tham` (thâm) | **năm** · **nam** · **tham khảo** | xếp dịch vụ sai sang `DA_TRE_HOA` | bỏ, thay bằng `tri nam` · `bi nam` · `nam da` · `vet tham` |

★ Và một thay đổi về **thiết kế**, không chỉ về từ: `canh_bao_do` giờ chia **hai tầng**.

> *"Có trường hợp nào biến chứng khi dùng dịch vụ này ko ah"* — đây là **rào cản trước mổ**, ⛔ không phải khiếu nại. Code không phân biệt được hai cái đó.

→ Tầng `chac` (cụm chỉ xuất hiện trong khiếu nại thật) vào thẳng `P0`. Tầng `nghi` (*biến chứng* · *nhiễm trùng* · *hoàn tiền* · *không hài lòng*) ⛔ **không** vào `P0`, chỉ **buộc** hội thoại đó vào mẫu AI đọc. Sau khi sửa: `P0 = 0` trong cả 3 ngày — và đó là con số đúng.

---

## 6 · 🔴 Chín khoản đang chặn

| # | Chặn gì | Chặn chỉ số / đầu ra nào | Ai mở |
|---|---|---|---|
| 1 | **Bản đồ 40 mã NV → tên · nhóm · hạng** | bảng Nhóm · xếp hạng A/B/C · luật chia inbox · giáo án theo nhóm | QL trực page |
| 2 | **Bảng phân ca theo khung giờ** | cột *Số NV* của ma trận cohort · trần tải/ca · câu *"khung này thiếu người"* | QL ca |
| 3 | **Giờ trực chính thức** (3 con số đang xung đột) | mẫu số của **toàn bộ** SLA | Anh / QL |
| 4 | **Số chi quảng cáo** | Chi phí/SĐT · mốc realtime 13h theo % mục tiêu ngày | Performance |
| 5 | **Trường thị trường / tỉnh thành** | toàn bộ mục 4 của note — hiện phủ 10,4% | Caresoft / QL |
| 6 | **Tag bàn giao / lead** | mức ưu tiên `P5` | Caresoft / Sale |
| 7 | **62 inbox nhóm `KHAC`** chưa có trong danh sách dịch vụ chốt | mục tiêu CR của nhóm này | QL |
| 8 | **Bản xuất nhiều page** | chiều cắt theo Page — hiện chỉ 1 page | Caresoft |
| 9 | **Đóng dấu *chốt*** cho `tools/muc-tieu.json` | mọi cờ 🟢🟡🔴 hiện chỉ để tham khảo | Anh / QL |

Thêm hai khoản **không mở được bằng dữ liệu**, phải đổi cách xuất:

- **SĐT đã bị che thành `[SĐT ẩn]`** → ⛔ không đo được *tỷ lệ SĐT hợp lệ ≥ 92%* (note §6), ⛔ không khử trùng khách theo số.
- **Chưa có lịch sử 30 ngày** → ⛔ không tách *inbox mới* vs *khách cũ quay lại*, ⛔ không đo *tái khai thác inbox cũ 3–30 ngày*.

---

## 7 · ⚠ Một cảnh báo về bản xuất

Bộ che của Caresoft **hở ở ba chỗ** (chi tiết `TP-03 §3`):

1. **21 tên khách thật lọt qua** ở dòng `**HT:** <tên> đã trả lời một quảng cáo.` — 21/1.847 ≈ 1,1%.
2. Có chỗ tên **khách** bị che thành `[tên NV]` → ⛔ không dùng nhãn này để suy ai là nhân viên.
3. **60 hội thoại** có nhân viên nhắc lại một SĐT mà khách **chưa từng gửi trong hội thoại** → số đến từ kênh khác (gọi, Zalo, form). Cột `nv_co_sdt_ma_kh_khong` ghi lại, ⛔ không tính vào SĐT thô.

→ ⛔ **Không commit `du-lieu/` và `out/`.** `.gitignore` đã chặn. Repo này public.

---

## 8 · Cách chạy lại y hệt

```bash
python tools/tp.py kiem    "du-lieu/Bệnh viện thẩm mỹ Kangnam_20261103-20261105.txt"
python tools/tp.py tinh    "du-lieu/Bệnh viện thẩm mỹ Kangnam_20261103-20261105.txt"
python tools/tp.py bao-cao --ky 03-11_05-11-2026
python tools/tp.py viec    "du-lieu/Bệnh viện thẩm mỹ Kangnam_20261103-20261105.txt" --ngay 05/11
python tools/tp.py mau     "du-lieu/Bệnh viện thẩm mỹ Kangnam_20261103-20261105.txt" --n 120
```

Kết quả: `out/03-11_05-11-2026/` gồm `ht.csv` (2.087 dòng × 75 cột) · `so.json` · `bao-cao.md` (10 mục) · `viec-0511.csv` · `mau-ai.md` (135 hội thoại), và `out/lich-su.csv` (3 dòng ngày).
