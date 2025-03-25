import random
import string

_alfabet = string.ascii_uppercase + string.digits

# генерация короткой ссылки
def random_alfanum(n: int) -> str:
    return "".join(random.choice(_alfabet) for _ in range(n))
