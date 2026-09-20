frappe.ui.form.on("eSign Request", {
    refresh: function(frm) {
        if (!frm.is_new()) {
            if (frm.doc.esign_status === "Pending" || frm.doc.esign_status === "Failed") {
                frm.add_custom_button(__("Send Aadhaar OTP"), function() {
                    frm.call({
                        method: "send_otp",
                        doc: frm.doc,
                        freeze: true,
                        freeze_message: __("Dispatching OTP to registered mobile..."),
                        callback: function(r) {
                            frm.reload_doc();
                        }
                    });
                }).addClass("btn-primary");
            }

            if (frm.doc.esign_status === "OTP Sent") {
                frm.add_custom_button(__("Enter OTP & eSign"), function() {
                    frappe.prompt([
                        {"fieldname": "otp", "fieldtype": "Data", "label": __("Enter 6-Digit OTP sent to Mobile"), "reqd": 1, "default": "123456"}
                    ], function(values) {
                        frm.call({
                            method: "complete_esign",
                            doc: frm.doc,
                            freeze: true,
                            freeze_message: __("Cryptographically signing document with CCA DSC..."),
                            callback: function(r) {
                                frm.reload_doc();
                                frappe.msgprint({
                                    title: __("Document eSigned Successfully"),
                                    message: __("Aadhaar eSign completed with tamper-proof digital signature hash.<br><b>Hash:</b> " + frm.doc.digital_signature_hash),
                                    indicator: "green"
                                });
                            }
                        });
                    }, __("Aadhaar eSign OTP Verification"), __("Sign Document"));
                }).addClass("btn-success");
            }
        }
    }
});
