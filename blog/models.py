from django.db import models
from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
	"""用户信息表"""
	nid = models.AutoField(primary_key=True)
	phone = models.CharField(max_length=11, null=True, unique=True)
	avatar = models.FileField(upload_to='avatars/', default='avatars/default.jpg', verbose_name='头像')
	create_time = models.DateTimeField(auto_now_add=True)
	blog = models.OneToOneField(to='Blog', to_field='nid', null=True, on_delete=models.PROTECT)

	def __str__(self):
		return self.username


class Blog(models.Model):
	"""博客信息表"""
	nid = models.AutoField(primary_key=True)
	title = models.CharField(max_length=100)  # 个人博客标题
	site = models.CharField(max_length=50, unique=True)  # 个人博客后缀
	theme = models.CharField(max_length=50)  # 博客主题

	def __str__(self):
		return self.title


class Category(models.Model):
	"""文章分类"""
	nid = models.AutoField(primary_key=True)
	title = models.CharField(max_length=32)  # 分类名
	blog = models.ForeignKey(to="Blog", to_field="nid", on_delete=models.CASCADE)  # 外键关联博客，一个博客站点可以有多个分类

	def __str__(self):
		return self.title


class Tag(models.Model):
	"""标签"""
	nid = models.AutoField(primary_key=True)
	name = models.CharField(max_length=32)  # 标签名
	blog = models.ForeignKey(to='Blog', to_field='nid', on_delete=models.CASCADE)  # 外键关联博客，一个博客站点可以有多个标签

	def __str__(self):
		return self.name


class Article(models.Model):
	"""文章"""
	nid = models.AutoField(primary_key=True)
	title = models.CharField(max_length=50)  # 文章标题
	desc = models.CharField(max_length=255)  # 文章描述
	create_time = models.DateTimeField()

	category = models.ForeignKey(Category, on_delete=models.PROTECT)  # 外键关联分类，一个分类可以有多篇文章
	user = models.ForeignKey(to='UserInfo', to_field='nid', on_delete=models.PROTECT)  # 文章作者
	tag = models.ManyToManyField(
		to='Tag',
		through='Article2Tag',
		through_fields=('article', 'tag'),
	)

	def __str__(self):
		return self.title


class ArticleDetail(models.Model):
	"""文章详情表"""
	nid = models.AutoField(primary_key=True)
	content = models.TextField()
	article = models.OneToOneField(to='Article', to_field='nid', on_delete=models.CASCADE)


class Article2Tag(models.Model):
	"""文章和标签多对多关系表"""
	nid = models.AutoField(primary_key=True)
	article = models.ForeignKey(to='Article', to_field='nid', on_delete=models.CASCADE)
	tag = models.ForeignKey(to='Tag', to_field='nid', on_delete=models.CASCADE)

	class Meta:
		unique_together = (('article', 'tag'),)


class ArticleUpDown(models.Model):
	"""文章点赞"""
	nid = models.AutoField(primary_key=True)
	user = models.ForeignKey(to="UserInfo", null=True, on_delete=models.CASCADE)
	article = models.ForeignKey(to="Article", null=True, on_delete=models.CASCADE)
	is_up = models.BooleanField(default=True)

	class Meta:
		unique_together = (("article", "user"),)


class Comment(models.Model):
	"""评论表"""
	nid = models.AutoField(primary_key=True)
	time = models.DateTimeField(auto_now_add=True)
	content = models.TextField(max_length=255)
	article = models.ForeignKey(to='Article', to_field='nid', on_delete=models.CASCADE)
	author = models.ForeignKey(to='UserInfo', to_field='nid', on_delete=models.CASCADE)
	parent_comment = models.ForeignKey("self", null=True, on_delete=models.CASCADE)

	def __str__(self):
		return self.content
