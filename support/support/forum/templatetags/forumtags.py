from django import template
register = template.Library()


@register.filter(name='answers', is_safe=True)
def submissions(query):
    return query.answer_set.order_by('-last_modified')
