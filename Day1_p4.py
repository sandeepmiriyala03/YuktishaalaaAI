def show_friends(*args):

    for name in args:
        print(f"Hello  {name}!")

# టెస్టింగ్:
show_friends("a", "b") 
show_friends("c", "d", "e", "f")