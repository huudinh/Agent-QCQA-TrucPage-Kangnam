# -*- coding: utf-8 -*-
"""Điểm Q6 · Q7 do AI chấm khi đọc mẫu phân tầng — NGUỒN DUY NHẤT.

Trước đây bảng này bị chép hai bản, ở v2agg.py (dict) và v2slices.py (tuple),
nên sửa một bên là hai bảng nói hai điểm khác nhau mà không ai biết.

  Q6 · Xử lí từ chối      — khách nêu rào cản hoặc từ chối cho số: có đổi lý do
                            ở lượt xin thứ hai, có mở kênh thay thế, có cho khách
                            đường rút — hay chỉ lặp lại câu cũ.  Thang 0–2.
  Q7 · Tuân thủ kịch bản  — đủ ba nhịp: hỏi 1–2 câu phân loại → trao một mảnh
                            giá trị thật (đọc ảnh, tính chỉ số, nêu khoảng giá)
                            → xin số gắn lý do.  Thang 0–2.

Mục tiêu cả hai: 1,5.  `doc` = số hội thoại đã đọc của người đó trong mẫu.

⛔ Điểm gắn với ĐÚNG kỳ AI_KY. Chạy kỳ khác thì v2agg.py cảnh báo; chấm lại
   bằng `python tools/tp.py mau "du-lieu/<file>.txt" --n <n>` rồi thay bảng này.
"""

AI_KY = '01-11_08-11-2026'

# Mẫu đã đọc: 204 hội thoại phân tầng của kỳ 03–08/11 cho 17 người đầu, cộng
# 36 hội thoại lấy riêng cho 3 người chỉ xuất hiện khi mở rộng sang 01–02/11.
AI_MAU = '204 hội thoại (03–08/11) + 36 hội thoại (01–08/11)'

# nv: (q6, q7, số hội thoại đã đọc)
AI = {
    "NV-236425444": (1.9, 1.8, 23),
    "NV-205107209": (1.3, 1.6, 21),
    "NV-202194914": (1.1, 1.4, 17),
    "NV-198843202": (1.7, 1.8, 16),
    "NV-238736928": (1.2, 1.3, 14),
    "NV-258612608": (1.5, 1.6, 13),
    "NV-232258930": (1.6, 1.8, 11),
    "NV-254668856": (1.5, 1.6, 11),
    "NV-262546620": (1.7, 1.8, 10),
    "NV-198842634": (1.3, 1.4, 9),
    "NV-202193608": (1.1, 1.6, 8),
    "NV-269001161": (1.7, 1.7, 7),
    "NV-264113743": (1.3, 1.6, 7),
    "NV-262546406": (1.2, 1.2, 7),
    "NV-226199192": (1.1, 1.3, 7),
    "NV-240896987": (0.9, 1.0, 7),
    "NV-198842558": (1.5, 1.4, 5),

    # ba người chỉ lộ ra khi kỳ mở rộng sang 01–02/11 và phạm vi page rộng hơn
    "NV-240857594": (1.8, 1.8, 12),   # khách quốc tế: giải thích sâu, buông đẹp khi khách chốt nơi khác
    "NV-259154835": (1.3, 1.4, 12),   # khách quốc tế: báo giá rõ, nhưng hồi đáp chậm và nhiều lượt rỗng
    "NV-271687143": (1.5, 1.3, 12),   # chạm muộn là chính; lần duy nhất gặp từ chối thì xử lí tốt
}


def dict_dang_khoa():
    """Dạng {'q6':…, 'q7':…, 'doc':…} cho v2agg.py."""
    return {k: {'q6': v[0], 'q7': v[1], 'doc': v[2]} for k, v in AI.items()}
