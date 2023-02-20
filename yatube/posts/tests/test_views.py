from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User


class TestView(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
#        cls.user = User.objects.create_user(username='auth')
        cls.author = User.objects.create_user(username='author')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_group',
            description='Тестовое описание'
        )
        cls.post = Post.objects.create(
            author=cls.author,
            text='Тестовый пост про чтот то',
            group=cls.group
        )
        cls.author_client = Client()
        cls.author_client.force_login(TestView.author)

    def test_of_using_correct_templates(self):
        """Проверка соответствия шаблонов."""
        templates = {
            reverse('posts:index'): 'posts/index.html',
            reverse(
                'posts:group_list',
                kwargs={'slug': TestView.group.slug}
            ): 'posts/group_list.html',
            reverse(
                'posts:profile',
                kwargs={'username': TestView.author.username}
            ): 'posts/profile.html',
            reverse(
                'posts:post_detail',
                kwargs={'post_id': TestView.post.pk}
            ): 'posts/post_detail.html',
            reverse(
                'posts:post_edit',
                kwargs={'post_id': TestView.post.pk}
            ): 'posts/create_post.html',
            reverse('posts:post_create'): 'posts/create_post.html',
        }

        for url, template in templates.items():
            with self.subTest(url=url):
                response = TestView.author_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_context(self):
        pass
