# colored lids

This package extends the [_grayboxes_](https://github.com/dwweiss/grayBoxes/wiki) package with tools for the implementation of the theoretical submodels

[[Link to coloredlids wiki]](https://github.com/dwweiss/coloredlids/wiki)



<br>

### Content

    coloredlids
        data        Conversion of data, operations on data frames
        electric    Electric fields
        flow        Velocity and pressure distribution in flow of gases and liquids
        heat        Heat transfer by conduction, convection and radiation
        hints       Some python tricks
        instruments Tools for reading from instruments
        magnetic    Magnetic fields
        mass        Mass transfer by diffusion
        matter      Properties of solids, liquids and gases
        mechanic    Structural mechanics
        mesh        Primitives for building geometries and meshes
        numerics    Numerical solution of differential and integral equations
        tools       Tools for data manipulation
        
    tests
        Test cases

    doc
        Figures and manuals used in wiki

### Installation

    git clone https://github.com/dwweiss/coloredlids.git  
    python3 setup.py install --user

### Dependencies

This package is dependent on package _grayboxes_. This dependency is satisfied if _coloredlids_ is installed with the commands in section _Installation_.

