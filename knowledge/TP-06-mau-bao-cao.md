# TP-06 · Mẫu báo cáo

> Ba mẫu: **Sáng** (`NGÀY`) · **Trưa** (`TRƯA`) · **Tuần** (`TUẦN`). Thêm hai mẫu phụ: trang riêng một người (`NV`) và giáo án (`COACH`).
> ★ Mọi bảng số **copy từ `out/<ky>/bao-cao.md`**, ⛔ không tự tính lại.

---

## 1 · Báo cáo Sáng — lệnh `NGÀY`

Dài tối đa **2 trang**. Thứ tự cố định, ⛔ không đổi.

```
# BÁO CÁO SÁNG TRỰC PAGE · <ngày> · <giờ chạy>

Cỡ mẫu: <n> hội thoại hợp lệ / <N> đọc được · kỳ <từ> → <đến> · page <tên>
Số CHỐT: CR24 cho inbox <D-2> · CR48 cho inbox <D-3>
Số TẠM: <liệt kê> — ⛔ không dùng để đánh giá nhân viên

## 1 · Một dòng tình hình
<một câu: CR48 chốt là bao nhiêu, so hôm qua và so cùng thứ tuần trước, và
 mắt xích nào trong phân rã đang rơi nhiều nhất>

## 2 · Bảng chốt
<bảng mục 1 của bao-cao.md: Ngày · Inbox · SĐT · CR24(mẫu) · CR48(mẫu) · chưa đủ giờ>
<bảng so mục tiêu, kèm cờ 🟢🟡🔴 và dấu ⚠ cho mục tiêu còn 'demo'>

## 3 · Ba vấn đề lớn nhất hôm nay
Mỗi vấn đề ĐÚNG khuôn này, ⛔ không thêm bớt:
  ① SỐ      — con số + mẫu + so với cái gì
  ② NHÓM    — 1 trong 6 nhóm nguyên nhân (TP-02 §6)
  ③ AI CHỊU — Trực page / QL ca / Performance-Ads / Sale / 🔧 Hệ thống
  ④ VIỆC    — một hành động, có hạn giờ
  ⑤ BẰNG    — 1–2 HT-xxxxxxxx
  ⑥ QUY MÔ  — số hội thoại gặp lỗi / tổng hội thoại nhận

★ Thứ tự chẩn đoán cố định: loại nguyên nhân NGOÀI trực page trước
  (chất lượng inbox, phân bổ), rồi mới tới quy trình → kịch bản → kỹ năng.

## 4 · Việc hôm nay — tối đa 30 dòng
<bảng từ out/<ky>/viec-<ngày>.csv, THÊM cột "Câu gợi ý nhắn tiếp" do BẠN viết>

| Ưu tiên | Mã hội thoại | Page / Dịch vụ | NV xử lý | Tình trạng (1 dòng) | Câu gợi ý nhắn tiếp | Hạn | Kết quả |

Cột "Kết quả" để TRỐNG — NV điền trên Google Sheet. Lần chạy sau đọc lại cột
này để đo "tỷ lệ cứu được".

## 5 · 🔧 Việc hệ thống — ⛔ KHÔNG trừ điểm người
<ba thứ của TP-02 §6: inbox ngoài giờ · bỏ sót vắt ca · hội thoại 1 chiều>

## 6 · Câu mẫu của ngày
Một câu, lấy từ TP-07 hoặc từ một hội thoại thắng trong mẫu hôm nay.
Dùng cho họp đầu ca 10 phút.

## 7 · ⚠ Thứ đang chặn
<liệt kê từ phiếu chất lượng dữ liệu; ⛔ không bỏ mục này dù không có gì mới>
```

### Luật của Báo cáo Sáng

- ⛔ Không quá **3** vấn đề. Vấn đề thứ 4 trở đi ghi vào mục `👁 theo dõi`, một dòng mỗi cái.
- ⛔ Không quá **30** dòng việc. Thừa thì cắt theo thứ tự ưu tiên, và ghi *"còn n dòng ở `viec-<ngày>.csv`"*.
- Mỗi câu gợi ý nhắn tiếp phải **dùng được ngay**: đúng dịch vụ, đúng rào cản khách đã nêu, ⛔ không chung chung.
- Mục 7 **luôn có**, dù chỉ để ghi *"không có thay đổi so hôm qua"*.

