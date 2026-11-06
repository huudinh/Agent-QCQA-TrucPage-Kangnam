# TP-04 · Master data

> 🔴 **SỔ NÀY CHƯA ĐƯỢC ĐIỀN.** Nó là **thứ duy nhất** đang chặn bốn đầu ra của hệ.
> File máy đọc: `tools/master-nv.json` (bản thật, ⛔ không commit) · `tools/master-nv.mau.json` (bản mẫu).

---

## 1 · Vì sao sổ này chặn

| Đầu ra | Chặn vì |
|---|---|
| Bảng theo **Nhóm** | không biết mã NV nào thuộc nhóm nào |
| **Xếp hạng A/B/C** theo tuần | không biết hạng QL để đối chiếu, không biết tên để gửi trang riêng |
| **Luật chia inbox** (trần tải/ca · hạng C nhận ≤ 20% dịch vụ giá trị cao) | không biết hạng, không có bảng phân ca |
| **Giáo án coaching** theo nhóm | không biết ai kèm ai |

★ Những đầu ra **không** bị chặn, chạy ngay được: toàn bộ chỉ số theo ngày · khung giờ · dịch vụ · **từng mã NV** · CEI · hàng chờ P0–P6 · mẫu cho AI đọc.

---

## 2 · 🔴 Khoản chặn số 1 — bản đồ mã NV → tên

Bản xuất 03–05/11/2026 có **40 mã NV**. Phương án §7.1 cho **16 tên** do QL phân hạng:

| Nhóm (QL đánh giá) | Nhân viên |
|---|---|
| A | Hải Anh · Kiều Hương · Liên · Thắm · Nhi · Hoa |
| B | Mai · Ngọc · Hoài Linh · Đặng Hương · Thành · Lương · Thùy Linh |
| C | Tuyết Nhi · Mỹ Linh · Mỹ Chung |

⚠ **40 ≠ 16.** Không có cách nào ghép tên với mã từ dữ liệu: bản xuất che tên nhân viên thành `[tên NV]`, và chỗ che còn bị nhầm nhãn (`TP-03 §3`). ⛔ Agent **không** tự ghép, ⛔ không đoán theo khối lượng.

Trong 40 mã: **31 mã** từng giữ vai trò chính ở ít nhất một hội thoại; **17 mã** có ≥ 10 hội thoại (đủ mẫu để phân loại); 9 mã chỉ xuất hiện như người trả lời phụ.

**Cần QL điền** — mỗi dòng một mã, lấy từ Caresoft › Quản lý người dùng:

```json
"NV-236425444": { "ten": "<tên thật>", "nhom": "Nhóm 2", "hang": "A" }
```

Số hội thoại từng mã giữ vai chính trong kỳ đã được ghi sẵn ở trường `ht_lam_chinh` của `tools/master-nv.json` để QL dễ nhận ra ai là ai.

---

## 3 · 🔴 Khoản chặn số 2 — bảng phân ca

Cần: mỗi khung giờ có bao nhiêu người trực, gồm những mã nào.

Dùng để: điền cột *Số NV* của ma trận cohort · tính **tải/ca** · nói được câu *"khung này FRT cao vì thiếu người"* thay vì chỉ *"khung này FRT cao"*.

Khung giờ cần phủ (⚠ hai khung dưới đây hiện **ngoài giờ trực**, cần biết có ai trực không):

| Khung | Inbox trong kỳ | FRT đo được |
|---|---|---|
| 00–06h | 115 (5,5%) | `—` ngoài giờ |
| 22–24h | 181 (8,7%) | `—` ngoài giờ |

→ **296 inbox (14,2%) rơi vào khoảng không có người trực.** Đây là việc 🔧 hệ thống, cần quyết định: xếp ca đêm, hay bot chào + 2 nút hỏi nhanh.

---

## 4 · 🔴 Khoản chặn số 3 — page → dịch vụ, và danh sách dịch vụ

### 4.1 Page

Bản xuất chỉ có **1 page**: `Bệnh viện thẩm mỹ Kangnam`. note §3 hỏi *"1 page = 1 dịch vụ?"* — với bản xuất này câu hỏi chưa trả lời được.

