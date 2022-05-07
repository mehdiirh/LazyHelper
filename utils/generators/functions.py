import random
import string


def generate_unique_id(length: int = 32, model=None, field: str = 'api_key') -> str:
    """
    generate a unique hex ID

    Args:
        length (int): expected length of string
        model (Model): if model presents, function will check if id is unique on the model's `field`
        field (str): the field to search for unique id

    Returns:
        str: hex unique id
    """

    while True:
        token = [random.choice(string.hexdigits) for _ in range(length)]
        token = ''.join(token)
        token = token.lower()

        # if tracking ID is duplicate, generate a new one
        if model and field:
            if model.objects.filter(**{field: token}).exists():
                continue

        return token

