# TP-02 · CORE chỉ số

> Sổ định nghĩa. ⛔ Không nêu một chỉ số nào mà không khớp định nghĩa ở đây.
> Mọi ngưỡng đọc từ `tools/muc-tieu.json`. ⚠ Toàn bộ ngưỡng hiện ở trạng thái `demo` — **chưa ai chốt**.

---

## 1 · Chỉ số gốc

```
CR48 = SĐT thô mới xin được trong 48h ÷ inbox mới (đã đủ 48h)
```

Mọi chỉ số khác trong sổ này tồn tại để giải thích **vì sao CR48 tăng hay giảm**. Nếu một chỉ số không trả lời được câu đó, nó là chỉ số theo dõi (`👁`), ⛔ không phải chỉ số đánh giá.

---

## 2 · Định nghĩa chuẩn

| Chỉ số | Định nghĩa dùng trong code | Cột trong `ht.csv` |
|---|---|---|
| **Inbox mới** | Một hội thoại có **ít nhất một tin của khách** trong kỳ. Loại: tuyển dụng, đối tác, rác (`tu_dien.json › spam_loai_tru`) và hội thoại không có tin khách nào | `hop_le`, `loai_tru` |
| **SĐT thô** | Có **ít nhất một tin của KHÁCH** chứa `[SĐT ẩn]`. Mỗi hội thoại tính **1 lần** | `co_sdt`, `t_sdt` |
| **CR24 / CR48** | Inbox ra SĐT trong 24h/48h **kể từ tin đầu tiên của khách** ÷ inbox đã đủ 24h/48h | `sdt_24h`, `sdt_48h`, `du_24h`, `du_48h` |
| **FRT tin đầu** | Khoảng từ **tin đầu tiên của khách** tới **tin đầu tiên của người** (⛔ không tính BOT). Chỉ tính khi tin của khách rơi **trong giờ trực** | `frt_dau_giay` |
| **FRT ngoài giờ** | Cùng phép tính, nhưng tin của khách rơi **ngoài giờ trực** → đếm riêng, ⛔ không gộp vào SLA | `frt_dau_ngoai_gio_giay` |
| **FRT giữa hội thoại** | Trung vị các lượt chờ **từ lượt thứ 2 trở đi** | `frt_giua_tv_giay` |
| **Bỏ sót** | Một lượt chờ **trong giờ** kéo quá 30 phút, hoặc không ai trả lời đến hết kỳ | `bo_sot` |
| **Bỏ sót vắt ca** | Khách nhắn khi còn trong giờ, nhưng câu trả lời chỉ đến **sau khi ca đóng** → 🔧 lỗi **xếp ca** | `bo_sot_vat_ca` |
| **Đã xin số** | Có ít nhất một tin **của người** khớp `tu_dien.json › xin_so` (⛔ không tính tin BOT) | `da_xin_so`, `so_lan_xin` |
| **Tỷ lệ xin được** | Ra số ÷ đã xin số | — |
| **Chạm lại** | Một tin của người gửi khi khách đang im **> 30 phút** và đã có người trả lời trước đó → tức là người **chủ động** nhắn | `so_lan_cham_lai`, `cham_lai_24h` |
| **Phiên chat** | Khối tin hai chiều liền nhau; phiên **đóng** khi cả hai phía im > 30 phút. `phien_phut` = độ dài **phiên đầu** (phiên đi xin số) | `so_phien`, `phien_phut`, `phien_dai_nhat_phut` |
| **Hội thoại 1 chiều** | Khách nhắn **đúng 1 tin** rồi im, dù người đã trả lời. ★ Đây là chỉ số của **Ads**, ⛔ không trừ điểm người trực | `mot_chieu` |
| **CEI** | CR thực tế của NV ÷ CR kỳ vọng. Kỳ vọng = CR của **team** ở từng ô `dịch vụ × nhiệt(lọc) × khung giờ`, cộng theo số inbox người đó nhận ở mỗi ô | `so.json › cei24`, `cei48` |

### 2.1 ⚠ Hai thang nhiệt — biết rõ cái nào dùng để làm gì

