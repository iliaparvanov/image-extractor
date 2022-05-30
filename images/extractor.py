from io import BytesIO
from filetype import helpers, filetype
import hashlib
import logging
import PIL.Image
import requests

from django.core.exceptions import ObjectDoesNotExist
from .models import Image

logger = logging.getLogger(__name__)

class Extractor:
    '''
    The Extractor object contains a url and can verify if the url points to a valid image
    and extract information about the image.


    Attributes:
        url (str): Url possibly pointing to an image
        image_content (bytearray): Image data as bytes. Contains data if verify() is called and the url point to a valid image.
        sha1 (bytearray): sha1 hash of the image (valid after extraction)
        height (int): height of the image (valid after extraction)
        height (int): height of the image (valid after extraction)
        type (str): extension of the image, eg. jpg, png... (valid after extraction)
    '''
    def __init__(self, url):
        self.url = url
        self.image_content = bytearray()
        self.sha1 = bytearray()
        self.height = 0
        self.width = 0
        self.type = ""

    def verify(self):
        '''Checks if the url can be accessed and points to a valid image. If yes, caches the image content (bytes).

        Returns:
            valid (bool): Whether the url points to a valid image
        '''
        try:
            page = requests.get(self.url)
        except Exception as e:
            logger.error(f"Encountered exception {e} while trying to get {self.url}")
            return False

        # Check status code
        if (page.status_code != 200):
            return False

        # Check if binary data is valid image
        try:
            if (helpers.is_image(page.content)):
                # Cache the binary data to avoid duplicate request
                self.image_content = page.content
                return True
        except TypeError as e:
            logger.error(e)
            return False

    def extractAndSave(self, image_pk):
        '''First, extracts information about the image and then saves it to the database.

        Args:
            image_pk (int): Primary key of the image entry in the database
        '''
        self.extract()
        self.save(image_pk)

    def extract(self):
        '''Extracts sha1, height, width and type (extension) of the image.
        Verifies the url if it has not been verified already.

        Raises:
            TypeError: Url is invalid

        Returns:
            None
        '''
        # First, check if url was verified
        if (not self.image_content and not self.verify()):
            raise TypeError("Url is not a real image")

        # Extract data 
        self.sha1 = hashlib.sha1(self.image_content).hexdigest()
        img = PIL.Image.open(BytesIO(self.image_content))
        self.width, self.height = img.size
        self.type = filetype.guess(self.image_content).extension

    def save(self, image_pk):
        '''Saves the extracted information into the database for entry with primary key image_pk.

        Args:
            image_pk (int): Primary key of the image entry in the database
        '''
        try:
            image_entry = Image.objects.get(pk=image_pk)
        except ObjectDoesNotExist:
            logger.error(f"Image with pk {image_pk} does not exist")
            return
        
        image_entry.url = self.url
        image_entry.hash = self.sha1.encode('utf-8')
        image_entry.width = self.width
        image_entry.height = self.height
        image_entry.type = self.type
        image_entry.save()