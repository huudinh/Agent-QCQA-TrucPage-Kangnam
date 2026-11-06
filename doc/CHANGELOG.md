# CHANGELOG

## v1.0 · 06/11/2026 — bản đầu, đã kiểm chứng trên dữ liệu thật

**Nguồn thiết kế:** `doc/phuong-an-ai-qcqa-truc-page-daily-kangnam.md` (06/11/2026) và `doc/note-chot-muc-tieu-truc-page.md` (bản `demo-1`, kỳ 11/2026).
**Dữ liệu kiểm chứng:** `Bệnh viện thẩm mỹ Kangnam_20261103-20261105.txt` — 2.087 hội thoại · 03–05/11/2026.

### Thêm mới

- `tools/tp.py` — lớp L0 + L1. Năm lệnh: `kiem` · `tinh` · `bao-cao` · `viec` · `mau`.
  Tính **75 cột** cho từng hội thoại, gộp theo **8 chiều cắt**, xuất `bao-cao.md` 10 mục.
- `tools/tu_dien.json` — từ điển khớp từ khóa: 7 nhóm dịch vụ · xin số · từ chối · 7 rào cản · 3 tín hiệu nóng · cảnh báo đỏ **hai tầng** · lọc spam · thị trường.
- `tools/muc-tieu.json` — toàn bộ mục tiêu và ngưỡng từ note, mỗi mục có `trang_thai`. ⚠ Tất cả còn `demo`.
- `tools/master-nv.json` + `.mau.json` — TP-04, đã dò sẵn **40 mã NV** thật kèm số hội thoại từng mã giữ vai chính. 🔴 Chưa điền tên/nhóm/hạng.
- 7 sổ tri thức `knowledge/TP-01 … TP-07`.
- 5 prompt mẫu `prompts/`.
- `SYSTEM-PROMPT.md` (11.196 ký tự) · `SYSTEM-PROMPT-NGAN.md` (6.373 ký tự, vừa trần 8.000 của ChatGPT).
- `doc/04-kiem-chung-du-lieu-that.md` — toàn bộ số của lần chạy thật.

### Ba quyết định thiết kế khác phương án gốc — và vì sao

| # | Phương án gốc | Bản này làm | Vì sao |
|---|---|---|---|
| ① | Một thang nhiệt KF-60, 5 tín hiệu, HOT ≥ 4 | **Hai thang**: `nhiet_code` (giữ nguyên KF-60) + `nhiet_loc` (4 tín hiệu, **bỏ ③ "đã cho SĐT"**, HOT ≥ 2) | Tín hiệu ③ là *kết quả*, không phải *tín hiệu quan tâm*. Giữ nó thì mức ưu tiên `P1` — "HOT chưa số" — **rỗng**: đo thật trên 2.086 hội thoại cho **0**. Bộ `nhiet_loc` cho **156**. Ngưỡng chọn theo độ phân biệt đo được (CR thô 14,9% → 25,3% → 31,0% → 55,0% theo số tín hiệu) |
| ② | "Hot chưa số tồn" là một chỉ số | Thêm **CEI24** cạnh CEI48, và nói rõ **kỳ ngắn thì đọc CEI24** | Luật so công bằng + kỳ 3 ngày → chỉ 679 inbox đủ 48h so với 1.427 đủ 24h. CEI48 trên mẫu đó không đủ sức phân biệt |
| ③ | "Hội thoại bị bỏ sót > 30 phút ≤ 2%" | Tách **`bo_sot_vat_ca`** (khách nhắn còn trong giờ, trả lời chỉ đến sau khi ca đóng) ra khỏi `bo_sot_trong_ca` | Đo thật: 313 bỏ sót, trong đó **157 là vắt ca**. Gộp chung thì con số 15,0% nhìn như lỗi người trực, trong khi phần quy được cho người chỉ là **5,3%**. Luật ⑨ *"lỗi hệ không trừ điểm người"* đòi phải tách |

### Hai lỗi phát hiện khi chạy thật và đã sửa

