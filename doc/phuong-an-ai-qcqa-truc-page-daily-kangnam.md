# Phương án triển khai AI Project QC/QA Trực page Daily – Kangnam

📅 6/11/2026 · @Someone

## 1. Strategic Insight

Khuyến nghị: xây Project "KANGNAM TPQ – Trực Page QC/QA" theo mô hình **code tính số 100%, AI chỉ đọc chất lượng trên mẫu có chọn lọc**, chạy tự động 2 lần/ngày sau 2 mốc upload, kế thừa KF-60 (chấm nóng/lạnh) và KF-62 (chân dung) đã duyệt.

**Bài toán thật không phải báo cáo, mà là "rò SĐT".** Mỗi inbox đã trả tiền quảng cáo. Inbox không ra số trong 48h gần như là mất chi phí. Tăng tỷ lệ SĐT/inbox là đòn bẩy rẻ nhất trong toàn phễu: không cần thêm ngân sách, CP/SĐT giảm ngay.

**Ba nguyên tắc thiết kế:**

1. **Số liệu phải tính bằng code, không để AI đếm.** Mỗi ngày có hàng trăm đến hàng nghìn hội thoại. AI đếm tay sẽ sai và mỗi ngày sai một kiểu, không so sánh kỳ được.
2. **So nhân viên phải công bằng theo chất lượng inbox nhận được.** Bạn nhận inbox lạnh (hỏi giá, khung đêm) sẽ luôn thua bạn nhận inbox nóng. Cần chỉ số "thực tế ÷ kỳ vọng", nếu không TOP A có thể chỉ là "TOP inbox ngon". >> Chia theo khung giờ, bao gồm cả SLA: 8h00 – 21h30 (không bao gồm giờ làm việc + thời gian đào mess buổi sáng).
3. **Mỗi báo cáo phải ra việc cụ thể có mã hội thoại.** QL phải biết nhân viên nào cần xử lí gấp việc gì, các việc cần ưu tiên cho cả team.

**4 bước tư duy của hệ thống:** Mục tiêu = Conversion (SĐT/inbox) → Phân khúc = inbox mới giai đoạn Warm/Hot chưa số → Vai trò = cửa chuyển đổi đầu tiên của hệ sinh thái → Đòn bẩy 80/20 = Hot chưa số + SLA khung giờ yếu + 2–3 nhân viên nhóm C nhận nhiều inbox nóng.

## 2. Ba phương án triển khai

Chọn **PA2** để chạy ngay trong 2 tuần; PA3 là đích đến khi khối lượng vượt ~1.500 hội thoại/ngày hoặc cần dashboard thời gian thực.

| Tiêu chí | PA1 – Project thủ công | PA2 – Project + lịch tự động (khuyến nghị) | PA3 – Pipeline đầy đủ |
|---|---|---|---|
| Cách chạy | QL tải file lên chat, gõ lệnh `NGÀY` | Scheduled task 8:45 và 13:15 đọc folder Google Drive, code tính sẵn bộ chỉ số >> AI đọc và phân tích | Caresoft API → kho dữ liệu (BigQuery/Sheets) → Looker Studio; AI chỉ làm lớp chẩn đoán & coaching |
| Thời gian lên | 3–5 ngày | 1 tuần (gồm 1 tuần hiệu chỉnh) | 6–8 tuần, cần IT/Caresoft |
| Phụ thuộc người | Cao: quên upload/quên gõ là mất ngày | Thấp: chỉ cần file đúng giờ, đúng tên | Rất thấp |
| Độ nhất quán số liệu | Trung bình | Cao (cùng 1 script tính) | Cao nhất |
| Giới hạn khối lượng AI đọc | ~150–200 hội thoại/lần | 100% tính số; AI đọc 80–150 hội thoại mẫu/lần (cân nhắc để code chạy lọc trước, chia tách các phần số liệu về tương tác 1 lần, phân chia độ nóng data) | Không giới hạn (AI qua API theo lô) |
| So sánh 7 ngày/cùng kỳ | Khó, phải tải lại file cũ | Có, lịch sử lưu vào 1 Google Sheet tổng | Có, sẵn trong kho |
| Chi phí bổ sung | 0 | 0 (dùng gói Claude hiện có) | API + hạ tầng + IT |
| Phù hợp với quyết định D22 (chưa làm pipeline Caresoft) | Đúng | Đúng | Cần anh duyệt lại |

