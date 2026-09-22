// ZENVIQ Flow Shell — Desktop Application Structure
// Injects custom sidebar, hides Frappe chrome, manages navigation state

frappe.ready(function() {
    // Guard against double injection
    if (document.getElementById('z-sidebar')) return;

    // ── Build Sidebar ──
    const userName = frappe.session.user_fullname || frappe.session.user;
    const userInitial = userName.charAt(0).toUpperCase();

    const sidebar = document.createElement('div');
    sidebar.id = 'z-sidebar';
    sidebar.innerHTML = `
        <div id="z-sidebar-logo">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
                <polyline points="2 17 12 22 22 17"></polyline>
                <polyline points="2 12 12 17 22 12"></polyline>
            </svg>
            ZENVIQ
        </div>

        <div class="z-nav-section">Overview</div>
        <a class="z-nav-item" data-route="zenviq_home" id="nav-home">Lending</a>
        <a class="z-nav-item" data-route="zenviq_home" id="nav-my-work">My Work</a>

        <div class="z-nav-section">Lending</div>
        <a class="z-nav-item" data-route="List/Lending Lead" id="nav-leads">Leads</a>
        <a class="z-nav-item" data-route="List/Borrower Profile" id="nav-borrowers">Borrowers</a>
        <a class="z-nav-item" data-route="List/Loan Application" id="nav-applications">Applications</a>
        <a class="z-nav-item" data-route="List/Loan" id="nav-loans">Loans</a>

        <div class="z-nav-section">Intelligence</div>
        <a class="z-nav-item" data-route="owner-cockpit" id="nav-insights">Insights</a>

        <div class="z-nav-section">System</div>
        <a class="z-nav-item" data-route="modules" id="nav-modules">ERP Modules</a>

        <div class="z-sidebar-bottom">
            <div class="z-user-profile">
                <div class="z-user-avatar">${userInitial}</div>
                <div>
                    <div class="z-user-name">${userName}</div>
                    <div class="z-user-role">Administrator</div>
                </div>
            </div>
        </div>
    `;
    document.body.prepend(sidebar);

    // ── Sidebar Click Handlers ──
    sidebar.querySelectorAll('.z-nav-item').forEach(function(item) {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const route = this.getAttribute('data-route');
            if (route) {
                frappe.set_route(route);
            }
        });
    });

    // ── Active State Management ──
    function updateActiveNav() {
        const route = frappe.get_route();
        const routeStr = route.join('/');

        sidebar.querySelectorAll('.z-nav-item').forEach(function(item) {
            item.classList.remove('active');
        });

        if (route[0] === 'zenviq_home') {
            document.getElementById('nav-home').classList.add('active');
        } else if (route[0] === 'owner-cockpit') {
            document.getElementById('nav-insights').classList.add('active');
        } else if (route[0] === 'List') {
            if (route[1] === 'Lending Lead') document.getElementById('nav-leads').classList.add('active');
            else if (route[1] === 'Borrower Profile') document.getElementById('nav-borrowers').classList.add('active');
            else if (route[1] === 'Loan Application') document.getElementById('nav-applications').classList.add('active');
            else if (route[1] === 'Loan') document.getElementById('nav-loans').classList.add('active');
        } else if (route[0] === 'modules') {
            document.getElementById('nav-modules').classList.add('active');
        }

        // Ensure Frappe chrome stays hidden
        var navbar = document.querySelector('header.navbar');
        if (navbar) navbar.style.display = 'none';
        var layoutSide = document.querySelector('.layout-side-section');
        if (layoutSide) layoutSide.style.display = 'none';

        // Redirect old workspace route
        if (route[0] === 'workspace' && route[1] === 'ZENVIQ Lending') {
            frappe.set_route('zenviq_home');
        }
    }

    frappe.router.on('change', updateActiveNav);
    updateActiveNav();

    // ── Inject AI Panel ──
    if (!document.getElementById('z-glass-ai-panel')) {
        var panelWrapper = document.createElement('div');
        panelWrapper.innerHTML = `
            <div id="z-ai-floating-btn" style="
                position: fixed; right: 0; top: 50%; transform: translateY(-50%);
                background: #1D1D1B; color: #FFF;
                padding: 10px 7px 10px 10px;
                border-radius: 8px 0 0 8px;
                cursor: pointer; z-index: 9998;
                display: flex; align-items: center; justify-content: center;
                transition: background 150ms ease;
            ">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#9B8AFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="12" y1="2" x2="12" y2="22"></line>
                    <line x1="2" y1="12" x2="22" y2="12"></line>
                    <line x1="4.93" y1="4.93" x2="19.07" y2="19.07"></line>
                    <line x1="19.07" y1="4.93" x2="4.93" y2="19.07"></line>
                </svg>
            </div>

            <div id="z-glass-ai-panel" class="z-glass-ai-panel">
                <div class="z-glass-header">
                    <h3 class="z-glass-title">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#6C5CE7" stroke-width="2.5"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>
                        ZENVIQ
                    </h3>
                    <button style="background:transparent;border:none;cursor:pointer;color:#8A8781;padding:4px;" title="Close">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                    </button>
                </div>
                <div class="z-glass-body" id="z-glass-body"></div>
                <div class="z-glass-footer">
                    <input type="text" class="z-glass-input" placeholder="Ask anything...">
                    <button style="position:absolute;right:40px;top:50%;transform:translateY(-50%);background:transparent;border:none;color:#6C5CE7;cursor:pointer;">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
                    </button>
                </div>
            </div>
        `;

        // Append children to body
        while (panelWrapper.firstChild) {
            document.body.appendChild(panelWrapper.firstChild);
        }

        // Event handlers
        document.getElementById('z-ai-floating-btn').addEventListener('click', function() {
            window.zenviq_toggle_ai_panel();
        });
        document.getElementById('z-ai-floating-btn').addEventListener('mouseover', function() {
            this.style.background = '#000000';
        });
        document.getElementById('z-ai-floating-btn').addEventListener('mouseout', function() {
            this.style.background = '#1D1D1B';
        });

        // Close button
        document.querySelector('#z-glass-ai-panel .z-glass-header button').addEventListener('click', function() {
            window.zenviq_toggle_ai_panel();
        });
    }

    // ── Global AI Panel Toggle ──
    window.zenviq_toggle_ai_panel = function() {
        var panel = document.getElementById('z-glass-ai-panel');
        if (!panel) return;
        var isOpen = panel.classList.contains('open');

        if (!isOpen) {
            var route = frappe.get_route();
            var bodyEl = document.getElementById('z-glass-body');
            var html = '';

            if (route[0] === 'Form' && route[1] && route[2]) {
                html = '<div class="z-glass-context">'
                    + '<div style="font-weight:600;margin-bottom:4px;color:var(--z-text);">I have context for ' + route[2] + '.</div>'
                    + '<div style="font-size:13px;color:var(--z-text-secondary);">' + route[1] + ' record</div>'
                    + '</div>'
                    + '<div style="margin-bottom:10px;font-size:11px;font-weight:600;color:var(--z-text-muted);text-transform:uppercase;letter-spacing:0.5px;">Suggested</div>'
                    + '<div class="z-glass-chip">Summarize ' + route[1].toLowerCase() + '</div>'
                    + '<div class="z-glass-chip">Identify risk factors</div>'
                    + '<div class="z-glass-chip">Check policy conditions</div>'
                    + '<div class="z-glass-chip">Draft approval note</div>';
            } else {
                html = '<div class="z-glass-context">'
                    + '<div style="font-weight:600;margin-bottom:4px;color:var(--z-text);">How can I help you today?</div>'
                    + '<div style="font-size:13px;color:var(--z-text-secondary);">Global Workspace</div>'
                    + '</div>'
                    + '<div style="margin-bottom:10px;font-size:11px;font-weight:600;color:var(--z-text-muted);text-transform:uppercase;letter-spacing:0.5px;">Suggested</div>'
                    + '<div class="z-glass-chip">What is our current GNPA?</div>'
                    + '<div class="z-glass-chip">Show me high risk borrowers</div>'
                    + '<div class="z-glass-chip">Write a branch performance summary</div>';
            }

            bodyEl.innerHTML = html;
            panel.classList.add('open');
        } else {
            panel.classList.remove('open');
        }
    };
});
