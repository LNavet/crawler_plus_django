from django.test import TestCase
from django.contrib.auth import get_user_model

# Create your tests here.


class UserAccountTests(TestCase):

    def test_new_superuser(self):
        EMAIL = "alejandra@mail.com"
        db = get_user_model()
        super_user = db.objects.create_superuser(
            EMAIL, "Alejandra", "Goodson", "t3stPassw0rd")
        self.assertEqual(str(super_user), EMAIL)
        self.assertEquals(super_user.email, EMAIL)
        self.assertEquals(super_user.first_name, "Alejandra")
        self.assertEquals(super_user.last_name, "Goodson")
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_active)

        with self.assertRaises(ValueError):
            db.objects.create_superuser(email=EMAIL, first_name="Alejandra", last_name="Goodson",
                                        password="t3stPassw0rd", is_staff=False)
        with self.assertRaises(ValueError):
            db.objects.create_superuser(email=EMAIL, first_name="Alejandra", last_name="Goodson",
                                        password="t3stPassw0rd", is_superuser=False)
        with self.assertRaises(ValueError):
            db.objects.create_superuser(email="", first_name="Alejandra", last_name="Goodson",
                                        password="t3stPassw0rd")
        with self.assertRaises(ValueError):
            db.objects.create_superuser(email=EMAIL, first_name="", last_name="Goodson",
                                        password="t3stPassw0rd")
        with self.assertRaises(ValueError):
            db.objects.create_superuser(email=EMAIL, first_name="Alejandra", last_name="",
                                        password="t3stPassw0rd")
        with self.assertRaises(ValueError):
            db.objects.create_superuser(email=EMAIL, first_name="Alejandra", last_name="Goodson",
                                        password="")

    def test_new_user(self):
        EMAIL = "alejandra@mail.com"
        db = get_user_model()
        normal_user = db.objects.create_user(
            EMAIL, "Alejandra", "Goodson", "t3stPassw0rd")
        self.assertEqual(str(normal_user), EMAIL)
        self.assertEquals(normal_user.email, EMAIL)
        self.assertEquals(normal_user.first_name, "Alejandra")
        self.assertEquals(normal_user.last_name, "Goodson")
        self.assertFalse(normal_user.is_superuser)
        self.assertFalse(normal_user.is_staff)
        self.assertFalse(normal_user.is_active)

        with self.assertRaises(ValueError):
            db.objects.create_user(email="", first_name="Alejandra", last_name="Goodson",
                                   password="t3stPassw0rd")
        with self.assertRaises(ValueError):
            db.objects.create_user(email=EMAIL, first_name="", last_name="Goodson",
                                   password="t3stPassw0rd")
        with self.assertRaises(ValueError):
            db.objects.create_user(email=EMAIL, first_name="Alejandra", last_name="",
                                   password="t3stPassw0rd")
        with self.assertRaises(ValueError):
            db.objects.create_user(email=EMAIL, first_name="Alejandra", last_name="Goodson",
                                   password="")
