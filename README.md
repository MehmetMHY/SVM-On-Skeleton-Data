# Application of SVM on RAD & HJPD Skeleton Representations to classify certain human actions
- Date: 11-1-2020

## About:
- For this project, the "MSR Daily Activity 3D Dataset" (MDA3) was used. This dataset contains 16 human activities gathered from a Xbox Kinetic sensor and stored as skeletons which are just real world, (x, y, z), cooridnate of 20 joints points on a human. To get more information about this dataset, please checkout this link: https://wangjiangb.github.io/my_data.html.
- This project contains 2 main elements: representation & Classification.
- Representation: The data is represented either in RAD and/or HJPD.
- Classification: The representation is used with SVM, powered by LIBSVM, to create a model and predict human actions.
- This project was modified to act as a library towards converting skeleton data into RAD or HJPD representations and applying SVM to those representations. 

## Notes:
- For this project, the complete MDA3 dataset and a modified MDA3 dataset is used. The modified MDA3 only contains acitvities 8, 10, 12, 13, 15, & 16. Also the modified verison has some "corrupted" data points in it well the complete dataset does not.
- The main scripts and the datasets are contained in the tools/ directory.
- Took though and run the main.py script to get an idea of how everything works
- File Exploring:
    - README.md : Project's README.
    - confusion_matrix : Where the confusion matrix of the models are, can be, stored.
    - extra : Just extra/random files/assets.
    - main.py : An example of script of how to use this library.
    - reps : Where the data's representation(s) are, can be, stored.
    - tools : Where the main scripts/function and datasets are stored.

## Results:
-----------------------------------------------------------
- DataType: reps/rad_d2.t
- Accuracy: 62.5%
-----------------------------------------------------------
- DataType: reps/cust_d2.t
- Accuracy: 70.83%
-----------------------------------------------------------

## Requirements:
- Python3
- Modules: 
    - LIBSVM
    - Pandas
    - Matplotlib
    - Scipy
    - Numpy 

## Sources:
- Information About The Xbox Kinetic Sensor:
    - https://www.youtube.com/watch?v=uq9SEJxZiUg
    - https://medium.com/@lisajamhoury/understanding-kinect-v2-joints-and-coordinate-system-4f4b90b9df16
    - https://en.wikipedia.org/wiki/Kinect
    - https://www.jameco.com/Jameco/workshop/Howitworks/xboxkinect.html#:~:text=Hardware,body%2Dtype%20and%20facial%20features.

- Information About SVM(s) & LibSVM:
    - Installing LIBSVM:
        - https://www.csie.ntu.edu.tw/~cjlin/libsvm/
        - https://pypi.org/project/libsvm/
        - https://github.com/cjlin1/libsvm
    - SVM & LIBSVM Logic & Documentation:
        - https://www.csie.ntu.edu.tw/~cjlin/papers/guide/guide.pdf
        - https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/

- Information About The Dataset Used/Modifed:
    - https://wangjiangb.github.io/my_data.html

- Information About Representations:
    - https://arxiv.org/pdf/1601.01006.pdf



