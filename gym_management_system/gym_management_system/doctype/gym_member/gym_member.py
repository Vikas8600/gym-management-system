# Copyright (c) 2022, Milan Pethani and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import get_link_to_form
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class GymMember(Document):
	def validate(self):
		self.create_customer()
	
	def create_customer(self):
		if self.customer:
			return

		customer_doc = frappe.new_doc("Customer")
		customer_doc.customer_name = self.member_name
		customer_doc.customer_type = "Individual"
		customer_doc.gender = self.gender
		customer_doc.customer_group = frappe.db.get_singles_value("Gym Settings", "default_customer_group")
		if not customer_doc.customer_group:
			frappe.throw(_("Please Define Default Customer Group in {}".format(frappe.bold(get_link_to_form("Gym Settings","Gym Settings")))))

		customer_doc.territory = frappe.db.get_singles_value("Gym Settings", "default_territory")
		if not customer_doc.territory:
			frappe.throw(_("Please Define Default Territory in {}".format(frappe.bold(get_link_to_form("Gym Settings","Gym Settings")))))

		customer_doc.save(ignore_permissions= True)
		self.customer = customer_doc.name		
