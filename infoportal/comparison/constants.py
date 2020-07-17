import re

COMMENT_RE = re.compile(br'<!--.*?-->', re.S)
TAG_RE = re.compile(br'<(script|style).*?>.*?</\1>|<.*?>', re.S)
HEAD_RE = re.compile(br'<\s*head\s*>', re.S | re.I)
WS_RE = re.compile(br'^([ \n\r\t]|&nbsp;)+$')
WORD_RE = re.compile(
    br'([^ \n\r\t,.&;/#=<>()-]+|(?:[ \n\r\t]|&nbsp;)+|[,.&;/#=<>()-])'
)


STOPWORDS_EN = (
    'a',
    'about',
    'an',
    'and',
    'are',
    'as',
    'at',
    'be',
    'by',
    'for',
    'from',
    'have',
    'how',
    'I',
    'in',
    'is',
    'it',
    'of',
    'on',
    'or',
    'that',
    'the',
    'this',
    'to',
    'was',
    'what',
    'when',
    'where',
    'who',
    'will',
    'with',
)


STOPWORDS_RU = (
    'бы',
    'был',
    'была',
    'были',
    'было',
    'быть',
    'в',
    'вам',
    'вами',
    'вас',
    'весь',
    'во',
    'вот',
    'вы',
    'да',
    'для',
    'до',
    'его',
    'ее',
    'её',
    'ей',
    'ему',
    'если',
    'есть',
    'еще',
    'ещё',
    'ею',
    'же',
    'за',
    'и',
    'из',
    'или',
    'им',
    'ими',
    'их',
    'к',
    'как',
    'кем',
    'ко',
    'когда',
    'кого',
    'кому',
    'которая',
    'которого',
    'которое',
    'которой',
    'котором',
    'которому',
    'которою',
    'которую',
    'которые',
    'который',
    'которым',
    'которыми',
    'которых',
    'кто',
    'меня',
    'мне',
    'мной',
    'мною',
    'мог',
    'моги',
    'могите',
    'могла',
    'могли',
    'могло',
    'могу',
    'могут',
    'мое',
    'моё',
    'моего',
    'моей',
    'моем',
    'моём',
    'моему',
    'моею',
    'можем',
    'может',
    'можете',
    'можешь',
    'мои',
    'мой',
    'моим',
    'моими',
    'моих',
    'мочь',
    'мою',
    'моя',
    'мы',
    'на',
    'нам',
    'нами',
    'нас',
    'наш',
    'наша',
    'наше',
    'нашего',
    'нашей',
    'нашем',
    'нашему',
    'нашею',
    'наши',
    'нашим',
    'нашими',
    'наших',
    'нашу',
    'не',
    'него',
    'нее',
    'неё',
    'ней',
    'нем',
    'нём',
    'нему',
    'нет',
    'нею',
    'ним',
    'ними',
    'них',
    'но',
    'о',
    'об',
    'один',
    'одна',
    'одни',
    'одним',
    'одними',
    'одних',
    'одно',
    'одного',
    'одной',
    'одном',
    'одному',
    'одною',
    'одну',
    'он',
    'она',
    'они',
    'оно',
    'от',
    'по',
    'при',
    'с',
    'сам',
    'сама',
    'сами',
    'самим',
    'самими',
    'самих',
    'само',
    'самого',
    'самом',
    'самому',
    'саму',
    'со',
    'та',
    'так',
    'такая',
    'такие',
    'таким',
    'такими',
    'таких',
    'такого',
    'такое',
    'такой',
    'таком',
    'такому',
    'такою',
    'такую',
    'те',
    'тебе',
    'тебя',
    'тем',
    'теми',
    'тех',
    'то',
    'тобой',
    'тобою',
    'того',
    'той',
    'тот',
    'тою',
    'у',
    'уже',
    'что',
    'чтобы',
    'эта',
    'эти',
    'этим',
    'этими',
    'этих',
    'это',
    'этого',
    'этой',
    'этом',
    'этому',
    'этот',
    'этою',
    'эту',
    'я',
)
