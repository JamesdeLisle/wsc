def simpFactor(value, top):
    if value in [0, top - 1]:
        return 1.0
    elif value % 2 == 0:
        return 4.0
    else:
        return 2.0
