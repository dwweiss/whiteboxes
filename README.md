# White boxes

This package provides user-defined theoretical models which are compatible to the [_grayboxes_](https://github.com/dwweiss/grayBoxes/wiki) package.

[[Link to whiteboxes wiki]](https://github.com/dwweiss/whiteboxes/wiki)



<br>

### Content

    whiteboxes
        data        Conversion of data, operations on data frames
        flow        Velocity and pressure distribution in flow of gases and liquids
        gui         Graphic user interfaces
        heat        Heat transfer by conduction, convection and radiation
        hints       Some python hints
        instruments Tools for reading from instruments
        matter      Properties of solids, liquids and gases
        mesh        Primitives for building geometries and meshes
        numerics    Numerical solution of differential and integral equations
        tools       Tools for data manipulation
        
    test
        Test cases

    doc
        Figures and manuals used in wiki

### Installation

    git clone https://github.com/dwweiss/whiteboxes.git  
    python3 setup.py install --user

### Dependencies

This package is dependent on package _grayboxes_. This dependency is satisfied if _whiteboxes_ is installed with the commands in section _Installation_.

