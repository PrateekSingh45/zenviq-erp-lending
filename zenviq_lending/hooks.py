app_name = "zenviq_lending"
app_title = "ZENVIQ Individual Lending System"
app_publisher = "ZENVIQ Technology Solutions"
app_description = "End-to-end lending management for individual borrowers"
app_email = "info@zenviq.com"
app_license = "mit"
app_color = "#3F51B5"

required_apps = ["erpnext", "lending"]

# Modules
modules = [
	{
		"module_name": "ZENVIQ Lending",
		"category": "Modules",
		"color": "#3F51B5",
		"icon": "octicon octicon-credit-card",
		"type": "module",
		"label": "ZENVIQ Lending",
		"description": "Individual Lending Management System",
	}
]

# DocType JS
doctype_js = {
	"Lending Lead": "public/js/lending_lead.js",
	"Borrower Profile": "public/js/borrower_profile.js",
	"KYC Verification": "public/js/kyc_verification.js",
	"eSign Request": "public/js/esign_request.js",
	"Loan Closure Request": "public/js/loan_closure_request.js",
	"Collection Task": "public/js/collection_task.js",
}

# Scheduled Tasks
scheduler_events = {
	"daily": [
		"zenviq_lending.tasks.update_dpd_buckets",
		"zenviq_lending.tasks.flag_npa_loans",
		"zenviq_lending.tasks.create_collection_tasks",
	],
}