**Vì sao PA2:** giữ đúng nhịp anh đã đặt (8:30 và 13:00), không cần IT, và tách rõ việc của code (đếm) với việc của AI (đọc, chẩn đoán, viết câu gợi ý). Khi lên PA3, bộ định nghĩa chỉ số và rubric của PA2 dùng lại nguyên vẹn.

**Nếu chưa bật được lịch tự động:** chạy PA1 tuần đầu với cùng bộ knowledge file, chỉ khác là QL gõ lệnh tay.

## 3. Kiến trúc hệ thống

Hệ thống có 5 lớp; lớp 1–2 là code (đúng tuyệt đối, lặp lại được), lớp 3–5 là AI (đọc, chẩn đoán, ra việc).

| Lớp | Làm gì | AI/công cụ | Đầu ra |
|---|---|---|---|
| L0 – Nạp & kiểm dữ liệu | Đọc file mới trong folder, kiểm cột, gộp trùng tin nhắn giữa file 13h và file 8h30 hôm sau, lọc spam/khách cũ/tuyển dụng | Python | Phiếu chất lượng dữ liệu (số dòng, % thiếu cột, cảnh báo) |
| L1 – Máy tính chỉ số | Đếm inbox mới, SĐT, thời gian phản hồi, cohort khung giờ, so kỳ; ghi nối tiếp vào Sheet lịch sử | Python + Google Sheet tổng | Bảng số theo Nhóm/NV/Dịch vụ/Page/Thị trường |
| L2 – AI chấm hội thoại | Chấm KF-60 (Hot/Warm/Cold), gán chân dung KF-62, chấm rubric tư vấn TP-05 trên mẫu phân tầng | Claude, lô ≤ 40 hội thoại | JSON từng hội thoại + bằng chứng trích câu |
| L3 – Chẩn đoán | Ghép số (L1) với chất lượng (L2) → cây nguyên nhân 6 nhóm | Claude | 3 vấn đề lớn nhất trong ngày, có số |
| L4 – Danh sách việc | Chọn hội thoại ưu tiên, giao NV, gợi ý câu nhắn tiếp | Luật + Claude | Bảng việc có mã hội thoại, hạn xử lý |
| L5 – Học theo tuần | Tổng hợp WIN/Fail, cập nhật kịch bản chuẩn, gợi ý giáo án coaching | Claude, thứ 2 hàng tuần | TP-07 Thư viện WIN (chờ anh duyệt) |

**Bộ knowledge file cần xây cho Project mới (TP = Trực Page):**

| File | Nội dung | Trạng thái |
|---|---|---|
| TP-01 Instructions | Vai trò, lệnh (`NGÀY`, `TRƯA`, `NV <tên>`, `TUẦN`, `COACH`), quy tắc cứng | Cần viết |
| TP-02 CORE chỉ số | Định nghĩa, công thức, ngưỡng RAG, quy tắc so kỳ (mục 4) | Cần viết |
| TP-03 Đặc tả dữ liệu | Cột Caresoft bắt buộc, quy ước tên file, che dữ liệu cá nhân | Mở rộng từ KF-67-03 (chế độ B) |
| TP-04 Master data | 1. Nhóm<br>2. Danh sách NV = Mã NV caresoft<br>3. Cách chia hạng A, B, C<br>4. Hệ thống page, dịch vụ, thị trường, tài khoản QC | Anh/QL cung cấp |
| TP-05 Rubric QA hội thoại | Chấm kịch bản, kỹ năng XLTC, quy trình, chăm sóc lại (mục 5) | Cần viết |
| TP-06 Mẫu báo cáo | Báo cáo Sáng, Nhịp Trưa, Tuần | Cần viết |
| TP-07 Thư viện WIN/Fail | Kịch bản chuẩn, câu mẫu theo dịch vụ/rào cản; cập nhật hàng tuần | Sinh ra từ tuần 1 |
| Dùng lại | KF-60 chấm nóng/lạnh, KF-62 chân dung, KF-11 tuân thủ | Đã có |

## 4. Đầu ra 1 – Bộ chỉ số đánh giá trực page

