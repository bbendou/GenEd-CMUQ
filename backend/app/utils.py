def semester_sort_key(sem: str):
    """
    Sort a semester code based on an academic cycle:
      - For Fall (F): effective_year = int(year), order = 0.
      - For Spring (S) and Summer (M): effective_year = int(year) - 1,
        order = 1 for Spring, 2 for Summer.
    For example:
      F20 -> (20, 0)
      S21 -> (20, 1)
      M21 -> (20, 2)
      F21 -> (21, 0)
    """
    letter = sem[0].upper()
    try:
        year = int(sem[1:])
    except Exception:
        year = 0

    if letter == "F":
        effective_year = year
        order = 0
    elif letter == "S":
        effective_year = year - 1
        order = 1
    elif letter == "M":
        effective_year = year - 1
        order = 2
    else:
        effective_year = year
        order = 3

    return effective_year, order
