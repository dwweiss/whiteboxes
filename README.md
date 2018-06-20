# coloredLids

This package extends the [_grayboxes_](https://github.com/dwweiss/grayBoxes/wiki) package by providing theoretical submodels _**f**(x)_. Complexer functions _**f**(x)_ are often implemented as a tree of objects derived from the _grayboxes.Model_ class.  The instance of _Model_ at the tree root defines the contract between the empirical and theoretical submodels.

The lid color of the theoreical submodels in [Fig. 1](#figure-1-gray-box-model-comprising-white-boxes-with-colored-lids-and-black-boxes) indicates functionality for simulating  <font color="red">heat transfer</font>, <font color="blue">fluid flow</font>, <font color="green">mass transfer</font> and <font color="yellow">structural mechanics</font>.

[[Link to coloredLids wiki]](https://github.com/dwweiss/coloredlids/wiki)

<br>
<br>

![](https://github.com/dwweiss/coloredlids/blob/master/doc/fig/colored_boxes_top.png)

##### Figure 1: Gray box model comprising a black box and white box subsets

<br>

### Content of project 

    src
        data        Conversion of data, operations on data frames
        empirical   Data-driven models
        flow        Solutions to velocity and pressure distribution
        heat        Solutions to heat transfer
        mass        Mass transfer (diffusion)
        matter      Properties of solids, liquids and gases
        mech        Structural mechanics
        mesh        Primitives for building geometries and meshes
        numerics    Numerical solution of differential and integral equations
        tools       Tools for data manipulation
        
    tests
        Selected test cases

    doc
        Figures and manuals used in wiki

### Installation

    git clone https://github.com/dwweiss/coloredlids.git  
    sudo python3 setup.py install 

### Dependencies

Package _coloredlids_ is dependent on package _grayBoxes_, [[info]](https://github.com/dwweiss/grayBoxes#dependencies)
