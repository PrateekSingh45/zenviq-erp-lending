frappe.ui.form.on("Loan Closure Request", {
    refresh: function(frm) {
        if (!frm.is_new() && frm.doc.docstatus === 1) {
            if (!frm.doc.noc_generated) {
                frm.add_custom_button(__("Generate NOC Certificate"), function() {
                    frm.call({
                        method: "generate_noc",
                        doc: frm.doc,
                        freeze: true,
                        freeze_message: __("Issuing No Objection Certificate & updating CIBIL..."),
                        callback: function(r) {
                            frm.reload_doc();
                        }
                    });
                }).addClass("btn-primary");
            }
        }
    }
});
