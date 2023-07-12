from django import template

register = template.Library()

@register.filter
def censor(value):
    banned_words = ['нежелательное_слово1', 'нежелательное_слово2']  # Здесь перечислите нежелательные слова, которые нужно заменить
    for word in banned_words:
        value = value.replace(word, '*' * len(word))
    return value