def format_number(number):
    suffixes = ["", "K", "M", "B", "T"]
    i = 0

    while abs(number) >= 1000 and i < len(suffixes) - 1:
        number /= 1000.0
        i += 1

    return (
        f"{number:.1f}{suffixes[i]}"
        if i > 0 and i < len(suffixes)
        else str(int(number))
    )
