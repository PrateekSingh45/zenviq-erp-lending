frappe.ui.form.on("Lending Lead", {
    refresh: function(frm) {
        if (!frm.is_new() && frm.doc.lead_status !== "Converted") {
            frm.add_custom_button(__("Convert to Borrower"), function() {
                frappe.confirm(
                    __("Do you want to convert this lead to a formal Borrower Profile?"),
                    function() {
                        frm.call({
                            method: "convert_to_borrower",
                            doc: frm.doc,
                            freeze: true,
                            freeze_message: __("Creating Borrower Profile..."),
                            callback: function(r) {
                                frm.reload_doc();
                                if (r.message) {
                                    frappe.set_route("Form", "Borrower Profile", r.message);
                                }
                            }
                        });
                    }
                );
            }).addClass("btn-primary");
        }
    }
});
