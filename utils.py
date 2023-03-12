from random import randint
from string import ascii_letters


def _generate_digit_string_of_len(length: int) -> str:
    return "".join([str(randint(0, 9)) for _ in range(length)]).strip()
    

def _generate_letters_string(length: int) -> str:
    possible_chars = ascii_letters + "-" + "_"

    return "".join([possible_chars[randint(0, len(possible_chars) - 1)] for _ in range(length)])


def create_phone_number() -> str:
    three_1 = _generate_digit_string_of_len(3)
    three_2 = _generate_digit_string_of_len(3)
    two_1 = _generate_digit_string_of_len(2)
    two_2 = _generate_digit_string_of_len(2)

    return f"+7-{three_1}-{three_2}-{two_1}-{two_2}"
    

def create_email() -> str:
    email_part_1 = _generate_letters_string(randint(5, 16))

    return f"{email_part_1}@gmail.com"
    
 
def create_address() -> str:
    part_1 = _generate_letters_string(randint(5, 16))
    part_2 = _generate_letters_string(randint(5, 16))
    part_3 = _generate_letters_string(randint(5, 16))

    return ", ".join([part_1, part_2, part_3])


def create_passport_seria() -> str:
    return _generate_digit_string_of_len(4)


def create_passport_number() -> str:
    return _generate_digit_string_of_len(6)


def create_balance() -> float:
    part_1 = randint(0, 1_000_000)
    part_2 = randint(0, 100)
    
    return float(f"{part_1}.{part_2}")


def create_fio() -> str:
    part_1 = _generate_letters_string(randint(5, 10))
    part_2 = _generate_letters_string(randint(5, 10))
    part_3 = _generate_letters_string(randint(5, 10))

    return " ".join([part_1, part_2, part_3])


def create_birthday() -> str:
    year = f"19{_generate_digit_string_of_len(2)}"
    month = f"{randint(1, 12)}".rjust(2, "0")
    day = f"{randint(1, 28)}".rjust(2, "0")

    return "-".join([year, month, day])
