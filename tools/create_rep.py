from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
from scipy.stats import iqr
import pandas as pd
import numpy as np
import math
import os

# prints list
def printList(items):
    for i in range(len(items)):
        print(items[i])

# sets any nah to 0 value
def removeNAH(data):
    for i in range(len(data)):
        for j in range(len(data[i])):
            if(str(data[i][j]) == 'nan'):
                data[i][j] = 0
    return data

# read text file into list of lists
def readFile(name):
    with open(name) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    final = []
    for i in range(len(content)):
        final.append(list(map(float, content[i].split())))
    return removeNAH(final)

# grabs all values for a certain frame
def frameOnly(frame, values):
    result = []
    for i in range(len(values)):
        if(values[i][0] == frame):
            x = values[i]
            x.pop(0) ; x.pop(0)
            result.append(x)
    return result

# returns distance between two 3D points
def TDD(p1, p2):
    return float(np.linalg.norm(np.array(p1)-np.array(p2)))

# finds the angle of b point based on points a and c
def findAngle(a, b, c):
    a = np.array(a) ; b = np.array(b) ; c = np.array(c)
    ba = a - b
    bc = c - b
    top = np.dot(ba, bc)
    bottom = np.linalg.norm(ba) * np.linalg.norm(bc)
    if(bottom == 0):
        cosang = 0
    else:
        cosang = top / bottom
    ans = np.arccos(cosang)
    # returns value in degrees
    return np.degrees(ans)

# removes lower and upper bound of data
def cleanData(a):
    a = np.array(a)
    iqr2 = iqr(a)
    q1 = np.quantile(a, .25)
    q3 = np.quantile(a, .75)
    lower = q1 - (1.5*iqr2) # Lower = Q1 - 1.5*IQR
    upper = q3 + (1.5*iqr2) # Upper = Q3 + 1.5*IQR
    z = []
    for i in range(len(a)):
        if(a[i] >= lower and a[i] <= upper):
            z.append(a[i])
        else:
            if(a[i] < lower):
                z.append(lower)
            else:
                z.append(upper)
    return np.array(z)

# creates normalized histogram for distance values (RAD)
def makeHist(data):
    BIN_SIZE = 9 #!BINSIZE
    weights = np.ones_like(data)/float(len(data))
    ans = plt.hist(data, bins=BIN_SIZE, density=False, weights=weights)
    return ans

# creates normalized histogram for angle values (RAD)
def makeHistAng(data):
    BIN_SIZE = 23 #!BINSIZE
    weights = np.ones_like(data)/float(len(data))
    ans = plt.hist(data, bins=BIN_SIZE, density=False, weights=weights)
    return ans

# determines joint displacement (HJPD)
def jointDisplacement(p_c, p_x):
    p_c = np.array(p_c)
    p_x = np.array(p_x)
    return list(p_x - p_c)

# creates normalized histogram for displacements (HJPD)
def makeHistCustom(data):
    BIN_SIZE = 8 #!BINSIZE
    weights = np.ones_like(data)/float(len(data))
    ans = plt.hist(data, bins=BIN_SIZE, density=False, weights=weights)
    return ans

def getLabel(values):
    ans = ""
    for i in range(len(values)):
        if(values[i] == "_"):
            break
        elif(i > 0):
            ans = ans + values[i]
    ans = str(int(ans))
    return ans

# writes results into desired file in LIBSVM format (P3D2 - modification)
def writeData(fileName, data, rawData):
    ans = []
    for i in range(len(data)):
        point = getLabel(rawData[i]) + " "
        for j in range(len(data[i])):
            if(j == len(data[i])-1):
                point = point + str(j+1) + ":" + str(data[i][j])
            else:
                point = point + str(j+1) + ":" + str(data[i][j]) + " "
        ans.append(point)
    with open(fileName, 'w') as f:
        for item in ans:
            f.write("%s\n" % item)
    print("File Created")

