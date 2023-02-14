# Copyright (c) 2022, Milan Pethani and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import get_link_to_form, format_date
from frappe.model.document import Document

class GymMemberFitnessJourney(Document):
	def on_submit(self):
		exists_fitness = frappe.db.get_value(self.doctype, {'date': self.date, 'gym_member': self.gym_member, 
							'docstatus':1, 'name':("!=", self.name)},'name')
		
		if exists_fitness:
			frappe.throw(_("{} {} already is assigned to member {} for {}").format(
				self.doctype,
				get_link_to_form(self.doctype, exists_fitness), 
				get_link_to_form("Gym Member",self.gym_member), 
				format_date(self.date)
			))