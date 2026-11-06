#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
trang-huong-dan.py · Agent-QCQA-TrucPage-Kangnam

Sinh `tools/huong-dan.html` — trang hướng dẫn cài đặt + prompt mẫu, có nút Copy
từng file. Nội dung các file được NHÚNG THẬT từ repo, ⛔ không gõ lại bằng tay,
nên sửa file tri thức rồi chạy lại là trang tự khớp.

Hệ thiết kế dùng chung với artifact `Agent-LDP-Kangnam`:
  Be Vietnam Pro + Lora · maroon #8A1F33 · gold #86560D · band #3A1425

Cách dùng:
    python tools/trang-huong-dan.py
    # rồi publish tools/huong-dan.html làm artifact
"""

import html
import json
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RA = os.path.join(GOC, "tools", "huong-dan.html")
KHUNG = os.path.join(GOC, "tools", "mau-trang")   # khung HTML tách rời cho dễ sửa
REPO = "https://github.com/huudinh/Agent-QCQA-TrucPage-Kangnam"


def doc(p):
    with open(os.path.join(GOC, p), encoding="utf-8") as f:
        return f.read()


# ───────────────────────── FILE NHÚNG TỪ REPO ─────────────────────────

# (khóa, đường dẫn, nhãn, badge, cách dùng)
FILE = [
    ("A", "SYSTEM-PROMPT.md", "Thẻ A · Bộ não đầy đủ", "DÁN",
     "Dán vào ô <b>Project instructions</b> của Claude / Gemini. Ô này không giới hạn ký tự."),
    ("B", "SYSTEM-PROMPT-NGAN.md", "Thẻ B · Bản ngắn", "DÁN",
     "Chỉ dùng cho <b>ChatGPT Custom GPT</b> — ô Instructions ở đó chặn ở 8.000 ký tự."),
    ("TP01", "knowledge/TP-01-chi-dan-lenh.md", "TP-01 · Chỉ dẫn &amp; lệnh", "UPLOAD",
     "Vai trò · 7 lệnh · 12 luật bất biến · làm gì khi thiếu dữ liệu."),
    ("TP02", "knowledge/TP-02-core-chi-so.md", "TP-02 · CORE chỉ số", "UPLOAD ★★",
     "Định nghĩa từng chỉ số · <b>hai thang nhiệt</b> · luật so công bằng · luật chốt/tạm · 6 nhóm nguyên nhân."),
    ("TP03", "knowledge/TP-03-dac-ta-du-lieu.md", "TP-03 · Đặc tả dữ liệu", "UPLOAD ★",
     "Cú pháp bản xuất Caresoft · giờ trực đang xung đột · ba chỗ bộ che PII hở · cột đang thiếu."),
    ("TP04", "knowledge/TP-04-master-data.md", "TP-04 · Master data", "UPLOAD 🔴",
     "Đang <b>chặn</b> bảng Nhóm và xếp hạng A/B/C. Vẫn phải upload để agent biết nó đang thiếu gì."),
    ("TP05", "knowledge/TP-05-rubric-qa-hoi-thoai.md", "TP-05 · Rubric QA hội thoại", "UPLOAD ★★",
     "Thang 100: <code>Q1</code>–<code>Q6</code> · 6 lỗi nghiêm trọng <code>LN-1…6</code> · câu mẫu đạt/không đạt."),
    ("TP06", "knowledge/TP-06-mau-bao-cao.md", "TP-06 · Mẫu báo cáo", "UPLOAD",
     "Khuôn Báo cáo Sáng · Nhịp Trưa · Tuần · trang riêng nhân viên · giáo án."),
    ("TP07", "knowledge/TP-07-thu-vien-win-fail.md", "TP-07 · Thư viện WIN/Fail", "UPLOAD ⏳",
     "Hạt giống từ kỳ đầu — mọi câu còn <b>CHỜ DUYỆT</b>. Agent đọc để không tự bịa câu mẫu."),
    ("PNGAY", "prompts/prompt-ngay.md", "prompt-ngay.md", "KHÔNG UPLOAD",
     "Prompt dạng file cho lệnh <code>NGÀY</code>. Copy vào chat, ⛔ không upload làm tri thức."),
    ("PTRUA", "prompts/prompt-trua.md", "prompt-trua.md", "KHÔNG UPLOAD",
     "Prompt dạng file cho lệnh <code>TRƯA</code>."),
    ("PNV", "prompts/prompt-nv.md", "prompt-nv.md", "KHÔNG UPLOAD",
     "Prompt dạng file cho lệnh <code>NV</code>."),
    ("PTUAN", "prompts/prompt-tuan.md", "prompt-tuan.md", "KHÔNG UPLOAD",
     "Prompt dạng file cho lệnh <code>TUẦN</code>."),
    ("PCOACH", "prompts/prompt-coach.md", "prompt-coach.md", "KHÔNG UPLOAD",
     "Prompt dạng file cho lệnh <code>COACH</code>."),
]


# ───────────────────────── PROMPT MẪU ─────────────────────────
# (số, nhóm, tiêu đề, ghi chú ngắn, nội dung)

P = []


def p(nhom, tieu_de, ghi_chu, noi_dung):
    P.append({"n": len(P) + 1, "nhom": nhom, "t": tieu_de, "k": ghi_chu,
              "s": noi_dung.strip()})


# ── nhóm: cài đặt & kiểm tra ──
p("setup", "Kiểm agent đã nạp đủ sổ chưa", "chạy ngay sau khi dựng Project", """
Liệt kê đúng 7 sổ tri thức bạn đang có, mỗi sổ một dòng theo mẫu:
  <mã sổ> · <tên> · <mục lớn nhất trong sổ đó>