**Cần:** danh sách page đang chạy + mapping page → dịch vụ, và bản xuất gộp nhiều page.

### 4.2 Dịch vụ

note §3 chốt **6** dịch vụ. Dữ liệu thật cho thấy **thiếu ít nhất một nhóm**:

| Mã | Tên (note §3) | Inbox kỳ 03–05/11 | Trạng thái |
|---|---|---|---|
| `MAT` | Mắt | 516 | ✅ |
| `DA_TRE_HOA` | Da / Trẻ hóa | 516 | ✅ |
| `BODY` | Body / Hút mỡ | 349 | ✅ |
| `MUI` | Mũi | 248 | ✅ |
| `HAM_MAT` | Hàm mặt | 142 | ✅ |
| `NGUC` | Ngực | 140 | ✅ |
| `KHAC` | — | **62** | 🔴 **chưa có trong danh sách chốt** |
| `KHONG_XAC_DINH` | — | 113 | ⚠ khách chưa nói đủ để biết hỏi về gì |

**`KHAC` gồm gì:** tạo hình môi · hút tuyến mồ hôi / hôi nách (`Endo dry`) · vùng kín · triệt lông. Riêng *hút tuyến mồ hôi* đã có quảng cáo chạy mạnh (`Hut tuyen_Hot hơn hè` — 68 inbox trong 3 ngày).

**Cần quyết:** 62 inbox này xếp vào dịch vụ nào, hay mở thêm dòng trong note §3. Và mục tiêu CR24/CR48 của chúng là bao nhiêu.

### 4.3 Dịch vụ giá trị cao

Hiện `tools/tu_dien.json › dich_vu_gia_tri_cao` đặt `HAM_MAT · NGUC · MUI`, suy từ phương án §6.1 (*"PTTM, Giảm béo, Nha khoa"*) và note §3 (cột *Giá trị*). ⚠ Hai nguồn không khớp nhau — **cần chốt**, vì nó quyết định thứ tự xếp việc trong cùng mức ưu tiên và trần *"hạng C nhận ≤ 20% giá trị cao"*.

---

## 5 · Cấu trúc nhóm — chờ xác nhận

note §8 đưa cơ cấu mẫu 3 nhóm × 12 người. ⚠ Bản xuất có 40 mã → cơ cấu thật khác bản mẫu.

| Nhóm | Dịch vụ phụ trách (note §8) | Trần inbox/ngày theo hạng |
|---|---|---|
| Nhóm 1 | Hàm mặt · Ngực | A ≤ 80 · B ≤ 65 · C ≤ 50 |
| Nhóm 2 | Mắt · Mũi | như trên |
| Nhóm 3 | Body · Da | như trên |

⚠ Đo trên kỳ thật: mã nhận nhiều nhất là **212 hội thoại/3 ngày ≈ 71/ngày** — còn dưới trần hạng A, nhưng **vượt trần hạng C (50)** nếu mã đó là hạng C. ⛔ Chưa biết hạng nên chưa kết luận được. Đây chính là lý do `TP-04` chặn.

---

## 6 · Checklist để mở chặn

- [ ] Bản đồ **40 mã NV → tên · nhóm · hạng** → điền `tools/master-nv.json`
- [ ] **Bảng phân ca** theo khung giờ (gồm 00–06h và 22–24h: có ai trực không?)
- [ ] Chốt **giờ trực**: 08:00–21:30 · 08–22h · hay 08:30–22:00 → `muc-tieu.json › dinh_nghia.gio_truc`
- [ ] Quyết **62 inbox nhóm `KHAC`** xếp vào đâu, mục tiêu CR bao nhiêu
- [ ] Chốt danh sách **dịch vụ giá trị cao**
- [ ] Danh sách **page** + mapping page → dịch vụ, và xin bản xuất gộp nhiều page
- [ ] Chốt **cách xác định thị trường**: theo page · theo tag · hay thêm trường vào Caresoft
- [ ] Xin Caresoft bổ sung **tag bàn giao / lead** để mở mức ưu tiên P5
- [ ] Đóng dấu **chốt** cho các con số trong `tools/muc-tieu.json` (hiện toàn bộ là `demo`)
