import io
import os

from items.models import Item
from stepik_drf import settings
from django.core.management.base import BaseCommand, CommandError

import requests
from PIL import Image
from urllib.parse import urlparse
from json.decoder import JSONDecodeError


data_source_url = 'https://raw.githubusercontent.com/stepik-a-w/drf-project-boxes/master/foodboxes.json'


def download_image(url):
    static_dir = settings.STATIC_URL
    directory = f"{static_dir[1:]}images"
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            image_resp = resp.content

            # verifying image using PIL
            image = Image.open(io.BytesIO(image_resp))
            image.verify()

            url_filename = os.path.basename(urlparse(url).path)

            try:
                os.makedirs(directory)
            except FileExistsError:
                pass

            try:
                filename = f"{directory}/{url_filename}"
                file = open(filename, 'xb')
            except FileExistsError:
                counter = 2
                while True:
                    filename = f"{directory}/{url_filename}_{counter}"
                    try:
                        file = open(filename, 'wb')
                        break
                    except FileExistsError:
                        pass
            file.write(image_resp)
            return filename
    except ConnectionError:
        raise CommandError(f"Error getting image from {url}")


class Command(BaseCommand):
    help = 'Syncs reviews from the data source'

    def handle(self, *args, **options):
        resp = requests.get(data_source_url)
        if resp.status_code != 200:
            raise CommandError(f"Error getting data from {data_source_url}: "
                               f"[HTTP {resp.status_code}]\n{resp.content}", returncode=1)
        else:
            try:
                resp_dict = resp.json()
            except JSONDecodeError:
                raise CommandError(f"Error deserializing data from {data_source_url}", returncode=2)

        counter = 0

        for resp_item in resp_dict:
            item_id = resp_item['id']
            try:
                Item.objects.get(pk=resp_item['id'])
            except Item.DoesNotExist:
                item = Item()
                item.id = item_id
                item.title = resp_item['title']
                item.description = resp_item['description']
                item.weight = resp_item['weight_grams']
                item.price = resp_item['price']
                item.image = download_image(resp_item['image'])

                # other available fields were skipped
                item.save()
                counter += 1
        if counter > 0:
            self.stdout.write(self.style.SUCCESS(f"Successfully added {counter} of {len(resp_dict)} items."))
        else:
            self.stdout.write(self.style.SUCCESS(f"No new items were added."))
