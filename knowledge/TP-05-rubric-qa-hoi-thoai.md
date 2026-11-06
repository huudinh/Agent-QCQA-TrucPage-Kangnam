# TP-05 · Rubric QA hội thoại

> Sổ chấm. AI chấm trên `out/<ky>/mau-ai.md` — mẫu do **code** chọn, ⛔ AI không tự chọn hội thoại.
> Một hội thoại chấm **đúng một lần** (`TP-01 §7` luật ③).

---

## 1 · Thang điểm

| Mã | Nhóm tiêu chí | Điểm | Chấm bằng |
|---|---|---|---|
| `Q1` | **SLA phản hồi** | 20 | ★ số từ `ht.csv`, ⛔ AI không đọc lại |
| `Q2` | **Khai thác nhu cầu** — 2 câu vàng | 15 | AI đọc |
| `Q3` | **Trả lời đúng & đủ** | 15 | AI đọc |
| `Q4` | **Xử lý từ chối (XLTC)** | 20 | AI đọc |
| `Q5` | **Xin số & chốt** | 25 | ★ nhịp từ `ht.csv` + AI đọc câu |
| `Q6` | **Ngôn từ & tuân thủ** | 5 | AI đọc |
| | **Tổng** | **100** | |

★ `Q1` và phần nhịp của `Q5` lấy **thẳng từ cột trong `ht.csv`** — ⛔ AI không ước lượng lại thời gian hay số lượt.

**Phân loại hội thoại:** 🟢 ≥ 80 · 🟡 60–79 · 🔴 < 60.
Một **lỗi nghiêm trọng** (§3) → trần **49 điểm** cho hội thoại đó, bất kể các mục khác.

---

## 2 · Bảng tiêu chí

### Q1 · SLA phản hồi — 20đ · ★ lấy từ `ht.csv`

| Tiêu chí | Cột | Đạt | Điểm |
|---|---|---|---|
| Q1.1 Phản hồi tin đầu, **trong giờ** | `frt_dau_giay` | ≤ 120 giây | 10 |
| | | 121–300 giây | 6 |
| | | > 300 giây | 0 |
| | | tin đầu **ngoài giờ** | **`—`** → loại khỏi mẫu số |
| Q1.2 Phản hồi giữa hội thoại | `frt_giua_tv_giay` | ≤ 180 giây | 5 |
| Q1.3 Không bỏ sót | `bo_sot`, `bo_sot_vat_ca` | `bo_sot = 0` | 5 |
| | | `bo_sot_vat_ca = 1` | **`—`** → 🔧 việc hệ thống, ⛔ không trừ |

⛔ **`—` không phải `✗`.** Tiêu chí không phát sinh thì **loại khỏi mẫu số**, điểm quy về thang 100 trên các tiêu chí còn lại.

### Q2 · Khai thác nhu cầu — 15đ

**Hai câu vàng** phải có trước khi báo giá: ① *tình trạng hiện tại* (đã can thiệp chưa, đang gặp gì) ② *mong muốn / mốc thời gian*.

| Tiêu chí | Đạt khi | Điểm |
|---|---|---|
| Q2.1 Hỏi tình trạng trước khi tư vấn | có ít nhất 1 câu hỏi về tình trạng/tiền sử | 6 |
| Q2.2 Xin ảnh hoặc thông tin định lượng khi dịch vụ cần | mũi/mí/hàm → ảnh · body → chiều cao cân nặng | 5 |
| Q2.3 Hỏi mốc thời gian dự định làm | có | 4 |

Ví dụ **đạt**, nguyên văn từ kỳ 03–05/11:
> *"Để em hỗ trợ chị đúng nhất, chị cho em xin 1–2 ảnh vùng mắt để em xem qua giúp c nha"*
> *"Chiều cao cân nặng của mình là bao nhiêu ạ"*

### Q3 · Trả lời đúng & đủ — 15đ

| Tiêu chí | Đạt khi | Điểm |
|---|---|---|
| Q3.1 Trả lời **đúng câu khách hỏi** trước khi chuyển hướng | có | 6 |
| Q3.2 Có **trao giá trị sơ bộ** (nhận định từ ảnh/thông tin khách gửi) | có, và nói bằng **tình trạng**, ⛔ không bằng tính từ | 6 |
| Q3.3 Không trả lời dài rập khuôn | ⛔ không copy nguyên khối > 5 dòng khi khách hỏi 1 câu ngắn | 3 |