Chỉ số gốc là **CR48 = SĐT thô mới xin được trong 48h ÷ inbox mới**. Mọi chỉ số khác để giải thích vì sao CR48 tăng/giảm.

### 4.1 Định nghĩa chuẩn (phải chốt trước khi chạy)

| Chỉ số | Định nghĩa đề xuất | Vì sao quan trọng |
|---|---|---|
| Inbox mới | Hội thoại có tin đầu tiên của khách trong kì, khách chưa nhắn page đó trong 30 ngày. Loại spam, tuyển dụng, đối tác, khách cũ hỏi lịch (tách thành "inbox chăm sóc") | Không tách thì CR bị pha loãng hoặc bơm phồng |
| SĐT thô | Khách gửi dãy số VN hợp lệ (10 số, đầu 03/05/07/08/09 hoặc +84) hoặc Zalo; mỗi khách tính 1 lần. Ưu tiên trường SĐT của Caresoft nếu có | Đếm bằng regex + cờ Caresoft, không để AI đoán |
| CR24 / CR48 | Inbox mới ra SĐT trong 24h/48h tính từ tin đầu tiên ÷ inbox mới | Đo đúng năng lực, không phụ thuộc giờ khách nhắn |
| FRT | Thời gian phản hồi chung của cả hội thoại của người (không tính bot), trung vị + % trong SLA | Nguyên nhân số 1 của mất số ở khung tối/đêm |
| Tỷ lệ xin số | SĐT thô ÷ hội thoại | Đo chất lượng câu xin số |
| Hot chưa số tồn | Hội thoại KF-60 = HOT_CHUA_SO chưa có số sau 2h | Việc phải xử lý ngay |
| CEI (chỉ số hiệu quả điều chỉnh) | CR thực tế của NV ÷ CR kỳ vọng. CR kỳ vọng = CR trung bình team theo từng ô (dịch vụ × nhiệt độ × khung giờ), cộng theo số inbox NV nhận ở mỗi ô | So NV công bằng; CEI ≥ 1,1 là giỏi thật, không phải nhờ inbox ngon |

**Quy tắc "chốt" và "tạm".** File 8:30 chỉ có tin đến hết D-1, nên CR24 của inbox D-1 chưa đủ 24h. Báo cáo sáng ngày D ghi: CR24 **chốt** cho inbox D-2, CR48 **chốt** cho inbox D-3, CR **tạm** cho inbox D-1. Không đánh giá NV bằng số tạm.

### 4.2 So sánh kỳ (mọi bảng đều có 4 cột so)

| So với | Dùng để |
|---|---|
| Ngày trước (kỳ trước) | Phát hiện sự cố ngay |
| Cùng thứ tuần trước (cùng kỳ) | Loại ảnh hưởng thứ trong tuần (cuối tuần inbox khác hẳn) |
| 7 ngày gần nhất vs 7 ngày trước đó | Xu hướng thật, bỏ nhiễu ngày |

**Chiều cắt:** Nhóm · Nhân viên · Dịch vụ · Page · Thị trường (Hà Nội / Hồ Chí Minh / Các tỉnh khác / VN / Việt kiều / Quốc tế). Mẫu < 30 inbox/ô → gắn nhãn "mẫu nhỏ", gộp 7 ngày, không xếp hạng.

### 4.3 Ma trận cohort khung giờ (Inbox → SĐT thô)

Mỗi dòng là khung giờ inbox đến; mỗi cột là % đã ra số sau mốc thời gian. Ô tô màu nhiệt (đỏ = thấp hơn trung bình 7 ngày ≥ 20%).

| Khung giờ inbox | Inbox | FRT trung vị (phút) | ≤ 15 phút | ≤ 1h | ≤ 4h | ≤ 24h | ≤ 48h | Nhân viên |
|---|---|---|---|---|---|---|---|---|
| 00–07h | | | | | | | | |
| 07–09h | | | | | | | | |
| 09–11h | | | | | | | | |
| 11–13h | | | | | | | | |
| 13–15h | | | | | | | | |
| 15–17h | | | | | | | | |
| 17–19h | | | | | | | | |
| 19–21h | | | | | | | | |
| 21–24h | | | | | | | | |

