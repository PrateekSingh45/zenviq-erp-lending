# 🏆 ZENVIQ Step-by-Step Demo Script (Hinglish)

> **Pro Tip:** Keep this script open in a split screen or print it out. Read it naturally. Speak confidently using industry terms (AUM, NPA, FOIR, DPD).

---

## 🔹 Phase 1: The Hook & CEO Cockpit (Minutes 0–4)
**Screen to show:** Slide 6 (CEO Cockpit) or Live Dashboard (`/app/owner-cockpit`)

**What to say:**
"Good morning Sir/Ma'am. Zyada tar ERP presentations boring form-filling se start hoti hain, but main start karna chahunga wahan se jo aapke liye sabse important hai — **Aapka Command Center.**

Ye ZENVIQ ka Executive Owner Cockpit hai. Har subah 8 baje, bina apni finance ya operations team ke Excel sheets ka wait kiye, aapko apne business ka real-time view milta hai:
1. **Total AUM (Asset Under Management):** Live status ki market mein kitna paisa roll ho raha hai.
2. **Collection Efficiency & PAR 30+:** Kitne accounts early warning zone (NPA hone se pehle) mein hain.
3. **Treasury Liquidity:** Aapke paas fresh disbursements ke liye kitna capital available hai.

Tally aur legacy LMS mein ye sab dekhne ke liye 3-4 din ka lag hota hai. ZENVIQ mein ye instant hai. Ab main aapko dikhata hu ki ek borrower ka loan **7 minutes ke andar** kaise process hota hai."

---

## 🔹 Phase 2: Instant Onboarding & eKYC (Minutes 4–8)
**Screen to show:** Live System ➔ Borrower Profile (Rajesh Kumar Sharma)

**What to say:**
"Traditional process mein branch officer ko PAN, Aadhaar aur salary slips collect karne mein 2-3 din lag jate hain. ZENVIQ mein verification **instantaneous** hai.

Yahan dekhiye, single click se hum **Aadhaar eKYC** run karte hain. (Click *Verify Aadhaar*).
Jaise hi hum **Verify PAN** pe click karte hain, NSDL se direct name match ho jata hai.
Aur sabse best part — **Fetch CIBIL**. (Click *Fetch CIBIL*). System automatically bureau report pull karke credit score aur risk grade (jaise 'Low Risk') assign kar deta hai. 

*Abhi demo ke liye humne Sandbox APIs use kiye hain, but actual deployment mein aapke Karza, Perfios, ya CIBIL ke production credentials plug-in ho jayenge.*"

---

## 🔹 Phase 3: Automated Underwriting (Minutes 8–12)
**Screen to show:** Live System ➔ Credit Assessment (ZCRED-00001)

**What to say:**
"Credit manager ko calculator leke FOIR ya Debt-to-Income (DTI) ratio nikalne ki zaroorat nahi hai. 
Aap yahan income analysis dekh sakte hain. System ne automatically **FOIR 27.1%** calculate kar liya hai, jo regulatory guidelines ke bilkul andar hai.

Aapki internal credit policy ke hisaab se system ek 'Underwriting Score' generate karta hai (jaise yahan 98/100 hai) aur **Approve** recommend karta hai. 
Approval ke baad, system directly RBI-compliant **Sanction Letter (KFS - Key Fact Statement)** generate kar deta hai jisme EMI aur interest rates clearly mentioned hote hain."

---

## 🔹 Phase 4: eSign & Auto-Debit Mandate (Minutes 12–15)
**Screen to show:** Live System ➔ eSign Request (ZSGN-00002)

**What to say:**
"Physical ink signatures ab obsolete ho gaye hain. Yahan se hum borrower ko sidha Aadhaar OTP bhejte hain. (Show *Send Aadhaar OTP*).
OTP dalte hi Loan Agreement par **Digital Signature Hash** (SHA256) lag jata hai aur CCA India ka audit trail ban jata hai. 

Sath hi sath, NPCI **eNACH mandate** bhi register ho jata hai with UMRN number. Iska matlab agle mahine se 5 tareekh ko EMI borrower ke bank se seedha auto-debit ho jayegi. No cheque collection, no manual chasing."

---

## 🔹 Phase 5: Double-Entry Ledger & Repayment (Minutes 15–20)
**Screen to show:** Live System ➔ Loan (`ACC-LOAN-2026-00001`) aur uske Repayments

**What to say:**
"Ye ZENVIQ ka sabse bada advantage hai — **Double-Entry General Ledger integration**. 

Market mein zyada tar LMS tools accounting se link nahi hote, jisse finance team ko daily entries manual karni padti hain. ZENVIQ mein jab bhi loan disburse hota hai ya koi EMI aati hai, system automatically usko Principal, Interest Income, aur Penal charges mein split karke General Ledger update kar deta hai. 

Zero reconciliation gap. Month-end closing ab hafton ka nahi, kuch ghanto ka kaam hai."

---

## 🔹 Phase 6: Collections, NPA & DPD Buckets (Minutes 20–25)
**Screen to show:** Live System ➔ Collection Task (`ZCOLL-00001`) & DPD Aging Report

**What to say:**
"Lending business risk manage karne se chalta hai. Agar kisi ki EMI bounce hoti hai, toh system usko auto-detect karke **DPD (Days Past Due)** buckets mein daal deta hai — SMA-0, SMA-1, SMA-2.

Yahan Collection Task mein telecallers call history aur 'Promise to Pay' date log kar sakte hain. System automatically **24% penal interest** charge karta hai aur 90+ days cross hone par account ko NPA mark karke provision calculate kar leta hai. Legal notice bhi single click se generate ho jata hai."

---

## 🔹 Phase 7: Commercial Proposal & Closing (Minutes 25–30)
**Screen to show:** Slide 9 (Pricing Slide)

**What to say:**
"Sir/Ma'am, aapko ek aur generic software nahi chahiye. Aapko ek aisi scalable foundation chahiye jahan aap 500 se 50,000 borrowers tak scale kar sakein bina operations cost badhaye.

Humara pricing model bilkul transparent hai: **Enterprise Dedicated Package (₹10L–₹20L one-time)**.
Isme hum aapko aapke khud ke private cloud (AWS/Azure) par deployment dete hain. 
Unlimited users, branches, aur loan accounts — iska matlab scaling par koi software penalty nahi. 

Sabse badi baat, saare core ERP modules (Finance, HRMS, CRM) ka **koi extra cost nahi** hai. Aap sirf 3rd party API (WhatsApp, CIBIL, eSign) ka actual cost pay karte hain.

Main propose karunga ki hum ek **14-Day Live Pilot** start karein. Aapki team 15-20 live loans system se process karegi with your actual rules. Agar system perform karta hai, toh we go live. 
Can we schedule a technical onboarding call this Thursday taaki hum aapke accounts chart ko map karna shuru kar sakein?"