Ví dụ **đạt** (trao giá trị sơ bộ, nói bằng tình trạng):
> *"Qua ảnh em thấy phần da mí trên của chị khá chùng, xuất hiện nhiều nếp gấp và che phủ nếp mí, hai bên mắt cũng chưa thật sự cân đối…"*

### Q4 · Xử lý từ chối — 20đ

Chấm **chỉ khi** hội thoại có rào cản (`rao_can` ≠ rỗng) hoặc `tu_choi_cho_so = 1`. Không phát sinh → `—`.

| Rào cản | Xử lý đúng mẫu | Xử lý sai |
|---|---|---|
| **Giá** (`GIA` — 1.149/2.086 HT, 55%) | hỏi tình trạng → khoảng giá có điều kiện → chuyển sang gọi để báo đúng | ⛔ báo giá trần trụi không điều kiện · ⛔ im lặng · ⛔ đẩy sang gọi mà không trả lời gì |
| **Sợ biến chứng** (`SO_BIEN_CHUNG` — 252 HT) | thừa nhận lo lắng → nói quy trình kiểm soát → ⛔ không cam kết kết quả | ⛔ *"chị yên tâm 100%"* · ⛔ bỏ qua câu hỏi |
| **Chưa tin bác sĩ** (`CHUA_TIN_BAC_SI`) | dẫn case tương đồng → mời hội chẩn | ⛔ gắn chức danh/số ca chưa đối chiếu chứng chỉ |
| **Đau / nghỉ dưỡng** (`DAU_NGHI`) | mốc hồi phục theo giai đoạn | ⛔ nói *"không đau"* |
| **Xa / thời gian** (`XA_THOI_GIAN`) | nêu chi nhánh gần + hỗ trợ đi lại đang có | ⛔ bỏ lửng |
| **Người nhà** (`NGUOI_NHA`) | gửi tài liệu để khách trao đổi ở nhà + hẹn lại | ⛔ ép chốt ngay |
| **Bảo hành** (`BAO_HANH`) | 🔴 ⛔ **không nêu con số** — ba mức đang xung đột, chưa có văn bản | ⛔ nêu *trọn đời / 10 năm / 3 năm* |

| Tiêu chí | Đạt khi | Điểm |
|---|---|---|
| Q4.1 Nhận ra và **chạm vào** rào cản khách nêu | có | 8 |
| Q4.2 Xử lý **đúng mẫu** của rào cản đó | theo bảng trên | 8 |
| Q4.3 Sau khi bị từ chối cho số, **thử cách xin thứ 2** | `so_lan_xin ≥ 2` khi `tu_choi_cho_so = 1` | 4 |

★ Số thật của kỳ 03–05/11: **40 hội thoại** khách từ chối cho số, trong đó **47,5% vẫn ra số** — cao hơn mục tiêu demo 25%. Đây là chỗ **đang làm tốt**, nên lấy câu từ đây vào `TP-07`.

### Q5 · Xin số & chốt — 25đ · ★ nhịp lấy từ `ht.csv`

| Tiêu chí | Cột | Đạt | Điểm |
|---|---|---|---|
| Q5.1 **Có xin số** | `da_xin_so` | = 1 | 8 |
| Q5.2 Xin **trước tin NV thứ 5** | `luot_nv_xin_dau` | ≤ 4 | 5 |
| Q5.3 Xin **trong 5 phút đầu** | `phut_den_xin_dau` | ≤ 5 | 4 |
| Q5.4 Câu xin có **gắn lợi ích** | AI đọc | có | 5 |
| Q5.5 Không để **phiên dài mà chưa xin** | `phien_dai_chua_xin` | = 0 | 3 |

★ Số thật của kỳ: chỉ **54,2%** hội thoại từng có lượt xin số · chỉ **49,2%** xin trước tin NV thứ 5 · trung vị **29,6 phút** mới xin lần đầu (mục tiêu demo ≤ 5 phút) · **181 hội thoại** có phiên > 15 phút mà chưa xin số lần nào. → `Q5` là nhóm **yếu nhất** của kỳ.

Ví dụ câu xin **có gắn lợi ích** (nguyên văn từ kỳ):
> *"Dạ, với tình trạng của mình hiện tại em sẽ gửi hội chẩn bác sỹ về phương pháp cũng như chi phí cho mình chị nha. Chị cho em xin Số Điện Thoại để em lưu thông tin, khi có kết quả trợ lý bác sỹ sẽ liên hệ tới chị ạ"*
> *"Để bác sĩ đánh giá đúng nền mũi và báo chi phí sát với mình, anh cho em xin số điện thoại để trợ lý bác sĩ gọi tư vấn kỹ cho anh"*

