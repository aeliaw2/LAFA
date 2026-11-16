import pycountry

MANUAL_FIXES = {
    "China, mainland": "CHN",
    "China": None,  # FAOSTAT's combined "China" (mainland + HK + Macao + Taiwan) is excluded
}


def m49_to_iso3(code):
    code = str(code).replace("'", "").strip().zfill(3)
    country = pycountry.countries.get(numeric=code)
    return country.alpha_3 if country else None


def name_to_iso3(name):
    name = str(name).strip()
    if name in MANUAL_FIXES:
        return MANUAL_FIXES[name]
    try:
        return pycountry.countries.lookup(name).alpha_3
    except LookupError:
        return None


def is_iso3_country(code):
    return pycountry.countries.get(alpha_3=str(code).strip()) is not None


if __name__ == "__main__":
    print(m49_to_iso3("'004"))              # AFG
    print(name_to_iso3("Kenya"))            # KEN
    print(name_to_iso3("China, mainland"))  # CHN
    print(name_to_iso3("World"))            # None
    print(is_iso3_country("AFE"))           # False