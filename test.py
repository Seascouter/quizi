x = {
    "y": lambda: print("hello"),
    "z": lambda: print(5+5)
}

x["y"]()
x["z"]()
x["z"]()
