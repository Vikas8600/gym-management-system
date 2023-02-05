import frappe


def execute():
    add_gym_locker_no()
    return

def add_gym_locker_no():
    lockers = [1,2,3,4,5,6,7,8,9,10]
    docs = [frappe.new_doc("Gym Locker") for item in lockers]
    for index, doc in enumerate(docs):
        doc.locker_no = str(lockers[index])
        doc.save(docs)
    return
