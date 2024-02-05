from django.db import models
from django.contrib.auth.models import User
import os
from django.utils.safestring import mark_safe
from django.template.defaultfilters import truncatechars
import qrcode
from io import BytesIO
from PIL import Image, ImageDraw
from django.core.files import File
from urllib import request
from datetime import datetime, date
import re  # Import regular expressions

from urllib.request import urlopen
from tempfile import NamedTemporaryFile
# Create your models here.
def sanitized_filename(url):
    # Remove or replace invalid characters for filenames
    return re.sub(r'[^\w\s-]', '', url.replace(':', '_').replace('/', '_'))


def avatar_upload_to(instance, filename):
    # Get the username of the user
    username = instance.user.username
    # Use the username to create a folder in the avatars folder
    folder = f'avatars/{username}'
    # Return the path to the avatar image
    return os.path.join(folder, filename)

def ai_buddy_upload_to(instance, filename):
    # Get the username of the user
    username = instance.user.username
    # Use the username to create a folder in the avatars folder
    folder = f'ai_buddy/{username}/'
    # Return the path to the avatar image
    return os.path.join(folder, filename)

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=avatar_upload_to, blank=True, null=True, max_length=1000)
    url = models.URLField(default='www.pipinstallpython.com', blank=True, null=True, max_length=1000)

    description = models.TextField(blank=True)
    donation_link = models.URLField(blank=True, null=True)
    youtube_link = models.URLField(blank=True, null=True)
    discord_link = models.URLField(blank=True, null=True)
    reddit_link = models.URLField(blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)
    snapchat_link = models.URLField(blank=True, null=True)
    dm_link = models.URLField(blank=True, null=True)
    website_link = models.URLField(blank=True, null=True)
    credits = models.FloatField(default=0)
    qr_image = models.ImageField(upload_to=f'QR_Location/%Y/%m/%d/', default='None.png', blank=True)
    theme = models.CharField(max_length=100, default='SOLAR')
    lat = models.FloatField(blank=True, default=0)
    lon = models.FloatField(blank=True, default=0)
    birthday = models.DateField(blank=True, default=date(1996, 1, 18))

    @property
    def qr_short_description(self):
        return truncatechars(self.url, 10000)

    def qr_photo(self):
        if self.qr_image == 'None.png':
            return mark_safe(
                f'<img src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.pirate.si%2Fwp-content%2Fuploads%2F2019%2F08%2Ferror-pic.png&f=1&nofb=1" width="100" />')
        else:
            return mark_safe(f'<img src="{self.qr_image.url}" width="100" />')

    def admin_photo(self):
        return mark_safe(f'<img src="{self.avatar.url}" width="50" height="125" />')

    def save(self, *args, **kwargs):
        # make the qr img
        img = qrcode.make(self.url)
        # establish a larger canvas
        canvas = Image.new('RGB', (369, 369), 'white')
        # join the img and canvas together
        draw = ImageDraw.Draw(canvas)
        canvas.paste(img)
        # Use sanitized_filename to generate a safe filename
        sanitized_url = sanitized_filename(self.url)
        filename = f"qr-{sanitized_url}.png"
        # save as a PNG
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        # upload image to the model field
        self.qr_image.save(filename, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)

    qr_photo.short_description = 'Image'
    qr_photo.allow_tags = True

    admin_photo.short_description = 'Image'
    admin_photo.allow_tags = True

    def __str__(self):
        return f'{self.user}'

