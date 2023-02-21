from random import randint

from django.test import Client, TestCase
from django.urls import reverse
from django.core.paginator import Page
from django.http import HttpResponse
from django.conf import settings

from posts.models import Group, Post, User
from posts.forms import PostForm


class TestView(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
#        cls.user = User.objects.create_user(username='auth')
        cls.authors = (
            User.objects.create_user(username='pshk'),
            User.objects.create_user(username='leo')
        )
        # cls.author = User.objects.create_user(username='author')
        # cls.leo = User.objects.create_user(username='leo')
        cls.groups = (
            Group.objects.create(title='Group1', slug='group1', description='Group1'),
            Group.objects.create(title='Group2', slug='group2', description='Group2')
        )
        
        # cls.group = Group.objects.create(
        #     title='Тестовая группа',
        #     slug='test_group',
        #     description='Тестовое описание'
        # )
        # cls.post = Post.objects.create(
        #     author=cls.author,
        #     text='Тестовый пост про чтот то',
        #     group=cls.group
        # )
        cls.author_client = Client()
        cls.author_client.force_login(TestView.authors[0])
        cls.count_post = (settings.NUMBER_OF_LINES_ON_PAGE
                          + round(settings.NUMBER_OF_LINES_ON_PAGE / 2))

        for i in range(1, cls.count_post):
            Post.objects.create(
                text=i,
                author=TestView.authors[randint(0, len(TestView.authors) - 1)],
                group=TestView.groups[randint(0, len(cls.groups) - 1)]
            )

        # cls.URLS_DATA = {
        #     reverse('posts:index'): {
        #         'template': 'posts/index.html',
        #         'context': {'page_obj': Page}
        #     },

        #     reverse(
        #         'posts:group_list',
        #         kwargs={'slug': TestView.groups[0].slug}
        #     ): {
        #         'template': 'posts/group_list.html',
        #         'context': {'group': Group, 'page_obj': Page}              
        #     },

        #     reverse(
        #         'posts:profile',
        #         kwargs={'username': TestView.authors[0].username}
        #     ): {
        #         'template': 'posts/profile.html',
        #         'context': {'author': User, 'page_obj': Page}
        #     },

        #     reverse(
        #         'posts:post_detail',
        #         kwargs={'post_id': Post.objects.get(pk=1).pk}
        #     ): {
        #         'template': 'posts/post_detail.html',
        #         'context': {'post': Post}
        #     },

        #     reverse(
        #         'posts:post_edit',
        #         kwargs={'post_id': Post.objects.get(pk=1).pk}
        #     ): {
        #         'template': 'posts/create_post.html',
        #         'context': {'is_edit': bool, 'form': PostForm}
        #     },

        #     reverse('posts:post_create'): {
        #         'template': 'posts/create_post.html',
        #         'context': {'form2': PostForm}
        #     }
        # }

        cls.URLS_DATA = (
            (
                reverse('posts:index'), 
                'posts/index.html',
                {'page_obj': Page}
            ),

            (
                reverse(
                    'posts:group_list',
                    kwargs={'slug': TestView.groups[0].slug}
                ),
                'posts/group_list.html',
                {'group': Group, 'page_obj': Page}              
            ),

            (
                reverse(
                    'posts:profile',
                    kwargs={'username': TestView.authors[0].username}
                ),
                'posts/profile.html',
                {'author': User, 'page_obj': Page}
            ),

            (
                reverse(
                    'posts:post_detail',
                    kwargs={'post_id': Post.objects.get(pk=1).pk}
                ),
                'posts/post_detail.html',
                {'post': Post}
            ),

            (
                reverse(
                    'posts:post_edit',
                    kwargs={'post_id': Post.objects.get(pk=1).pk}
                ),
                'posts/create_post.html',
                {'is_edit': bool, 'form': PostForm}
            ),

            (
                reverse('posts:post_create'),
                'posts/create_post.html',
                {'form': PostForm}
            )
        )

    def test_of_using_correct_templates(self):
        """Проверка соответствия шаблонов."""
        # templates = {
        #     reverse('posts:index'): 'posts/index.html',
        #     reverse(
        #         'posts:group_list',
        #         kwargs={'slug': TestView.group.slug}
        #     ): 'posts/group_list.html',
        #     reverse(
        #         'posts:profile',
        #         kwargs={'username': TestView.author.username}
        #     ): 'posts/profile.html',
        #     reverse(
        #         'posts:post_detail',
        #         kwargs={'post_id': TestView.post.pk}
        #     ): 'posts/post_detail.html',
        #     reverse(
        #         'posts:post_edit',
        #         kwargs={'post_id': TestView.post.pk}
        #     ): 'posts/create_post.html',
        #     reverse('posts:post_create'): 'posts/create_post.html',
        # }

        # for url, template in templates.items():
        #     with self.subTest(url=url):
        #         response = TestView.author_client.get(url)
        #         self.assertTemplateUsed(response, template)

        for url, template, dict_ in TestView.URLS_DATA:
            with self.subTest(url=url):
                response = TestView.author_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_context_element_name_and_type(self):
        """Проверим на соответствие контекста."""
    #     context_url = {
    #         reverse('posts:index'): {'page_obj': Page},
    #         reverse(
    #             'posts:group_list',
    #             kwargs={'slug': TestView.group.slug}
    #         ): {'group': Group, 'page_obj': Page},
    #         reverse(
    #             'posts:profile',
    #             kwargs={'username': TestView.author.username}
    #         ): {'author': User, 'page_obj': Page},
    #         reverse(
    #             'posts:post_detail',
    #             kwargs={'post_id': TestView.post.pk}
    #         ): {'post': Post},
    #         reverse(
    #             'posts:post_edit',
    #             kwargs={'post_id': TestView.post.pk}
    #         ): {'is_edit': bool, 'form': PostForm},
    #         reverse('posts:post_create'): {'form': PostForm},
    #     }

    #     for url, context in context_url.items():
    #         with self.subTest(url=url):
    #             response: HttpResponse = TestView.author_client.get(url)
    #             for elem, type_elem in context.items():
    #                 self.assertIsInstance(
    #                     response.context.get(elem),
    #                     type_elem
    #                 )

        for url, template, dict_ in TestView.URLS_DATA:
            with self.subTest(url=url):
                response: HttpResponse = TestView.author_client.get(url)

                for elem, type_elem in dict(dict_).items():
                    self.assertIsInstance(
                        response.context.get(elem),
                        type_elem
                    )
