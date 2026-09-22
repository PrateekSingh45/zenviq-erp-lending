frappe.pages['zenviq_home'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: '',
        single_column: true
    });

    $(wrapper).find('.page-head').hide();

    var container = $('<div class="z-home"></div>').appendTo(page.main);

    container.html(`
        <div class="z-home-header">
            <div>
                <h1 class="z-home-title">Lending</h1>
                <p class="z-home-subtitle">Portfolio and lending operations</p>
            </div>
            <button class="btn btn-primary" onclick="frappe.new_doc('Loan Application')">+ New application</button>
        </div>

        <div class="z-metrics">
            <div class="z-metric">
                <div class="z-metric-val">₹18.4 Cr</div>
                <div class="z-metric-lbl">AUM</div>
            </div>
            <div class="z-metric">
                <div class="z-metric-val">1,284</div>
                <div class="z-metric-lbl">ACTIVE LOANS</div>
            </div>
            <div class="z-metric">
                <div class="z-metric-val">94.2%</div>
                <div class="z-metric-lbl">COLLECTION</div>
            </div>
            <div class="z-metric">
                <div class="z-metric-val">4.8%</div>
                <div class="z-metric-lbl">PAR 30</div>
            </div>
            <div class="z-metric">
                <div class="z-metric-val">42</div>
                <div class="z-metric-lbl">APPLICATIONS</div>
            </div>
        </div>

        <div class="z-sep"></div>

        <div class="z-two-col">
            <div class="z-col-main">
                <h3 class="z-section-title">Portfolio</h3>
                <div class="z-chart-area">
                    <svg viewBox="0 0 400 120" preserveAspectRatio="none" style="width:100%;height:120px;">
                        <defs>
                            <linearGradient id="chartFill" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="0%" stop-color="#E5E2DB" stop-opacity="0.4"/>
                                <stop offset="100%" stop-color="#E5E2DB" stop-opacity="0"/>
                            </linearGradient>
                        </defs>
                        <path d="M0,100 L50,80 L100,85 L150,60 L200,65 L250,40 L300,45 L350,20 L400,30 L400,120 L0,120 Z" fill="url(#chartFill)"/>
                        <polyline fill="none" stroke="#1E1E1C" stroke-width="1.5" points="0,100 50,80 100,85 150,60 200,65 250,40 300,45 350,20 400,30"/>
                    </svg>
                </div>
            </div>
            <div class="z-col-side">
                <h3 class="z-section-title">Needs attention</h3>
                <div class="z-att-list">
                    <div class="z-att-row">
                        <span class="z-att-num">8</span>
                        <span class="z-att-label">approvals pending</span>
                    </div>
                    <div class="z-att-row">
                        <span class="z-att-num">5</span>
                        <span class="z-att-label">accounts &gt;30 DPD</span>
                    </div>
                    <div class="z-att-row">
                        <span class="z-att-num">3</span>
                        <span class="z-att-label">failed KYC verifications</span>
                    </div>
                    <div class="z-att-row">
                        <span class="z-att-num">2</span>
                        <span class="z-att-label">CIBIL alerts</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="z-sep"></div>

        <div class="z-insight">
            <div class="z-insight-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#6C5CE7" stroke-width="2.5"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>
            </div>
            <div class="z-insight-content">
                <h3 class="z-insight-heading">ZENVIQ Insight</h3>
                <p class="z-insight-text">Collections weakened in Aligarh this week. 18 accounts represent most of the movement.</p>
                <a class="z-insight-link" onclick="zenviq_toggle_ai_panel()">Investigate →</a>
            </div>
        </div>
    `);

    $('<style>').text(`
        .z-home {
            max-width: 1100px;
            color: var(--z-text);
        }

        .z-home-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            margin-bottom: 44px;
        }
        .z-home-title {
            font-size: 28px;
            font-weight: 600;
            margin: 0 0 4px 0;
            letter-spacing: -0.5px;
            color: var(--z-text);
        }
        .z-home-subtitle {
            font-size: 15px;
            color: var(--z-text-secondary);
            margin: 0;
        }

        .z-metrics {
            display: flex;
            gap: 48px;
            margin-bottom: 0;
        }
        .z-metric {}
        .z-metric-val {
            font-size: 32px;
            font-weight: 500;
            color: var(--z-text);
            letter-spacing: -0.8px;
            line-height: 1.1;
            margin-bottom: 6px;
        }
        .z-metric-lbl {
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--z-text-muted);
        }

        .z-sep {
            height: 1px;
            background: var(--z-border);
            margin: 44px 0;
        }

        .z-two-col {
            display: flex;
            gap: 56px;
        }
        .z-col-main { flex: 2; }
        .z-col-side { flex: 1; }

        .z-section-title {
            font-size: 17px;
            font-weight: 600;
            color: var(--z-text);
            margin: 0 0 20px 0;
        }

        .z-chart-area {
            border-bottom: 1px solid var(--z-border);
        }

        .z-att-list {
            display: flex;
            flex-direction: column;
            gap: 14px;
        }
        .z-att-row {
            display: flex;
            align-items: baseline;
            gap: 12px;
        }
        .z-att-num {
            font-size: 16px;
            font-weight: 600;
            color: var(--z-text);
            min-width: 22px;
        }
        .z-att-label {
            font-size: 14px;
            color: var(--z-text-secondary);
        }

        .z-insight {
            display: flex;
            gap: 16px;
            align-items: flex-start;
        }
        .z-insight-icon {
            flex-shrink: 0;
            margin-top: 2px;
        }
        .z-insight-heading {
            font-family: 'Instrument Serif', serif;
            font-size: 22px;
            font-weight: 400;
            font-style: italic;
            color: var(--z-accent);
            margin: 0 0 8px 0;
        }
        .z-insight-text {
            font-size: 15px;
            line-height: 1.6;
            color: var(--z-text);
            margin: 0 0 12px 0;
        }
        .z-insight-link {
            font-size: 14px;
            font-weight: 500;
            color: var(--z-text-secondary);
            cursor: pointer;
            text-decoration: none;
        }
        .z-insight-link:hover {
            color: var(--z-text);
        }
    `).appendTo(page.main);
};
