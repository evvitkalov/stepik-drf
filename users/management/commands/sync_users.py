from users.models import User
from django.core.management.base import BaseCommand, CommandError

import requests
from json.decoder import JSONDecodeError


data_source_url = 'https://raw.githubusercontent.com/stepik-a-w/drf-project-boxes/master/recipients.json'


class Command(BaseCommand):
    help = 'Syncs users from the data source'

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
            user_id = resp_item['id']
            try:
                User.objects.get(pk=resp_item['id'])
            except User.DoesNotExist:
                user = User()

                user.id = user_id
                user.username = resp_item['email'].split('@')[0]
                user.email = resp_item['email']
                user.password = resp_item['password']

                user.first_name = resp_item['info']['name']
                user.last_name = resp_item['info']['surname']
                user.middle_name = resp_item['info']['patronymic']

                user.address = resp_item['contacts']['city_kladr']
                user.phone_number = resp_item['contacts']['phoneNumber']

                # other available fields were skipped
                user.save()
                counter += 1
        if counter > 0:
            self.stdout.write(self.style.SUCCESS(f"Successfully added {counter} of {len(resp_dict)} items."))
        else:
            self.stdout.write(self.style.SUCCESS(f"No new items were added."))