Rồi trả lời gọn 5 câu:
1. Chỉ số gốc của bạn là gì, công thức ra sao?
2. Hai thang nhiệt khác nhau ở đâu, và vì sao phải có thang thứ hai?
3. Mẫu số của CR48 gồm những inbox nào, loại ra những inbox nào?
4. Ba thứ nào là "lỗi hệ", tuyệt đối không trừ điểm người trực?
5. Bạn đang thiếu gì để chạy được bảng xếp hạng A/B/C?

⛔ Nếu thiếu sổ nào thì nói thẳng thiếu sổ đó, đừng trả lời bằng trí nhớ chung.
""")

p("setup", "Smoke test — bắt agent tự chặn", "agent PHẢI từ chối, không được trả lời", """
Cho tôi CR48 của hôm nay và xếp hạng A/B/C cho 5 bạn trực page tốt nhất.
""")

p("setup", "Giải thích CEI cho người không làm số", "dùng khi họp với QL", """
Giải thích cho tôi chỉ số CEI bằng ngôn ngữ của người quản lý trực page,
không dùng công thức toán.

Yêu cầu:
- Đúng 5 câu.
- Có một ví dụ cụ thể: một bạn phản hồi nhanh, xin số nhiều, mà CEI vẫn dưới 1,0 —
  giải thích điều đó nghĩa là gì và việc phải làm là gì.
- Kết bằng một câu trả lời cho câu hỏi: "vì sao không xếp hạng bằng tỷ lệ ra số thô?"
""")

p("setup", "Đổi giờ trực rồi tính lại", "khi anh/QL đã chốt giờ trực", """
Giờ trực đã được chốt là <08:00–21:30 | 08:00–22:00 | ... >.

Nói cho tôi biết, trước khi tôi chạy lại script:
1. Những chỉ số nào trong báo cáo sẽ ĐỔI vì đổi giờ trực, và đổi theo hướng nào.
2. Những chỉ số nào KHÔNG đổi.
3. Dòng nào trong tools/muc-tieu.json tôi phải sửa, sửa thành gì.
4. Câu lệnh tp.py đầy đủ để chạy lại với giờ trực mới.

⚠ Và nhắc tôi: số của các kỳ đã chạy bằng giờ cũ có còn so sánh được với kỳ mới không?
""")

# ── nhóm: NGÀY ──
p("ngay", "Báo cáo Sáng — bản đầy đủ", "lệnh chính, chạy 8:45 mỗi ngày", """
NGÀY <dd/mm>

Ba file kèm theo:
- bao-cao.md   → toàn bộ bảng số đã tính bằng code (L1). ★ COPY SỐ TỪ ĐÂY, ⛔ không tự tính lại.
- mau-ai.md    → mẫu hội thoại do code chọn theo tầng (L2). Chấm rubric TP-05 trên file này.
- viec-<ddmm>.csv → hàng chờ P0–P6 code đã xếp (L4). Bạn chỉ THÊM cột "Câu gợi ý nhắn tiếp".

Làm đúng thứ tự TP-06 §1:
1. Một dòng tình hình.
2. Bảng chốt + nói rõ số nào CHỐT, số nào TẠM.
3. ĐÚNG 3 vấn đề lớn nhất. Mỗi vấn đề đúng khuôn 6 ô:
   ① SỐ (kèm cỡ mẫu + so với cái gì) ② NHÓM nguyên nhân (1 trong 6)
   ③ AI CHỊU ④ VIỆC có hạn giờ ⑤ 1–2 HT-xxxxxxxx làm bằng ⑥ QUY MÔ lỗi/tổng.
   ★ Thứ tự chẩn đoán: loại nguyên nhân NGOÀI trực page trước (chất lượng inbox,
     phân bổ), rồi mới quy trình → kịch bản → kỹ năng.
4. Bảng "Việc hôm nay" ≤ 30 dòng, có cột Câu gợi ý nhắn tiếp do bạn viết.
   Mỗi câu phải đúng dịch vụ + đúng rào cản khách đã nêu, dùng được ngay.
   Cột "Kết quả" để TRỐNG.
5. 🔧 Việc hệ thống — ⛔ không trừ điểm người.
6. Câu mẫu của ngày (1 câu, cho họp đầu ca 10 phút).
7. ⚠ Thứ đang chặn.

⛔ Không đếm hội thoại. ⛔ Không nêu số không có trong bao-cao.md.
⛔ Không coi nhiet_loc là điểm KF-60 — bạn tự chấm KF-60 khi đọc mau-ai.md.
⛔ Không coi cờ canh_bao_nghi là khiếu nại.
""")

p("ngay", "Báo cáo Sáng — bản 10 dòng cho nhóm Zalo QL", "gửi lên nhóm, không gửi file", """
NGÀY <dd/mm>

Chỉ cần bản gửi nhóm Zalo QL. Đúng 10 dòng, không bảng, không markdown:
- Dòng 1: cỡ mẫu + kỳ + số nào chốt.
- Dòng 2–4: ba vấn đề, mỗi vấn đề một dòng, bắt đầu bằng con số.
- Dòng 5–8: bốn việc gấp nhất, mỗi dòng = mã hội thoại + ai làm + hạn giờ.
- Dòng 9: câu mẫu của ngày.
- Dòng 10: thứ đang chặn, hoặc "không có thay đổi".

⛔ Không nêu tên nhân viên — dùng mã NV. ⛔ Không nêu tên hay SĐT khách.
""")

p("ngay", "Chỉ lấy phần chẩn đoán", "khi QL chỉ hỏi 'hôm nay vấn đề gì'", """
Đọc bao-cao.md kèm theo. Bỏ qua mọi mục khác, chỉ làm mục 3 của TP-06 §1:
ĐÚNG 3 vấn đề lớn nhất, mỗi vấn đề đúng khuôn 6 ô.

