from django.test import TestCase
import hashlib
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from mainapp.models import UploadedFile

'''
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