**Cách đọc:** FRT cao + "≤ 1h" thấp = thiếu người ca đó. FRT tốt mà "≤ 24h" vẫn thấp = lỗi kịch bản/kỹ năng. Khoảng cách "≤ 24h" → "≤ 48h" lớn = chăm sóc lại đang có tác dụng, nên nhân rộng.

=>> Đưa ra nhận định chung và phân tích các vấn đề nóng: Nhân viên nào tốt ở đâu, khung giờ nào? Có nên phân tích theo page không?

## 5. Đầu ra 2 – Phân tích nguyên nhân & giải pháp

AI chẩn đoán theo thứ tự cố định: loại nguyên nhân ngoài trực page trước (chất lượng inbox, phân bổ), rồi mới quy lỗi cho quy trình, kịch bản, kỹ năng. Mỗi kết luận phải có số + 1–2 hội thoại bằng chứng + Quy mô lỗi đang gặp thực tế/tổng hội thoại nhận.

Phân rã cốt lõi: **SĐT = Inbox mới × % phản hồi đúng SLA × Tỷ lệ xin số + SĐT từ chăm sóc lại**. Về nào rơi nhiều nhất so với 7 ngày là nơi đào sâu.

| # | Nhóm nguyên nhân | Tín hiệu đo (code / AI) | Ngưỡng nghi vấn (tạm, hiệu chỉnh sau 2 tuần) | Giải pháp mẫu |
|---|---|---|---|---|
| 1 | Chất lượng inbox | % Cold, % "chỉ hỏi giá", % chưa rõ nhu cầu (KF-60/62) theo page/QC | % Warm+Hot giảm ≥ 15% so với 7 ngày | Chuyển Performance: QC/page nào kéo inbox lạnh; không quy lỗi NV |
| 2 | Phân bổ inbox không hợp lý | Inbox/NV/ca so với năng lực; % Hot giao cho nhóm C; NV xử lý > X hội thoại song song | Nhóm C nhận > 25% Hot; NV vượt 1,3× tải trung bình ca | Luật chia: Hot/PTTM giá trị cao ưu tiên nhóm A; trần tải/ca; nhóm C nhận Beauty/Spa + có kèm cặp |
| 3 | Quy trình (SLA) | FRT, % trong SLA, khoảng lặng giữa 2 lượt trả lời, khách nhắn cuối mà không ai trả | FRT trung vị > 5 phút giờ hành chính; > 15 phút ngoài giờ | Xếp lại ca theo ma trận cohort; bot chào + 2 nút hỏi nhanh ban đêm; cảnh báo tồn đọng |
| 4 | Kịch bản tư vấn | % đã xin số; xin số ở lượt thứ mấy; câu xin có gắn lợi ích không; có hỏi "2 câu vàng" phân loại nhu cầu không | % đã xin số < 70%; xin số sau lượt 6 | Chuẩn hóa 3 nhịp: hỏi nhu cầu → trao giá trị sơ bộ → xin số gắn lợi ích ("bác sĩ xem ảnh và gọi tư vấn riêng") |
| 5 | Kỹ năng tư vấn (XLTC) | AI chấm: gặp từ chối (giá, sợ biến chứng, chưa tin bác sĩ, "để suy nghĩ") có xử lý đúng mẫu không; báo giá trần trụi; trả lời dài, rập khuôn | Tỷ lệ xin được < 50% khi đã xin; ≥ 2 lỗi XLTC/10 hội thoại | Thư viện câu XLTC theo rào cản × dịch vụ (lấy từ hội thoại thắng của nhóm A); roleplay 15 phút/ngày |
| 6 | Chăm sóc, tái khai thác | % hội thoại chưa số được nhắn lại trong 24h; SĐT ra từ lượt nhắn lại | < 60% Warm chưa số được nhắn lại trong 24h | Chuỗi nhắn lại 3 nhịp trong cửa sổ 24h của Meta (giờ thứ 2 · 6 · 22 tính từ tin cuối của khách); quá 24h → chuyển remarketing/CDP |

**Đầu ra chẩn đoán mỗi ngày:** tối đa 3 vấn đề, mỗi vấn đề gồm: số (ví dụ "CR48 khung 19–21h = 18% so với 31% trung bình"), nhóm nguyên nhân, người chịu trách nhiệm (Trực page / QL ca / Performance / Sale), việc cụ thể, hội thoại bằng chứng.

