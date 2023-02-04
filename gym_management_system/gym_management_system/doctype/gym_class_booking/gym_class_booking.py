# Copyright (c) 2022, Milan Pethani and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import get_link_to_form, format_date
from frappe.model.document import Document

class GymClassBooking(Document):
	def on_submit(self):
		exists_class_booking = frappe.db.exists(self.doctype, {'class_type': self.class_type, 'gym_member': self.gym_member, 
								'date': self.date, 'docstatus':1, 'name': ("!=", self.name)})
		
		if exists_class_booking:
			frappe.throw(_("Class Booking {} already booked for member {} with {} on {}").format(
				frappe.bold(get_link_to_form(self.doctype, exists_class_booking)),
				frappe.bold(get_link_to_form("Gym Member",self.gym_member)),
				frappe.bold(self.class_type), 
				frappe.bold(format_date(self.date)), 
			))
