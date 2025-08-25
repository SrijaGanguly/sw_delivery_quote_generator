# credits for the format lookup to https://github.com/phalt/swapi/blob/master/resources/renderers.py


wookie_lookup = {
        "a": "ra",
        "b": "rh",
        "c": "oa",
        "d": "wa",
        "e": "wo",
        "f": "ww",
        "g": "rr",
        "h": "ac",
        "i": "ah",
        "j": "sh",
        "k": "or",
        "l": "an",
        "m": "sc",
        "n": "wh",
        "o": "oo",
        "p": "ak",
        "q": "rq",
        "r": "rc",
        "s": "c",
        "t": "ao",
        "u": "hu",
        "v": "ho",
        "w": "oh",
        "x": "k",
        "y": "ro",
        "z": "uf"
}

def convert_to_wookie(json_file, write_file_path=""):
    """
    this function converts a json file to wookie format and generates another json file with the same output
    :param json_file: the file to convert
    :return: a json file in wookie language
    """
    with open(json_file, "r") as read_file:
        json_data = read_file.read()

    translation_table = str.maketrans(wookie_lookup)
    new_json_data = json_data.translate(translation_table)

    with open(write_file_path + "sales_vehicle_delivery_quote_wookie.json", "w") as write_file:
        write_file.write(new_json_data)
