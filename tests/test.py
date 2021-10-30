if __name__ == "__main__":
    var = 44
    var = var | (1<<0)
    print(var)
    print(var & ~(1 << 2))