| Thang | Tín hiệu | Dùng để |
|---|---|---|
| `nhiet_code` | 5 tín hiệu KF-60: ① nêu dịch vụ/tình trạng ② mốc thời gian ≤ 14 ngày ③ **đã cho SĐT** ④ hỏi điều kiện thực hiện ⑤ đồng ý khung giờ gọi. HOT ≥ 4 · WARM 2–3 · COLD 0–1 | giữ đúng KF-60 để so được với các agent khác |
| `nhiet_loc` ★ | 4 tín hiệu — **bỏ ③** — HOT ≥ 2 · WARM 1 · COLD 0 | xếp ưu tiên `P1`/`P3` và **chọn mẫu cho AI đọc** |

⛔ **Vì sao phải có `nhiet_loc`:** tín hiệu ③ là *kết quả*, không phải *tín hiệu quan tâm*. Giữ nó trong phép tính thì "HOT **chưa** số" gần như không tồn tại — muốn HOT phải có 4/5 tín hiệu, thiếu ③ là phải đủ cả 4 cái còn lại. Đo trên kỳ 03–05/11/2026: `nhiet_code` cho **0** hội thoại "HOT chưa số", tức là mức ưu tiên `P1` — **đúng cái việc đáng làm nhất** — sẽ rỗng. Cùng kỳ đó, `nhiet_loc` cho **140**.

⛔ **Và vì sao ô CEI dùng `nhiet_loc`, không dùng `nhiet_code`:** `nhiet_code` có ③ "đã cho SĐT" nên lấy nó làm ô là đưa **kết quả vào mẫu số kỳ vọng** — CEI sẽ luôn xấp xỉ 1 và mất hết ý nghĩa.

★ Cả hai thang đều là **bộ lọc từ khóa**. ⛔ Chúng KHÔNG phải điểm KF-60. Điểm KF-60 chính thức do **AI** chấm ở lớp L2.

---

## 3 · ★ Luật "so công bằng" và luật "chốt / tạm"

### 3.1 So công bằng

Mẫu số CR24 chỉ gồm inbox **đã đủ 24h** kể từ tin đầu của khách; CR48 chỉ gồm inbox **đã đủ 48h**. Mốc chặn là **00:00 ngày sau ngày cuối kỳ** — sau mốc đó không còn tin của khách trong file, nên tính vào là **chắc chắn sai thấp**.

Inbox chưa đủ giờ **không vào tỷ lệ**; chúng hiện riêng ở cột *Chưa đủ 24h / Chưa đủ 48h*.

### 3.2 Chốt / tạm

File 8:30 chỉ có tin đến hết D-1. Báo cáo sáng ngày D:

| Số | Trạng thái | Cho inbox ngày |
|---|---|---|
| CR24 | **chốt** | D-2 |
| CR48 | **chốt** | D-3 |
| CR24 / CR48 | **tạm** | D-1 |

⛔ Không đánh giá nhân viên bằng số **tạm**.

### 3.3 ⚠ Hệ quả khi kỳ ngắn

Một bản xuất 3 ngày (ví dụ 03–05/11) cho:

- CR48 **chốt** chỉ cho ngày đầu → mẫu nhỏ hơn CR24 khoảng một nửa.
- → **Trong kỳ ngắn, đọc CEI24, ⛔ không đọc CEI48.** Đo trên kỳ 03–05/11/2026: mẫu đủ 48h = 679 HT, mẫu đủ 24h = 1.427 HT.

---

## 4 · So sánh kỳ — mọi bảng có 3 cột so

| So với | Dùng để |
|---|---|
| Ngày trước | Phát hiện sự cố ngay |
| Cùng thứ tuần trước | Loại ảnh hưởng thứ trong tuần — cuối tuần inbox khác hẳn |
| 7 ngày gần nhất vs 7 ngày trước đó | Xu hướng thật, bỏ nhiễu ngày |

Lịch sử nằm ở `out/lich-su.csv`, mỗi dòng một ngày. Kỳ nào chưa có mốc thì ghi `⚠ chưa có mốc so sánh`, ⛔ không tự đặt mốc.

**Chiều cắt:** Nhóm · Nhân viên · Dịch vụ · Page · Thị trường · Khung giờ.

