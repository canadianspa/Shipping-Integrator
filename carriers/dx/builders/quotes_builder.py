from builders.quote import build_quote


def build_quotes():
    quotes = [
        build_quote("dx", "H2", "DX 2man - Standard"),
        build_quote("dx", "H1", "DX 2man - Overnight"),
        build_quote("dx", "HS", "DX 2man - Saturday"),
    ]

    return quotes
