frappe.ui.form.on('Borrower Profile', {
    refresh: function(frm) {
        frm.page.wrapper.find('.page-body').css('padding-top', '0');

        if (frm.layout.wrapper.find('.z-crm-header').length === 0) {
            var statusText = frm.doc.status || 'Active';
            var statusBg = statusText === 'Active' ? '#EAF2ED' : '#EFEDE8';
            var statusColor = statusText === 'Active' ? '#24674B' : '#5F5C57';

            var crm_header = $(`
                <div class="z-crm-header" style="
                    background: transparent;
                    padding: 0 0 20px 0;
                    margin-bottom: 28px;
                    border-bottom: 1px solid var(--z-border, #E5E2DB);
                    display: flex;
                    justify-content: space-between;
                    align-items: flex-start;
                ">
                    <div>
                        <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
                            <h2 style="margin:0;font-size:22px;font-weight:600;color:#1E1E1C;">
                                ${frm.doc.first_name || ''} ${frm.doc.last_name || ''}
                            </h2>
                            <span style="
                                background:${statusBg};color:${statusColor};
                                padding:2px 8px;border-radius:4px;
                                font-size:12px;font-weight:500;
                            ">${statusText}</span>
                        </div>
                        <div style="font-size:14px;color:#64615C;">
                            ${frm.doc.name}
                            &middot; ${frm.doc.risk_category || 'Low'} risk
                            &middot; CIBIL ${frm.doc.cibil_score || 'N/A'}
                        </div>
                    </div>
                    <div style="display:flex;gap:8px;align-items:center;">
                        <button class="btn ai-btn" onclick="zenviq_toggle_ai_panel()" style="font-size:13px;">Ask ZENVIQ</button>
                        <button class="btn btn-default" style="padding:0 8px!important;" onclick="frappe.msgprint('More actions')">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="1"></circle><circle cx="19" cy="12" r="1"></circle><circle cx="5" cy="12" r="1"></circle></svg>
                        </button>
                    </div>
                </div>
            `);
            frm.layout.wrapper.prepend(crm_header);
        }
    }
});
