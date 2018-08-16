# colored lids

This package extends the [_grayboxes_](https://github.com/dwweiss/grayBoxes/wiki) package by providing toolbox for the implementation of theoretical submodels

[[Link to coloredlids wiki]](https://github.com/dwweiss/coloredlids/wiki)



<br>

### Content

    coloredlids
        data        Conversion of data, operations on data frames
        electric    Electric fields
        flow        Solutions to velocity and pressure distribution
        heat        Heat transfer by conduction, convection and radiation
        magnetic    Magnetic fields
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
    python3 setup.py install --user

### Dependencies

This package is dependent on package _grayboxes_. This dependency is satisfied if _coloredlids_ is installed with the commands in section _Installation_.