## 6. Đầu ra 3 – Việc cần xử lý trong ngày

Mỗi lần chạy xuất một bảng "Việc hôm nay" tối đa 30 dòng, mỗi dòng = 1 mã hội thoại + NV xử lý + câu gợi ý nhắn tiếp. QL trực page giao trong 10 phút đầu ca.

### 6.1 Luật xếp ưu tiên hội thoại

| Ưu tiên | Loại hội thoại | Cách nhận diện | Hạn xử lý | Ai |
|---|---|---|---|---|
| P0 | Cảnh báo đỏ N4 (khiếu nại, biến chứng, dọa đăng mạng) | KF-60 N4 / từ khóa | ≤ 30 phút | QL chi nhánh + CSKH |
| P1 | Hot chưa số, còn trong cửa sổ 24h của Meta | KF-60 HOT_CHUA_SO, tin cuối của khách < 24h | Trước 10h (báo cáo sáng) / trước 14h (trưa) | NV nhóm A hoặc NV cũ nếu là A/B |
| P2 | Khách nhắn cuối, chưa ai trả lời | Tin cuối = KHÁCH, > 15 phút | Ngay | NV đang giữ hội thoại |
| P3 | Warm chưa số, cửa sổ 24h sắp đóng (còn < 6h) | Thời điểm tin cuối của khách | Trước khi hết 24h | NV giữ hội thoại |
| P4 | Đã xin số bị từ chối, chưa thử cách xin thứ 2 | AI đọc: từ chối + không có lượt xin lại | Trong ca | NV giữ hội thoại, có câu mẫu TP-07 |
| P5 | Có SĐT nhưng chưa thấy bàn giao Sale | Có SĐT, không có tag bàn giao/lead Caresoft | Trong ca | Admin Sale |
| P6 | Inbox lạnh quá 24h | Cold/N1 | Tự động | Đưa vào tệp remarketing (CDP) |

Trong cùng mức ưu tiên, xếp theo: điểm KF-60 cao → dịch vụ giá trị cao (PTTM, Giảm béo, Nha khoa) → cửa sổ 24h còn ít.

### 6.2 Mẫu bảng "Việc hôm nay"

| Ưu tiên | Mã hội thoại | Page / Dịch vụ | NV xử lý | Tình trạng (1 dòng) | Câu gợi ý nhắn tiếp | Hạn | Kết quả |
|---|---|---|---|---|---|---|---|
| P1 | 1029384 | Kangnam Mũi HN / MŨI | [NV] | Khách sửa mũi, đã gửi ảnh, chưa để số | "Bác sĩ đã xem ảnh, muốn gọi 5 phút giải thích hướng sửa cho mình…" | 10:00 | Đã có số / Không phản hồi / Từ chối |

(Dòng mẫu là ví dụ minh họa, không phải dữ liệu thật.)

**Vòng phản hồi:** NV ghi cột "Kết quả" trên Google Sheet. Lần chạy sau tự kiểm tra: hội thoại được giao có ra số không → đo "tỷ lệ cứu được" theo NV và theo câu gợi ý. Đây là nguồn dữ liệu tốt nhất để biết câu nào là mẫu win.

### 6.3 Nhịp vận hành trong ngày

| Giờ | Việc | Ai |
|---|---|---|
| Trước 8:15 | Xuất toàn bộ tin D-1 từ Caresoft, bỏ vào folder đúng tên | Code |
| 8:45 | Hệ thống chạy Báo cáo Sáng: chỉ số chốt + chẩn đoán + Việc hôm nay | AI |
| 9:00 | QL giao việc, họp đầu ca 10 phút (1 vấn đề + 1 câu mẫu của ngày) | QL trực page |
| Trước 13:05 | Xuất tin từ 0h đến 13:00 hôm nay | Code |
| 13:30 | Nhịp Trưa: inbox buổi sáng, việc sáng chưa xong, Hot/Warm cần cứu trước khi hết 24h | AI |
| 17:00 | QL chốt cột Kết quả, bàn giao ca tối | QL trực page |

## 7. Đầu ra 4 – Chu kỳ tuần: công thức WIN, bài học Fail, coaching

