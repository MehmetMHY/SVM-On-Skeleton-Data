from tools import create_rep as cr
from tools import libsvm_predict as lsp
import os

# read file into a list
def file_to_list(file):
    temp = []
    with open(file) as f:
        temp = f.readlines()
    return [x.strip() for x in temp]

# print content of a list, line by line
def print_list(data):
    for i in data:
        print(i)

# indent or "clear" the terminal
def clean_or_space(ID):
    if(ID == 1):
        os.system("clear")
    else:
        print()

# create RAD skeleton representation for test and train datasets
cr.generateDataFiles_RAD("tools/mod_dataset/test/", "rad_d2.t")
cr.generateDataFiles_RAD("tools/mod_dataset/train/", "rad_d2")

# create HJPD skeleton representation for test and train datasets
cr.generateDataFiles_HJPD("tools/mod_dataset/test/", "cust_d2.t")
cr.generateDataFiles_HJPD("tools/mod_dataset/train/", "cust_d2")

# move representations to reps/ directory
cr.moveDir("rad_d2*", "reps/")
cr.moveDir("cust_d2*", "reps/")

print("\n4 Files Created And Moved- DONE! \n")

# use LIBSVM to create a model & predictions for RAD representation
model, real, guess, testData, predictions = lsp.libsvm_predict('reps/rad_d2', 'reps/rad_d2.t', 2, 0.5)

# create confusion matrix for predictions from RAD representation
lsp.cleanFilePrint(real, guess, testData)

# use LIBSVM to create a model & predictions for HJ
model, real, guess, testData, predictions = lsp.libsvm_predict('reps/cust_d2', 'reps/cust_d2.t', 2, 12)
lsp.cleanFilePrint(real, guess, testData)

cr.moveDir("*CM.txt", "confusion_matrix")

# Print complete message
print("\nDONE!")

# print final confusion matrixs
clean_or_space(1) # print a space or "clear" terminal
print_list(file_to_list("confusion_matrix/reps_rad_d2_t_CM.txt"))
print()
print_list(file_to_list("confusion_matrix/reps_cust_d2_t_CM.txt"))
