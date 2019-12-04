# Scheduler

**Description**:  Given a list of constraints such as professor's availabilties to teach, preferences to teach,  and classroom capacities, scheduler generates a class schedule that maps professors to classrooms. 

**Technology stack**: Scheduler is written completely in Python 3 and it is intended to be run on a Jupyter notebook. 

**Status**:  Scheduler is in a runnable state and produces correct results. Efforts are made in making more tests, documatations, as well as adding additional features. 

## Constraint Satisfaction Problems (CSPs)

Scheduling lectures in classrooms is a classic example of constraint satisfaction problems (CSPs), which are mathematical questions defined as a set of objects whose state must satisfy a number of constraints or limitations. Therefore, scheduler uses a randomized CSP algorithm to schedule classses to professors and classrooms. 

Course and professors are modelled as nodes. Among these nodes, there are **unary constraints**, such as professor's availability, and **binary constraints**, such as the conflicts between some different classes taught by different professors. There are constraint functions that are used to weight the constraints among the nodes. For example, **room_has_capacity** checks to see if given room has a big enough capacity. If not, it would become a weighted unary constraint on a particular node.

After modelling the nodes and establishing the conflicts, the scheduler solves the CSPs by randomly choosing conflict nodes that have the lowest weight and assign them with new values (mapping new professors to the course). The rationale behind it is that we want to always to start with lowest-weighted conflicts and resolve them as we go. The scheduler concludes a valid schedule once no conflicts are present  or after **max_iter** (default to 100) attempts, it concludes that there's no possible valid schedule to be generated.


##  Dependencies

* Install Python 3 [here](https://www.python.org/downloads/).
* Install Git [here](https://git-scm.com/downloads). 
* Install Jupyter Notebook [here](https://jupyter.org/install).

## Installation

Install the development requirements:

```shell
pip install -r docker/requirement-dev.txt
```

## Usage

* Open Jupyter Notebook with the pre-configured, well-documentated [notebook](./notebook/SchedInterface.ipynb). 
* Run the notebook line by line with the dummy data until the final output is generated. 
* To change the input, edit the input [excel file](./my_data.xlsx).

## How to test the software

Because Scheduler is written using a randomized algorithm, the produced outcome is indeterministic and therefore an intergration is not in place and not possible. However, we have a unit test suites whcih you could run using the following options: 

* Manually run the [unit tests](./scheduler/tests).
* Alternatively, all unit tests are automatically run when a new change is pushed to the repository, enabled by **Travis CI**. 

## Known issues

Currently None.

## Getting help

If you have questions, concerns, bug reports, etc, please file an issue in this repository's Issue Tracker.

----

## Credits and references

* Requirement files and unit tests insipired by [indras_net](https://github.com/gcallah/indras_net). 