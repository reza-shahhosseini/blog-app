from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Post
from django.urls import reverse
# Create your tests here.
class BlogTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser',email='test@email.com',password='secret')
        self.post=Post.objects.create(title='A Good Title', author=self.user, body='Nice body content')

    def test_string_representation(self):
        post = Post(title='A Sample Title')
        self.assertEqual(str(post) , post.title)

    def test_post_content(self):
        self.assertEqual(f'{self.post.title}' , 'A Good Title')
        self.assertEqual(f'{self.post.author}' , 'testuser')
        self.assertEqual(f'{self.post.body}' , 'Nice body content')

    def test_post_list_view(self):
        res = self.client.get(reverse('home'))
        self.assertEqual(res.status_code , 200)
        self.assertContains(res,'Nice body content')
        self.assertTemplateUsed(res,'home.html')

    def test_post_detail_view(self):
        res=self.client.get('/post/1/')
        no_response = self.client.get('/post/100000/')
        self.assertEqual(res.status_code,200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(res,'A Good Title')
        self.assertTemplateUsed(res,'post_detail.html')