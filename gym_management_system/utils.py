import frappe
from frappe import _, unscrub
from frappe.utils import get_link_to_form, today, add_days, cint, format_date

from frappe.core.doctype.communication.email import _make as make_communication
from six import iteritems

def create_sales_invoice(self):
    try:
        si_doc = frappe.new_doc("Sales Invoice")
        si_doc.customer = frappe.get_value("Gym Member", self.gym_member, "customer")
        si_doc.posting_date = today()
        default_no_of_days_for_due_date = frappe.get_value("Gym Settings", 'default_no_of_days_for_due_date', 'value')
        si_doc.due_date = add_days(si_doc.posting_date, default_no_of_days_for_due_date)

        default_item_key = "default_membership_item" if self.doctype == "Gym Membership" else "default_subscription_item"
        default_item = frappe.get_value("Gym Settings", default_item_key, 'value')

        if not default_item:
            frappe.throw(_("Please Define {} Item in {}".format(unscrub(default_item_key), frappe.bold(get_link_to_form("Gym Settings","Gym Settings")))))
        
        si_doc.append('items', {
            'item_code': default_item,
            'qty': 1,
            'rate': self.amount
        })

        si_doc.save(ignore_permissions=True)
        si_doc.submit()
        self.db_set('sales_invoice', si_doc.name)
    except Exception as e:
        frappe.logger("gym").exception(e)

def send_weekly_summary_mails():

    def header(gym_member, start_date, end_date):
        return f"""Hey, <strong> {gym_member} </strong><br><br>
        Here is your Weekly Summary for Gym Classes between <strong>{format_date(start_date)}</strong> and <strong>{format_date(end_date)}</strong><br>
        <table border="1" cellspacing="0" cellpadding="0" width="35%">
            <thead>
                <tr>
                    <th width="20%" valign="top" align="center">Type</th>
                    <th width="15%" valign="top" align="center">Date</th>
                </tr>
            </thead>
            <tbody>"""


    def table(class_type, date):
        date = format_date(date)
        return """<tr>
                <td width="20%" valign="top" align="center"> {} </td>
                <td width="15%" valign="top" align="center"> {} </td>
            </tr>
            """.format(class_type, date)

    def footer():
        return """</tbody></table><br><br>
                Thank you for your active participation and inputs, We hope you enjoyed the experience.
                """
    
    start_date = add_days(today(), -7)
    end_date = today()
    class_booking_data = frappe.db.get_all("Gym Class Booking", 
                            {"docstatus": 1, "date":  ["between", (start_date, end_date)]},
                            ["class_type", "gym_member", "date"], order_by= "date asc")

    gym_member_dict = {}
    for row in class_booking_data:
        if row.gym_member not in gym_member_dict:
            gym_member_dict[row.gym_member] = [row]
        else:
            gym_member_dict[row.gym_member].append(row)
    
    for gym_member, details in iteritems(gym_member_dict):
        table_content = ''
        for row in details:
            table_content += table(row.class_type, row.date)

        message = header(gym_member, start_date, end_date) + '' + table_content + '' + footer()
        recipient = frappe.db.get_value("Gym Member", gym_member, "email_id")
        try:
            frappe.sendmail(
                recipients= recipient,
                subject = 'Weekly Summary of Gym Classes',
                message = message,
            )

            make_communication(
                content= message,
                subject= 'Weekly Summary of Gym Classes',
                recipients= recipient,
                communication_medium="Email",
                send_email=False,
                communication_type="Automated Message",
            )

        except:
            frappe.log_error("Mail Sending Issue", frappe.get_traceback())
            continue