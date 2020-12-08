from builders.quote import build_quote


def build_quotes():
    quotes = [
        build_quote("dx", "ON", "DX 1man - Overnight"),
        build_quote("dx", "930", "DX 1man - Overnight 9:30"),
        build_quote("dx", "AM", "DX 1man - Overnight pre-noon"),
        build_quote("dx", "3Day", "DX 1man - 3Day"),
        build_quote("dx", "SAT", "DX 1man - Saturday"),
        build_quote("dx", "S93", "DX 1man - Saturday 9:30"),
        build_quote("dx", "H2", "DX 2man - Standard"),
        build_quote("dx", "H1", "DX 2man - Overnight"),
        build_quote("dx", "HS", "DX 2man - Saturday"),
    ]

    return quotes
