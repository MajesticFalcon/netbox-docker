from django.contrib.contenttypes.models import ContentType
from extras.models import CustomLink
from startup_script_utils import load_yaml
import sys


custom_links = load_yaml('/opt/netbox/initializers/custom_links.yml')

if custom_links is None:
  sys.exit()

def get_content_type_id(content_type_str):
  for type in ContentType.objects.all():
    if type.name == content_type_str:
      return type.id

for link in custom_links:
  content_type = link.pop('content_type')
  link['content_type_id'] = get_content_type_id(content_type)
  if link['content_type_id'] is None:
    print("⚠️ Error determining content type id for user declared var: {0}".format(content_type))
  else:
    CustomLink(**link).save()

