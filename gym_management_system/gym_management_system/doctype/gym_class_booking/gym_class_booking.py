# Copyright (c) 2022, Milan Pethani and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import get_link_to_form, format_date
from frappe.model.document import Document

class GymClassBooking(Document):
    def on_submit(self):
        existing_booking = frappe.db.get_value(self.doctype, {'class_type': self.class_type, 'gym_member': self.gym_member, 
                                'date': self.date, 'docstatus':1, 'name': ("!=", self.name)}, 'name')
        
        if existing_booking:
            frappe.throw(_("Class Booking {} already booked for member {} with {} on {}").format(
                get_link_to_form(self.doctype, existing_booking),
                get_link_to_form("Gym Member",self.gym_member),
                self.class_typ, 
                format_date(self.date), 
            ))