Thêm một yêu cầu: với mỗi vấn đề, nói rõ bạn đã LOẠI những nguyên nhân nào
trước khi chốt nhóm nguyên nhân đó, và loại bằng con số nào.
Ví dụ: "loại nhóm ③ quy trình vì FRT trung vị 0,9 phút, tốt nhất cả kỳ".
""")

p("ngay", "So hai ngày để tìm ngày hỏng", "khi một chỉ số tụt mạnh", """
Đọc bao-cao.md và out/lich-su.csv kèm theo.

Chỉ số <tên chỉ số> đang tụt. Trả lời bốn câu:
1. Tụt từ ngày nào, mức tụt bao nhiêu điểm, cỡ mẫu từng ngày.
2. Cùng ngày đó, những chỉ số nào KHÔNG tụt? (dùng để loại nguyên nhân)
3. Chiều cắt nào tụt nặng nhất: khung giờ · dịch vụ · nhân viên · nguồn quảng cáo?
4. Một giả thuyết duy nhất, kèm cách kiểm bằng 3 hội thoại cụ thể từ mau-ai.md.

⚠ Ô nào dưới 30 hội thoại thì gắn nhãn MẪU NHỎ và ⛔ không xếp hạng.
⚠ Chưa có cùng thứ tuần trước thì ghi "⚠ chưa có mốc so sánh", ⛔ không tự đặt mốc.
""")

# ── nhóm: TRƯA ──
p("trua", "Nhịp Trưa", "13:30, trên bản xuất 00:00–13:00", """
TRƯA <dd/mm>

Tối đa 1 trang. ĐÚNG ba việc, theo TP-06 §2:
1. Sáng nay so sáng hôm qua và so cùng thứ tuần trước.
   Chỉ 3 dòng: Inbox · SĐT thô · FRT tin đầu trung vị.
   ⚠ Mọi tỷ lệ ở đây là số TẠM — chưa inbox nào đủ 24h. Nói rõ câu đó.
2. Việc sáng chưa xong: đọc viec-<ngày>.csv, lọc dòng cột Kết quả còn trống
   và đã quá hạn. Ghi rõ ai đang giữ.
3. Cần cứu trước khi hết cửa sổ 24h: P1 + P3 còn < 6 giờ, ít thời gian nhất lên trên.
   Mỗi dòng: mã hội thoại · NV · còn bao nhiêu giờ · câu gợi ý.

⛔ KHÔNG chấm điểm nhân viên. ⛔ KHÔNG chẩn đoán lại. Nhịp Trưa chỉ cứu số trong ngày.
""")

p("trua", "Cứu gấp — chỉ danh sách, không báo cáo", "gửi trực tiếp cho trưởng ca", """
TRƯA <dd/mm> — chỉ phần 3.

Cho tôi danh sách cứu gấp, xếp theo thời gian còn lại ÍT NHẤT lên trên.
Mỗi dòng đúng một dòng văn bản, định dạng:

  [còn <x>h] HT-xxxxxxxx · <dịch vụ> · NV-xxxxxxxxx — <câu gợi ý nhắn tiếp>

Câu gợi ý phải: đúng dịch vụ, chạm vào rào cản khách đã nêu, và có gắn lợi ích
(hội chẩn bác sĩ / báo chi phí sát / giới hạn thời gian gọi).
⛔ Không dùng câu xin số khan kiểu "Chị cho em xin SĐT nhé".
""")

# ── nhóm: NV ──
p("nv", "Trang riêng một người", "gửi đúng người đó, không phát nhóm", """
NV <mã NV>

Kèm: bao-cao.md (mục 7 có CEI24/CEI48) + ht.csv + phần mau-ai.md của người này.

Theo TP-06 §4:
1. Cỡ mẫu của người này: tổng HT · mẫu đủ 24h · mẫu đủ 48h.
   ⛔ Nếu < 10 HT: ghi "chưa đủ mẫu để phân loại" và DỪNG. Không viết tiếp.
2. Số của bạn, cạnh số của team: Inbox · SĐT · CR24 thực · CR24 kỳ vọng · CEI24
   · FRT tin đầu · % đã xin số.
   Giải thích CEI bằng một câu đời thường:
   "với đúng loại inbox bạn nhận, team làm được <x>%; bạn làm được <y>%."
   ⚠ Kỳ < 14 ngày thì đọc CEI24, ⛔ không đọc CEI48.
3. Ba hội thoại làm bằng: 2 mất số + 1 thắng, trích nguyên văn.
   Mỗi hội thoại chỉ ra ĐÚNG MỘT mã Q của TP-05 bị trượt.
4. Việc của bạn — luật một việc:
   hạng D và B → 1 việc · C → tối đa 2 việc · A → 1 việc nâng cấp + 2 đoạn chat mẫu.
   Mỗi việc: hành động + CÂU MẪU DÙNG ĐƯỢC NGAY + đo thế nào kỳ sau.
5. Kết thúc bằng đúng câu:
   "Điểm dùng để phân việc kèm cặp. Không phải căn cứ kỷ luật hay xếp hạng công khai."

⛔ Trang này KHÔNG chứa tên, điểm hay hội thoại của người khác.
⛔ Không nhận xét gì mà không gắn được vào mã Q + HT-xxxxxxxx.
⛔ Không trừ điểm cho: inbox ngoài giờ · bỏ sót vắt ca · hội thoại 1 chiều.
""")

p("nv", "Người có SLA tốt mà CEI thấp", "ca khó nhất — và hay gặp nhất", """
NV <mã NV>

Bạn này có FRT và % đã xin số TỐT HƠN mức team, nhưng CEI24 dưới 0,9.
Nghĩa là xin đúng giờ và xin nhiều mà khách vẫn không cho số.

Nên bỏ qua phần SLA. Chỉ làm đúng một việc: đọc các hội thoại của bạn này trong
mau-ai.md và chỉ ra NỘI DUNG CÂU XIN đang sai ở đâu.

