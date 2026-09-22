frappe.pages['owner-cockpit'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: '',
        single_column: true
    });

    $(wrapper).find('.page-head').hide();

    var container = $('<div class="z-home"></div>').appendTo(page.main);

    container.html(`
        <div class="z-home-header" style="margin-bottom:24px;">
            <div>
                <h1 class="z-home-title">ZENVIQ Insights</h1>
            </div>
        </div>

        <ul class="z-tabs">
            <li class="active"><a href="#">Portfolio</a></li>
            <li><a href="#">Risk</a></li>
            <li><a href="#">Collections</a></li>
            <li><a href="#">Branches</a></li>
            <li><a href="#">AI Analysis</a></li>
        </ul>

        <div class="z-insights-grid">
            <div class="z-insight-metric">
                <div class="z-im-val">\u20b918.4 Cr</div>
                <div class="z-im-lbl">AUM</div>
                <div class="z-im-trend positive">+4.2% this month</div>
            </div>
            <div class="z-insight-metric">
                <div class="z-im-val">94.2%</div>
                <div class="z-im-lbl">COLLECTION</div>
                <div class="z-im-trend positive">+1.1% this month</div>
            </div>
            <div class="z-insight-metric wide">
                <div class="z-im-val">1,284</div>
                <div class="z-im-lbl">ACTIVE LOANS</div>
                <div class="z-im-trend positive">+38 this month</div>
            </div>
        </div>

        <div class="z-two-col" style="margin-top:32px;">
            <div class="z-col-main">
                <div class="z-insight-metric" style="padding:28px;">
                    <div class="z-section-title" style="margin-bottom:20px;">Portfolio movement</div>
                    <svg viewBox="0 0 400 140" preserveAspectRatio="none" style="width:100%;height:140px;">
                        <defs>
                            <linearGradient id="iFill" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="0%" stop-color="#E5E2DB" stop-opacity="0.3"/>
                                <stop offset="100%" stop-color="#E5E2DB" stop-opacity="0"/>
                            </linearGradient>
                        </defs>
                        <path d="M0,120 L57,100 L114,105 L171,70 L228,75 L285,40 L342,48 L400,15 L400,140 L0,140 Z" fill="url(#iFill)"/>
                        <polyline fill="none" stroke="#1E1E1C" stroke-width="1.5" points="0,120 57,100 114,105 171,70 228,75 285,40 342,48 400,15"/>
                    </svg>
                </div>
            </div>
            <div class="z-col-side">
                <div class="z-insight-metric" style="padding:28px;">
                    <div class="z-section-title" style="margin-bottom:20px;">Collection activity</div>
                    <div class="z-heatmap">
                        <div class="zh-row"><div class="zh-cell l1"></div><div class="zh-cell l3"></div><div class="zh-cell l1"></div><div class="zh-cell l2"></div><div class="zh-cell l1"></div><div class="zh-cell l3"></div><div class="zh-cell l2"></div></div>
                        <div class="zh-row"><div class="zh-cell l3"></div><div class="zh-cell l2"></div><div class="zh-cell l3"></div><div class="zh-cell l1"></div><div class="zh-cell l2"></div><div class="zh-cell l1"></div><div class="zh-cell l3"></div></div>
                        <div class="zh-row"><div class="zh-cell l1"></div><div class="zh-cell l1"></div><div class="zh-cell l2"></div><div class="zh-cell l3"></div><div class="zh-cell l1"></div><div class="zh-cell l2"></div><div class="zh-cell l1"></div></div>
                        <div class="zh-row"><div class="zh-cell l2"></div><div class="zh-cell l3"></div><div class="zh-cell l1"></div><div class="zh-cell l1"></div><div class="zh-cell l3"></div><div class="zh-cell l2"></div><div class="zh-cell l2"></div></div>
                        <div class="zh-row"><div class="zh-cell l1"></div><div class="zh-cell l2"></div><div class="zh-cell l2"></div><div class="zh-cell l3"></div><div class="zh-cell l1"></div><div class="zh-cell l1"></div><div class="zh-cell l3"></div></div>
                    </div>
                </div>
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
            margin: 0;
            letter-spacing: -0.5px;
            color: var(--z-text);
        }

        .z-tabs {
            display: flex;
            gap: 28px;
            list-style: none;
            padding: 0;
            margin: 0 0 36px 0;
            border-bottom: 1px solid var(--z-border);
        }
        .z-tabs > li > a {
            display: inline-block;
            padding: 10px 0;
            font-size: 14px;
            font-weight: 500;
            color: #66645F;
            text-decoration: none;
            border-bottom: 2px solid transparent;
            transition: color 150ms ease;
        }
        .z-tabs > li > a:hover { color: #1F1F1D; }
        .z-tabs > li.active > a {
            color: #1F1F1D;
            font-weight: 600;
            border-bottom-color: #1F1F1D;
        }

        .z-insights-grid {
            display: grid;
            grid-template-columns: 1fr 1fr 2fr;
            gap: 20px;
        }
        .z-insight-metric {
            background: #F8F7F4;
            border: 1px solid #E8E6E0;
            border-radius: 12px;
            padding: 22px;
        }
        .z-insight-metric.wide { grid-column: span 1; }
        .z-im-val {
            font-size: 32px;
            font-weight: 500;
            color: var(--z-text);
            letter-spacing: -0.5px;
            margin-bottom: 6px;
        }
        .z-im-lbl {
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--z-text-muted);
        }
        .z-im-trend {
            font-size: 13px;
            font-weight: 500;
            margin-top: 14px;
            color: var(--z-text-secondary);
        }
        .z-im-trend.positive { color: #176B62; }
        .z-im-trend.negative { color: #97443D; }

        .z-two-col {
            display: flex;
            gap: 20px;
        }
        .z-col-main { flex: 3; }
        .z-col-side { flex: 2; }

        .z-section-title {
            font-size: 15px;
            font-weight: 600;
            color: var(--z-text);
            margin: 0;
        }

        .z-heatmap {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        .zh-row { display: flex; gap: 4px; }
        .zh-cell {
            flex: 1;
            height: 24px;
            border-radius: 3px;
        }
        .zh-cell.l1 { background: var(--z-shell-active); }
        .zh-cell.l2 { background: #D5D2CB; }
        .zh-cell.l3 { background: #176B62; opacity: 0.6; }
    `).appendTo(page.main);
};
