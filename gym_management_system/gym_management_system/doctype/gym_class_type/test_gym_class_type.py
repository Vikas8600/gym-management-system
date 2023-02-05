# Copyright (c) 2022, Milan Pethani and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


def create_gym_type():
    doc = frappe.new_doc("Gym Class Type")
    doc.class_type = "Cycling"
    doc.save()
    return doc.name

class TestGymClassType(FrappeTestCase):
    def setUp(self):
        self.gym_type = create_gym_type()

    def tearDown(self):
        frappe.delete_doc("Gym Class Type", self.gym_type)
    
    def test_gym_class_type(self):
        self.assertEqual(self.gym_type, "Cycling")