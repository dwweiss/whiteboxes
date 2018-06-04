# coloredLids

_coloredLids_ extends the [_grayBoxes_](https://github.com/dwweiss/grayBoxes/wiki) project by deriving objects from the _grayboxes.Model_ class. That class is merely an interface to an empty white box model. It defines the contract between the gray box and subsets of the white boxes model. The lid color of the subsets in [Fig. 1](#figure-1-gray-box-model-comprising-white-boxes-with-colored-lids-and-black-boxes) indicates functionality for simulating  <font color="red">heat transfer</font>, <font color="blue">fluid flow</font>, <font color="green">mass transfer</font> and <font color="yellow">structural mechanics</font>.

[[Link to coloredLids wiki]](https://github.com/dwweiss/coloredLids/wiki)

<br>
<br>

![](https://github.com/dwweiss/coloredlids/blob/master/doc/fig/colored_boxes_top.png)

##### Figure 1: Gray box model comprising a black box and white box subsets

<br>

### Content of project 

    coloredLids
        data        Conversion of data, operations on data frames
        empirical   Data-driven models
        flow        Solutions to velocity and pressure distribution
        heat        Solutions to heat transfer
        mass        Mass transfer (diffusion)
        matter      Properties of solids, liquids and gases
        mech        Structural mechanics
        mesh        Primitives for building geometries and meshes
        numeric     Numerical solution of differential and integral equations
        tools       Tools for data manipulation
        
    tests
        Selected test cases

    doc
        Figures and manuals used in wiki

### Installation

    git clone https://github.com/dwweiss/coloredLids.git  
    sudo python3 setup.py install 

### Dependencies

Package _coloredLids_ is dependent on package _grayBoxes_, [[info]](https://github.com/dwweiss/grayBoxes#dependencies)