Trả về:
1. Ba câu xin số bạn này hay dùng nhất — trích nguyên văn, kèm số lần thấy.
2. Với mỗi câu: thiếu thành phần nào (lợi ích? thời điểm? đã trả lời câu khách hỏi chưa?).
3. Câu nên nói thay — lấy từ TP-07, ⛔ không tự viết. Nếu TP-07 chưa có câu cho
   rào cản đó thì ghi "⏳ chưa có câu đã duyệt".
4. Đúng MỘT việc cho tuần tới, kèm cách đo.
""")

p("nv", "So hai người cùng nhóm", "khi QL hỏi 'ai cần kèm trước'", """
Đọc bao-cao.md mục 7 kèm theo. So <mã NV 1> với <mã NV 2>.

Bảng 2 cột, mỗi dòng một chỉ số: Inbox · mẫu 24h · CR24 thực · CR24 kỳ vọng
· CEI24 · FRT tin đầu · % đã xin số · % bỏ sót trong ca.

Rồi trả lời đúng hai câu:
1. Ai cần kèm trước, và kèm về VIỆC GÌ (một việc duy nhất)?
2. Có dấu hiệu nào cho thấy chênh lệch này đến từ CHẤT LƯỢNG INBOX ĐƯỢC CHIA
   chứ không từ năng lực? Dẫn con số.

⚠ Người nào dưới 10 hội thoại thì ⛔ không so, chỉ ghi "chưa đủ mẫu".
> Kết bằng câu: "Điểm dùng để phân việc kèm cặp. Không phải căn cứ kỷ luật hay xếp hạng công khai."
""")

# ── nhóm: TUẦN ──
p("tuan", "Chu kỳ tuần — bản đầy đủ", "thứ 2, trên bản xuất gộp 7 ngày", """
TUẦN <từ dd/mm> → <đến dd/mm>

Kèm: bao-cao.md · out/lich-su.csv · kết quả chấm rubric TP-05 của tuần
     · viec-*.csv đã có cột Kết quả · knowledge/TP-07.

Bốn phần, theo TP-06 §3:

PHẦN 1 · Xếp hạng bằng dữ liệu, đối chiếu đánh giá của QL
  Điểm thang 100 = 50% CEI + 20% SLA + 20% rubric TP-05 + 10% tỷ lệ cứu được.
  ⛔ Thiếu bất kỳ thành phần nào → KHÔNG chạy bảng này, ghi rõ thiếu gì (TP-02 §7).
  Ma trận hiệu chỉnh: hạng dữ liệu × hạng QL. Trả lời 3 câu:
    - ≥ 80% khớp không?
    - Bạn nào QL xếp A mà CEI < 0,9 → bạn đó có đang được chia inbox ngon?
    - Bạn nào QL xếp C mà CEI ≥ 1,1 → bạn đó có đang bị giao inbox khó?

PHẦN 2 · Công thức WIN từ nhóm A
  Đọc mẫu hội thoại ra số của nhóm A — ★ do CODE lọc, ⛔ bạn KHÔNG tự chọn.
  Rút 4 thứ: ① nhịp hội thoại ② câu xin số thắng ③ câu XLTC thắng theo rào cản
             ④ câu nhắn lại thắng.
  Mỗi công thức ghi: số lần dùng · tỷ lệ ra số · so trung bình team.
  ★ Chỉ đề xuất vào kịch bản chuẩn khi ≥ 10 lần dùng VÀ hơn trung bình team.
  ⛔ Không lấy câu từ hội thoại có lỗi nghiêm trọng LN-1…6.
  ⛔ Câu nào nêu giá hoặc bảo hành → 🔴 chờ văn bản, không duyệt.

PHẦN 3 · Bài học Fail từ nhóm B/C
  ★ Ba dạng F1–F3 (không xin số · xin quá muộn · tư vấn dài không chốt) code đã
    đếm được trên 100% hội thoại — dùng số đó, ⛔ không lấy mẫu lại.
    Chỉ nhóm ⑤ (kỹ năng XLTC) mới cần đọc mẫu.
  Chọn 3 lỗi mất số nhiều nhất. Mỗi lỗi: câu NV đã nói → vì sao mất → câu nên nói.

PHẦN 4 · Chương trình coaching tuần
  Bảng 4 dòng: Nhóm C · Nhóm B · Nhóm A · Theo dịch vụ.
  Mỗi dòng: trọng tâm · hình thức · thời lượng · chỉ số nghiệm thu sau 1 tuần.

⚠ Mọi thay đổi kịch bản chuẩn ghi trạng thái "CHỜ DUYỆT" cho tới khi QL trực page chốt.
⛔ Không tự đưa câu vào mục ĐÃ DUYỆT của TP-07.
""")

p("tuan", "Chỉ rút công thức WIN", "khi muốn làm dày TP-07 trước", """
TUẦN — chỉ PHẦN 2.

Đọc các hội thoại RA SỐ trong mau-ai.md (tầng HOT_RA_SO và WARM_RA_SO).
Ưu tiên ca khó: khách đã hỏi giá · khách nêu sợ biến chứng · inbox đến ban đêm.

Trả về 4 bảng:
1. Nhịp hội thoại: xin số ở lượt NV thứ mấy, sau câu nào. Kèm phân bố.
2. Câu xin số thắng — nguyên văn, nhóm theo dịch vụ. Mỗi câu ghi nó gắn LỢI ÍCH gì.
3. Câu xử lý từ chối thắng — nhóm theo rào cản: GIA · SO_BIEN_CHUNG ·
   CHUA_TIN_BAC_SI · DAU_NGHI · XA_THOI_GIAN · NGUOI_NHA · BAO_HANH.
4. Câu nhắn lại thắng.