# Relative Angles and Distances Representation (RAD)
def RAD(rawData, directory, fileName):
    writingList = []
    # for each instance in Train or Test do
    for i in range(len(rawData)):
        loc = directory + str(rawData[i])
        print(loc, i+1)
        data = readFile(loc)
        maxFrame = int(data[len(data)-1][0])
        dist = []
        angs = []
        # for frame t = 1, ..., T do
        for j in range(1, maxFrame+1):
            frame = frameOnly(j, data) ; frame = removeNAH(frame)
            # Select joints that form a star skeleton
            center = frame[0]
            head = frame[3]
            leftHand = frame[7]
            leftFeet = frame[15]
            rightHand = frame[11]
            rightFeet = frame[19]
            # Compute and store distances between body extremities to body center
            dist.append([TDD(center, leftHand),
                         TDD(center, leftFeet),
                         TDD(center, head),
                         TDD(center, rightFeet),
                         TDD(center, rightHand)])
            # Compute and store angles between two adjacent body extremities
            angs.append([findAngle(leftFeet, center, leftHand),
                       findAngle(head, center, leftHand),
                       findAngle(leftFeet, center, rightFeet),
                       findAngle(head, center, rightHand),
                       findAngle(rightFeet, center, rightHand)])

        C_LH = [] ; C_LF = [] ; C_HD = [] ; C_RF = [] ; C_RH = []
        AC_LH = [] ; AC_LF = [] ; AC_HD = [] ; AC_RF = [] ; AC_RH = []

        for k in range(0, len(dist)):
            C_LH.append(dist[k][0])
            C_LF.append(dist[k][1])
            C_HD.append(dist[k][2])
            C_RF.append(dist[k][3])
            C_RH.append(dist[k][4])

            AC_LH.append(angs[k][0])
            AC_LF.append(angs[k][1])
            AC_HD.append(angs[k][2])
            AC_RF.append(angs[k][3])
            AC_RH.append(angs[k][4])

        # Each histogram is normalized by dividing T to compensate for different number of frames in a data instance

        # Compute a histogram of N bins for each distance
        a = makeHist(cleanData(C_LH))
        b = makeHist(cleanData(C_LF))
        c = makeHist(cleanData(C_HD))
        d = makeHist(cleanData(C_RF))
        e = makeHist(cleanData(C_RH))

        # Compute a histogram of M bins for each angle
        aa = makeHistAng(cleanData(AC_LH))
        ab = makeHistAng(cleanData(AC_LF))
        ac = makeHistAng(cleanData(AC_HD))
        ad = makeHistAng(cleanData(AC_RF))
        ae = makeHistAng(cleanData(AC_RH))

        # Concatenate all normalized histograms into a one-dimensional vector of length 5(M + N)
        values = np.concatenate((list(a[0]),
                                 list(b[0]),
                                 list(c[0]),
                                 list(d[0]),
                                 list(e[0]),
                                 list(aa[0]),
                                 list(ab[0]),
                                 list(ac[0]),
                                 list(ad[0]),
                                 list(ae[0])), axis=0)

        writingList.append(list(values))

    # Convert ALL feature vector as a single line in the rad d1 or rad d1.t file
    writeData(fileName, writingList, rawData)

# Histogram of Joint Position Differences Representation (HJPD)
def HJPD(rawData, directory, fileName):
    writingList = []
    # for each instance in Train or Test do
    for i in range(len(rawData)):
        loc = directory + str(rawData[i])
        print(loc, i+1)
        data = readFile(loc)
        maxFrame = int(data[len(data)-1][0])
        dx = [] ; dy = [] ; dz = []
        # for frame t = 1, ..., T do
        for j in range(1, maxFrame+1):
            frame = frameOnly(j, data)
            center = frame[1] # referenced joint (center joint)

            # find displacement between All location joints and referenced joint (center joint)
            for k in range(1, 20+1):
                value = jointDisplacement(center, frame[k-1])
                dx.append(value[0])
                dy.append(value[1])
                dz.append(value[2])

        # Each histogram is normalized by dividing T to compensate for different number of frames in a data instance
        # Compute a histogram for delta x, y, and z
        x = makeHist(cleanData(dx))
        y = makeHist(cleanData(dy))
        z = makeHist(cleanData(dz))

        # Concatenate all normalized histograms into a one-dimensional vector
        final = np.concatenate((x[0], y[0], z[0]), axis=0)

        writingList.append(final)

    # Convert ALL feature vector as a single line in the outputed file
    writeData(fileName, writingList, rawData)

def generateDataFiles_RAD(path, filename):
    fileDir = os.listdir(path)
    print("Generating RAD for selected data...")
    RAD(fileDir, path, filename)
    print("Created " + filename + " for " + path + " dataset!")

def generateDataFiles_HJPD(path, filename):
    fileDir = os.listdir(path)
    print("Generating HJPD for selected data...")
    HJPD(fileDir, path, filename)
    print("Created " + filename + " for " + path + " dataset!")

def moveDir(filenames, newDir):
    command = "mv " + str(filenames) + " " + str(newDir)
    os.system(str(command))



