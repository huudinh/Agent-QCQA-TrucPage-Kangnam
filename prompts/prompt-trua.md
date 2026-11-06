# Prompt · Nhịp Trưa (`TRƯA`)

> Chạy 13:30, trên bản xuất 00:00 → 13:00 cùng ngày.
> Kèm `out/<ky>/bao-cao.md` của bản trưa + `viec-<ngày>.csv` của **buổi sáng** (đã có cột Kết quả).

---

```
TRƯA <dd/mm>

Tối đa 1 trang. ĐÚNG ba việc, theo TP-06 §2:

1. Sáng nay so sáng hôm qua và so cùng thứ tuần trước.
   Chỉ 3 dòng: Inbox · SĐT thô · FRT tin đầu trung vị.
   ⚠ Mọi tỷ lệ ở đây là số TẠM — chưa inbox nào đủ 24h. Nói rõ câu đó.
   ⚠ Mốc "≥38% mục tiêu ngày lúc 13h" (note §1) chỉ nêu khi mục tiêu SĐT/ngày
     đã CHỐT; còn 'demo' thì ghi "⚠ chưa có mốc chốt".

2. Việc sáng chưa xong: đọc viec-<ngày>.csv, lọc dòng cột Kết quả còn trống
   và đã quá hạn. Ghi rõ ai đang giữ.

3. Cần cứu trước khi hết cửa sổ 24h: P1 + P3 còn < 6 giờ, ít thời gian nhất lên trên.
   Mỗi dòng: mã hội thoại · NV · còn bao nhiêu giờ · câu gợi ý.

⛔ KHÔNG chấm điểm nhân viên. ⛔ KHÔNG chẩn đoán lại. Nhịp Trưa chỉ cứu số trong ngày.
```