---

## 2 · Nhịp Trưa — lệnh `TRƯA`

Dài tối đa **1 trang**. Chỉ ba việc.

```
# NHỊP TRƯA · <ngày> · 13:30

Cỡ mẫu: inbox từ 00:00 đến 13:00 hôm nay = <n>
⚠ Mọi tỷ lệ ở đây là số TẠM — chưa inbox nào đủ 24h.

## 1 · Sáng nay so sáng hôm qua và so cùng thứ tuần trước
<bảng 3 dòng: Inbox · SĐT thô · FRT tin đầu trung vị. Mỗi dòng 2 cột so>
⚠ Mốc "≥ 38% mục tiêu ngày lúc 13h" của note §1 KHÔNG tính được:
   cần mục tiêu SĐT/ngày đã CHỐT, hiện còn 'demo'.

## 2 · Việc sáng chưa xong
<đọc lại viec-<ngày>.csv: dòng nào cột Kết quả còn trống và đã quá hạn>

## 3 · Cần cứu trước khi hết cửa sổ 24h
<P1 + P3 có con_24h < 6 giờ, xếp theo thời gian còn lại ít nhất lên trên>
Mỗi dòng: mã hội thoại · NV · còn bao nhiêu giờ · câu gợi ý.
```

⛔ Nhịp Trưa **không** chấm điểm nhân viên, **không** chẩn đoán lại. Nó chỉ cứu số trong ngày.

---

## 3 · Chu kỳ tuần — lệnh `TUẦN`

Chạy **thứ 2**. Ba phần, mỗi phần một trang.

```
# BÁO CÁO TUẦN TRỰC PAGE · tuần <từ> → <đến>

Cỡ mẫu: <n> hội thoại · <m> hội thoại đã chấm rubric TP-05
⚠ Mọi thay đổi kịch bản chuẩn ở trạng thái "CHỜ DUYỆT" cho tới khi QL trực page chốt.

## PHẦN 1 · Xếp hạng bằng dữ liệu, đối chiếu đánh giá của QL
<bảng điểm thang 100 theo TP-02 §7>
<ma trận hiệu chỉnh: hạng dữ liệu × hạng QL, và 3 câu hỏi kiểm tra>
> Điểm dùng để phân việc kèm cặp. Không phải căn cứ kỷ luật hay xếp hạng công khai.

## PHẦN 2 · Công thức WIN từ nhóm A
<đọc 30–50 hội thoại ra số tốt nhất của nhóm A — ★ do CODE lọc, ⛔ AI không tự chọn>
Rút ra 4 thứ:
  ① Nhịp hội thoại — xin số ở lượt thứ mấy, sau câu nào
  ② Câu xin số thắng — theo dịch vụ × chân dung, NGUYÊN VĂN, đã che danh tính
  ③ Câu xử lý từ chối thắng — theo từng rào cản
  ④ Câu nhắn lại thắng
Mỗi công thức ghi: số lần dùng · tỷ lệ ra số · so với trung bình team.
★ Chỉ đưa vào kịch bản chuẩn khi ≥ 10 lần dùng VÀ hơn trung bình team.

## PHẦN 3 · Bài học Fail từ nhóm B/C
<đọc 30–50 hội thoại WARM/HOT không ra số của nhóm B/C — ★ do CODE lọc>
Xếp lỗi theo 6 nhóm nguyên nhân, đếm tần suất, chọn 3 lỗi mất số nhiều nhất.
Mỗi lỗi: câu NV đã nói → vì sao mất → câu nên nói (lấy từ PHẦN 2).

## PHẦN 4 · Chương trình coaching tuần
<bảng 4 dòng: Nhóm C · Nhóm B · Nhóm A · Theo dịch vụ>
Mỗi dòng: trọng tâm · hình thức · thời lượng · chỉ số nghiệm thu sau 1 tuần.
```

### ⚠ Câu hỏi còn mở trong phương án, trả lời ở đây

