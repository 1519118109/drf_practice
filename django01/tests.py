from django.test import TestCase

# Create your tests here.

import arrow

print(arrow.now().format('YYYY-MM-DD HH:mm:ss'))