frappe.ui.form.on("Collection Task", {
    refresh: function(frm) {
        if (!frm.is_new() && frm.doc.collection_status !== "Resolved") {
            frm.add_custom_button(__("Log Follow-Up Activity"), function() {
                frappe.prompt([
                    {"fieldname": "action_type", "fieldtype": "Select", "label": __("Contact Channel"), "options": "\nPhone Call\nSMS\nEmail\nField Visit\nLegal Notice\nWhatsApp", "reqd": 1, "default": "Phone Call"},
                    {"fieldname": "result", "fieldtype": "Select", "label": __("Call Outcome"), "options": "\nConnected\nNot Reachable\nNo Answer\nPromised Payment\nRefused\nDisconnected", "reqd": 1, "default": "Connected"},
                    {"fieldname": "action_detail", "fieldtype": "Small Text", "label": __("Conversation Notes / Summary"), "reqd": 1}
                ], function(values) {
                    frm.call({
                        method: "log_action",
                        doc: frm.doc,
                        args: {
                            action_type: values.action_type,
                            action_detail: values.action_detail,
                            result: values.result
                        },
                        callback: function() {
                            frm.reload_doc();
                            frappe.show_alert({message: __("Follow-up logged successfully!"), indicator: "green"});
                        }
                    });
                }, __("Log Collection Follow-up"), __("Save Activity"));
            }).addClass("btn-primary");
        }
    }
});
