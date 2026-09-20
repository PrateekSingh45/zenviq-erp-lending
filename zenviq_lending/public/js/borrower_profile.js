frappe.ui.form.on("Borrower Profile", {
    refresh: function(frm) {
        if (!frm.is_new()) {
            // Action buttons
            frm.add_custom_button(__("Fetch CIBIL (Sandbox)"), function() {
                frappe.show_alert({message: __("Connecting to CIBIL Bureau API (Sandbox)..."), indicator: "orange"});
                frm.call({
                    method: "fetch_credit_score",
                    doc: frm.doc,
                    freeze: true,
                    freeze_message: __("Pulling Credit Score & Trade Lines..."),
                    callback: function(r) {
                        frm.reload_doc();
                        frappe.msgprint({
                            title: __("CIBIL Report Retrieved"),
                            message: __("<b>Credit Score:</b> " + frm.doc.credit_score + "<br><b>Risk Category:</b> " + frm.doc.risk_category + "<br><b>Active Loan Accounts:</b> " + (frm.doc.existing_loan_count || 0)),
                            indicator: "green"
                        });
                    }
                });
            }, __("Verifications"));

            frm.add_custom_button(__("Verify Aadhaar eKYC"), function() {
                frm.call({
                    method: "run_ekyc_aadhaar",
                    doc: frm.doc,
                    freeze: true,
                    freeze_message: __("Verifying Aadhaar with UIDAI Gateway..."),
                    callback: function(r) {
                        frm.reload_doc();
                    }
                });
            }, __("Verifications"));

            frm.add_custom_button(__("Verify PAN NSDL"), function() {
                frm.call({
                    method: "verify_pan",
                    doc: frm.doc,
                    freeze: true,
                    freeze_message: __("Validating PAN with Income Tax DB..."),
                    callback: function(r) {
                        frm.reload_doc();
                    }
                });
            }, __("Verifications"));

            // Fast navigation
            frm.add_custom_button(__("New Loan Application"), function() {
                frappe.new_doc("Loan Application", {
                    applicant: frm.doc.customer || "",
                    applicant_name: frm.doc.full_name,
                    company: "ZENVIQ Finance Demo Private Limited"
                });
            }, __("Quick Actions"));

            frm.add_custom_button(__("New Credit Assessment"), function() {
                frappe.new_doc("Credit Assessment", {
                    borrower_profile: frm.doc.name,
                    declared_monthly_income: frm.doc.monthly_income,
                    verified_monthly_income: frm.doc.monthly_income,
                    existing_emi: frm.doc.existing_emi_total || 0,
                    credit_score: frm.doc.credit_score || 720
                });
            }, __("Quick Actions"));

            frm.add_custom_button(__("New KYC Record"), function() {
                frappe.new_doc("KYC Verification", {
                    borrower_profile: frm.doc.name,
                    aadhaar_number: frm.doc.aadhaar_number,
                    pan_number: frm.doc.pan_number
                });
            }, __("Quick Actions"));
        }
    }
});
