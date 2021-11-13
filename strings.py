STRINGS = eval(open("resources/strings.json", mode="r", encoding="UTF-8").read())


def get(key):
    return STRINGS[key]
