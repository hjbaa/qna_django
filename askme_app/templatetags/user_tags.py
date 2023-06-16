from django import template

register = template.Library()


@register.filter
def upvoted_for(user, obj):
    return user.profile.upvoted_for(obj)


@register.filter
def downvoted_for(user, obj):
    return user.profile.downvoted_for(obj)


@register.filter
def author_of(user, obj):
    return obj.author == user
