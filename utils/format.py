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


def format_time(seconds: int):
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        if seconds % 60 == 0:
            return f"{seconds // 60}min"
        else:
            return f"{seconds // 60}min et {seconds % 60}s"
    elif seconds < 86400:
        if (seconds % 3600) // 60 == 0:
            return f"{seconds // 3600}h"
        else:
            return f"{seconds // 3600}h et {(seconds % 3600) // 60}min"
    else:
        if (seconds % 86400) // 3600 == 0:
            return f"{seconds // 86400}j"
        else:
            return f"{seconds // 86400}j et {(seconds % 86400) // 3600}h"
