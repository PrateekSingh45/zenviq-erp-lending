from datetime import datetime
import random
import hashlib
import time

def send_esign_otp(borrower_name=None, document_type="Loan Agreement"):
    tx_id = f"ESIGN-TXN-{int(time.time())}-{random.randint(1000, 9999)}"
    return {
        "status": "OTP_SENT",
        "mode": "SANDBOX",
        "provider": "Aadhaar eSign Gateway (Sandbox)",
        "transaction_id": tx_id,
        "document_type": document_type,
        "recipient": borrower_name or "Applicant",
        "masked_mobile": "+91 98XXXXXX21",
        "otp_expiry_minutes": 10,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "disclaimer": "Simulated Aadhaar eSign OTP transaction for POC."
    }

def complete_esign(transaction_id=None, document_type="Loan Agreement"):
    tx_id = transaction_id or f"ESIGN-TXN-{int(time.time())}"
    raw_hash_input = f"{tx_id}-{document_type}-{time.time()}"
    sig_hash = hashlib.sha256(raw_hash_input.encode()).hexdigest()[:32].upper()
    
    return {
        "status": "SIGNED",
        "mode": "SANDBOX",
        "provider": "Aadhaar eSign Gateway (Sandbox)",
        "transaction_id": tx_id,
        "document_type": document_type,
        "signature_hash": f"SHA256:{sig_hash}",
        "certificate_issuer": "CCA India eSign CA 2026",
        "signing_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ip_address": "49.36.120.88",
        "audit_trail_reference": f"AUDIT-ZENVIQ-{random.randint(100000, 999999)}",
        "disclaimer": "Simulated Aadhaar digital signature for POC."
    }
