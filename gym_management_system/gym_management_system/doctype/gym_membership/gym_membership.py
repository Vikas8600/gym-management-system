# Copyright (c) 2022, Milan Pethani and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import get_link_to_form, format_date, getdate
from frappe.model.document import Document

from gym_management_system.utils import create_sales_invoice

class GymMembership(Document):
    def validate(self):
        self.validate_dates()
        self.validate_amount()

    def on_submit(self):
        self.validate_membership()
        create_sales_invoice(self)
    
    def on_update_after_submit(self):
        self.validate_membership()

    def validate_dates(self):
        if getdate(self.membership_start_date) > getdate(self.membership_end_date):
            frappe.throw(_("Membership End Date cannot be before Membership Start Date"))

    def validate_amount(self):
        if not self.amount:
            frappe.throw(_("Please Add Membership Amount"))

    def validate_membership(self):
        exists_membership = frappe.db.sql(f"""
            select name from `tabGym Membership`
            where docstatus = 1 and enabled = 1 and name != '{self.name}' and gym_member = %s
                and (membership_start_date between %s and %s or membership_end_date between %s and %s)
            """, (self.gym_member, self.membership_start_date, self.membership_end_date, self.membership_start_date, self.membership_end_date))
            
        if exists_membership:
            frappe.throw(_("Membership {} already exists for member {} between {} and {}".format(
                get_link_to_form(self.doctype, exists_membership[0][0]),
                get_link_to_form("Gym Member",self.gym_member),
                format_date(self.membership_start_date),
                format_date(self.membership_end_date),
            )))
    