| Chiều | Trạng thái trên dữ liệu thật |
|---|---|
| Khung giờ · Dịch vụ · Nhân viên (mã) | ✅ chạy được |
| Nguồn inbox (QC / comment / trực tiếp) | ✅ chạy được |
| Nhóm · Hạng A/B/C | 🔴 chờ `TP-04` |
| Page | 🔴 bản xuất chỉ có **1 page** → chiều cắt rỗng |
| Thị trường | 🔴 bản xuất **không có trường này**, suy từ chữ khách, độ phủ ~10% → ⛔ không dùng để đánh giá |

### Ngưỡng RAG

| Mức | Điều kiện | Cờ |
|---|---|---|
| Đạt | ≥ 100% mục tiêu | 🟢 |
| Cảnh báo | 85–99% | 🟡 |
| Không đạt | < 85% | 🔴 |

Thêm ba luật cảnh báo: giảm > 10% so cùng kỳ → 🔴 · inbox tăng ≥ 15% mà SĐT không tăng → kiểm **chất lượng inbox** (việc của Ads) · CP/SĐT tăng > 15% → báo Ads.

---

## 5 · Ma trận cohort khung giờ

Dòng = khung giờ **tin đầu của khách**. Cột = % đã ra số sau mốc. Bộ khung mặc định theo note §5: `00–06 · 06–09 · 09–12 · 12–14 · 14–18 · 18–22 · 22–24`. Bộ 9 khung của phương án §4.3 chạy bằng `--khung pa`.

**Cách đọc:**

| Thấy gì | Nghĩa | Việc của ai |
|---|---|---|
| FRT cao **+** `≤1h ra số` thấp | **thiếu người ca đó** | QL ca — xếp lại ca |
| FRT tốt **mà** `≤24h` vẫn thấp | **lỗi kịch bản / kỹ năng** | Trực page — `TP-05`, `TP-07` |
| Khoảng cách `≤24h → ≤48h` **lớn** | chăm sóc lại **đang có tác dụng** → nhân rộng | QL trực page |
| Khung giờ có FRT = `—` | cả khung nằm ngoài giờ trực | 🔧 việc hệ thống: bot chào + 2 nút hỏi nhanh |

---

## 6 · Phân rã nguyên nhân — thứ tự cố định

```
SĐT = Inbox mới × % phản hồi đúng SLA × Tỷ lệ xin số + SĐT từ chăm sóc lại
```

★ **Loại nguyên nhân ngoài trực page TRƯỚC**, rồi mới quy lỗi cho quy trình, kịch bản, kỹ năng.

| # | Nhóm nguyên nhân | Tín hiệu đo | Ngưỡng nghi vấn (⚠ tạm) | Ai chịu |
|---|---|---|---|---|
| 1 | **Chất lượng inbox** | % COLD · % hội thoại 1 chiều · % chỉ hỏi giá · CR theo tên quảng cáo | % WARM+HOT giảm ≥ 15% so 7 ngày · 1 chiều > 15% | Performance / Ads — ⛔ không quy lỗi NV |
| 2 | **Phân bổ inbox** | Inbox/NV/ca so trần tải · % HOT giao cho hạng C | Hạng C nhận > 25% HOT · NV vượt 1,3× tải TB ca | QL ca |
| 3 | **Quy trình (SLA)** | FRT · % trong SLA · khoảng lặng · bỏ sót · bỏ sót vắt ca | FRT trung vị > 5 phút giờ hành chính · > 15 phút ngoài giờ | QL ca + 🔧 hệ thống |
| 4 | **Kịch bản** | % đã xin số · lượt NV thứ mấy khi xin · thời gian đến lần xin đầu | % đã xin số < 70% · xin sau lượt 6 | Trực page |
| 5 | **Kỹ năng XLTC** | AI chấm `TP-05`: gặp từ chối có xử lý đúng mẫu không · báo giá trần trụi · trả lời dài rập khuôn | Tỷ lệ xin được < 50% khi đã xin · ≥ 2 lỗi XLTC/10 HT | Trực page + coaching |
| 6 | **Chăm sóc, tái khai thác** | % chưa số được nhắn lại trong 24h · SĐT ra ở cửa sổ 24–48h | < 60% WARM chưa số được nhắn lại trong 24h | Trực page |

