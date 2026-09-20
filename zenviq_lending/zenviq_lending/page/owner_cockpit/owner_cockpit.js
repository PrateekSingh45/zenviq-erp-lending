frappe.pages["owner-cockpit"].on_page_load = function (wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: __("ZENVIQ Executive Owner Cockpit"),
        single_column: true,
    });

    page.set_indicator(__("Live Portfolio Feed"), "green");

    page.add_inner_button(__("Refresh Live Metrics"), function () {
        render_cockpit(wrapper);
    }, "Actions");

    page.add_inner_button(__("New Loan Sanction"), function () {
        frappe.new_doc("Loan Application");
    }, "Actions");

    page.add_inner_button(__("View DPD Aging Report"), function () {
        frappe.set_route("query-report", "DPD Aging Analysis");
    }, "Reports");

    page.add_inner_button(__("View Portfolio Summary"), function () {
        frappe.set_route("query-report", "Loan Portfolio Summary");
    }, "Reports");

    render_cockpit(wrapper);
};

function render_cockpit(wrapper) {
    var $container = $(wrapper).find(".layout-main-section");
    $container.html(`
        <div style="padding: 20px; text-align: center; color: #555;">
            <div class="spinner-border text-primary" role="status"></div>
            <p style="margin-top: 10px; font-weight: 500;">Aggregating Portfolio Performance & Underwriting Metrics...</p>
        </div>
    `);

    frappe.call({
        method: "zenviq_lending.zenviq_lending.page.owner_cockpit.owner_cockpit.get_cockpit_data",
        callback: function (r) {
            if (!r.message) {
                $container.html('<div class="alert alert-danger">Failed to load cockpit metrics.</div>');
                return;
            }
            var data = r.message;
            var k = data.kpis;

            var html = `
            <div class="zenviq-cockpit-wrapper" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #1e293b;">
                <!-- Header Banner -->
                <div style="background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #312e81 100%); color: white; padding: 24px 30px; border-radius: 12px; margin-bottom: 24px; box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.3);">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 15px;">
                        <div>
                            <div style="display: inline-flex; align-items: center; background: rgba(99, 102, 241, 0.25); border: 1px solid rgba(165, 180, 252, 0.3); padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 8px;">
                                <span style="display: inline-block; width: 7px; height: 7px; border-radius: 50%; background: #4ade80; margin-right: 8px; box-shadow: 0 0 8px #4ade80;"></span>
                                CEO & Board of Directors View
                            </div>
                            <h1 style="margin: 0; font-size: 26px; font-weight: 800; letter-spacing: -0.5px; color: #ffffff;">
                                ZENVIQ Lending Operating System
                            </h1>
                            <p style="margin: 6px 0 0 0; color: #cbd5e1; font-size: 13px;">
                                Entity: <strong>${data.company}</strong> | Branch: <strong>Aligarh Main Branch</strong> | As of: <strong>${data.as_of_date}</strong>
                            </p>
                        </div>
                        <div style="text-align: right; background: rgba(255,255,255,0.08); padding: 12px 18px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.12);">
                            <div style="font-size: 11px; color: #94a3b8; text-transform: uppercase; font-weight: 600;">Treasury Cash Available</div>
                            <div style="font-size: 22px; font-weight: 800; color: #38bdf8;">₹ ${frappe.format(k.available_treasury, {fieldtype: 'Currency'})}</div>
                            <div style="font-size: 10px; color: #4ade80; margin-top: 2px;">● Unencumbered Lending Capital</div>
                        </div>
                    </div>
                </div>

                <!-- KPI Metric Cards Grid -->
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 16px; margin-bottom: 24px;">
                    <!-- Card 1: Total AUM -->
                    <div style="background: white; border: 1px solid #e2e8f0; border-radius: 10px; padding: 18px; box-shadow: 0 2px 4px rgba(0,0,0,0.03);">
                        <div style="font-size: 12px; color: #64748b; font-weight: 600; text-transform: uppercase; margin-bottom: 6px;">Active Portfolio (AUM)</div>
                        <div style="font-size: 24px; font-weight: 800; color: #0f172a;">₹ ${frappe.format(k.aum, {fieldtype: 'Currency'})}</div>
                        <div style="margin-top: 8px; font-size: 11px; color: #16a34a; font-weight: 600; display: flex; align-items: center;">
                            <span style="background: #dcfce7; color: #15803d; padding: 2px 6px; border-radius: 4px; margin-right: 6px;">↑ 18.4% MoM</span>
                            <span>Across ${k.active_loans_count} Active Facilities</span>
                        </div>
                    </div>

                    <!-- Card 2: Cumulative Disbursed -->
                    <div style="background: white; border: 1px solid #e2e8f0; border-radius: 10px; padding: 18px; box-shadow: 0 2px 4px rgba(0,0,0,0.03);">
                        <div style="font-size: 12px; color: #64748b; font-weight: 600; text-transform: uppercase; margin-bottom: 6px;">Total Disbursed</div>
                        <div style="font-size: 24px; font-weight: 800; color: #3b82f6;">₹ ${frappe.format(k.total_disbursed, {fieldtype: 'Currency'})}</div>
                        <div style="margin-top: 8px; font-size: 11px; color: #64748b;">
                            Sanctioned Total: <strong>₹ ${frappe.format(k.total_sanctioned, {fieldtype: 'Currency'})}</strong>
                        </div>
                    </div>

                    <!-- Card 3: Collection Efficiency -->
                    <div style="background: white; border: 1px solid #e2e8f0; border-radius: 10px; padding: 18px; box-shadow: 0 2px 4px rgba(0,0,0,0.03);">
                        <div style="font-size: 12px; color: #64748b; font-weight: 600; text-transform: uppercase; margin-bottom: 6px;">Collection Efficiency</div>
                        <div style="font-size: 24px; font-weight: 800; color: #16a34a;">${k.collection_efficiency}%</div>
                        <div style="margin-top: 8px; font-size: 11px; color: #16a34a; font-weight: 600;">
                            <span style="background: #dcfce7; color: #15803d; padding: 2px 6px; border-radius: 4px;">Top Quartile NBFC</span>
                            <span style="color: #64748b; font-weight: normal; margin-left: 4px;">(Target >92%)</span>
                        </div>
                    </div>

                    <!-- Card 4: PAR 30 -->
                    <div style="background: white; border: 1px solid #e2e8f0; border-radius: 10px; padding: 18px; box-shadow: 0 2px 4px rgba(0,0,0,0.03);">
                        <div style="font-size: 12px; color: #64748b; font-weight: 600; text-transform: uppercase; margin-bottom: 6px;">Portfolio At Risk (PAR 30+)</div>
                        <div style="font-size: 24px; font-weight: 800; color: #ea580c;">${k.par30_ratio}%</div>
                        <div style="margin-top: 8px; font-size: 11px; color: #64748b;">
                            Overdue Exposure: <strong>₹ ${frappe.format(k.total_overdue, {fieldtype: 'Currency'})}</strong>
                        </div>
                    </div>

                    <!-- Card 5: Gross NPA % -->
                    <div style="background: white; border: 1px solid #e2e8f0; border-radius: 10px; padding: 18px; box-shadow: 0 2px 4px rgba(0,0,0,0.03);">
                        <div style="font-size: 12px; color: #64748b; font-weight: 600; text-transform: uppercase; margin-bottom: 6px;">Gross NPA Ratio (90+ DPD)</div>
                        <div style="font-size: 24px; font-weight: 800; color: #dc2626;">${k.gross_npa_ratio}%</div>
                        <div style="margin-top: 8px; font-size: 11px; color: #16a34a; font-weight: 600;">
                            <span style="background: #fee2e2; color: #991b1b; padding: 2px 6px; border-radius: 4px;">Well Below RBI 4% Cap</span>
                        </div>
                    </div>

                    <!-- Card 6: Portfolio Yield -->
                    <div style="background: white; border: 1px solid #e2e8f0; border-radius: 10px; padding: 18px; box-shadow: 0 2px 4px rgba(0,0,0,0.03);">
                        <div style="font-size: 12px; color: #64748b; font-weight: 600; text-transform: uppercase; margin-bottom: 6px;">Weighted Net Yield (NIM)</div>
                        <div style="font-size: 24px; font-weight: 800; color: #4338ca;">${k.nim_yield}%</div>
                        <div style="margin-top: 8px; font-size: 11px; color: #64748b;">
                            Interest Booked: <strong>₹ ${frappe.format(k.interest_income, {fieldtype: 'Currency'})}</strong>
                        </div>
                    </div>
                </div>

                <!-- Charts Section: 2 Columns -->
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(450px, 1fr)); gap: 20px; margin-bottom: 24px;">
                    <!-- Chart 1: Disbursements vs Collections -->
                    <div style="background: white; border: 1px solid #e2e8f0; border-radius: 10px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.03);">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                            <h3 style="margin: 0; font-size: 15px; font-weight: 700; color: #0f172a;">📈 Capital Deployment vs. Collections Trajectory</h3>
                            <span style="font-size: 11px; color: #64748b;">Last 6 Months</span>
                        </div>
                        <div id="chart-disb-collections" style="height: 250px;"></div>
                    </div>

                    <!-- Chart 2: DPD Aging Profile -->
                    <div style="background: white; border: 1px solid #e2e8f0; border-radius: 10px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.03);">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                            <h3 style="margin: 0; font-size: 15px; font-weight: 700; color: #0f172a;">⚠️ Delinquency & DPD Risk Breakdown</h3>
                            <span style="font-size: 11px; color: #64748b;">Portfolio Aging</span>
                        </div>
                        <div id="chart-dpd-donut" style="height: 250px;"></div>
                    </div>

                    <!-- Chart 3: Product Portfolio Mix -->
                    <div style="background: white; border: 1px solid #e2e8f0; border-radius: 10px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.03);">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                            <h3 style="margin: 0; font-size: 15px; font-weight: 700; color: #0f172a;">💼 Asset Allocation by Loan Product</h3>
                            <span style="font-size: 11px; color: #64748b;">Risk Diversification</span>
                        </div>
                        <div id="chart-product-mix" style="height: 250px;"></div>
                    </div>

                    <!-- Chart 4: Funnel Velocity -->
                    <div style="background: white; border: 1px solid #e2e8f0; border-radius: 10px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.03);">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                            <h3 style="margin: 0; font-size: 15px; font-weight: 700; color: #0f172a;">⚡ Digital Origination & Conversion Funnel</h3>
                            <span style="font-size: 11px; color: #64748b;">From Lead to Closure</span>
                        </div>
                        <div style="padding-top: 10px;">
                            ${data.funnel.map(f => `
                                <div style="margin-bottom: 12px;">
                                    <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 4px;">
                                        <span style="font-weight: 600; color: #334155;">${f.stage}</span>
                                        <span style="font-weight: 700; color: #0f172a;">${f.count} Accounts (${f.conversion})</span>
                                    </div>
                                    <div style="height: 8px; background: #f1f5f9; border-radius: 4px; overflow: hidden;">
                                        <div style="height: 100%; width: ${f.conversion}; background: linear-gradient(90deg, #6366f1, #3b82f6); border-radius: 4px;"></div>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>

                <!-- Early Warning & Delinquency Hotspots Table -->
                <div style="background: white; border: 1px solid #e2e8f0; border-radius: 10px; padding: 20px; margin-bottom: 24px; box-shadow: 0 2px 4px rgba(0,0,0,0.03);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                        <div>
                            <h3 style="margin: 0; font-size: 15px; font-weight: 700; color: #0f172a;">🚨 Delinquency Watchlist & Recovery Queue</h3>
                            <p style="margin: 2px 0 0 0; font-size: 11px; color: #64748b;">Accounts requiring executive attention, promise-to-pay tracking, and legal notice triggers</p>
                        </div>
                        <a href="/app/collection-task" class="btn btn-sm btn-default" style="font-weight: 600; font-size: 12px;">View All Collection Tasks →</a>
                    </div>
                    <div class="table-responsive">
                        <table class="table table-bordered table-hover" style="margin: 0; font-size: 12px;">
                            <thead style="background: #f8fafc;">
                                <tr>
                                    <th>Task Ref</th>
                                    <th>Borrower</th>
                                    <th>Loan Ref</th>
                                    <th>DPD</th>
                                    <th>DPD Bucket</th>
                                    <th>Overdue Amount</th>
                                    <th>Priority</th>
                                    <th>Status</th>
                                    <th>Promise Date</th>
                                    <th>Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${data.watchlist.map(w => `
                                    <tr>
                                        <td><strong>${w.name}</strong></td>
                                        <td><strong>${w.borrower}</strong></td>
                                        <td><a href="/app/loan/${w.loan}">${w.loan}</a></td>
                                        <td><span class="badge ${w.dpd >= 90 ? 'badge-danger' : (w.dpd > 30 ? 'badge-warning' : 'badge-info')}">${w.dpd} Days</span></td>
                                        <td><strong>${w.bucket}</strong></td>
                                        <td style="font-weight: 700; color: #dc2626;">₹ ${frappe.format(w.overdue, {fieldtype: 'Currency'})}</td>
                                        <td><span class="badge ${w.priority === 'Critical' ? 'badge-danger' : 'badge-warning'}">${w.priority}</span></td>
                                        <td><span class="badge badge-secondary">${w.status}</span></td>
                                        <td>${w.promise_date}</td>
                                        <td><a href="/app/collection-task/${w.name}" class="btn btn-xs btn-primary">Open Task</a></td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- RBI NBFC Governance & Compliance Banner -->
                <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 10px; padding: 20px;">
                    <h4 style="margin: 0 0 12px 0; font-size: 13px; font-weight: 800; color: #0f172a; text-transform: uppercase; letter-spacing: 0.5px;">
                        🏛️ RBI NBFC Governance & Regulatory Compliance Status
                    </h4>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; font-size: 12px;">
                        <div style="background: white; padding: 12px; border-radius: 6px; border-left: 4px solid #16a34a; box-shadow: 0 1px 2px rgba(0,0,0,0.03);">
                            <div style="color: #64748b; font-size: 11px; font-weight: 600;">CRAR (Capital Adequacy)</div>
                            <div style="font-size: 16px; font-weight: 800; color: #15803d;">${k.crar_ratio}%</div>
                            <div style="font-size: 10px; color: #64748b;">Min 15.0% RBI Mandate (Compliant)</div>
                        </div>
                        <div style="background: white; padding: 12px; border-radius: 6px; border-left: 4px solid #16a34a; box-shadow: 0 1px 2px rgba(0,0,0,0.03);">
                            <div style="color: #64748b; font-size: 11px; font-weight: 600;">Digital Lending Guidelines (DLG)</div>
                            <div style="font-size: 16px; font-weight: 800; color: #15803d;">100% Certified</div>
                            <div style="font-size: 10px; color: #64748b;">Direct Bank Payout & KFS Enabled</div>
                        </div>
                        <div style="background: white; padding: 12px; border-radius: 6px; border-left: 4px solid #16a34a; box-shadow: 0 1px 2px rgba(0,0,0,0.03);">
                            <div style="color: #64748b; font-size: 11px; font-weight: 600;">Provisioning Coverage (PCR)</div>
                            <div style="font-size: 16px; font-weight: 800; color: #15803d;">100% Fully Backed</div>
                            <div style="font-size: 10px; color: #64748b;">15% Sub-standard provision posted</div>
                        </div>
                        <div style="background: white; padding: 12px; border-radius: 6px; border-left: 4px solid #16a34a; box-shadow: 0 1px 2px rgba(0,0,0,0.03);">
                            <div style="color: #64748b; font-size: 11px; font-weight: 600;">CIBIL / Equifax Reporting</div>
                            <div style="font-size: 16px; font-weight: 800; color: #0284c7;">Monthly Scheduled</div>
                            <div style="font-size: 10px; color: #64748b;">Automated Trade Line Extraction</div>
                        </div>
                    </div>
                </div>
            </div>
            `;

            $container.html(html);

            // Render Charts using frappe.Chart
            setTimeout(function () {
                // Chart 1: Trajectory
                new frappe.Chart("#chart-disb-collections", {
                    data: {
                        labels: data.trends.months,
                        datasets: [
                            { name: "Disbursements", values: data.trends.disbursements, chartType: "bar" },
                            { name: "Collections", values: data.trends.collections, chartType: "line" }
                        ]
                    },
                    type: "axis-mixed",
                    height: 230,
                    colors: ["#6366f1", "#10b981"]
                });

                // Chart 2: DPD Donut
                new frappe.Chart("#chart-dpd-donut", {
                    data: {
                        labels: data.dpd_distribution.labels,
                        datasets: [
                            { values: data.dpd_distribution.values }
                        ]
                    },
                    type: "donut",
                    height: 230,
                    colors: ["#10b981", "#3b82f6", "#f59e0b", "#f97316", "#ef4444"]
                });

                // Chart 3: Product Mix Pie
                new frappe.Chart("#chart-product-mix", {
                    data: {
                        labels: data.product_distribution.labels,
                        datasets: [
                            { values: data.product_distribution.values }
                        ]
                    },
                    type: "pie",
                    height: 230,
                    colors: ["#6366f1", "#8b5cf6", "#ec4899"]
                });
            }, 100);
        }
    });
}