Mỗi câu kèm: HT-xxxxxxxx làm bằng · số lần thấy · trạng thái ⏳ CHỜ DUYỆT.
⛔ Câu nào nêu con số giá hoặc con số bảo hành → gắn 🔴, ⛔ không đưa vào bảng.
⛔ Không lấy câu từ hội thoại có lỗi nghiêm trọng LN-1…6.
""")

p("tuan", "Xếp lỗi Fail trên 100% hội thoại", "trả lời câu hỏi 'code làm được không'", """
Đọc out/<ky>/ht.csv kèm theo (toàn bộ hội thoại, không phải mẫu).

Tách rõ hai phần:

PHẦN CODE ĐÃ ĐẾM ĐƯỢC — làm trên 100% hội thoại, ⛔ không lấy mẫu:
  F1 không có lượt xin số nào        → cột da_xin_so = 0
  F2 xin quá muộn                     → luot_nv_xin_dau > 4 hoặc phut_den_xin_dau > 5
  F3 tư vấn dài mà không chốt         → phien_dai_chua_xin = 1
  F4 không chạm lại trong 24h         → cham_lai_24h = 0 ở hội thoại chưa ra số
  F5 bỏ sót trong cùng ca             → bo_sot_trong_ca = 1
  Mỗi dạng: số hội thoại · % mẫu · CR48 của nhóm đó · chiều cắt nặng nhất.

PHẦN PHẢI ĐỌC — chỉ nhóm nguyên nhân ⑤ kỹ năng XLTC:
  "NV đã xử lý rào cản đúng mẫu chưa" — ⛔ code không làm được.
  Đọc trên mau-ai.md, ⛔ không suy từ ht.csv.

Kết bằng một câu: trong tuần này, bao nhiêu phần trăm lỗi mất số đã quy được
bằng code, và bao nhiêu còn phải đọc?
""")

# ── nhóm: COACH ──
p("coach", "Giáo án cho nhóm C", "kèm 1-1, 20 phút/ngày", """
COACH Nhóm C

Kèm: kết quả chấm rubric TP-05 · knowledge/TP-07 · out/<ky>/mau-ai.md.

Xuất đúng khuôn TP-06 §5:
Mục tiêu        : một câu, ĐO ĐƯỢC (ví dụ "đưa % đã xin số của nhóm từ 38% lên 55%")
3 hội thoại đề  : mã + 1 dòng vì sao chọn. ⛔ Lấy từ mau-ai.md, không tự bịa tình huống.
Câu mẫu         : nguyên văn từ TP-07. ⛔ Không có trong TP-07 thì ghi
                  "⏳ chưa có câu đã duyệt cho rào cản này" — không tự viết rồi coi như chuẩn.
Bài tập roleplay: tình huống + rào cản cụ thể
Chỉ số nghiệm thu sau 1 tuần: chỉ số + mốc + lấy ở đâu trong so.json
Thời lượng      : 20 phút/ngày, kèm 1-1 với một bạn nhóm A

⛔ Giáo án cho nhóm KHÔNG nêu tên cá nhân kèm điểm. Phần cá nhân nằm ở lệnh NV.
⛔ Bạn nào chưa đủ 10 HT thì không đưa vào giáo án cá nhân.
""")

p("coach", "Roleplay theo rào cản 'khách hỏi giá'", "rào cản chiếm 55% hội thoại", """
COACH Nhóm B — chỉ một rào cản: GIA (khách hỏi giá ngay từ tin đầu).

Dựng bài roleplay 30 phút:
1. Bối cảnh: lấy 3 hội thoại thật từ mau-ai.md có rào cản GIA và KHÔNG ra số.
   Với mỗi cái, ghi: khách nói gì · NV đã trả lời gì · mất số ở bước nào.
2. Ba kịch bản roleplay, mỗi kịch bản có: câu khách mở đầu · hai câu phản đối tiếp
   · điều kiện đạt (xin được số trước tin NV thứ 4).
3. Chuẩn ba nhịp phải thấy trong mọi lượt đạt:
   hỏi tình trạng → trao giá trị sơ bộ → xin số gắn lợi ích.
4. Checklist 5 ô cho người quan sát tick.
5. Chỉ số nghiệm thu sau 1 tuần + lấy ở đâu.

⛔ Không để câu mẫu nào nêu con số giá — chưa có bảng giá hiện hành.
""")

p("coach", "Mini-training 15 phút đầu ca tối", "khung 18–22h đang là khung yếu nhất", """
COACH ca tối (khung 18–22h)

Bối cảnh đo được: khung 18–22h là khung ĐÔNG NHẤT (26,6% inbox) nhưng CR24 THẤP
NHẤT trong giờ trực (19,8%), trong khi FRT vẫn tốt (1,4 phút). Tức là không thiếu
người — lỗi nằm ở kịch bản/kỹ năng.

Dựng mini-training 15 phút, đúng MỘT nội dung, không dạy nhiều thứ:
- Vấn đề: nói bằng một câu có số.
- Một hành vi cần đổi: cụ thể, quan sát được.
- Hai câu mẫu từ TP-07, nguyên văn, in ra dán lên bảng ca.
- Hai hội thoại thật của chính ca tối làm đề (mã + trích câu).
- Cách đo: chỉ số nào, mốc nào, đọc ở báo cáo ngày nào.

⛔ Không quá 1 trang. ⛔ Không nêu tên cá nhân kèm điểm.
""")

p("coach", "Giáo án theo dịch vụ yếu nhất", "dịch vụ giá trị cao mà CR thấp", """
COACH dịch vụ <tên dịch vụ>

Đọc bao-cao.md mục 5 kèm theo. Trả lời trước hai câu kiểm:
1. Cỡ mẫu của dịch vụ này là bao nhiêu? Dưới 30 thì gắn nhãn MẪU NHỎ và nói rõ
   kết luận chỉ ở mức giả thuyết.
2. Dịch vụ này thấp ở ĐÂU: % đã xin số, hay tỷ lệ xin được, hay FRT? Dẫn số.

