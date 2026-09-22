frappe.pages['zenviq_ai_chat'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'ZENVIQ AI Orchestrator',
        single_column: true
    });
    
    // Hide default Frappe page header to take full control
    $(wrapper).find('.page-head').hide();
    
    // Make wrapper full height
    $(wrapper).css({
        'height': 'calc(100vh - var(--navbar-height, 60px))',
        'display': 'flex',
        'flex-direction': 'column',
        'overflow': 'hidden',
        'background-color': '#ffffff',
        'margin': '0',
        'padding': '0'
    });
    
    // Frappe sometimes adds padding to container
    $(wrapper).closest('.container, .container-fluid').css({
        'padding': '0',
        'margin': '0',
        'width': '100%',
        'max-width': '100%'
    });
    
    $(wrapper).find('.page-body').css({
        'flex': '1',
        'display': 'flex',
        'flex-direction': 'row',
        'overflow': 'hidden',
        'padding': '0',
        'margin': '0'
    });
    
    $(wrapper).find('.layout-main-section').css({
        'padding': '0',
        'margin': '0',
        'border': 'none',
        'background': 'transparent'
    });

    $(page.body).html(`
        <style>
            /* Reset & Typography */
            .zai-container {
                display: flex;
                height: 100%;
                width: 100%;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                color: #1e293b;
                background: #ffffff;
                margin: 0;
            }
            
            /* Sidebar */
            .zai-sidebar {
                width: 260px;
                background: #f8fafc;
                border-right: 1px solid #e2e8f0;
                display: flex;
                flex-direction: column;
                padding: 24px 16px;
                flex-shrink: 0;
            }
            .zai-sidebar-header { margin-bottom: 24px; }
            .zai-brand { font-size: 15px; font-weight: 600; color: #0f172a; display: flex; align-items: center; gap: 8px; }
            .zai-brand-icon { width: 24px; height: 24px; background: linear-gradient(135deg, #6366f1, #a855f7); border-radius: 6px; color: white; display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: bold; }
            .zai-subtitle { font-size: 12px; color: #64748b; margin-top: 4px; margin-left: 32px; font-weight: 500; }
            
            .zai-new-chat-btn {
                width: 100%; padding: 10px 12px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px;
                color: #0f172a; font-weight: 500; font-size: 13px; cursor: pointer; text-align: left;
                display: flex; align-items: center; gap: 10px; box-shadow: 0 1px 2px rgba(0,0,0,0.02);
                transition: all 0.15s ease; outline: none;
            }
            .zai-new-chat-btn:hover { background: #f1f5f9; border-color: #cbd5e1; }
            
            .zai-nav-section { margin-top: 32px; }
            .zai-nav-title { font-size: 11px; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; padding-left: 8px; }
            .zai-nav-list { list-style: none; padding: 0; margin: 0; }
            .zai-nav-item { padding: 8px 10px; border-radius: 6px; font-size: 13px; color: #475569; cursor: pointer; display: flex; flex-direction: column; transition: background 0.15s; margin-bottom: 2px;}
            .zai-nav-item:hover { background: #f1f5f9; color: #0f172a; }
            .zai-nav-item-title { font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; display: flex; align-items: center; gap: 6px; }
            .zai-nav-item-title::before { content: "●"; font-size: 8px; color: #cbd5e1; }
            .zai-nav-item-time { font-size: 11px; color: #94a3b8; margin-top: 2px; padding-left: 14px; }
            
            .zai-sidebar-footer { margin-top: auto; padding-top: 16px; border-top: 1px solid #e2e8f0; display: flex; align-items: center; justify-content: space-between; font-size: 12px; color: #64748b; }
            .zai-status { display: flex; align-items: center; gap: 8px; }
            .zai-status-dot { width: 8px; height: 8px; background: #22c55e; border-radius: 50%; box-shadow: 0 0 0 2px #dcfce7; }
            
            /* Main Workspace */
            .zai-workspace {
                flex: 1;
                display: flex;
                flex-direction: column;
                background: #ffffff;
                position: relative;
            }
            .zai-header {
                height: 60px; border-bottom: 1px solid #e2e8f0; display: flex; align-items: center; justify-content: space-between; padding: 0 24px; flex-shrink: 0;
            }
            .zai-header-title { font-size: 15px; font-weight: 600; color: #0f172a; display: flex; align-items: center; gap: 6px; }
            .zai-header-badges { display: flex; gap: 8px; align-items: center; }
            .zai-badge { padding: 4px 8px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; font-size: 11px; font-weight: 500; color: #475569; }
            
            /* Chat History */
            .zai-history {
                flex: 1; overflow-y: auto; padding: 32px 0 0 0; display: flex; flex-direction: column; align-items: center; scroll-behavior: smooth;
            }
            .zai-message-container { width: 100%; max-width: 800px; padding: 0 24px; margin-bottom: 24px; display: flex; gap: 16px; }
            
            .zai-avatar { width: 28px; height: 28px; border-radius: 6px; flex-shrink: 0; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 600; margin-top: 2px; }
            .zai-avatar-user { background: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; }
            .zai-avatar-ai { background: linear-gradient(135deg, #6366f1, #a855f7); color: white; box-shadow: 0 2px 4px rgba(99, 102, 241, 0.2); }
            
            .zai-msg-content { flex: 1; min-width: 0; }
            .zai-msg-author { font-size: 13px; font-weight: 600; color: #0f172a; margin-bottom: 4px; display: flex; align-items: center; gap: 8px; }
            .zai-msg-time { font-size: 11px; color: #94a3b8; font-weight: 400; }
            .zai-msg-text { font-size: 14.5px; line-height: 1.6; color: #334155; }
            
            /* Empty State */
            .zai-empty-state {
                display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; width: 100%; max-width: 600px; padding: 24px; text-align: center; margin: auto;
            }
            .zai-empty-icon { font-size: 28px; color: #cbd5e1; margin-bottom: 16px; }
            .zai-empty-title { font-size: 24px; font-weight: 500; color: #0f172a; margin-bottom: 12px; letter-spacing: -0.5px; }
            .zai-empty-subtitle { font-size: 15px; color: #64748b; margin-bottom: 40px; line-height: 1.5; max-width: 400px; }
            
            .zai-suggestions { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; width: 100%; }
            .zai-suggestion-card {
                padding: 16px; border: 1px solid #e2e8f0; border-radius: 12px; text-align: left; background: #ffffff; cursor: pointer;
                transition: all 0.2s ease; box-shadow: 0 1px 2px rgba(0,0,0,0.02); display: flex; flex-direction: column; gap: 8px;
            }
            .zai-suggestion-card:hover { border-color: #cbd5e1; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.04); }
            .zai-suggestion-header { display: flex; align-items: center; gap: 8px; font-size: 13px; font-weight: 600; color: #0f172a; }
            .zai-suggestion-desc { font-size: 13px; color: #64748b; line-height: 1.4; }
            
            /* Composer */
            .zai-composer-wrapper {
                padding: 16px 24px 24px 24px; display: flex; justify-content: center; background: #ffffff; flex-shrink: 0;
            }
            .zai-composer {
                width: 100%; max-width: 800px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 12px 16px;
                box-shadow: 0 4px 24px rgba(0,0,0,0.06); display: flex; flex-direction: column; transition: border-color 0.2s, box-shadow 0.2s;
            }
            .zai-composer:focus-within { border-color: #cbd5e1; box-shadow: 0 8px 32px rgba(0,0,0,0.08); }
            .zai-composer-input {
                width: 100%; border: none; outline: none; font-size: 15px; color: #0f172a; resize: none; max-height: 200px; padding: 4px 0; font-family: inherit; line-height: 1.5; background: transparent;
            }
            .zai-composer-input::placeholder { color: #94a3b8; }
            .zai-composer-footer { display: flex; justify-content: space-between; align-items: center; margin-top: 12px; }
            .zai-shortcuts { font-size: 12px; color: #94a3b8; display: flex; gap: 12px; align-items: center; }
            .zai-kbd { background: #f1f5f9; padding: 2px 6px; border-radius: 4px; font-family: monospace; font-size: 11px; color: #64748b; border: 1px solid #e2e8f0; }
            .zai-send-btn {
                background: #0f172a; color: white; border: none; border-radius: 10px; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.2s;
            }
            .zai-send-btn:hover { background: #334155; transform: scale(1.05); }
            .zai-send-btn:disabled { background: #f1f5f9; color: #cbd5e1; cursor: not-allowed; transform: none; }
            
            /* Change Plan Card */
            .zai-plan-card {
                border: 1px solid #e2e8f0; border-radius: 12px; margin-top: 12px; background: #ffffff; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.04); max-width: 600px;
            }
            .zai-plan-header { padding: 12px 16px; background: #f8fafc; border-bottom: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center; }
            .zai-plan-title { font-size: 12px; font-weight: 600; color: #475569; text-transform: uppercase; letter-spacing: 0.5px; }
            .zai-risk-badge { font-size: 11px; padding: 4px 8px; border-radius: 4px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
            .risk-LOW { background: #dcfce7; color: #166534; }
            .risk-MEDIUM { background: #fef08a; color: #854d0e; }
            .risk-HIGH { background: #fee2e2; color: #991b1b; }
            
            .zai-plan-body { padding: 16px; font-size: 14px; }
            .zai-plan-summary { color: #0f172a; margin-bottom: 16px; line-height: 1.5; font-weight: 500; }
            
            .zai-diff-table { width: 100%; border-collapse: separate; border-spacing: 0; margin-bottom: 16px; border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden; }
            .zai-diff-table th, .zai-diff-table td { padding: 10px 12px; text-align: left; border-bottom: 1px solid #e2e8f0; font-size: 13px; }
            .zai-diff-table th { background: #f8fafc; color: #64748b; font-weight: 600; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; }
            .zai-diff-table tr:last-child td { border-bottom: none; }
            .zai-diff-add { color: #166534; background: #f0fdf4; font-weight: 500; }
            
            .zai-plan-meta { font-size: 12px; color: #64748b; display: flex; gap: 16px; margin-top: 16px; }
            .zai-plan-meta span { display: flex; align-items: center; gap: 4px; }
            
            .zai-plan-footer { padding: 12px 16px; border-top: 1px solid #e2e8f0; display: flex; justify-content: flex-end; gap: 8px; background: #fafafa; }
            
            .zai-btn { padding: 8px 16px; border-radius: 8px; font-size: 13px; font-weight: 500; cursor: pointer; transition: all 0.2s; border: 1px solid transparent; display: flex; align-items: center; gap: 6px; }
            .zai-btn-default { background: #ffffff; border-color: #cbd5e1; color: #334155; }
            .zai-btn-default:hover { background: #f8fafc; border-color: #94a3b8; }
            .zai-btn-primary { background: #0f172a; color: #ffffff; }
            .zai-btn-primary:hover { background: #334155; }
            
            /* Status / Execution */
            .zai-exec-status { display: flex; align-items: center; justify-content: space-between; font-size: 13px; font-weight: 500; padding: 12px 16px; border-top: 1px solid #e2e8f0; }
            .zai-exec-status.success { background: #f0fdf4; color: #166534; }
            .zai-exec-status.error { background: #fef2f2; color: #991b1b; }
            .zai-exec-status.loading { background: #f8fafc; color: #475569; justify-content: flex-start; }
            
            /* Animations */
            .typing-indicator { display: flex; align-items: center; color: #64748b; font-size: 13.5px; }
            .typing-indicator span { display: inline-block; width: 5px; height: 5px; background-color: #64748b; border-radius: 50%; margin-right: 4px; animation: bounce 1.4s infinite ease-in-out both; }
            .typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
            .typing-indicator span:nth-child(2) { animation-delay: -0.16s; }
            .typing-indicator span:nth-child(3) { margin-right: 12px; }
            @keyframes bounce {
                0%, 80%, 100% { transform: scale(0); }
                40% { transform: scale(1); }
            }
            .fade-in { animation: fadeIn 0.3s ease; }
            @keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
            
            /* Custom Scrollbar */
            ::-webkit-scrollbar { width: 6px; height: 6px; }
            ::-webkit-scrollbar-track { background: transparent; }
            ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
            ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
        </style>

        <div class="zai-container">
            <!-- Sidebar -->
            <div class="zai-sidebar">
                <div class="zai-sidebar-header">
                    <div class="zai-brand">
                        <div class="zai-brand-icon">Z</div>
                        ZENVIQ AI
                    </div>
                    <div class="zai-subtitle">ERP Orchestrator</div>
                </div>
                
                <button class="zai-new-chat-btn" onclick="zenviq_new_chat()">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                    New conversation
                </button>
                
                <div class="zai-nav-section">
                    <div class="zai-nav-title">Recent</div>
                    <ul class="zai-nav-list" id="zai-history-list">
                        <li class="zai-nav-item">
                            <span class="zai-nav-item-title">Add CIBIL Score field</span>
                            <span class="zai-nav-item-time">2 min ago</span>
                        </li>
                        <li class="zai-nav-item">
                            <span class="zai-nav-item-title">DPD Brackets Report</span>
                            <span class="zai-nav-item-time">14 min ago</span>
                        </li>
                    </ul>
                </div>
                
                <div class="zai-sidebar-footer">
                    <div class="zai-status">
                        <div class="zai-status-dot"></div>
                        Connected
                    </div>
                    <div style="color: #94a3b8;">v2.0</div>
                </div>
            </div>

            <!-- Workspace -->
            <div class="zai-workspace">
                <div class="zai-header">
                    <div class="zai-header-title">
                        ✨ ZENVIQ AI
                    </div>
                    <div class="zai-header-badges">
                        <span class="zai-badge">Production</span>
                        <span class="zai-badge" style="background:#f0fdf4; color:#166534; border-color:#bbf7d0;">GPT-4o</span>
                    </div>
                </div>
                
                <div class="zai-history" id="zai-chat-history">
                    <!-- Empty State Default -->
                    <div class="zai-empty-state" id="zai-empty">
                        <div class="zai-empty-icon">✦</div>
                        <div class="zai-empty-title">How can I help?</div>
                        <div class="zai-empty-subtitle">Configure, analyze or automate your ERP<br>using natural language.</div>
                        
                        <div class="zai-suggestions">
                            <div class="zai-suggestion-card" onclick="zenviq_set_prompt('Add a CIBIL Score field to Customer')">
                                <div class="zai-suggestion-header"><span style="color:#10b981;">+</span> Add a field</div>
                                <div class="zai-suggestion-desc">Add CIBIL Score to Customer</div>
                            </div>
                            <div class="zai-suggestion-card" onclick="zenviq_set_prompt('Create a new query report to list all pending loans')">
                                <div class="zai-suggestion-header"><span style="color:#6366f1;">⚡</span> Create report</div>
                                <div class="zai-suggestion-desc">List all pending loans</div>
                            </div>
                            <div class="zai-suggestion-card" onclick="zenviq_set_prompt('Build a dashboard for Branch performance')">
                                <div class="zai-suggestion-header"><span style="color:#f59e0b;">◫</span> Build dashboard</div>
                                <div class="zai-suggestion-desc">Branch performance dashboard</div>
                            </div>
                            <div class="zai-suggestion-card" onclick="zenviq_set_prompt('Show branches with PAR30 above 5%')">
                                <div class="zai-suggestion-header"><span style="color:#3b82f6;">↗</span> Analyze data</div>
                                <div class="zai-suggestion-desc">Show branches with PAR30 > 5%</div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="zai-composer-wrapper">
                    <div class="zai-composer">
                        <textarea class="zai-composer-input" id="zai-input" rows="1" placeholder="Ask ZENVIQ to change or analyze your ERP..."></textarea>
                        <div class="zai-composer-footer">
                            <div class="zai-shortcuts">
                                <span><span class="zai-kbd">⌘</span> + <span class="zai-kbd">Enter</span></span>
                            </div>
                            <button class="zai-send-btn" id="zai-submit" disabled>
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `);

    const textarea = document.getElementById('zai-input');
    const submitBtn = document.getElementById('zai-submit');
    
    textarea.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
        submitBtn.disabled = this.value.trim().length === 0;
    });
    
    textarea.addEventListener('keydown', function(e) {
        if ((e.metaKey || e.ctrlKey || (!e.shiftKey)) && e.key === 'Enter') {
            e.preventDefault();
            if(!submitBtn.disabled) $('#zai-submit').click();
        }
    });
    
    window.zenviq_set_prompt = function(text) {
        $('#zai-input').val(text);
        textarea.style.height = 'auto';
        submitBtn.disabled = false;
        $('#zai-submit').click();
    };
    
    window.zenviq_new_chat = function() {
        $('#zai-chat-history').html($('#zai-empty')[0].outerHTML);
        $('#zai-input').val('').focus();
        textarea.style.height = 'auto';
        submitBtn.disabled = true;
    };

    $('#zai-submit').on('click', function() {
        let text = $('#zai-input').val().trim();
        if (!text) return;

        $('#zai-empty').hide(); 
        
        $('#zai-chat-history').append(`
            <div class="zai-message-container fade-in">
                <div class="zai-avatar zai-avatar-user">You</div>
                <div class="zai-msg-content">
                    <div class="zai-msg-author">You <span class="zai-msg-time">Just now</span></div>
                    <div class="zai-msg-text">${frappe.utils.escape_html(text).replace(/\\n/g, '<br>')}</div>
                </div>
            </div>
        `);
        
        $('#zai-input').val('');
        textarea.style.height = 'auto';
        submitBtn.disabled = true;
        scroll_bottom();

        let thinking_id = 'msg-' + frappe.utils.get_random(5);
        $('#zai-chat-history').append(`
            <div class="zai-message-container fade-in" id="${thinking_id}">
                <div class="zai-avatar zai-avatar-ai">Z</div>
                <div class="zai-msg-content">
                    <div class="zai-msg-author">ZENVIQ AI</div>
                    <div class="zai-msg-text">
                        <div class="typing-indicator"><span></span><span></span><span></span> Inspecting ERPNext...</div>
                    </div>
                </div>
            </div>
        `);
        scroll_bottom();

        frappe.call({
            method: 'zenviq_lending.zenviq_ai.api.chat.generate_change_plan',
            args: { prompt: text },
            callback: function(r) {
                if (r.message && r.message.status === 'success') {
                    render_plan(thinking_id, r.message.request_id, r.message.plan);
                } else {
                    let err = r.message ? r.message.message : 'An error occurred.';
                    $('#' + thinking_id + ' .zai-msg-text').html(`
                        <div style="color: #991b1b; background: #fef2f2; padding: 12px 16px; border-radius: 8px; font-size: 13.5px; border: 1px solid #fecaca; max-width: 600px;">
                            <strong>I couldn't apply this change.</strong><br><br><span style="color:#b91c1c;">${err}</span>
                        </div>
                    `);
                }
                scroll_bottom();
            }
        });
    });

    function scroll_bottom() {
        let hist = document.getElementById('zai-chat-history');
        if(hist) hist.scrollTop = hist.scrollHeight;
    }

    function render_plan(msg_id, request_id, plan) {
        let risk_map = { 'GREEN': 'LOW', 'YELLOW': 'MEDIUM', 'RED': 'HIGH' };
        let ui_risk = risk_map[plan.risk_level] || 'MEDIUM';
        
        let tools_called = (plan.operations || []).length;
        let diff_html = '';
        
        if (tools_called > 0) {
            diff_html = '<table class="zai-diff-table"><tr><th>Operation</th><th>Target</th></tr>';
            plan.operations.forEach(op => {
                let short_target = op.tool;
                if(op.parameters) {
                    try {
                        let p = JSON.parse(op.parameters);
                        short_target = p.fieldname || p.name || p.doctype_name || op.tool;
                    } catch(e) {}
                }
                diff_html += `<tr><td class="zai-diff-add">+ ${frappe.utils.escape_html(op.tool)}</td><td>${frappe.utils.escape_html(short_target)}</td></tr>`;
            });
            diff_html += '</table>';
        }

        let card_html = `
            <div class="zai-plan-card fade-in">
                <div class="zai-plan-header">
                    <span class="zai-plan-title">Change Plan</span>
                    <span class="zai-risk-badge risk-${ui_risk}">${ui_risk} RISK</span>
                </div>
                <div class="zai-plan-body">
                    <div class="zai-plan-summary">${frappe.utils.escape_html(plan.summary)}</div>
                    ${diff_html}
                    <div class="zai-plan-meta">
                        <span><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path></svg> ${plan.affected_objects ? plan.affected_objects.length : 0} objects affected</span>
                        <span><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="1 4 1 10 7 10"></polyline><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"></path></svg> Rollback available</span>
                    </div>
                </div>
                <div class="zai-plan-footer" id="footer-${request_id}">
                    <button class="zai-btn zai-btn-default" onclick="zenviq_cancel('${request_id}')">Cancel</button>
                    <button class="zai-btn zai-btn-primary" onclick="zenviq_apply('${request_id}', ${plan.requires_approval})">Approve & Apply</button>
                </div>
            </div>
        `;
        
        let exec_steps = '<div style="margin-bottom: 12px; font-size: 13.5px; color: #475569;">✓ Inspected ERP configuration<br>✓ Validated permissions<br>✓ Generated plan</div>';
        
        $('#' + msg_id + ' .zai-msg-text').html(exec_steps + card_html);
    }

    window.zenviq_cancel = function(req_id) {
        $('#footer-' + req_id).html('<div class="zai-exec-status loading" style="border:none;">Cancelled.</div>');
    };

    window.zenviq_apply = function(req_id, requires_approval) {
        $('#footer-' + req_id).html(`
            <div class="zai-exec-status loading" style="width: 100%; border:none;">
                <div class="typing-indicator" style="margin-right: 8px;"><span></span><span></span><span></span></div> Applying changes...
            </div>
        `);
        
        frappe.call({
            method: 'zenviq_lending.zenviq_ai.api.chat.apply_change_plan',
            args: { request_id: req_id },
            callback: function(r) {
                if (r.message && r.message.status === 'success') {
                    $('#footer-' + req_id).html(`
                        <div class="zai-exec-status success" style="width:100%; border:none;">
                            <div style="display:flex; align-items:center; gap:8px;">
                                <span>✓ Change applied successfully</span>
                            </div>
                            <button class="zai-btn zai-btn-default" style="font-size: 12px; padding: 4px 10px;" onclick="zenviq_rollback('${req_id}')">Undo</button>
                        </div>
                    `);
                } else {
                    $('#footer-' + req_id).html(`
                        <div class="zai-exec-status error" style="width:100%; border:none; justify-content: flex-start;">
                            ! Failed to apply: ${(r.message?r.message.message:'')}
                        </div>
                    `);
                }
            }
        });
    };

    window.zenviq_rollback = function(req_id) {
        frappe.confirm('Undo this AI change?', () => {
            $('#footer-' + req_id).html(`
                <div class="zai-exec-status loading" style="width: 100%; border:none;">
                    <div class="typing-indicator" style="margin-right: 8px;"><span></span><span></span><span></span></div> Undoing change...
                </div>
            `);
            frappe.call({
                method: 'zenviq_lending.zenviq_ai.api.rollback.rollback_change_plan',
                args: { request_id: req_id },
                callback: function(r) {
                    if (r.message && r.message.status === 'success') {
                        $('#footer-' + req_id).html(`
                            <div class="zai-exec-status" style="width:100%; border:none; background: #f8fafc; color: #475569; justify-content:flex-start;">
                                ↩️ Change rolled back
                            </div>
                        `);
                    } else {
                        $('#footer-' + req_id).html(`
                            <div class="zai-exec-status error" style="width:100%; border:none; justify-content:flex-start;">
                                ! Rollback failed: ${(r.message?r.message.message:'')}
                            </div>
                        `);
                    }
                }
            });
        });
    };
};
