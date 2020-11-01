from libsvm.svmutil import *
import pandas as pd
import os

# returns the accuracy of the predictions
def theAccuracy(real, predict):
    total = 0
    for i in range(len(real)):
        if(real[i] == predict[i]): total = total + 1
    return (round((total / len(real))*100, 2))

# creates confusion matrix
def confusionMatrix(actual, prediction):
    action = pd.Series(actual, name="Actual Activity Number")
    predict = pd.Series(prediction, name="LIBSVM Classification")
    confusion = pd.crosstab(action, predict)
    return confusion

# prints results (confusion matrix and accuracy %)
def cleanPrint(allReal, allGuess, files, clear):
    if(clear): os.system("clear ; clear")
    x = ""
    line = "-----------------------------------------------------------"
    for i in range(len(allReal)):
        print(line + "\nDataType: " + files + "\nAccuracy: " + str(theAccuracy(allReal[i], allGuess[i])) + "%\n" + line[0:len(line)-18] + "[Confusion_Matrix]")
        print(confusionMatrix(allReal[i], allGuess[i]))
        if(i == len(allReal)-1): print(line)


# prints results (confusion matrix and accuracy %)
def cleanFilePrint(allReal, allGuess, files):
    x = ""
    line = "-----------------------------------------------------------"
    for i in range(len(allReal)):
        x = (line + "\nDataType: " + files + "\nAccuracy: " + str(theAccuracy(allReal[i], allGuess[i])) + "%\n" + line[0:len(line)-18] + "[Confusion_Matrix]")
        x = x + "\n" + str(confusionMatrix(allReal[i], allGuess[i]))
        if(i == len(allReal)-1): x = x + "\n" + line

    # clean files string variable
    files = files.replace("/", "_")
    files = files.replace("-", "_")
    files = files.replace(".", "_")
    files = files + "_CM.txt"

    # save as text file
    text_file = open(files, "w")
    n = text_file.write(x)
    text_file.close()

# creates .predict file based on the generated p_label from svm_predict()
def createPredictFile(fileName, labels):
    with open(str(fileName + ".predict"), 'w') as f:
        for i in range(len(labels)):
            f.write(str(int(labels[i])) + "\n")

# - give a list of train datafiles, test datafiles, c values, gamma values and create a confustion matrix and .predict file
# - each index of these four arrays MUST correspond to each other!
def libsvm_predict(trainD, testDa, cValue, yValue):
    # reads selected training data into LIBSVM format
    train_y, train_x = svm_read_problem(trainD, return_scipy = True)

    # train option with -c for cost and -g for gama, by default its set to the RBF kernel
    option = "-c " + str(cValue) + " -g " + str(yValue)

    # trains with training data and set option, creates our learned C-SVM model
    m = svm_train(train_y, train_x, option)

    # reads selected test data into LIBSVM format
    test_y, test_x = svm_read_problem(testDa, return_scipy = True)

    # predict behavior labels from testing data based on learned C-SVM model
    p_label, p_acc, p_val = svm_predict(test_y, test_x, m)

    # reformat test_y and p_label
    allReal = []    ; allReal.append(test_y)
    allGuess = []   ; allGuess.append(p_label)

    return m, allReal, allGuess, testDa, p_label


