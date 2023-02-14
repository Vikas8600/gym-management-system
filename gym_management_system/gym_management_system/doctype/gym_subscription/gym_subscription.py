# Copyright (c) 2022, Milan Pethani and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import get_link_to_form, format_date, getdate
from frappe.model.document import Document

from gym_management_system.utils import create_sales_invoice

class GymSubscription(Document):
	def validate(self):
		self.validate_dates()
		self.validate_amount()

	def on_submit(self):
		self.validate_subscription()
		create_sales_invoice(self)

	def on_update_after_submit(self):
		self.validate_subscription()

	def validate_dates(self):
		if getdate(self.subscription_start_date) > getdate(self.subscription_end_date):
			frappe.throw(_("Subscription End Date cannot be before Subscription Start Date"))

	def validate_amount(self):
		if not self.amount:
			frappe.throw(_("Please Add Membership Amount"))

	def validate_subscription(self):
		exists_subscription = frappe.db.sql("""
			select
				name
			from
				`tabGym Subscription`
			where
				docstatus = 1 and enabled = 1 and name != '{current_name}' and gym_member = '{gym_member}'
				and (subscription_start_date between '{start_date}' and '{end_date}'
					OR subscription_end_date between '{start_date}' and '{end_date}')
		""".format(
					current_name= self.name,
					gym_member= self.gym_member, 
					start_date= self.subscription_start_date, 
					end_date= self.subscription_end_date)
		)

		if exists_subscription:
			frappe.throw(_("Subscription {} already exists for member {} between {} and {}".format(
				get_link_to_form(self.doctype, exists_subscription[0][0]),
				get_link_to_form("Gym Member",self.gym_member),
				format_date(self.subscription_start_date),
				format_date(self.subscription_end_date),
			)))