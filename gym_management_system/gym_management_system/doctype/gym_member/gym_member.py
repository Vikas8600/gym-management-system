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
		
		gym_settings = frappe.get_single("Gym Settings")
		customer_group = gym_settings.default_customer_group
		territory = gym_settings.default_territory

		if not customer_group:
			frappe.throw(_("Please Define Default Customer Group in {}".format(get_link_to_form("Gym Settings","Gym Settings"))))

		if not territory:
			frappe.throw(_("Please Define Default Territory in {}".format(get_link_to_form("Gym Settings","Gym Settings"))))

		customer_doc = frappe.new_doc("Customer")
		customer_doc.customer_name = self.member_name
		customer_doc.customer_type = "Individual"
		customer_doc.gender = self.gender
		customer_doc.customer_group = customer_group
		customer_doc.territory = territory
		customer_doc.save(ignore_permissions= True)
		self.customer = customer_doc.name		
