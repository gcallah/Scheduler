# Scheduler

* **Description**:  Given a list of constraints such as professor's availabilties to teach, preferences to teach,  and classroom capacities, scheduler generates a class schedule that maps professors to classrooms. 

  - **Technology stack**: Scheduler is written completely in Python 3. It is intended to be run on a Jupyter notebook. 
  - **Status**:  Scheduler is in a runnable state and produces correct results. Efforts are made in making more tests, documatations, as well as adding additional features. 
  - Scheduling lectures in classrooms is a classic example of constraint satisfaction problems (CSPs), which are mathematical questions defined as a set of objects whose state must satisfy a number of constraints or limitations. In this case, there are unary constraints, such as professor's availability, and binary constraints, such as the conflicts between some different classes taught by different professors. 


## Dependencies

* Install Python 3 [here](https://www.python.org/downloads/).
* Install Jupyter Notebook [here](https://jupyter.org/install).

## Installation

* Install the development requirements:

  ```shell
  pip install -r docker/requirement-dev.txt
  ```

## Usage

* Open Jupyter Notebook with the pre-configured, well-documentated [notebook](./notebook/SchedInterface.ipynb). 
* Run the notebook line by line with the dummy data until the final output is generated. 
* To change the input, edit the input [excel file](./my_data.xlsx).

## How to test the software

* Manually run the [unit tests](./scheduler/tests).
* Alternatively, all unit tests are automatically run when a new change is pushed to the repository, enabled by Travis CI. 

## Known issues

Document any known significant shortcomings with the software.

## Getting help

If you have questions, concerns, bug reports, etc, please file an issue in this repository's Issue Tracker.

----

## Credits and references

1. Requirement files and unit tests insipired by [indras_net](https://github.com/gcallah/indras_net). 