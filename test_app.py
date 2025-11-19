# python
import pytest
from app import detect_brand

@pytest.mark.parametrize("card,expected", [
    # Provided examples (sanitization of spaces)
    ("5170 2216 3104 7433", "MasterCard"),        # MasterCard (51..)
    ("2221000000000009", "MasterCard"),           # MasterCard new range (2221..)
    ("4485 6965 0319 0796", "VISA"),              # VISA (starts with 4, len 16)
    ("3498 955223 40325", "American Express"),    # AmEx (34, len 15)
    ("3831 570759 5268", "Diners Club"),          # Diners Club (starts 38, len 14)
    ("30500000000000", "Diners Club"),            # Diners Club (prefix 300-305, len 14)
    ("6011 8099 4610 7875", "Discover"),          # Discover (6011)
    ("6500000000000000", "Discover"),             # Discover (65)
    ("6440000000000000", "Discover"),             # Discover (644-649)
    ("6221260000000000", "Discover"),             # Discover (622126-622925)
    ("2149 9488963 8652", "EnRoute"),             # EnRoute (2149, len 15)
    ("3570 7990 8013 4720", "JCB"),               # JCB (3528-3589 range)
    ("213100000000000", "JCB"),                   # JCB legacy (2131, len 15)
    ("86990 5279 05523 0", "Voyager"),            # Voyager (starts 8699, len 15)
    ("7088000000000000", "Voyager"),              # Voyager (starts 7088, len 16)
    ("6062 8215 6288 2036", "HiperCard"),         # HiperCard (starts 60, len 16)
    ("384000000000000", "HiperCard"),             # HiperCard (starts 38, len 15)
    ("5098 0774 0084 8743", "Aura"),              # Aura (starts 50, len 16)

    # Sanitization: spaces and hyphens removed before detection
    ("  6011-8099 4610-7875  ", "Discover"),     

    # Invalid / Other cases
    ("", "Other"),                                # empty -> Other
    ("abcd efgh ijkl", "Other"),                  # non-digits -> Other
    ("4111", "Other"),                            # starts with 4 but too short -> Other
    ("1234567890123456", "Other"),                # digits but no matching pattern -> Other
])

def test_detect_brand_parametrized(card, expected):
    assert detect_brand(card) == expected# python