**Đầu ra chẩn đoán mỗi ngày:** tối đa **3 vấn đề**, mỗi vấn đề gồm ① một con số (kèm mẫu) ② nhóm nguyên nhân ③ người chịu trách nhiệm ④ việc cụ thể có hạn giờ ⑤ 1–2 `HT-xxxxxxxx` làm bằng ⑥ **quy mô lỗi / tổng hội thoại nhận**.

### ★ Luật "lỗi hệ không trừ điểm người"

Ba thứ sau **luôn** đi vào mục 🔧 VIỆC HỆ THỐNG, ⛔ không trừ điểm người trực:

1. Inbox đến **ngoài giờ trực** → FRT ghi `—`.
2. **Bỏ sót vắt ca** — khách nhắn còn trong giờ, câu trả lời chỉ đến sau khi ca đóng.
3. Hội thoại **1 chiều** — khách nhắn 1 tin rồi im.

---

## 7 · Điểm tuần thang 100

⚠ Hai bộ trọng số đang xung đột. `tools/muc-tieu.json` dùng bộ của **note §9** vì note là văn bản chốt; bộ của phương án §7.1 giữ lại để đối chiếu.

| Thành phần | note §9 (đang dùng) | phương án §7.1 |
|---|---|---|
| Chỉ số SĐT — ★ tính bằng **CEI**, ⛔ không bằng CR thô | 50% | 50% (CEI) |
| SLA phản hồi & xin số | 20% | 20% |
| Điểm QC — rubric `TP-05` | 20% | 20% |
| Chăm sóc & tái khai thác / tỷ lệ cứu được | 10% | 10% (tỷ lệ cứu được) |
| **Ngưỡng hạng** | A ≥ 90 · B 75–89 · C < 75 | A ≥ 75 · B 55–74 · C < 55 |

🔴 **Bảng điểm tuần hiện CHƯA chạy được.** Thiếu ba thứ:

1. `TP-04` — bản đồ mã NV → tên · nhóm · hạng.
2. Điểm rubric `TP-05` — việc của AI ở lớp L2, phải chấm xong mới có.
3. Cột **Kết quả** của bảng *Việc hôm nay* hôm trước — để tính *tỷ lệ cứu được*.

### Ma trận hiệu chỉnh tuần 1–2

So hạng theo dữ liệu với hạng QL cung cấp:

- ≥ 80% khớp → rubric đáng tin.
- Một bạn **A theo QL mà CEI < 0,9** → kiểm bạn đó có đang được chia inbox ngon không.
- Một bạn **C theo QL mà CEI ≥ 1,1** → khả năng bị giao inbox khó → xem lại luật chia.

---

## 8 · Những gì KHÔNG đo được trên bản xuất hiện tại

| Chỉ số trong note | Vì sao không đo được |
|---|---|
| Chi phí/SĐT · Mốc realtime 13h theo % mục tiêu ngày | Bản xuất hội thoại ⛔ không có số chi quảng cáo |
| Tỷ lệ SĐT **hợp lệ** (đúng đầu số) | SĐT đã bị che thành `[SĐT ẩn]` — ⛔ không còn chữ số để kiểm |
| SĐT khách cũ quay lại · Tái khai thác inbox cũ 3–30 ngày | ⛔ Chưa có lịch sử 30 ngày |
| Thị trường (Bắc / Nam / Quốc tế) | ⛔ Không có trường này; suy từ chữ khách → độ phủ ~10% |
| Page → dịch vụ | Bản xuất chỉ có **1 page** |
| P5 — có SĐT mà chưa bàn giao Sale | ⛔ Không có tag bàn giao / lead |
| Tin chỉ có sticker / like | Bản xuất gộp thành `[Hình ảnh/Video/Đính kèm]` |
| Số NV trực theo từng khung giờ | ⛔ Không có bảng phân ca |

⛔ Thấy một chỉ số trong bảng này thì ghi `—` kèm lý do, ⛔ không ước lượng, ⛔ không lấy số khác gán sang.