Ví dụ câu xin **không gắn lợi ích** (xin khan):
> *"Chị cho em xin SĐT nhé!"* — đặt ngay sau khi khách hỏi giá, chưa trả lời gì.

### Q6 · Ngôn từ & tuân thủ — 5đ

| Tiêu chí | Đạt khi | Điểm |
|---|---|---|
| Q6.1 Xưng hô đúng, không viết tắt khó hiểu | có | 2 |
| Q6.2 Không sai chính tả gây hiểu lầm về dịch vụ/giá | có | 2 |
| Q6.3 Chào mở đầu có tên khách / có nhận diện | có | 1 |

---

## 3 · Sáu lỗi nghiêm trọng — trần 49 điểm

| Mã | Lỗi | Nhận diện |
|---|---|---|
| `LN-1` | **Báo sai giá** hoặc nêu giá dịch vụ ngoài mắt khi chưa có bảng giá hiện hành | có con số giá trong tin NV |
| `LN-2` | **Cam kết kết quả** chắc chắn | *"chắc chắn đẹp"* · *"100% thành công"* · *"không đau"* |
| `LN-3` | **Nêu con số bảo hành** | *trọn đời* · *10 năm* · *3 năm* cho dịch vụ ngoài mắt |
| `LN-4` | **Trả lời câu bệnh nền / chống chỉ định** thay bác sĩ | khách nêu huyết áp · tiểu đường · đang cho con bú · thuốc đang dùng → NV tự kết luận được/không được làm |
| `LN-5` | **Nói quá về bác sĩ** — chức danh, số năm, số ca chưa đối chiếu chứng chỉ | có số/chức danh cụ thể |
| `LN-6` | **Lộ thông tin khách khác** · dìm đối thủ · thái độ gắt | có |

⛔ Một hội thoại có lỗi nghiêm trọng thì **không** được dùng làm câu mẫu `TP-07`, dù `Q5` cao.

---

## 4 · Cách ghi kết quả chấm

Mỗi hội thoại một khối:

```
HT-xxxxxxxx · <dịch vụ> · NV-nnnnnnnnn · <tầng mẫu>
KF-60: HOT | WARM | COLD        (★ điểm của BẠN, ⛔ không copy nhiet_loc của script)
KF-62: <mã chân dung>           (tra thư viện, ⛔ không tự đặt)
Q1 ..  Q2 ..  Q3 ..  Q4 ..  Q5 ..  Q6 ..  → Tổng ../100   🟢🟡🔴
Lỗi nghiêm trọng: — | LN-n
Vì sao rơi: nội dung | trực page | hệ thống | khách tự dừng | không rơi   (ĐÚNG MỘT giá trị)
Bằng chứng: "<trích nguyên văn câu của NV hoặc khách>"
Việc: <một hành động, kèm câu mẫu dùng được ngay>
```

★ **Tổng phải khớp**: tổng "vì sao rơi" = cỡ mẫu · tổng KF-60 = cỡ mẫu.

⛔ **Không** nhận xét về một nhân viên mà không gắn được vào một mã `Q` + một `HT-xxxxxxxx`.

---

## 5 · Hiệu chỉnh

Rubric này là **bản 1**, viết từ phương án §5 và từ 2.086 hội thoại thật của kỳ 03–05/11/2026. Ba việc phải làm sau 2 tuần chạy:

1. **Đối chiếu hạng**: so hạng theo điểm rubric với hạng QL (`TP-04 §2`). ≥ 80% khớp → rubric đáng tin; lệch nhiều → kiểm trọng số `Q`.
2. **Hiệu chỉnh ngưỡng `Q5.3`**: mục tiêu demo *xin số trong 5 phút* so với thực tế trung vị *29,6 phút* chênh quá xa. Hoặc mục tiêu sai, hoặc kịch bản sai — ⛔ không tự đổi mục tiêu, phải hỏi QL.
3. **Chuyển `Q4` sang đo 100% bằng code nếu được**: câu hỏi của phương án §7.3 (*"Code làm được không?"*) — hiện code đã **đếm được rào cản** và **đếm được số lượt xin lại**, nhưng ⛔ **không** đánh giá được *xử lý có đúng mẫu không*. Phần đó cần đọc hiểu. Khi `TP-07` đủ dày, có thể khớp câu NV với câu mẫu bằng code và chỉ để AI xử lý phần lệch.
