# Copyright (c) 2022, Milan Pethani and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import get_link_to_form
from frappe.model.document import Document

class GymLockerBooking(Document):
    def validate(self):
        existing_locker_booking = frappe.db.get_value("Gym Locker Booking", {'gym_locker': self.gym_locker, 'gym_member': self.gym_member, 'enabled': 1, 'name': ("!=", self.name)}, 'name')
        
        if existing_locker_booking:
            frappe.throw(_("Locker {0} already is assigned to {1}. Disable the {2} to active current locker booking.").format(
                self.gym_locker, 
                get_link_to_form("Gym Member",self.gym_member), 
                get_link_to_form("Gym Locker Booking", existing_locker_booking)
            ))
