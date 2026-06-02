def customizing(func):
    
        print("Making pizza...")
        func()
        print("Adding sauce...")
        print("completed your customized pizza!")
        # print("==================================")

@customizing
def vegetarian_pizza():
    print("Adding vegetables...")

@customizing
def pepperoni_pizza():
    print("Adding pepperoni...")

vegetarian_pizza()
pepperoni_pizza()