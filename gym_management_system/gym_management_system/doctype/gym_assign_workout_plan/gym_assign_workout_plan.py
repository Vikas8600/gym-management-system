# Copyright (c) 2023, Milan Pethani and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate
from frappe.model.document import Document

class GymAssignWorkoutPlan(Document):
	def validate(self):
		self.validate_dates()

	def validate_dates(self):
		if getdate(self.from_date) > getdate(self.to_date):
			frappe.throw(_("To Date cannot be before From Date"))
