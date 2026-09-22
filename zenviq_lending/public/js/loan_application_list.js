frappe.listview_settings['Loan Application'] = {
    onload: function(listview) {
        // Inject the Right Context Panel DOM if it doesn't exist
        if (!$('#zenviq-context-panel').length) {
            $('body').append(`
                <div id="zenviq-context-panel" class="z-context-panel">
                    <div class="z-panel-header">
                        <h3 style="margin:0; font-size: 16px; font-weight: 600;" id="z-cp-title">Application</h3>
                        <button class="btn btn-xs btn-default" onclick="$('#zenviq-context-panel').removeClass('open')">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                        </button>
                    </div>
                    <div class="z-panel-body" id="z-cp-body">
                        <!-- Content populated dynamically -->
                    </div>
                    <div class="z-panel-footer">
                        <button class="z-btn z-btn-primary w-100" id="z-cp-open-full">Open Full Record</button>
                    </div>
                </div>
            `);
        }
        
        // Custom styling for the list wrapper
        $('.list-row-head').addClass('z-list-header-modern');
    },

    // Override the default click behavior to open the panel instead of the form
    on_row_click: function(listview, docname) {
        // Fetch the document details quickly via Frappe API
        frappe.call({
            method: 'frappe.client.get',
            args: {
                doctype: 'Loan Application',
                name: docname
            },
            callback: function(r) {
                if(r.message) {
                    let doc = r.message;
                    $('#z-cp-title').text(docname);
                    
                    // Populate the CRM-like summary
                    let html = `
                        <div style="margin-bottom: 24px;">
                            <div style="font-size: 11px; font-weight: 600; color: var(--z-text-muted); text-transform: uppercase; margin-bottom: 4px;">Borrower</div>
                            <div style="font-size: 16px; font-weight: 500; color: var(--z-text-primary);">${doc.applicant_name || 'Unknown'}</div>
                        </div>
                        
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px;">
                            <div>
                                <div style="font-size: 11px; font-weight: 600; color: var(--z-text-muted); text-transform: uppercase; margin-bottom: 4px;">Requested Amount</div>
                                <div style="font-size: 14px; color: var(--z-text-primary);">${frappe.format(doc.requested_amount, {fieldtype: 'Currency'})}</div>
                            </div>
                            <div>
                                <div style="font-size: 11px; font-weight: 600; color: var(--z-text-muted); text-transform: uppercase; margin-bottom: 4px;">Stage</div>
                                <div style="font-size: 14px; color: var(--z-text-primary);">${doc.workflow_state || doc.status || 'Draft'}</div>
                            </div>
                        </div>

                        <div style="background: var(--z-bg-sidebar); border: 1px solid var(--z-border-subtle); border-radius: 8px; padding: 16px; margin-bottom: 24px;">
                            <div style="font-size: 12px; font-weight: 600; color: var(--z-ai-accent); margin-bottom: 8px; display:flex; align-items:center; gap:6px;">
                                ✦ AI Summary
                            </div>
                            <div style="font-size: 13px; color: var(--z-text-secondary); line-height: 1.5;">
                                Application has been in ${doc.workflow_state || 'current stage'} for a few days. Ensure KYC verification is completed before proceeding to underwriting.
                            </div>
                        </div>
                        
                        <div style="font-size: 12px; font-weight: 600; color: var(--z-text-muted); text-transform: uppercase; margin-bottom: 12px;">Recent Activity</div>
                        <div style="font-size: 13px; color: var(--z-text-secondary); border-left: 2px solid var(--z-border); padding-left: 12px; margin-left: 6px;">
                            <div style="margin-bottom: 8px;">
                                <strong style="color:var(--z-text-primary);">System</strong><br>
                                Created application ${docname}
                                <div style="font-size: 11px; color: var(--z-text-muted); margin-top:2px;">${frappe.datetime.global_date_format(doc.creation)}</div>
                            </div>
                        </div>
                    `;
                    
                    $('#z-cp-body').html(html);
                    $('#z-cp-open-full').off('click').on('click', function() {
                        frappe.set_route('Form', 'Loan Application', docname);
                    });
                    
                    $('#zenviq-context-panel').addClass('open');
                }
            }
        });
        
        return false; // Prevent default navigation
    }
};
