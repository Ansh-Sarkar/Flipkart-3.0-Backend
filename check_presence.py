required = ["ansh1.txt","ansh2.txt","ansh3.txt"]
for file in required:
    try:
        temp = open(file)
        temp.close()
    else:
        temp = open(file,"w")
        temp.close()