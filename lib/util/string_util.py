import re


def remove_line_spaces(text):
    return '\n'.join([line for line in text.splitlines() if line.strip()])


def to_snake_case(text):
    text = re.sub(r'([a-z])([A-Z])', r'\1_\2', text)  # camelCase -> snake_case
    text = re.sub(r'[-\s]', '_', text)  # kebab-case, space -> snake_case
    return text.lower()


def to_camel_case(text):
    words = to_snake_case(text).split('_')
    return words[0] + ''.join(word.capitalize() for word in words[1:])


def to_pascal_case(text):
    words = to_snake_case(text).split('_')
    return ''.join(word.capitalize() for word in words)


def to_kebab_case(text):
    return to_snake_case(text).replace('_', '-')


def to_screaming_snake_case(text):
    return to_snake_case(text).upper()


def to_train_case(text):
    return '-'.join(word.capitalize() for word in to_snake_case(text).split('_'))


def to_dot_notation(text):
    words = re.split(r'[\s_\-]+', text)
    return ".".join(word.lower() for word in words)


def to_camel_case_line(text):
    lines = text.strip().split("\n")  # 줄 단위로 분리
    return "\n".join([to_camel_case(line) for line in lines])


def to_snake_case_line(text):
    lines = text.strip().split("\n")  # 줄 단위로 분리
    return "\n".join([to_snake_case(line) for line in lines])


def to_pascal_case_line(text):
    lines = text.strip().split("\n")  # 줄 단위로 분리
    return "\n".join([to_pascal_case(line) for line in lines])


def to_screaming_snake_case_line(text):
    lines = text.strip().split("\n")  # 줄 단위로 분리
    return "\n".join([to_screaming_snake_case(line) for line in lines])


def to_kebab_case_line(text):
    lines = text.strip().split("\n")  # 줄 단위로 분리
    return "\n".join([to_kebab_case(line) for line in lines])


def to_train_case_line(text):
    lines = text.strip().split("\n")  # 줄 단위로 분리
    return "\n".join([to_train_case(line) for line in lines])


def to_dot_notation_line(text):
    lines = text.strip().split("\n")  # 줄 단위로 분리
    return "\n".join([to_dot_notation(line) for line in lines])

def ends_with_pattern(input_string, pattern):
    regex_pattern = pattern + "$"
    match = re.search(regex_pattern, input_string)
    return bool(match)

def is_none_or_empty(s):
    return s is None or s == ''