Thứ 2 hàng tuần, lệnh `TUẦN` xuất 3 phần. Mọi thay đổi kịch bản chuẩn đều ở trạng thái "Chờ duyệt" cho đến khi anh hoặc QL trực page chốt.

### 7.1 Xếp hạng bằng dữ liệu, đối chiếu với đánh giá của quản lý

Điểm tuần (thang 100) = **50% CEI** (CR48 điều chỉnh) + **20% SLA** + **20% điểm rubric TP-05** + **10% tỷ lệ cứu được** hội thoại được giao. A ≥ 75, B 55–74, C < 55 (tạm, hiệu chỉnh sau 2 tuần).

Dùng phân loại của quản lý làm **giả thuyết ban đầu** và bộ nhãn để kiểm tra rubric:

| Nhóm (QL đánh giá) | Nhân viên |
|---|---|
| A | Hải Anh, Kiều Hương, Liên, Thắm, Nhi, Hoa |
| B | Mai, Ngọc, Hoài Linh, Đặng Hương, Thành, Lương, Thùy Linh |
| C | Tuyết Nhi, Mỹ Linh, Mỹ Chung |

**Ma trận hiệu chỉnh tuần 1–2:** so hạng theo dữ liệu với hạng QL.

- Nếu ≥ 80% khớp → rubric đáng tin.
- Nếu một bạn A theo QL mà CEI < 0,9 → kiểm tra bạn đó có đang được chia inbox ngon không.
- Nếu một bạn C có CEI ≥ 1,1 → khả năng bạn đó bị giao inbox khó, cần xem lại luật chia.

### 7.2 Công thức WIN từ nhóm A

AI đọc 30–50 hội thoại ra số tốt nhất của nhóm A (ưu tiên ca khó: khách hỏi giá, sợ biến chứng, inbox đêm >> Có nên lọc bằng code không? Tránh để AI tự chọn.), rút ra:

- **Nhịp hội thoại:** xin số ở lượt thứ mấy, sau câu nào.
- **Câu xin số thắng** theo dịch vụ và chân dung (nguyên văn, đã che danh tính).
- **Câu xử lí từ chối thắng** theo từng rào cản: giá, sợ biến chứng, chưa tin bác sĩ, "để em suy nghĩ", "gửi giá qua đây"…
- **Câu nhắn lại thắng** (chăm sóc, tái khai thác).

Mỗi công thức ghi số lần dùng và tỷ lệ ra số; chỉ đưa vào kịch bản chuẩn khi ≥ 10 lần dùng và hơn trung bình team.

### 7.3 Bài học Fail từ nhóm B/C

AI đọc 30–50 hội thoại **Warm/Hot không ra số** của nhóm B/C, xếp lỗi theo 6 nhóm nguyên nhân (mục 5), đếm tần suất, chọn **3 lỗi gây mất số nhiều nhất**. Mỗi lỗi có: câu NV đã nói → vì sao mất → câu nên nói (lấy từ công thức WIN). >>> Code làm được không? Có chuẩn hóa không? Nếu code làm được thì lọc 100% hội thoại, k cần lấy mẫu.

### 7.4 Chương trình coaching tuần

| Đối tượng | Trọng tâm | Hình thức | Thời lượng | Đo sau 1 tuần |
|---|---|---|---|---|
| Nhóm C | 1 lỗi lớn nhất của từng bạn | Kèm cặp 1-1 với 1 bạn A; chấm 10 hội thoại/ngày | 20 phút/ngày | % đã xin số, CEI |
| Nhóm B | 3 lỗi chung của nhóm | Roleplay theo rào cản, dùng hội thoại thật làm đề | 2 buổi × 30 phút | Tỷ lệ xin được |
| Nhóm A | Chuẩn hóa công thức, dịch vụ mới | Viết/duyệt câu mẫu TP-07; làm mentor | 1 buổi | Số công thức được duyệt |
| Theo dịch vụ | Dịch vụ có CR48 giảm nhiều nhất tuần | Mini-training 15 phút đầu ca, kiến thức + câu mẫu | 3 ngày | CR48 dịch vụ |

AI xuất sẵn giáo án: mục tiêu, 3 hội thoại làm đề, câu mẫu, bài tập roleplay, chỉ số nghiệm thu.
