# Deep Finder

The code in this repository is described in [this pre-print](https://hal.inria.fr/hal-01966819/document). This paper has been submitted to Nature Communications and is currently under revision.

__Disclaimer:__ this is a preliminary version of the code, which is subject to improvements. For ease of use, we also plan to create a graphical interface in forthcoming months.

__News__: (29/01/20) A first version of the GUI is now available in folder pyqt/. [More information...](###Using the GUI) 

## Contents
- [System requirements](##System requirements)
- [Installation guide](##Installation guide)
- [Instructions for use](##Instructions for use)
- [Documentation](docs/build/html/index.html)

## System requirements
__Deep Finder__ has been implemented using __Python 3__ and is based on the __Keras__ package. It has been tested on Linux (Debian 8.6), and should also work on Mac OSX as well as Windows.

The algorithm needs an Nvidia GPU to run at reasonable speed (in particular for training). The present code has been tested on Tesla K80 and M40 GPUs. For running on other GPUs, some parameter values (e.g. patch and batch sizes) may need to be changed to adapt to available memory.

```diff
- If above conditions are not met, we cannot guarantee the functionality of our code at this time.
```

### Package dependencies
Users should install following packages in order to run Deep Finder. The package versions for which our software has been tested are displayed in brackets:
```
tensorflow-gpu (1.14.0)
keras          (2.3.1)
numpy          (1.16.4)
h5py           (2.9.0)
lxml           (4.3.4)
scikit-learn   (0.21.2)     
scikit-image   (0.15.0)  
matplotlib     (3.1.0)
mrcfile        (1.1.2)
PyQt5          (5.13.2)
```

## Installation guide
First install the packages:
```
pip install numpy tensorflow-gpu keras sklearn h5py lxml scikit-learn scikit-image matplotlib mrcfile PyQt5
```
For more details about installing Keras, please see [Keras installation instructions](https://keras.io/#installation).

Once the dependencies are installed, the user should be able to run Deep Finder.

## Instructions for use
### Using the scripts
Instructions for using Deep Finder are contained in folder examples/. The scripts contain comments on how the toolbox should be used. To run a script, first place yourself in its folder. For example, to run the target generation script:
```
cd examples/training/
python step1_generate_target.py
```

### Using the GUI
The GUI (Graphical User Interface) is available in folder pyqt/, and should be more intuitive for those who are not used to work with script. For now, 5 GUIs are available (target generation, training, segmentation, clustering) and allow the same functionalities as the scripts in example/. To run a GUI, first place yourself in its folder. For example, to run the target generation GUI:
```
cd pyqt/generate_target/
python gui_target.py
```

![Training GUI](./images/gui_segment.png)

In near future we plan to provide a data visualization tool.

__Notes:__ 
- working examples are contained in examples/analyze/, where Deep Finder processes the test tomogram from the [SHREC'19 challenge](http://www2.projects.science.uu.nl/shrec/cryo-et/2019/). 
- The script in examples/training/ will fail because the training data is not included in this Gitlab. 
- The evaluation script (examples/analyze/step3_launch_evaluation.py) is the one used in SHREC'19, which needs additional packages (pathlib and pycm, can be installed with pip). The performance of Deep Finder has been evaluated by an independent group, and the result of this evaluation has been published in Gubins & al., "SHREC'19 track: Classification in cryo-electron tomograms".
