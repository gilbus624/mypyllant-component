#!/usr/bin/env python3
import re

import country_list  # type: ignore
import requests

from .libs.myPyllant.const import BRANDS


def countries_with_realm(brand):
    country_codes = country_list.countries_for_language("en") + [
        ("XK", "Kosovo"),
    ]
    country_codes.sort(key=lambda x: x[1])

    for code, country in country_codes:
        if code == "CZ":
            country_name = "czechrepublic"
        elif code == "TR":
            country_name = "turkiye"
        else:
            country_name = re.sub(r"\W+", "", country.lower())
        r = requests.head(
            f"https://identity.vaillant-group.com/auth/realms/"
            f"{brand}-{country_name}-b2c/.well-known/openid-configuration"
        )
        if r.status_code == 200:
            yield country_name, country


def main():
    print("COUNTRIES = {")
    for brand in BRANDS.keys():
        if brand == "bulex":
            # Bulex has no country-specific realms
            continue
        print(f'    "{brand}": {{')
        for country_name, country in countries_with_realm(brand):
            print(f'        "{country_name}": "{country}",')
        print("    },")
    print("}")


if __name__ == "__main__":
    main()
