from functools import partial

from yhttp.core.guard import String, Integer, File


PG_INTMAX = 2147483647
URL_REGEX = r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()' \
    r']{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
TIMEZONE_REGEX = r'^(?:Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])$'
LOCALE_REGEX = r'^[a-z]{2}(-[A-Z]{2})?$'
PHONE_REGEX = r'^\+\d{1,2}\s\(\d{3}\)\s\d{3}\s\d{4}$'
EMAIL_REGEX = r'(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{' \
    r'|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x0' \
    r'1-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+' \
    r'[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0' \
    r'-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9' \
    r'])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f' \
    r']|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'


Email = partial(String, pattern=EMAIL_REGEX, length=(6, 254))
Phone = partial(String, pattern=PHONE_REGEX, length=(18, 18))
Locale = partial(String, pattern=LOCALE_REGEX, length=(2, 5))
Timezone = partial(String, pattern=TIMEZONE_REGEX, length=(6, 6))
Url = partial(String, pattern=URL_REGEX, length=(7, 2048))
Nickname = partial(String, length=(3, 20))
Username = partial(String, length=(1, 30))

ID = partial(Integer, range=(1, PG_INTMAX))
Title = partial(String, length=(3, 50))
Description = partial(String, length=(0, 1024))
VectorImage = partial(File, extensions=['.svg'])
BitmapImage = partial(File, extensions=[
    '.jpg',
    '.jpeg',
    '.webp',
    '.avif',
    '.gif',
    '.png'
])
PositiveInteger = partial(Integer, range=(0, PG_INTMAX))
