import frappe
from frappe.email.utils import get_port

def execute():
	'''
		1. Set default incoming mmail port in email domin
		2. Set default incoming mmail port in all email account (for those account where domain is missing)
	'''
	frappe.reload_doc("email", "doctype", "email_domain", force=True)
	frappe.reload_doc("email", "doctype", "email_account", force=True)

	setup_incomming_email_port_in_email_domains()
	setup_incomming_email_port_in_email_accounts()


def setup_incomming_email_port_in_email_domains():
	email_domains = frappe.db.get_all("Email Domain", ['incoming_port', 'use_imap', 'use_ssl', 'name'])
	for domain in email_domains:
		if not domain.incoming_port:
			incoming_port = get_port(domain)
			frappe.db.set_value("Email Domain", domain.name, 'incoming_port', incoming_port, update_modified=False)

			#update incoming email port in all
			frappe.db.sql('''update `tabEmail Account` set incoming_port=%s where domain = %s''', (domain.incoming_port, domain.name))

def setup_incomming_email_port_in_email_accounts():
	email_accounts = frappe.db.get_all("Email Account", ['incoming_port', 'use_imap', 'use_ssl', 'name', 'enable_incoming'])

	for account in email_accounts:
		if account.enable_incoming and not account.incoming_port:
			incoming_port = get_port(account)
			frappe.db.set_value("Email Account", account.name, 'incoming_port', incoming_port, update_modified=False)
