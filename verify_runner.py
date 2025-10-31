import os
import subprocess

# === Đường dẫn cấu hình ===
BASE = r"D:\PDF_SIGN_PROJECT_\output"
SIGNED_PDF = os.path.join(BASE, "BTVN2_signed.pdf")
TAMPERED_PDF = os.path.join(BASE, "tampered.pdf")
VERIFY_SCRIPT = os.path.join(r"D:\PDF_SIGN_PROJECT_", "verify_pdf_signature.py")
LOG_FILE = os.path.join(BASE, "verify_log.txt")

# --- 1️⃣ Tạo file tampered.pdf ---
with open(SIGNED_PDF, "rb") as f:
    data = f.read()

tampered = data + b"\n%Tampered content added after signature%\n"
with open(TAMPERED_PDF, "wb") as f:
    f.write(tampered)

print("✅ Đã tạo file tampered:", TAMPERED_PDF)

# --- 2️⃣ Chạy verify cho signed.pdf ---
with open(LOG_FILE, "w", encoding="utf-8") as log:
    log.write("=== VERIFY FILE: BTVN2_signed.pdf ===\n")
    subprocess.run(
        ["python", VERIFY_SCRIPT, SIGNED_PDF],
        stdout=log,
        stderr=subprocess.STDOUT,
        text=True,
    )

# --- 3️⃣ Chạy verify cho tampered.pdf ---
with open(LOG_FILE, "a", encoding="utf-8") as log:
    log.write("\n\n=== VERIFY FILE: tampered.pdf ===\n")
    subprocess.run(
        ["python", VERIFY_SCRIPT, TAMPERED_PDF],
        stdout=log,
        stderr=subprocess.STDOUT,
        text=True,
    )

print(f"📄 Xong! Kết quả được lưu tại: {LOG_FILE}")
