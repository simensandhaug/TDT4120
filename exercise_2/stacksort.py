def sort(stack1, stack2, stack3):
    size = 0
    while not stack1.empty():
        if size%2==0:
            stack2.push(stack1.pop())
        else:
            stack3.push(stack1.pop())
        size+=1
    mSort(stack2, size-(size//2), stack1, stack3, False)
    mSort(stack3, size//2, stack1, stack2, False)
    merge(stack2, stack3, size-(size//2), size//2, stack1, True)

def mSort(mainStack, size, splitToStack1, splitToStack2, asc):
    if(size==1):
        return 
    size1, size2 = split(mainStack, size, splitToStack1, splitToStack2)
    mSort(splitToStack1, size1, mainStack, splitToStack2, not asc)
    mSort(splitToStack2, size2, mainStack, splitToStack1, not asc)
    merge(splitToStack1, splitToStack2, size1, size2, mainStack, asc)

def split(mainStack, size, splitToStack1, splitToStack2):
    for i in range(size//2):
        splitToStack1.push(mainStack.pop())
    for i in range(size-(size//2)):
        splitToStack2.push(mainStack.pop())
    return size//2, size-(size//2)

def merge(stack1, stack2, size1, size2, stack3, asc):
    leftIn1, leftIn2 = size1, size2
    stack1Top, stack2Top = "", ""
    for i in range(size1+size2):
        if leftIn1==0:
            if stack2Top == "":
                stack3.push(stack2.pop())
            else:
                stack3.push(stack2Top)
                stack2Top = ""
            leftIn2-=1
        elif leftIn2==0:
            if stack1Top == "":
                stack3.push(stack1.pop())
            else:
                stack3.push(stack1Top)
                stack1Top = ""
            leftIn1-=1
        else:
            if stack1Top == "":
                stack1Top = stack1.pop()
            if stack2Top == "":
                stack2Top = stack2.pop()
            if (stack1Top<stack2Top)!=asc:
                stack3.push(stack1Top)
                leftIn1-=1
                stack1Top = ""
            else:
                stack3.push(stack2Top)
                leftIn2-=1
                stack2Top = ""   
highscore = True