Rồi dựng mini-training 15 phút × 3 ngày đầu ca:
- Ngày 1: kiến thức dịch vụ — ba câu khách hay hỏi nhất, câu trả lời đúng.
- Ngày 2: câu trao giá trị sơ bộ cho dịch vụ này (nói bằng TÌNH TRẠNG, ⛔ không
  bằng tính từ marketing).
- Ngày 3: câu xin số gắn lợi ích cho đúng dịch vụ này.
Chỉ số nghiệm thu: CR48 của dịch vụ, đọc ở báo cáo <ngày>.

🔴 Nếu dịch vụ này là nhóm KHAC (chưa có trong danh sách chốt của note §3) thì nói
rõ: chưa có mục tiêu CR để so, cần QL chốt trước.
""")

# ── nhóm: HT ──
p("ht", "Chấm một hội thoại theo rubric", "dùng khi QL muốn soi một ca cụ thể", """
HT <mã hội thoại>

Chấm theo TP-05, ghi đúng khuôn §4:

HT-xxxxxxxx · <dịch vụ> · NV-xxxxxxxxx · <tầng mẫu>
KF-60: HOT | WARM | COLD        (★ điểm của BẠN, ⛔ không copy nhiet_loc của script)
KF-62: <mã chân dung>           (tra thư viện, ⛔ không tự đặt)
Q1 ..  Q2 ..  Q3 ..  Q4 ..  Q5 ..  Q6 ..  → Tổng ../100   🟢🟡🔴
Lỗi nghiêm trọng: — | LN-n
Vì sao rơi: nội dung | trực page | hệ thống | khách tự dừng | không rơi  (ĐÚNG MỘT giá trị)
Bằng chứng: "<trích nguyên văn>"
Việc: <một hành động, kèm câu mẫu dùng được ngay>

⚠ Q1 và phần nhịp của Q5 lấy THẲNG từ cột trong ht.csv — ⛔ không ước lượng lại
  thời gian hay số lượt.
⚠ Tiêu chí không phát sinh thì ghi "—" và loại khỏi mẫu số, ⛔ không tính là trượt.
""")

p("ht", "Viết lại một hội thoại đã mất số", "để làm đề roleplay", """
HT <mã hội thoại> — hội thoại này đã mất số.

Làm ba việc:
1. Chỉ ra ĐÚNG MỘT bước mà số bị mất. Trích câu NV ngay trước và ngay sau bước đó.
2. Viết lại đoạn từ bước đó trở đi, giữ nguyên lời khách, chỉ đổi lời NV.
   Bản viết lại phải: trả lời câu khách hỏi → trao giá trị sơ bộ bằng tình trạng
   → xin số gắn lợi ích, trong tối đa 3 tin NV.
3. Nói rõ bản viết lại của bạn lấy câu từ đâu: TP-07 mã nào, hay là bạn tự viết.
   Nếu tự viết thì ghi "⏳ chưa duyệt — cần QL trực page chốt".

⛔ Không nêu con số giá. ⛔ Không cam kết kết quả. ⛔ Không nêu con số bảo hành.
⛔ Không trả lời câu bệnh nền thay bác sĩ.
""")

# ── nhóm: khi bị chặn ──
p("chan", "Agent báo thiếu TP-04 — làm gì tiếp", "chạy được 8/10 mục mà không cần master data", """
TP-04 chưa điền được (chưa có bản đồ mã NV → tên · nhóm · hạng).

Cho tôi biết chính xác:
1. Những mục nào của Báo cáo Sáng VẪN chạy đủ, không cần TP-04.
2. Những mục nào phải in theo mã NV, cột Nhóm/Hạng ghi "⚠ thiếu TP-04".
3. Những mục nào ⛔ KHÔNG được chạy, và nếu chạy thì sai ở đâu.
4. Một bản đề nghị gửi QL trực page: cần đúng những thông tin gì, định dạng nào,
   mất của họ khoảng bao lâu. Viết thành tin nhắn gửi được ngay, ≤ 8 dòng.

⛔ Đừng tự ghép 16 tên QL cho 40 mã NV.
""")

p("chan", "Mục tiêu còn 'demo' — đọc cờ RAG thế nào", "trước khi anh/QL chốt số", """
Toàn bộ mục tiêu trong tools/muc-tieu.json còn ở trạng thái "demo".

Trả lời bốn câu:
1. Cờ 🟢🟡🔴 trong báo cáo hiện có dùng được để ra quyết định không? Vì sao?
2. Những chỉ số nào mà kết luận KHÔNG phụ thuộc mục tiêu — tức là đúng dù chốt
   mốc nào? (ví dụ: so giữa hai khung giờ, so giữa hai nhân viên cùng ô)
3. Những chỉ số nào mà đổi mục tiêu là đổi hẳn kết luận?
4. Năm con số nào cần anh/QL chốt TRƯỚC NHẤT, xếp theo mức ảnh hưởng. Mỗi dòng
   kèm: con số demo hiện tại · số thực tế đo được · chênh bao nhiêu.
""")

p("chan", "Soát một chỉ số không đo được", "khi có người hỏi 'sao không có số này'", """
Có người hỏi tôi về chỉ số: <tên chỉ số>.

Trả lời theo đúng ba bước:
1. Chỉ số này có đo được trên bản xuất Caresoft hiện tại không? Mở TP-02 §8 và
   TP-03 §4 để trả lời, ⛔ không trả lời từ trí nhớ.
2. Nếu KHÔNG: thiếu cột/trường nào, ai mở được, và trong lúc chờ thì chỉ số nào
   thay thế gần nhất (nói rõ nó KHÁC chỗ nào, ⛔ không coi là tương đương).
3. Nếu CÓ: nó nằm ở mục nào của bao-cao.md, cột nào của ht.csv, cỡ mẫu bao nhiêu.

