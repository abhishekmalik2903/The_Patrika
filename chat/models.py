from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, validate_comma_separated_integer_list
from django.db import models
from autoslug import AutoSlugField

# Create your models here.


class Profile(models.Model):
    """ Users Profile or Personal information """
    GENDERCHOICES = (("Male", "Male"), ("Female", "Female"), ("Decline to identify", "Decline to identify"))

    picture = models.ImageField(upload_to='images', default='nick.jpg')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=105)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone Number")
    phone = models.CharField(max_length=17, validators=[phone_regex])
    email = models.EmailField(max_length=150)
    birthday = models.DateTimeField()
    gender = models.CharField(max_length=30, choices=GENDERCHOICES)
    description = models.TextField(null=True, blank=True)
    friends = models.CharField(
        max_length=100000,
        default="",
        validators=[validate_comma_separated_integer_list]
    )
    slug = AutoSlugField(populate_from='username')

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class FriendMessage(models.Model):
    """ Messages that just has a title and text for staff to send to user and Vias varsa.
    Also is used to make Friend Request"""
    from_user = models.CharField(max_length=105)
    to_user = models.ForeignKey(Profile)
    title = models.CharField(max_length=150, null=True, blank=True)
    message = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class Chat(models.Model):
    """ Main Blog message.

        Really three types of Chat's a Post a Comment and a Private Message. A Post has a title and has sharing
    options while a Comment and Private Message is only text and image. A Private Message has the sharing option of
    Private Message while a Comment is Public but only displayed occoding to the the preference of the parent Post.
    A comment is either a comment on a post or another comment which is a comment on a post. A private Message is just
    like a text messaging between two users.

        They are four sharing choices: 1) Public - the post is seen by anyone who is logged in 2) Friends - the post is
    only shown to friends. 3) Only Me - the post is only shown to the user himself. 4) Private Message - the post
    is only showed to the user and a posific friend he chose.   All messages are seen the the staff.
    """
    SHARINGCHOICES = (
        ("Public", "Public"),
        ("Friends", "Friends"),
        ("Only Me", "Only Me"),
        ("Private Message", "Private Message")
    )
    comment = models.ForeignKey('self', null=True, blank=True, default=None)
    distance_from_sourse = models.PositiveIntegerField(default=1)
    likes = models.CharField(
        max_length=100000,
        default="",
        validators=[validate_comma_separated_integer_list]
    )
    private_message = models.ForeignKey(Profile, null="True")

    amount_likes = models.IntegerField(default=0)
    title = models.CharField(max_length=400, default="Post", null=True, blank=True)
    image = models.ImageField(upload_to='images',
                              null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    share = models.CharField(max_length=50, choices=SHARINGCHOICES)
    user = models.ForeignKey(Profile, related_name='user')
    users = models.ManyToManyField(Profile, null=True, related_name='users')
    time_posted = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        if self.title == "Post":
            if self.text:
                return "Text: {}".format(self.text)
            else:
                return "pk: {}".format(self.pk)
        return self.title

    def clean(self):
        if self.comment == self:
            raise ValidationError("a chat cant be a comment on its self")
