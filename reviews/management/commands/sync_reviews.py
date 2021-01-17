from users.models import User
from reviews.models import Review
from django.core.management.base import BaseCommand, CommandError

import requests
from json.decoder import JSONDecodeError


data_source_url = 'https://raw.githubusercontent.com/stepik-a-w/drf-project-boxes/master/reviews.json'


class Command(BaseCommand):
    help = 'Syncs items from the data source'

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
            review_id = resp_item['id']
            try:
                Review.objects.get(pk=resp_item['id'])
            except Review.DoesNotExist:
                author_id = resp_item['author']
                try:
                    review = Review()

                    review.id = review_id
                    review.author = User.objects.get(pk=author_id)
                    review.text = resp_item['content']

                    review.created_at = resp_item.get('created_at', '1970-01-01')
                    if resp_item.get('published_at') != str():
                        review.published_at = resp_item.get('published_at', '1970-01-01')
                    review.status = resp_item['status']

                    review.save()
                    counter += 1
                except User.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"Review #{review_id} skipped: user {author_id} does not "
                                                         f"exist"))
        if counter > 0:
            self.stdout.write(self.style.SUCCESS(f"Successfully added {counter} of {len(resp_dict)} items."))
        else:
            self.stdout.write(self.style.SUCCESS(f"No new items were added."))
