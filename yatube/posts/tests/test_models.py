from django.contrib.auth import get_user_model
from django.test import TestCase

from posts.models import Group, Post

User = get_user_model()


class TestModel(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост проверим длинну сохраняемого текста',
        )

    def test_text_length_post(self):
        len_text = len(str(TestModel.post))
        self.assertEquals(len_text, 15, 'Некорректная длина текста')

    def test_text_value_post(self):
        self.assertEquals(
            str(TestModel.post),
            TestModel.post.text[:15],
            'Некорректное значение текста __str__'
        )

    def test_text_value_group(self):
        self.assertEquals(
            str(TestModel.group),
            TestModel.group.title,
            'Некорректное значение текста __str__'
        )
    
            
