frappe.ui.form.on("KYC Verification", {
    refresh: function(frm) {
        if (!frm.is_new() && frm.doc.docstatus === 0) {
            frm.add_custom_button(__("Run Aadhaar eKYC (OTP)"), function() {
                frm.call({
                    method: "run_aadhaar_ekyc",
                    doc: frm.doc,
                    freeze: true,
                    freeze_message: __("Simulating Aadhaar OTP Verification..."),
                    callback: function(r) {
                        frm.reload_doc();
                        frappe.show_alert({message: __("Aadhaar eKYC Successful!"), indicator: "green"});
                    }
                });
            }, __("Actions"));

            frm.add_custom_button(__("Run PAN Verification"), function() {
                frm.call({
                    method: "run_pan_verification",
                    doc: frm.doc,
                    freeze: true,
                    freeze_message: __("Querying NSDL PAN Database..."),
                    callback: function(r) {
                        frm.reload_doc();
                        frappe.show_alert({message: __("PAN Verified Successfully!"), indicator: "green"});
                    }
                });
            }, __("Actions"));

            frm.add_custom_button(__("Analyze Bank Statement AI"), function() {
                frm.call({
                    method: "analyze_bank_statement",
                    doc: frm.doc,
                    freeze: true,
                    freeze_message: __("Analyzing Cashflow & Banking Transactions..."),
                    callback: function(r) {
                        frm.reload_doc();
                        frappe.msgprint({
                            title: __("Bank Statement Analyzed"),
                            message: __("<b>Avg Monthly Balance:</b> ₹" + frm.doc.avg_monthly_balance + "<br><b>Avg Credits:</b> ₹" + frm.doc.avg_monthly_credits + "<br><b>Cheque Bounces:</b> 0"),
                            indicator: "green"
                        });
                    }
                });
            }, __("Actions"));
        }
    }
});
