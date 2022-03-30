from django import template

register = template.Library()


@register.filter(name='persian_int')
def persian_int(english_int):
    devanagari_nums = ('۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹')
    number = str(english_int)
    return ''.join(devanagari_nums[int(digit)] for digit in number)


@register.filter(name='persianize_digits')
def persian_int(string):
    persianize = dict(zip("0123456789", '۰۱۲۳۴۵۶۷۸۹'))
    return ''.join(persianize[digit] if digit in persianize else digit for digit in str(string))
