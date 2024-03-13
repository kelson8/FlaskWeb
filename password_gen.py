import string
import random

def password_gen(characters_number):
    s1 = list(string.ascii_lowercase)
    s2 = list(string.ascii_uppercase)
    s3 = list(string.digits)
    s4 = list(string.punctuation)

    random.shuffle(s1)
    random.shuffle(s2)
    random.shuffle(s3)
    random.shuffle(s4)

    part1 = round(characters_number * (30 / 100))
    part2 = round(characters_number * (20 / 100))

    result = []

    for x in range(part1):
        result.append(s1[x])
        result.append(s2[x])

    for x in range(part2):
        result.append(s3[x])
        result.append(s4[x])

    # Shuffle result
    random.shuffle(result)

    # Join result
    password = ''.join(result)
    return password