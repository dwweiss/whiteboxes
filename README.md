# coloredLids

_coloredLids_ extends the _grayBoxes_ project by deriving classes from _grayboxes.Model_. That class provides just an interface to empty white boxes which are now filled and "closed with colored lids". The lid color of the white boxes in [Fig. 1](#figure-1-gray-box-models) indicates functionality for simulating heat transfer, fluid flow, mass transfer and structural mechanics.

<br>

![](https://github.com/dwweiss/coloredlids/blob/master/doc/fig/colored_boxes_top.png)

##### Figure 1: Gray box models

<br>

## Table of Contents 

    src/data
        Conversion of data, operations on data frames
        
    src/doc
        Documentation
        
    src/empirical 
        Data-driven models
        
    src/flow 
        Analytical solutions to velocity distribution and pressure loss
        
    src/heat 
        Analytical solutions to heat transfer
        
    src/matter
        Physical and chemical properties of solids, liquids and gases
        
    src/mesh     
        Primitives for building geometries and meshes
        
    src/numeric 
        Numerical solution of differential and integral equations
        
    src/tests  
        Selected test cases
        
    src/tools
        Tools for data manipulation
        

## Installation

    $ wget https://github.com/dwweiss/coloredlids.git


## Dependency

_coloredLids_ is dependent on _grayBoxes_, install with:

    $ wget https://github.com/dwweiss/grayboxes.git
