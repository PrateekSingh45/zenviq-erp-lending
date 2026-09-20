from datetime import datetime
import random

def verify_aadhaar(aadhaar_number, full_name=None):
    cleaned = (aadhaar_number or "").replace(" ", "").replace("-", "")
    last_four = cleaned[-4:] if len(cleaned) >= 4 else "1234"
    masked = f"XXXXXXXX{last_four}"
    ref_id = f"UIDAI-SBX-{random.randint(10000000, 99999999)}"
    
    return {
        "status": "SUCCESS",
        "mode": "SANDBOX",
        "provider": "UIDAI e-KYC Sandbox (DigiLocker)",
        "verified": True,
        "reference_id": ref_id,
        "masked_aadhaar": masked,
        "name_as_per_aadhaar": full_name or "Rajesh Kumar Sharma",
        "dob": "1988-07-15",
        "gender": "M",
        "address": {
            "house": "42-B",
            "street": "Civil Lines",
            "landmark": "Near Company Garden",
            "city": "Aligarh",
            "state": "Uttar Pradesh",
            "pincode": "202001",
            "country": "India"
        },
        "verified_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "disclaimer": "This is simulated data for demonstration and POC purposes only."
    }

def verify_pan(pan_number, full_name=None):
    pan = (pan_number or "ABCDE1234F").upper().strip()
    return {
        "status": "VALID",
        "mode": "SANDBOX",
        "provider": "NSDL PAN Verification API (Sandbox)",
        "verified": True,
        "pan_number": pan,
        "registered_name": full_name or "RAJESH KUMAR SHARMA",
        "category": "INDIVIDUAL",
        "aadhaar_seeding_status": "LINKED",
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "disclaimer": "This is simulated data for demonstration and POC purposes only."
    }
