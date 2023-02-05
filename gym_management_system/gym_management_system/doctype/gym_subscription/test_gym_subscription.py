# Copyright (c) 2022, Milan Pethani and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase
from datetime import datetime

def create_gym_sub_type():
    doc = frappe.new_doc("Gym Subscription Type")
    doc.subscription_type = "The 24-Hour Access Membership Gym"
    doc.save()
    return doc.name

def create_gym_member():
    doc = frappe.new_doc("Gym Member")
    doc.member_name = "Ram"
    doc.email_id = "ram@yopmail.com"
    doc.gender = "Male"
    doc.save()
    return doc.name

def create_gym_trainer():
    doc = frappe.new_doc("Gym Trainer")
    doc.trainer_name = "Sham"
    doc.email_id = "sham@yopmail.com"
    doc.save()
    return doc.name

def create_gym_subscription(subscription_type,gym_member,gym_trainer):
    doc = frappe.new_doc("Gym Subscription")
    doc.subscription_type = subscription_type
    doc.gym_member = gym_member
    doc.gym_trainer = gym_trainer
    doc.subscription_start_date = datetime.strptime("05-02-2023", '%m-%d-%Y').date()
    doc.subscription_end_date = datetime.strptime("07-02-2023", '%m-%d-%Y').date()
    doc.amount = "200"
    doc.save()
    return doc

class TestGymSubscription(FrappeTestCase):
    def setUp(self):
        subscription_type = create_gym_sub_type()
        gym_member = create_gym_member()
        gym_trainer = create_gym_trainer()
        self.gym_sub_doc = create_gym_subscription(subscription_type,gym_member,gym_trainer)

    def test_gym_gym_sub(self):
        self.assertEqual(datetime.strptime("07-02-2023", '%m-%d-%Y').date(), self.gym_sub_doc.subscription_end_date)

