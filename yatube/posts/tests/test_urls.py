from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from posts.models import Group, Post

User = get_user_model()

class TestUrl(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.author = User.objects.create_user(username='author')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_group',
            description='Тестовое описание'
        )
        cls.post = Post.objects.create(
            author=cls.author,
            text='Тестовый пост проверим длинну сохраняемого текста',
            group=cls.group
        )

    def setUp(self) -> None:
        self.guest_client = Client()
        self.auth_client = Client()
        self.auth_client.force_login(TestUrl.user)


    def test_exists_url_all(self):
        """Проверка доступность для всех."""
        set_urls = {
            '/': HTTPStatus.OK,
            f'/group/{TestUrl.group.slug}/': HTTPStatus.OK,
            f'/profile/{TestUrl.user.username}/': HTTPStatus.OK,
            f'/posts/{TestUrl.post.pk}/': HTTPStatus.OK,
            'unexisting_page/': HTTPStatus.NOT_FOUND,
        }

        for url, result in set_urls.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(
                    response.status_code,
                    result,
                    f'Не удалось перейти по адресу: {url}'
                )

    def test_not_avaible_url_for_not_auth(self):
        """Проверка на недоступность для обычного пользователя."""
        set_urls = {
            f'/posts/{TestUrl.post.pk}/edit/': HTTPStatus.FOUND,
            '/create/': HTTPStatus.FOUND,
        }

        for url, result in set_urls.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(
                    response.status_code,
                    result,
                    'Не корректная адресация'
                )

    def  test_avaible_url_for_auth(self):
        """Проверим доступность для авторизованного."""
        set_urls = {
            f'/posts/{TestUrl.post.pk}/edit/': HTTPStatus.OK,
            '/create/': HTTPStatus.OK,
        }

        for url, result in set_urls.items():
            with self.subTest(url=url):
                response = self.auth_client.get(url)
                self.assertEqual(
                    response.status_code,
                    result,
                    f'Не удалось перейти по адресу: {url}'
                )

    def test_avaible_url_for_author(self):
        pass


    # def test_urls_uses_correct_template_not_auth(self):
    #     """Проверим шаблоны для неавторизованного пользователя."""
    #     templates = {
    #         '/': 'posts/index.html',
    #         f'/group/{TestUrl.group.slug}/': 'posts/group_list.html',
    #         '/profile/auth/': 'posts/profile.html',
    #         f'/posts/{TestUrl.post.pk}/': 'posts/post_detail.html',
    #         f'/posts/{TestUrl.post.pk}/edit/': 'posts/create_post.html',
    #         '/create/': 'posts/create_post.html',
    #     }

    #     for url, template in templates.items():
    #         with self.subTest(url=url):
    #             response = self.guest_client.get(url)
    #             self.assertTemplateUsed(response, template)

    # def test_urls_uses_correct_template_auth(self):
    #     """Проверим шаблоны для авторизованного пользователя тоже."""        
    #     templates = {
    #         '/': 'posts/index.html',
    #         f'/group/{TestUrl.group.slug}/': 'posts/group_list.html',
    #         '/profile/auth/': 'posts/profile.html',
    #         f'/posts/{TestUrl.post.pk}/': 'posts/post_detail.html',
    #         f'/posts/{TestUrl.post.pk}/edit/': 'posts/create_post.html',
    #         '/create/': 'posts/create_post.html',
    #     }

    #     for url, template in templates.items():
    #         with self.subTest(url=url):
    #             response = self.auth_client.get(url)
    #             self.assertTemplateUsed(response, template)

