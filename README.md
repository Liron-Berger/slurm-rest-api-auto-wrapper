# slurm-rest-api-auto-wrapper
Scrape the [Slurm Rest API webpage](https://slurm.schedmd.com/rest_api.html) and create python api calls with pydantic models.
See the [auto generated python api](slurm_rest_api.py)

Scrapes all the [models](https://slurm.schedmd.com/rest_api.html#__Models) and from each one creates a pydantic model object (recursively) with types for each field.
Scrapes all the [methods](https://slurm.schedmd.com/rest_api.html#__Methods) and for each generates a function wrapping the api endpoint with the correct args (using the auto generated pydantic models). 

##### Using the generated file:
```python
In [1]: from slurm_rest_api import User, slurmdbdGetCluster

In [2]: User?
Init signature:
User(
    *,
    administrator_level: str = None,
    associations: slurm_rest_api.UserAssociations = None,
    coordinators: List[slurm_rest_api.CoordinatorInfo] = None,
    default: slurm_rest_api.UserDefault = None,
    name: str = None,
) -> None
Init docstring:
Create a new model by parsing and validating input data from keyword arguments.

Raises ValidationError if the input data cannot be parsed to form a valid model.
File:           ~/workspace/slurm_rest_api/slurm_rest_api.py
Type:           ModelMetaclass
Subclasses:     

In [3]: slurmdbdGetCluster?
Signature: slurmdbdGetCluster(cluster_name) -> 'ClusterInfo'
Docstring:
Get cluster info (slurmdbdGetCluster)

:param cluster_name: Path Parameter — Slurm cluster name
File:      ~/workspace/slurm_rest_api/slurm_rest_api.py
Type:      function

In [4]: slurmdbdGetCluster("my_cluster")
```

##### How to run:
```
python3.10 ./scripts/parse_slurm_rest_website.py
```
Will output a `slurm_rest_api.py` file (The same file as given in the root of this repository).

##### Known issues:
- [ ] `optional` parameters before `required` parameters (happens only in `slurmdbdDeleteAssociation` and was fixed in `slurm_rest_api.py` file manually)
- [ ] `POST` methods are currently not receiving any payload. (There is no documentation in slurm for this so I'm not sure how to generate these automatically)
- [ ] Add some sort of `connect` method to pass the actual slurmrestd host and port.
