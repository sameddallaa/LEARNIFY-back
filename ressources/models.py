from django.db import models
from profiles.models import User, Teacher, Year, Student

# Create your models here.


def valid_coeff(coeff):
    if coeff < 0:
        raise ValueError('Coefficient must be a positive number')

class Subject(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    main_teacher = models.ForeignKey(Teacher, null=True, on_delete=models.SET_NULL)
    teachers = models.ManyToManyField(Teacher, related_name='subjects',default=[main_teacher], null=True, blank=True)
    year = models.ForeignKey(Year, on_delete=models.SET_NULL, null=True)
    coefficient = models.IntegerField(validators=[valid_coeff])
    credit = models.IntegerField()
    place = models.CharField(default='Amphi D', max_length=255)
    
    
    def save(self, *args, **kwargs):
        # if self.main_teacher not in self.teachers:
        #     self.teachers.add(self.main_teacher)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name
    
    
class Chapter(models.Model):
    
    name = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    number = models.IntegerField(default=1)
    is_visible = models.BooleanField(default=True)
    
    
    def save(self, *args, **kwargs):
        existing_chapters = Chapter.objects.filter(subject=self.subject).distinct().count()
        self.number = existing_chapters + 1
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    chapter = models.ForeignKey(Chapter, null=True, on_delete=models.SET_NULL)
    content = models.FileField(upload_to='courses/')
    number = models.IntegerField(default=1)
    
    def save(self, *args, **kwargs):
        existing_courses = Course.objects.filter(chapter=self.chapter).count()
        self.number = existing_courses + 1
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
class TD(models.Model):
    
    class Meta:
        verbose_name = 'TD'
        verbose_name_plural = 'TDs'
        
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    chapter = models.ForeignKey(Chapter, null=True, on_delete=models.SET_NULL)
    content = models.FileField(upload_to='tds/')
    number = models.IntegerField(null=True, blank=True, default=1)
    
    def save(self, *args, **kwargs):
        existing_tds = TD.objects.filter(chapter=self.chapter).count()
        self.number = existing_tds + 1
        
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title
    
    
class TP(models.Model):
    
    class Meta:
        verbose_name = 'TP'
        verbose_name_plural = 'TPs'
        
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    chapter = models.ForeignKey(Chapter, null=True, on_delete=models.SET_NULL)
    content = models.FileField(upload_to='tps/')
    number = models.IntegerField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        existing_tps = TP.objects.filter(chapter=self.chapter).distinct().count()
        self.number = existing_tps + 1
        
        super().save(*args, **kwargs)
    def __str__(self):
        return self.title
    
    
class Homework(models.Model):
        
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    chapter = models.ForeignKey(Chapter, null=True, on_delete=models.SET_NULL)
    deadline = models.DateTimeField(null=True, blank=True)
    content = models.FileField(upload_to='devoirs/')
    number = models.IntegerField(null=True, blank=True, default=1)
    
    def save(self, *args, **kwargs):
        existing_homeworks = Homework.objects.filter(chapter=self.chapter).count()
        self.number = existing_homeworks + 1
        
        super().save(*args, **kwargs)
    class Meta:
        verbose_name_plural = 'Homework'
    
    def __str__(self):
        return self.title
    
class Other(models.Model):
    
    title = models.CharField(max_length=255)
    link = models.URLField()
    number = models.IntegerField(default=1)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        existing_others = Other.objects.filter(chapter=self.chapter).count()
        self.number = existing_others + 1
        
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title
    
class Note(models.Model):
    owner = models.ForeignKey(Student, on_delete=models.CASCADE,)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    
    def __str__(self):
        return f'{self.owner}\'s note - {self.subject}'
    
class Quiz(models.Model):
    
    class Meta:
        verbose_name_plural = 'Quizzes'
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    deadline = models.DateTimeField(null=False)
    number = models.IntegerField(default=1)
    
    def save(self, *args, **kwargs):
        existing_quizzes = Quiz.objects.filter(chapter=self.chapter).count()
        self.number = existing_quizzes + 1
        
        super().save(*args, **kwargs)
        
    @property
    def questions(self):
        return Question.objects.filter(quiz=self)
    def __str__(self):
        return f'{self.chapter} - Quiz #{self.number}'

class Question(models.Model):
    content = models.TextField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    number = models.IntegerField(default=1)
    
    def save(self, *args, **kwargs):
        existing_questions = Question.objects.filter(quiz=self.quiz).count()
        self.number = existing_questions + 1
        
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f'{self.quiz} - Question #{self.number}'

class Answer(models.Model):
    content = models.CharField(max_length=255)
    is_correct = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.question} - {self.content}'
    
    
class Forum(models.Model):
    subject = models.OneToOneField(Subject, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.subject} - Forum'
    
    
class Post(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    upvotes = models.ManyToManyField(User, blank=True, related_name='upvoted_posts')
    downvotes = models.ManyToManyField(User, blank=True, related_name='downvoted_posts')
    attachment = models.FileField(blank=True, null=True, upload_to='forum/')
    # comments = models.ManyToManyField(Comment)
    @property
    def comments(self):
        return Comment.objects.filter(post=self).count()
    
    def __str__(self):
        return f'{self.title} - {self.forum} | Post by {self.author}'
    
    def upvote(self, user: User):
        if user in self.upvotes.all():
            self.upvotes.remove(user)
            self.save()
        else:
            self.upvotes.add(user)
        if user in self.downvotes.all():
            self.downvotes.remove(user)
        self.save()
    def downvote(self, user: User):
        if user in self.downvotes.all():
            self.downvotes.remove(user)
            self.save()
        else:
            self.downvotes.add(user)
        if user in self.upvotes.all():
            self.upvotes.remove(user)
        self.save()
        
    @property
    def get_votes(self):
        return self.upvotes.count() - self.downvotes.count()
        
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,)
    date = models.DateTimeField(auto_now_add=True,)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, null=True)
    upvotes = models.ManyToManyField(User, blank=True, related_name='upvoted_comments')
    downvotes = models.ManyToManyField(User, blank=True, related_name='downvoted_comments')
    attachment = models.FileField(blank=True, null=True, upload_to='forum/')
    def __str__(self):
        return f"{self.post} - comment by {self.author}"
    
    def save(self, *args, **kwargs):
        self.forum = self.post.forum
        super().save(*args, **kwargs)
        
    def upvote(self, user: User):
        self.upvotes.add(user)
        if user in self.downvotes.all():
            self.downvotes.remove(user)
        self.save()
    def downvote(self, user: User):
        self.downvotes.add(user)
        if user in self.upvotes.all():
            self.upvotes.remove(user)
        self.save()
        
    @property
    def get_votes(self):
        return self.upvotes.count() - self.downvotes.count()
class News(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='news/images/', null=True, blank=True)
    year = models.ForeignKey(Year, blank=True, null=True, on_delete=models.CASCADE)
    attachment = models.FileField(upload_to='news/attachments/', null=True, blank=True)
    
    
    class Meta:
        verbose_name_plural = 'News'
        
    def __str__(self):
        return f'{self.title}'