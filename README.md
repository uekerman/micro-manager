# Micro Manager

A manager tool to enable two-scale macro-micro coupling using the coupling library preCICE.

## Installing the package

### Using pip3

It is recommended to install [micro-manager from PyPI]() by running

```bash
pip3 install --user micro-manager
```

If the dependencies are not installed, then `pip` will attempt to install them for you. If you encounter problems in the direct installation, see the [dependencies section](https://github.com/precice/micro-manager#required-dependencies) below for links to installation procedures of all dependencies.

### Clone this repository and use pip3

#### Required dependencies

Ensure that the following dependencies are installed:

* [preCICE](https://github.com/precice/precice/wiki)
* python3 (this adapter **only supports python3**)
* [the python language bindings for preCICE](https://github.com/precice/python-bindings)
* [numpy](https://numpy.org/install/) and [mpi4py](https://mpi4py.readthedocs.io/en/stable/install.html)

#### Build and install the manager

After cloning this repository, go to the project directory `micro-manager` and run `pip3 install --user .`.

## Using the micro-manager

The micro-manager facilitates two-scale coupling between a macro-scale simulation and several micro-scale simulations. The manager creates and controls a set of micro-problems and couples them to one macro-simulation using preCICE. An existing micro-simulation script needs to be converted into a library have a specific structure so that the micro-manager can create and steer the micro-problems. The micro-simulation library needs to have a class so that the micro-manager can create objects of this class for each micro-simulation and steer them till the end of the coupled simulation.

The macro-problem script is coupled to preCICE directly. Check the section [couple your code](https://precice.org/couple-your-code-overview.html) in the preCICE documentation for more details.

### Steps to convert micro-simulation code to a callable library

* Create a class called `MicroSimulation` which consists of all the functions of the micro-simulation. It is good practice to define class member variables in the class constructor `__init__`.
* **Optional step**: Define a function `initialize` which computes the initial state of the micro-simulation and returns the initial values which need to be transferred to the macro-simulation. The return entity needs to be a Python dictionary having the names of the quantities being returned as the keys and the values of the quantities as the values in the dictionary.
* Create a function named `solve` which should consist of all the solving steps for one time step of a micro-simulation or if the micro-problem is steady-state then solving until the steady-state is achieved. The `solve` function returns the quantities that need to be written to the macro-side. The return entity needs to be a Python dictionary having the names of the quantities being returned as the keys and the values of the quantities as the values in the dictionary.
* If implicit coupling is required between the macro- and micro- problems, then you can additionally define two functions `save_checkpoint` and `revert_to_checkpoint`.
  * `save_checkpoint` saves the state of the micro-problem such that if the implicit time-step does not convergence, then the micro-problem can be reversed to this state.
  * `revert_to_checkpoint` reverts to the state which was saved earlier.

You can find an example of an adapted micro-problem in the [macro-micro-dummy](https://github.com/precice/micro-manager/tree/master/examples/macro-micro-dummy) example.

### Configuring the micro-manager

The micro-manager is configured using a JSON file. The configuration file for the [macro-micro-dummy](https://github.com/precice/micro-manager/tree/master/examples/macro-micro-dummy) looks like:

```json
{
    "micro_file_name": "micro_problem",
    "coupling_params": {
            "participant_name": "Micro-Manager",
            "config_file_name": "precice-config.xml",
            "macro_mesh_name": "macro-mesh",
            "read_data_names": {"macro-scalar-data": "scalar", "macro-vector-data": "vector"},
            "write_data_names": {"micro-scalar-data": "scalar", "micro-vector-data": "vector"}
    },
    "simulation_params": {
      "macro_domain_bounds": [0.0, 1.0, 0.0, 1.0, 0.0, 1.0],
      "total_time": 10.0,
      "timestep": 1.0,
      "t_output": 1.0
    }
}
```

The following quantities need to be configured:

* `micro_file_name`: It is the path to the micro-simulation script. The `.py` of the micro-simulation script is not necessary here.
* `coupling_params`:
  * `participant_name`: Name of the micro-manager as stated in the preCICE configuration.
  * `config_file_name`: Path to the preCICE XML configuration file.
  * `macro_mesh_name`: Name of the mesh as stated in the preCICE configuration.
  * `read_data_names`: A Python dictionary with the names of the data to be read from preCICE as keys and `"scalar"` or `"vector"`  as the corresponding value.
  * `write_data_names`: A Python dictionary with the names of the data to be written to from preCICE as keys and `"scalar"` or `"vector"`  as the corresponding value.
* `simulation_params`:
  * `macro_domain_bounds`: Minimum and maximum limits of the macro-domain, having the format `[xmin, xmax, ymin, ymax, zmin, zmax]`.
  * `total_time`: Total simulation time.
  * `timestep`: Initial time step of the simulation.
  * `t_output`: Time interval at which the micro-manager outputs the data.
