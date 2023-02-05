import frappe


def execute():
    add_gym_locker_no()
    add_gym_setting()
    return

def add_gym_locker_no():
    lockers = [1,2,3,4,5,6,7,8,9,10]
    docs = []
    for locker_no in lockers:
        if not frappe.db.exists("Gym Locker", str(locker_no)):
            doc = frappe.new_doc("Gym Locker")
            doc.locker_no = str(locker_no)
            doc.save()
    return


def add_gym_setting():
    doc = frappe.get_doc('Gym Settings')
    doc.default_customer_group = "Individual"
    doc.default_territory = "India"
    doc.save()
    return