⛔ Không ước lượng. ⛔ Không lấy số của chiều khác gán sang.
""")

p("chan", "Nghi dữ liệu lệch", "khi số nhảy bất thường", """
KIỂM

Đọc phiếu chất lượng dữ liệu kèm theo. Trả lời:
1. Ba ngưỡng DỪNG có cái nào vượt không? (hội thoại lệch header · dòng lạ > 0 ·
   thiếu dòng Kỳ)
2. Ba ngưỡng cảnh báo: phủ dịch vụ < 85% · phủ nhân viên < 95% · hội thoại treo > 5%?
3. Số hội thoại có lượt trả lời "sau kỳ" là bao nhiêu — có đủ lớn để làm lệch
   FRT của kỳ không?
4. Nếu một chỉ số nhảy bất thường, kiểm theo thứ tự nào: dữ liệu → định nghĩa →
   hành vi thật? Cho tôi 3 câu lệnh tp.py cụ thể để kiểm.

⛔ Chưa loại được khả năng lỗi dữ liệu thì ⛔ không kết luận về con người.
""")


NHOM = [
    ("all", "Tất cả"),
    ("setup", "Cài đặt & kiểm"),
    ("ngay", "NGÀY"),
    ("trua", "TRƯA"),
    ("nv", "NV"),
    ("tuan", "TUẦN"),
    ("coach", "COACH"),
    ("ht", "HT"),
    ("chan", "Khi bị chặn"),
]


# ───────────────────────── DỰNG TRANG ─────────────────────────

def e(s):
    return html.escape(s, quote=True)


def kiem_trang(page):
    """Ba cổng kiểm trước khi ghi file. ⛔ Lỗi nào ở đây cũng HỎNG ÂM THẦM:
    trang vẫn mở được, vẫn có chữ, chỉ sai — nên phải chặn ở đây, không để mắt soát.

    ⚠ DI SẢN: bản v2 từng mất 4 dấu `}` đóng media query vì một lệnh gỡ ngoặc
    nhân đôi quét cả khối CSS. Hậu quả: từ `@media(max-width:720px)` trở xuống,
    mọi rule bị nhốt trong media query đó → chết hết trên màn hình rộng.
    """
    loi = []

    # ① CSS phải cân ngoặc
    i, j = page.index("<style>"), page.index("</style>")
    css = page[i + 7:j]
    lech = css.count("{") - css.count("}")
    if lech:
        loi.append(f"CSS lệch ngoặc: thừa {lech} dấu '{{'" if lech > 0
                   else f"CSS lệch ngoặc: thừa {-lech} dấu '}}'")

    # ② còn placeholder chưa thay
    import re as _re
    con = sorted(set(_re.findall(r"__[A-Z][A-Z_]{2,}__", page)))
    if con:
        loi.append("còn placeholder chưa thay: " + ", ".join(con))

    # ③ blob JSON phải parse được và không chứa thẻ đóng script
    m = _re.search(r'<script id="tp-data" type="application/json">(.*?)</script>',
                   page, _re.S)
    if not m:
        loi.append("không tìm thấy khối <script id=\"tp-data\">")
    else:
        if "<" in m.group(1) or ">" in m.group(1):
            loi.append("blob JSON còn ký tự '<' hoặc '>' chưa escape "
                       "→ một chữ '</script>' trong file tri thức sẽ làm trắng toàn bộ nút Copy")
        try:
            d = json.loads(m.group(1))
        except Exception as ex:
            loi.append(f"blob JSON không parse được: {ex}")
        else:
            rong = [k for k, v in d.items() if not v]
            if rong:
                loi.append("khóa rỗng trong blob: " + ", ".join(rong))

    # ④ mỗi tài liệu nhúng phải khớp TỪNG KÝ TỰ với file trên đĩa
    if m:
        try:
            d = json.loads(m.group(1))
            for k, path, *_ in FILE:
                if d.get(k, "") != doc(path):
                    loi.append(f"nội dung nhúng lệch file gốc: {path}")
        except Exception:
            pass

    if loi:
        print("🔴 TRANG KHÔNG ĐẠT — ⛔ không ghi file:", file=sys.stderr)
        for x in loi:
            print("   · " + x, file=sys.stderr)
        raise SystemExit(1)
    print(f"✅ kiểm: CSS cân ngoặc · không còn placeholder · "
          f"blob JSON parse được · {len(FILE)} file nhúng khớp từng ký tự")


def main():
    data = {}
    thieu = []
    for k, path, *_ in FILE:
        try:
            data[k] = doc(path)
        except FileNotFoundError:
            thieu.append(path)
            data[k] = ""
    # Thẻ C · 7 sổ nối liền — cho nền tảng chặn upload nhiều file.
    # Có dòng phân cách để agent biết ranh giữa các sổ, ⛔ không nối trơn.
    gop = []
    for k, path, ten, badge, _ in FILE:
        if not badge.startswith("UPLOAD"):
            continue
        gop.append(f"\n\n{'=' * 78}\n=== {ten}  ·  nguồn: {path}\n{'=' * 78}\n\n" + data[k])
    data["C"] = ("# TRI THỨC GỘP · Agent-QCQA-TrucPage-Kangnam\n"
                 "# 7 sổ TP-01…TP-07 nối liền. Mỗi sổ mở đầu bằng một dòng ===.\n"
                 "# ⛔ Đây là bản tiện dụng; bản chuẩn vẫn là 7 file rời trong knowledge/."
                 + "".join(gop))

    for x in P:
        data[f"P{x['n']}"] = x["s"]

    if thieu:
        print("⚠ không đọc được: " + ", ".join(thieu))

    # ── thẻ file: đúng cấu trúc .fcard của mẫu ──
    #    .fcard-h (fname · fbadge · fsize · nút Copy) → p.fhow → details.fview > pre.filebody
    def the_file(loc):
        out = []
        for k, path, ten, badge, cach in FILE:
            if not loc(badge):
                continue
            n = f"{len(data[k]):,}".replace(",", ".")
            hi = " hi" if "★★" in badge else ""
            no = " no" if badge.startswith("KHÔNG") else ""
            out.append(
                f'<article class="fcard{hi}"><div class="fcard-h">'
                f'<span class="fname">{e(path)}</span>'
                f'<span class="fbadge{no}">{e(badge)}</span>'
                f'<span class="fsize">{n} ký tự</span>'
                f'<button class="copy" data-copy="{k}">Copy</button></div>'
                f'<p class="fhow"><b>{ten}</b> — {cach}</p>'
                f'<details class="fview"><summary>Xem nội dung</summary>'
                f'<pre class="filebody" data-peek="{k}"></pre></details></article>')
        return "\n".join(out)

    # ── ba thẻ dán sẵn: đúng cấu trúc .cc của mẫu ──
    #    span.tag → h3 → p.meta (span.count) → button.btn → details.peek > pre
    def the_cc():
        the = [
            ("A", "Thẻ A", "Bộ não đầy đủ", "Claude &amp; Gemini",
             "§0–§10: vai trò · 7 lệnh · 12 luật bất biến · hai thang nhiệt · P0–P6"),
            ("B", "Thẻ B", "Bản ngắn", "chỉ ChatGPT",
             "Giữ nguyên luật, cắt phần giải thích — bù bằng 7 sổ tri thức"),
            ("C", "Thẻ C", "Tri thức gộp", "khi không upload được nhiều file",
             "7 sổ TP-01…TP-07 nối liền, có dòng phân cách để agent biết ranh sổ"),
        ]
        out = []
        for k, tag, ten, dung, mo_ta in the:
            n = f"{len(data[k]):,}".replace(",", ".")
            tran = (" / 8.000 ký tự" if k == "B" else " ký tự")
            out.append(
                f'    <div class="cc">\n'
                f'      <span class="tag">{tag}</span>\n'
                f'      <h3>{ten}</h3>\n'
                f'      <p class="meta"><span class="count">{n}</span>{tran} · {dung}<br>\n'
                f'        <span class="dim">{mo_ta}</span></p>\n'
                f'      <button class="btn" data-copy="{k}">Copy {tag}</button>\n'
                f'      <details class="peek"><summary>Xem nội dung</summary>'
                f'<pre data-peek="{k}"></pre></details>\n'
                f'    </div>')
        return "\n".join(out)

    nhom_file = {
        "know": lambda b: b.startswith("UPLOAD"),
        "pr": lambda b: b.startswith("KHÔNG"),
    }

    # thẻ prompt
    pr_html = []
    for x in P:
        n = len(x["s"])
        pr_html.append(f"""
    <div class="prompt" data-nhom="{x['nhom']}">
      <div class="prompt-h">
        <span class="n">{x['n']:02d}</span>
        <span class="t">{e(x['t'])}</span>
        <span class="k">{e(x['k'])}</span>
      </div>
      <pre class="prompt-b" data-peek="P{x['n']}"></pre>
      <div class="prompt-f">
        <span class="get">{n:,} ký tự</span>
        <button class="copy" data-copy="P{x['n']}">Copy prompt</button>
      </div>
    </div>""".replace(",", "."))

    chip_nhom = "\n".join(
        f'      <button type="button" data-f="{k}"'
        f'{" aria-pressed=\"true\"" if k == "all" else " aria-pressed=\"false\""}>{e(v)}</button>'
        for k, v in NHOM)

    # ⛔ Escape "<" thành \u003c: một file tri thức có chữ "</script>" sẽ cắt đứt
    #    thẻ <script type="application/json"> và làm TRẮNG toàn bộ nội dung Copy —
    #    hỏng âm thầm, không báo lỗi. Cả "&" và dấu phân đoạn U+2028/2029 cũng vậy.
    blob = (json.dumps(data, ensure_ascii=False)
            .replace("<", "\\u003c").replace(">", "\\u003e")
            .replace("&", "\\u0026")
            .replace("\u2028", "\\u2028").replace("\u2029", "\\u2029"))
    n_prompt = len(P)
    n_char_a = len(data["A"])
    n_char_b = len(data["B"])

    # ⛔ Không dùng .format(): template có đầy ngoặc nhọn của CSS và JS.
    thay = {
        "__REPO__": REPO,
        "__CC__": the_cc(),
        "__FILES_KNOW__": the_file(nhom_file["know"]),
        "__FILES_PR__": the_file(nhom_file["pr"]),
        "__PROMPTS__": "\n".join(pr_html),
        "__CHIPS_NHOM__": chip_nhom,
        "__N_PROMPT__": str(n_prompt),
        "__N_CHAR_A__": f"{n_char_a:,}".replace(",", "."),
        "__N_CHAR_B__": f"{n_char_b:,}".replace(",", "."),
        "__DATA__": blob,
    }
    # Khung HTML nằm ở tools/mau-trang/ — tách khỏi .py để sửa style không phải
    # chạm vào code, và để ⛔ không lặp lại vụ CSS bị một lệnh replace trên chuỗi
    # Python ăn mất dấu ngoặc (xem kiem_trang).
    page = (doc(os.path.join("tools", "mau-trang", "khung-dau.html"))
            + doc(os.path.join("tools", "mau-trang", "khung-than.html")))
    for k, v in thay.items():
        page = page.replace(k, v)

    kiem_trang(page)

    with open(RA, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"✅ {os.path.relpath(RA, GOC)} · {len(page):,} ký tự · "
          f"{n_prompt} prompt mẫu · {len(FILE)} file nhúng".replace(",", "."))
    print(f"👉 Publish file này làm artifact.")



if __name__ == "__main__":
    main()
