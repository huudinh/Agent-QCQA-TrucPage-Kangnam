# MAU_hoi-thoai.md · khuôn bản xuất Caresoft

> Dùng để **đối chiếu khi Caresoft đổi cú pháp**. Nếu `tp.py kiem` báo "dòng lạ > 0",
> so bản xuất mới với file này để biết chỗ nào đã đổi.
> ⚠ Toàn bộ nội dung dưới đây là **giả lập**, ⛔ không phải hội thoại thật.

```
# <Tên page>_<YYYYMMDD>-<YYYYMMDD>

- Kỳ: 03/11/2026 → 05/11/2026
- Hội thoại: 2

---

# Page: <Tên page>

## 1. HT-0000000000aa

[03/11 09:15:02] **HT:** [tên KH] đã trả lời một quảng cáo.
[03/11 09:15:02] **QC:** Inbox từ quảng cáo <tên quảng cáo> — <mô tả quảng cáo>
[03/11 09:15:03] **BOT (<Tên page>):** <lời chào tự động của page>
[03/11 09:15:40] **KH:** <tin đầu của khách>
[03/11 09:16:05] **NV (NV-000000001) ⏱ 25 giây ✓:** <tin của người trực>
[03/11 09:18:30] **KH:** <khách trả lời, nhiều dòng thì
dòng tiếp KHÔNG có mốc thời gian>
[03/11 09:21:11] **NV (NV-000000001) ⏱ 2p41 ✗:** <tin trả lời chậm hơn ngưỡng>
[03/11 09:22:00] **KH:** [SĐT ẩn]
[03/11 09:22:18] **NV (NV-000000001) ⏱ 18 giây ✓:** <xác nhận>

## 2. HT-0000000000bb

[05/11 23:40:10] **HT:** [tên KH] đã trả lời một quảng cáo.
[05/11 23:40:12] **KH:** <tin đầu của khách, đến ngoài giờ trực>
*(lượt cuối được NV-000000002 trả lời lúc 06/11 08:35:00 ⏱ ngoài giờ — sau kỳ)*
```

## Những thứ `tp.py` BẮT BUỘC phải thấy

| Thành phần | Regex | Thiếu thì sao |
|---|---|---|
| Dòng kỳ | `^- Kỳ: dd/mm/yyyy → dd/mm/yyyy` | 🔴 **DỪNG** — không suy được năm, vì từng tin không ghi năm |
| Dòng tổng hội thoại | `^- Hội thoại: <n>` | ⚠ không đối chiếu được bản xuất có bị cắt |
| Mở đầu hội thoại | `^## <stt>\. HT-<hex>$` | 🔴 **DỪNG** — mọi tin thành "dòng lạ" |
| Một tin | `^\[dd/mm HH:MM:SS\] \*\*<VAI><hậu tố>:\*\* <nội dung>` | 🔴 **DỪNG** |
| Vai hợp lệ | `HT` · `QC` · `KH` · `BOT` · `NV` | vai khác → dòng lạ |
| Mã nhân viên | `NV-<số>` trong hậu tố của vai `NV` | không xác định được người trực |

## Sáu mã che của Caresoft

`[Số ẩn]` dãy số không phải SĐT · `[tên KH]` · `[Hình ảnh/Video/Đính kèm]` · `[SĐT ẩn]` **SĐT hợp lệ** · `[tên NV]` · `[Mẫu]`

★ `tp.py` đếm SĐT thô bằng sự có mặt của `[SĐT ẩn]` trong tin **của vai KH**. Đổi mã che là phải sửa `tp.py`.

## Ba hậu tố `⏱` của vai NV

`⏱ <n> giây ✓` · `⏱ <n>p<nn> ✓|✗` · `⏱ <n>g<nn>p ✗` · `⏱ ngoài giờ`

★ `tp.py` **tự tính lại FRT từ mốc giây**, ⛔ không đọc hậu tố. Hậu tố chỉ dùng để đối chiếu ở `tp.py kiem`.
