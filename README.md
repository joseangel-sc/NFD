# What is NFD? (WIP)

NOTE: I use 'Fungible' as a synonym of 'Trustable' cause no body knows what it really means. 
 
Many times we seal with json data that we don't have control over, for example one day, an API from which we need information returns data that looks like this: 
```
[{'a': 1, 'b'2}, {'a': 2, 'b': 5, 'c': 6}]
```
How should we deal with this in our columnar database? 

The popular approach I've seen is to have something like 

```
routes = ['a', 'b', 'c']  
```
and then have some python code that parses that and pushes into the db
```
insert into .... values [(1,2), (2, 5, 6)] 
```

Then, when the non trusted source adds a route, let's say 
```
[{'a': 2, 'b': 5, 'c': 6, 'd': {'nested_data': 'data'}]
```
A new PR is needed updating our routes to `['a', 'b', 'c', 'd:nested_data'`]

#Problems with this approach. 

Specially with cron jobs, when this is data that comes from source A and we pull the information to 
our systems everyday, this faces a big data loss problem.

## Proposed NFD solution: 

- Store the whole json for future proof 
- Create a table where we store the information of which routes have 
been already seen in the data
- Create a view based on the rows of the routes tables OR if the volume of the 
data is not overwhelming, create a table and duplicate this data.  

[possible diagram](https://github.com/joseangel-sc/NFD/blob/main/NFD.pdf)


as of 24/04/2022 NFD only gets the routes from a given dictionary and 
retrieves the information from a given route (see tests)

TODO: 

- Ingest multiple jsons at once. 
- Save the routes, sort them by popularity (so that 
the most common routes are the first inserted)
- Add connector to possible relational databases (postgres, mysql, possibly snowflake)
- ? Create repo with demo 
  




