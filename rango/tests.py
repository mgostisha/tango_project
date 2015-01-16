from django.test import TestCase
from django.core.urlresolvers import reverse

from rango.models import Category

def add_cat(name, views, likes):
	c = Category.objects.get_or_create(name=name)[0]
	c.views = views
	c.likes = likes
	c.save()
	return c

# Create your tests here.
class CategoryMethodTests(TestCase):

	def test_ensure_views_are_positive(self):
		"""
		views should be handled so they cannot ever be negative!
		"""
		cat = Category(name='test', views=-1, likes=0)
		cat.save()
		self.assertEqual((cat.views >= 0), True)

	def test_slug_line_creation(self):
		"""
		test checks to make sure that when a category is created, a correct slug line for the url is generated
		i.e. 'Random Category String' -> random-category-string
		"""
		cat = Category(name='Random Category String')
		cat.save()
		self.assertEqual(cat.slug, 'random-category-string')


class IndexViewTests(TestCase):

	def test_index_view_with_no_categories(self):
		"""
		If no categories exist, the correct message should be displayed.
		"""
		response = self.client.get(reverse('index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "There are no categories present.")
		self.assertQuerysetEqual(response.context['categories'], [])

	def test_index_view_with_categories(self):
		"""
		If categories exist, they should be displayed and held in the response's context.
		"""
		add_cat('test', 1, 1)
		add_cat('temp', 1, 1)
		add_cat('tmp', 1, 1)
		add_cat('tmp test temp', 1, 1)

		response = self.client.get(reverse('index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "tmp test temp")

		num_cats = len(response.context['categories'])
		self.assertEqual(num_cats, 4)