from unittest.mock import patch

from core import models
from django.contrib.auth import get_user_model
from django.test import TestCase


def sample_user(email="test@test.com", password="testpass1234"):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class UserTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = "test@test.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email, password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = "test@TEST.COM"
        user = get_user_model().objects.create_user(
            email=email, password="testpass123"
        )
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None, password="testpass123"
            )

    def test_new_user_no_password(self):
        """Test creating user with no password is possible"""
        email = "test@test.com"
        user = get_user_model().objects.create_user(email=email)
        self.assertEqual(user.email, email)

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        email = "super@test.com"
        password = "testpass1233"
        superuser = get_user_model().objects.create_superuser(
            email=email, password=password
        )
        self.assertEqual(superuser.email, email)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)


class TagTests(TestCase):
    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(user=sample_user(), name="Vegan")
        self.assertEqual(str(tag), tag.name)


class IngredientTests(TestCase):
    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name="Cucumber",
        )
        self.assertEqual(str(ingredient), ingredient.name)


class RecipeTests(TestCase):
    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title="Steak and mushroom sauce",
            time_minutes=5,
            price=5.00,
        )

        self.assertEqual(str(recipe), recipe.title)

    @patch("uuid.uuid4")
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = "test-uuid"
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, "test_image.jpg")

        expected_path = f"uploads/recipe/{uuid}.jpg"
        self.assertEqual(file_path, expected_path)
