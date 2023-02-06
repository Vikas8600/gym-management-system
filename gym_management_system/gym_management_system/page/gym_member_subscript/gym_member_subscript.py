import frappe
from erpnext.accounts.party import get_party_details

@frappe.whitelist()
def get_data(gym_member=None,start=0):
	conditions = ""
	if gym_member:
		conditions = " and subscription.gym_member = '{}'".format(gym_member)

	active_subscription_details = frappe.db.sql("""
        select
            subscription.subscription_type, subscription.gym_trainer, subscription.gym_member, 
            DATE_FORMAT(subscription.subscription_end_date, '%d-%m-%Y') as subscription_end_date, 
            DATEDIFF(subscription.subscription_end_date, CURDATE()) as remaining_days, 
            member.email_id, member.mobile_no, member.gender
        from
            `tabGym Subscription` as subscription
            JOIN `tabGym Member` as member on member.name = subscription.gym_member
        where
            subscription.docstatus = 1 and subscription.enabled = 1 and subscription.subscription_end_date >= CURDATE() and member.enabled = 1{conditions}
        order by subscription.gym_member asc
    """.format(conditions= conditions), as_dict= True)

	expired_subscription_details = frappe.db.sql("""
        select
            subscription.subscription_type, subscription.gym_trainer, subscription.gym_member,
            DATE_FORMAT(subscription.subscription_end_date, '%d-%m-%Y') as subscription_end_date, 
            0 as remaining_days, member.email_id, member.mobile_no, member.gender
        from
            `tabGym Subscription` as subscription
            JOIN `tabGym Member` as member on member.name = subscription.gym_member
        where
            subscription.docstatus = 1 and (subscription.enabled = 0 or subscription.subscription_end_date < CURDATE())and member.enabled = 1{conditions}
        order by subscription.gym_member asc
    """.format(conditions= conditions), as_dict= True)

	return active_subscription_details, expired_subscription_details