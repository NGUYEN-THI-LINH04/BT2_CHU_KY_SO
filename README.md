# BT2_CHU_KY_SO
# BÀI TẬP VỀ NHÀ – MÔN: AN TOÀN VÀ BẢO MẬT THÔNG TIN
# Chủ đề: Chữ ký số trong file PDF
## Giảng viên: Đỗ Duy Cốp
## Nguyễn Thị Linh_K225480106040
I. MÔ TẢ CHUNG
- Sinh viên thực hiện báo cáo và thực hành: phân tích và hiện thực việc nhúng, xác thực chữ ký số trong file PDF.
- Phải nêu rõ chuẩn tham chiếu (PDF 1.7 / PDF 2.0, PAdES/ETSI) và sử dụng công cụ thực thi (ví dụ iText7, OpenSSL, PyPDF, pdf-lib).
II. CÁC YÊU CẦU CỤ THỂ
## 1) Cấu trúc PDF liên quan chữ ký (Nghiên cứu)
- Mô tả ngắn gọn: Catalog, Pages tree, Page object, Resources, Content streams, XObject, AcroForm, Signature field (widget), Signature dictionary (/Sig), /ByteRange, /Contents, incremental updates, và DSS (theo PAdES).
  
- Liệt kê object refs quan trọng và giải thích vai trò của từng object trong lưu/truy xuất chữ ký.
  
- Đầu ra: 1 trang tóm tắt + sơ đồ object (ví dụ: Catalog → Pages → Page → /Contents ; Catalog → /AcroForm → SigField → SigDict).
## 2) Thời gian ký được lưu ở đâu?
- Nêu tất cả vị trí có thể lưu thông tin thời gian:
- /M trong Signature dictionary (dạng text, không có giá trị pháp lý).
- Timestamp token (RFC 3161) trong PKCS#7 (attribute timeStampToken).
- Document timestamp object (PAdES).
- DSS (Document Security Store) nếu có lưu timestamp và dữ liệu xác minh.
- Giải thích khác biệt giữa thông tin thời gian /M và timestamp RFC3161.
## 3) Các bước tạo và lưu chữ ký trong PDF (đã có private RSA)
- Viết script/code thực hiện tuần tự:
1. Chuẩn bị file PDF gốc.
2. Tạo Signature field (AcroForm), reserve vùng /Contents (8192 bytes).
3. Xác định /ByteRange (loại trừ vùng /Contents khỏi hash).
4. Tính hash (SHA-256/512) trên vùng ByteRange.
5. Tạo PKCS#7/CMS detached hoặc CAdES:
- Include messageDigest, signingTime, contentType.
- Include certificate chain.
- (Tùy chọn) thêm RFC3161 timestamp token.
6. Chèn blob DER PKCS#7 vào /Contents (hex/binary) đúng offset.
7. Ghi incremental update.
8. (LTV) Cập nhật DSS với Certs, OCSPs, CRLs, VRI.
- Phải nêu rõ: hash alg, RSA padding, key size, vị trí lưu trong PKCS#7.
- Đầu ra: mã nguồn, file PDF gốc, file PDF đã ký.4) Các bước xác thực chữ ký trên PDF đã ký
## 4) Các bước xác thực chữ ký trên PDF đã ký
- Các bước kiểm tra:
1. Đọc Signature dictionary: /Contents, /ByteRange.
2. Tách PKCS#7, kiểm tra định dạng.
3. Tính hash và so sánh messageDigest.
4. Verify signature bằng public key trong cert.
5. Kiểm tra chain → root trusted CA.
6. Kiểm tra OCSP/CRL.
7. Kiểm tra timestamp token.
8. Kiểm tra incremental update (phát hiện sửa đổi).
9. Nộp kèm script verify + log kiểm thử.
III. QUY TRÌNH THỰC HIỆN
1. Sinh khóa RSA và chứng thư số
- File: create_root_and_signer.py
### Kết quả
- certs/signer_cert.pem
- certs/signer_key.pem
- Ngoài ra nó còn có thêm cả
  + rootCA_cert.pem
  + rootCA_key.pem
2. Tạo và ký file PDF
### File: sign_manual.py
### Thực hiện:
  python sign_manual.py
### Chức năng:
1. Tải file docs/BTVN2.pdf
2. Tạo vùng Signature field (AcroForm)
3. Reserver vùng /Contents 8192 bytes
4. Tính hash SHA-256 trên vùng /ByteRange
5. Sinh ra PKCS#7 detached signature (bao gồm: messageDigest, signingTime, contentType, certificate chain)
6. Ghi blob PKCS#7 vào /Contents
7. Ghi file mới BTVN2_signed.pdf bằng incremental update
### Kết quả
- File BTVN2_signed.pdf(PDF đã có chữ ký số hợp lệ)
  <img width="1920" height="1080" alt="Screenshot 2025-10-31 161906" src="https://github.com/user-attachments/assets/74b0d031-616f-4dc8-858c-bd8695ae6841" />

### 3. Xác mình chữ ký PDF
### File: verify_pdf_signature.py
### Thực hiện:
python verify_pdf_signature.py
### Các bước xác mình:
1. Đọc Signature dictionary: /Contents, /ByteRange
2. Tách chuỗi PKCS#7 từ PDF
3. Kiểm tra messageDigest so với hash thực tế
4. Xác minh chữ ký bằng public key trong signer_cert.pem
5. Kiểm tra chứng thư (chain, validity date)
6. Kiểm tra có bị sửa đổi (so sánh ByteRange)
### Kết quả:
- Xác minh hợp lệ:
<img width="923" height="664" alt="Screenshot 2025-10-31 175831" src="https://github.com/user-attachments/assets/9d39145b-27f4-4349-a5d8-3a73196d2f39" />


  
