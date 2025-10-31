from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime, os

out_dir = r"D:\PDF_SIGN_PROJECT_\certs"
os.makedirs(out_dir, exist_ok=True)

# --- Tạo Root CA ---
root_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
root_subject = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "VN"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "MyRootCA"),
    x509.NameAttribute(NameOID.COMMON_NAME, "NGUYEN THI LINH ROOT CA"),
])
root_cert = (
    x509.CertificateBuilder()
    .subject_name(root_subject)
    .issuer_name(root_subject)
    .public_key(root_key.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.datetime.utcnow() - datetime.timedelta(days=1))
    .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=3650))
    .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
    .sign(root_key, hashes.SHA256())
)
with open(os.path.join(out_dir, "rootCA_key.pem"), "wb") as f:
    f.write(root_key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.TraditionalOpenSSL,
        serialization.NoEncryption(),
    ))
with open(os.path.join(out_dir, "rootCA_cert.pem"), "wb") as f:
    f.write(root_cert.public_bytes(serialization.Encoding.PEM))

# --- Tạo chứng chỉ người ký, ký bởi Root CA ---
user_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
user_subject = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "VN"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Ha Noi"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "Ha Noi"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "MySign"),
    x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, "Digital Signature Unit"),
    x509.NameAttribute(NameOID.COMMON_NAME, "NGUYỄN THỊ LINH"),
])
user_cert = (
    x509.CertificateBuilder()
    .subject_name(user_subject)
    .issuer_name(root_cert.subject)
    .public_key(user_key.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.datetime.utcnow() - datetime.timedelta(days=1))
    .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
    .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
    .sign(private_key=root_key, algorithm=hashes.SHA256())
)
with open(os.path.join(out_dir, "signer_key.pem"), "wb") as f:
    f.write(user_key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.TraditionalOpenSSL,
        serialization.NoEncryption(),
    ))
with open(os.path.join(out_dir, "signer_cert.pem"), "wb") as f:
    f.write(user_cert.public_bytes(serialization.Encoding.PEM))

print("✅ ĐÃ TẠO XONG Root CA + Chứng chỉ người ký (không có email)")
