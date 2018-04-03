# coloredLids

_coloredLids_ extends the _grayBoxes_ project by deriving from the _grayboxes.Model_ class. That class provides just an interface to empty white boxes which are here filled with subsets and "closed with multi-colored lids". The lid color of the white boxes in [Fig. 1](#figure-1-gray-box-model-comprising-white-boxes-with-colored-lids-and-black-boxes) indicates functionality for simulating  <font color="red">heat transfer</font>, <font color="blue">fluid flow</font>, <font color="green">mass transfer</font> and <font color="yellow">structural mechanics</font>.

<br>

![](https://github.com/dwweiss/coloredlids/blob/master/doc/fig/colored_boxes_top.png)

##### Figure 1: Gray box model comprising a black box and white box subsets

<br>

## Table of Contents 

    src/data
        Conversion of data, operations on data frames
        
    src/empirical 
        Data-driven models
        
    src/flow 
        Analytical solutions to velocity distribution and pressure loss
        
    src/heat 
        Analytical solutions to heat transfer
        
    src/matter
        Physical and chemical properties of solids, liquids and gases
        
    src/mass     
        Mass transfer (diffusion)

    src/mechanics     
        Structural mechanics

    src/mesh     
        Primitives for building geometries and meshes
        
    src/numeric 
        Numerical solution of differential and integral equations
        
    src/tests  
        Selected test cases
        
    src/tools
        Tools for data manipulation
        

## Installation

    $ wget https://github.com/dwweiss/coloredLids.git


## Dependency

_coloredLids_ is dependent on _grayBoxes_, install with:

    $ wget https://github.com/dwweiss/grayBoxes.git
