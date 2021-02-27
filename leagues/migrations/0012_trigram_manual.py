# manually created

from django.db import migrations
from django.contrib.postgres import operations

class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0011_auto_20200826_0336')
    ]

    operations = [
        operations.TrigramExtension()
    ]