| Câu hỏi (phương án §7.2, §7.3) | Trả lời |
|---|---|
| *"Lọc hội thoại WIN bằng code được không? Tránh để AI tự chọn."* | **Được, và đang làm thế.** `tp.py mau` chọn mẫu bằng code theo tầng `nhiệt × ra số`, trải đều theo dịch vụ × khung giờ. AI chỉ nhận file đã lọc. |
| *"Xếp lỗi Fail — code làm được không? Nếu được thì lọc 100% hội thoại, không cần lấy mẫu."* | **Một nửa.** Code đã đếm được **100%** hội thoại ở các cột đo được: `da_xin_so` · `luot_nv_xin_dau` · `phut_den_xin_dau` · `so_lan_xin` · `phien_dai_chua_xin` · `rao_can` · `cham_lai_24h` · `bo_sot`. Những lỗi thuộc nhóm 3, 4, 6 vì thế **đã có số trên toàn bộ 2.086 hội thoại**, ⛔ không cần lấy mẫu. Riêng nhóm 5 (**kỹ năng XLTC**) — *"xử lý rào cản có đúng mẫu không"* — ⛔ code không làm được, phải đọc. Đó là phần duy nhất còn lấy mẫu. |
| *"Có nên phân tích theo page không?"* (§4.3) | **Có, nhưng chưa chạy được**: bản xuất chỉ có 1 page. Thay thế tạm bằng chiều cắt theo **tên quảng cáo** — đã có trong `so.json › qc_ad_top`, và nó trả lời đúng câu *"QC nào kéo inbox lạnh"*. |

---

## 4 · Trang riêng một người — lệnh `NV <mã>`

Một trang, gửi **đúng người đó**.

```
# TRANG RIÊNG · <mã NV hoặc tên nếu đã có TP-04> · kỳ <...>

Cỡ mẫu của bạn: <n> hội thoại · <m> đủ 24h · <k> đủ 48h
<⛔ nếu n < 10: "chưa đủ mẫu để phân loại" và DỪNG>

## Số của bạn
<bảng: Inbox · SĐT · CR24 thực · CR24 kỳ vọng · CEI24 · FRT · % đã xin số>
CEI24 = <...>  → <🟢 giỏi thật / 🟡 quanh mức team / 🔴 dưới kỳ vọng>
Nghĩa: với đúng loại inbox bạn nhận, team làm được <x>%; bạn làm được <y>%.

## Ba hội thoại làm bằng
<2 hội thoại mất số + 1 hội thoại thắng, có trích câu>

## Việc của bạn
<luật một việc: hạng D và B 1 việc · C tối đa 2 việc · A 1 việc nâng cấp + 2 đoạn chat mẫu>
Mỗi việc: hành động + CÂU MẪU DÙNG ĐƯỢC NGAY + đo thế nào kỳ sau.

> Điểm dùng để phân việc kèm cặp. Không phải căn cứ kỷ luật hay xếp hạng công khai.
```

⛔ Trang của người này **không** chứa tên, điểm hay hội thoại của người khác. ⛔ Không phát vào nhóm chat chung.

---

## 5 · Giáo án — lệnh `COACH <nhóm | mã NV>`

```
# GIÁO ÁN COACHING · <đối tượng> · tuần <...>

Mục tiêu       : <một câu, đo được>
3 hội thoại đề : <mã + 1 dòng vì sao chọn>
Câu mẫu        : <từ TP-07, nguyên văn>
Bài tập roleplay: <tình huống + rào cản cụ thể>
Chỉ số nghiệm thu sau 1 tuần: <chỉ số + mốc>
Thời lượng     : <...>
```

| Đối tượng | Trọng tâm | Hình thức | Thời lượng | Đo sau 1 tuần |
|---|---|---|---|---|
| Nhóm C | 1 lỗi lớn nhất của từng bạn | kèm 1-1 với một bạn A; chấm 10 HT/ngày | 20 phút/ngày | % đã xin số · CEI |
| Nhóm B | 3 lỗi chung của nhóm | roleplay theo rào cản, dùng hội thoại thật làm đề | 2 buổi × 30 phút | tỷ lệ xin được |
| Nhóm A | chuẩn hóa công thức, dịch vụ mới | viết/duyệt câu mẫu `TP-07`; làm mentor | 1 buổi | số công thức được duyệt |
| Theo dịch vụ | dịch vụ có CR48 giảm nhiều nhất tuần | mini-training 15 phút đầu ca | 3 ngày | CR48 của dịch vụ đó |