| Lỗi | Biểu hiện | Sửa |
|---|---|---|
| Không cắt phiên chat | *"Độ dài phiên của hội thoại ra số"* ra **806,8 phút** vì nhiều hội thoại có NV nhắn lại hôm sau | Cắt phiên theo note §0 (im > 30 phút là đóng phiên) → **7,8 phút**. Lộ ra so sánh có nghĩa: ra số 7,8 phút vs chưa ra số **1,8 phút** |
| Từ khóa tiếng Việt bỏ dấu trùng nghĩa | `kien` trùng *dự kiến* / *Kiên Giang* → **38 `P0` sai (100% dương tính giả)** · `bao chi` trùng *bảo chị* → 3 `P0` sai · `sợ` → `so` trùng *số* trong "số điện thoại" → rào cản `SO_BIEN_CHUNG` phồng · `nam`/`tham` trùng *năm* / *tham khảo* → xếp dịch vụ sai | Thay bằng cụm dài (`khoi kien` · `len bao chi` · `so dau` · `tri nam` · `vet tham`). Và chia `canh_bao_do` thành hai tầng: `chac` → `P0`, `nghi` → ⛔ không vào `P0`, chỉ **buộc** vào mẫu AI đọc |

### Năm câu hỏi còn mở trong phương án — đã trả lời

| Câu hỏi | Trả lời |
|---|---|
| §4.3 *"Có nên phân tích theo page không?"* | **Có, nhưng bản xuất chỉ có 1 page.** Thay tạm bằng chiều cắt theo **tên quảng cáo** — và nó đã cho kết quả: chênh **CR48 62,5% vs 9,1%** giữa hai quảng cáo trong cùng 3 ngày |
| §7.2 *"Lọc hội thoại WIN bằng code được không? Tránh để AI tự chọn."* | **Được, và đang làm thế.** `tp.py mau` chọn theo tầng `nhiệt × ra số`, trải đều theo dịch vụ × khung giờ, và **buộc** mọi hội thoại có cờ cảnh báo vào mẫu |
| §7.3 *"Xếp lỗi Fail — code làm được không? Nếu được thì lọc 100%, không cần lấy mẫu."* | **Một nửa.** Nhóm nguyên nhân ③④⑥ đã có số trên **toàn bộ** 2.086 hội thoại → ⛔ không cần lấy mẫu. Riêng nhóm ⑤ (kỹ năng XLTC — *"xử lý rào cản có đúng mẫu không"*) phải đọc |
| §1 *"Chia theo khung giờ, bao gồm cả SLA: 8h00–21h30"* | ⚠ **Ba con số đang xung đột.** Bản xuất Caresoft tự khai giờ trực là **08:30–22:00** (đối chiếu từ 578 lượt có cờ `ngoài giờ`). `tp.py` theo Caresoft; cần chốt lại |
| §4.1 *"Ưu tiên trường SĐT của Caresoft nếu có"* | ⛔ **Không có.** SĐT đã bị che thành `[SĐT ẩn]` → đếm bằng sự có mặt của mã che trong tin **của khách**, và ⛔ không đo được *tỷ lệ SĐT hợp lệ* |

### 🔴 Chín khoản đang chặn

Xem `README.md` và `TP-04 §6`. Tóm: bản đồ 40 mã NV → tên/nhóm/hạng · bảng phân ca · giờ trực chính thức · số chi quảng cáo · trường thị trường · tag bàn giao lead · 62 inbox nhóm `KHAC` · bản xuất nhiều page · đóng dấu `chot` cho `muc-tieu.json`.

### Việc của bản sau

- [ ] Nạp đủ 14 ngày để bật cột *cùng thứ tuần trước* và *7 ngày vs 7 ngày trước*
- [ ] Đọc lại cột **Kết quả** của bảng *Việc hôm nay* → mở điểm tuần thang 100 và *tỷ lệ cứu được*
- [ ] Hiệu chỉnh ngưỡng `nhiet_loc` và `Q5.3` sau 2 tuần chạy (`TP-05 §5`)
- [ ] Đối chiếu hạng theo rubric với hạng QL — ma trận hiệu chỉnh `TP-02 §7`
