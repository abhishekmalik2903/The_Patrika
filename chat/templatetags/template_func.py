from django import template

from chat import models

register = template.Library()

# posts


@register.assignment_tag()
def post_filter(post, user, friends):
    """  filters appropriate posts on the main page """
    if friends == "admin":
        return True
    elif post.share == 'Public' or post.user == user:
        return True
    elif friends == False:
        return False
    if post.share == "Only Me":
        if user == post.user:
            return True
        else:
            return False
    elif post.share == "Private Message":
        if user == post.private_message:
            return True
        return False
    for sharer in post.users.all():
        if sharer.id in friends:
            return True

    if post.user.pk in friends:
        return True
    else:
        return False


# comments

@register.assignment_tag()
def has_comments(post, distance):
    """ returns comment on post or comments on comments """
    comments = models.Chat.objects.filter(comment=post).filter(distance_from_sourse=distance).order_by("time_posted")
    return comments


@register.inclusion_tag('chat/comment_loop.html')
def comments_list(comments):
    """ return comments on post to be used in comment_loop.html """
    return {'comments': comments}


@register.assignment_tag()
def new_distance(distance):
    """ adds one to distance occording to the post """
    return distance + 1


@register.assignment_tag()
def last_5_comments(comments, loop):
    """ returns the last 5 comments posted """
    length = len(comments) - 5
    # loop = int(loop) + 1
    if length < 0:
        return comments
    return comments[length:]


# like and share button

@register.assignment_tag()
def share_button_filter(post, user):
    """ Only shows button to share post if Post.is Friend and not shared by the person yet """
    if post.share == 'Public' or post.user == user:
        return False
    for sharer in post.users.all():
        if sharer == user:
            return False
    return True


@register.assignment_tag()
def like_list(likes):
    """returns a list of pk's of all the persons friends"""
    liked_list = likes.split(',')
    try:
        liked = [int(x) for x in liked_list]
        return liked
    except:
        return False


# messages.html

@register.assignment_tag()
def who_sent_messages(private_messages):
    """ returns a dict that has all the names of people that user has a chat with
    and the number of new messages from that person """
    messages_from = {}
    time = ""
    add = True
    for message in private_messages:
        username = message.user.username
        if time != message.user:
            try:
                time = models.Chat.objects.filter(private_message=message.user, user=message.private_message).latest(
                    'time_posted'
                )
                add = False
            except:
                add = True
        if add is False:
            if message.time_posted > time.time_posted:
                if username in messages_from:
                    messages_from[username] += 1
                else:
                    messages_from[username] = 1
            else:
                messages_from[username] = 0
        elif add is True:
            if username in messages_from:
                messages_from[username] += 1
            else:
                messages_from[username] = 1

    return messages_from


# friends.html

@register.assignment_tag()
def friendly_phone_format(phone):
    """ makes the phone number is user profiles to look more frienly with - between like: 1-888-888-8888 """
    phone_number = []
    for index in range(1, len(phone)+1):
        if index > 4:
            if (index - 4) % 3 == 1:
                phone_number.insert(0, "-")
        phone_number.insert(0, phone[-index])
    return "".join(phone_number)
