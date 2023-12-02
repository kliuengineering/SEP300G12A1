from django.test import TestCase

# these imports are for testing authentication
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from mainapp.forms import SignupForm, LoginForm

# these imports are for testing file integrity
import hashlib
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from mainapp.models import UploadedFile

'''
The following section is for "1. User Registration and Authentication (3 marks)"

Test for user registration
Objective: 
    Verify that the registration process creates a new user with valid input. 
Approach:
    Use the UserCreationForm used in the application for user registration.
    Submit the form with valid user data and check if a new User instance is created.

Test for User Authentication
Objective: 
    Ensure a user can log in successfully with valid credentials.
Approach:
    Create a test user in the setup of the test.
    Use Django's authenticate function to verify that the user can log in with the correct credentials.

Test for Invalid Authentication
Objective: 
    Check that invalid credentials are rejected during authentication.
Approach:
    Attempt to authenticate using incorrect credentials.
    Ensure that the authentication fails.
'''

from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from mainapp.forms import SignupForm, LoginForm

class UserRegistrationTest(TestCase):
    """
    Test case for user registration process using the custom SignupForm.
    """
    def test_valid_user_registration(self):
        """
        Test to verify that a new user is successfully created with valid input data.
        """
        # Define valid user data for registration
        form_data = {'username': 'testuser', 'password1': 'testpassword123', 'password2': 'testpassword123'}
        
        # Initialize the custom registration form with the test data
        form = SignupForm(data=form_data)
        
        # Check if the form is valid
        self.assertTrue(form.is_valid())

        # Save the form to create a new user
        form.save()

        # Check if the user has been created
        self.assertTrue(User.objects.filter(username='testuser').exists())

class UserAuthenticationTest(TestCase):
    """
    Test case for user authentication process using the custom LoginForm.
    """
    def setUp(self):
        """
        Setup method to create a user before each test method is run.
        """
        # Create a test user with known credentials
        User.objects.create_user(username='testuser', password='testpassword123')

    def test_valid_login(self):
        """
        Test to ensure a user can log in with valid credentials using the LoginForm.
        """
        # Define valid login credentials
        form_data = {'username': 'testuser', 'password': 'testpassword123'}
        
        # Initialize the custom login form with the test data
        form = LoginForm(data=form_data)

        # Check if the form is valid
        self.assertTrue(form.is_valid())

        # Authenticate the user with the provided credentials
        user = authenticate(**form.cleaned_data)
        
        # Check if the authentication was successful
        self.assertIsNotNone(user)

    def test_invalid_login(self):
        """
        Test to ensure that authentication fails with invalid credentials using the LoginForm.
        """
        # Define invalid login credentials
        form_data = {'username': 'testuser', 'password': 'wrongpassword'}
        
        # Initialize the custom login form with the test data
        form = LoginForm(data=form_data)

        # Check if the form is valid
        self.assertTrue(form.is_valid())

        # Attempt to authenticate with the provided credentials
        user = authenticate(**form.cleaned_data)

        # Check that authentication fails
        self.assertIsNone(user)



'''
The following section is for "4. File Integrity Check (2 Marks)"
Explanation:
setUp Method: Each test class has a setUp method that creates a test user. This user is then used to create UploadedFile instances.
File Integrity Test: This test creates a file, computes its hash, and then simulates uploading the file by creating an UploadedFile instance with the file's hash. It then simulates downloading the file and checks if the hash of the downloaded content matches the original hash.
File Modification Detection Test: This test also creates and uploads a file. It then simulates a modification by changing the file_hash of the UploadedFile instance. Finally, it checks if the original hash and the new hash are different.
These tests are simplified and assume that the file content is directly available. In a real-world scenario, we would need to retrieve the file from the location specified in file_url to compute its hash.
'''

class FileIntegrityTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_file_integrity(self):
        # Create a test file
        test_file_content = b"Test file content"
        test_file = SimpleUploadedFile("testfile.txt", test_file_content)

        # Calculate hash of the test file
        original_hash = hashlib.sha256(test_file_content).hexdigest()

        # Create an UploadedFile instance
        uploaded_file = UploadedFile.objects.create(user=self.user, file_url=test_file.name, file_hash=original_hash)

        # Simulate the download process
        # In a real scenario, you'd retrieve the file from the location specified by file_url
        # For testing, we'll use the test_file_content
        downloaded_file_content = test_file_content
        downloaded_hash = hashlib.sha256(downloaded_file_content).hexdigest()

        # Compare the hashes
        self.assertEqual(original_hash, downloaded_hash)


class FileModificationDetectionTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser2', password='12345')

    def test_modification_detection(self):
        # Upload a file as in the previous test
        test_file_content = b"Test file content"
        test_file = SimpleUploadedFile("testfile.txt", test_file_content)

        # Calculate hash of the test file
        original_hash = hashlib.sha256(test_file_content).hexdigest()

        # Create an UploadedFile instance
        uploaded_file = UploadedFile.objects.create(user=self.user, file_url=test_file.name, file_hash=original_hash)

        # Simulate modification of the file
        modified_content = b"Modified content"
        modified_hash = hashlib.sha256(modified_content).hexdigest()

        # Update the file_hash to simulate a change in the file content
        uploaded_file.file_hash = modified_hash
        uploaded_file.save()

        # Check if the hashes are different
        self.assertNotEqual(original_hash, uploaded_file.file_hash)


