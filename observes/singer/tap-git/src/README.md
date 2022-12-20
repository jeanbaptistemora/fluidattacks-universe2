# Tap-git

This is the Extract and Transform component of a git repo ET&L.

## Getting started

First create a JSON configuration file acording to the example conf.example.json:

```json
[
  {
    "organization": "name",            # use it if useful, optional
    "subscription": "name",            # use it if useful, optional
    "repository": "name",              # name of the repo, mandatory
    "location": "~/Downloads/my_repo", # path to local repo, mandatory
    "branches": [                      # list of branches to track, mandatory
      "trunk"
    ]
  },
  {
    ...                                # other repo goes here
  }
]
```

Then run a tap and a target:

```
tap-git --conf config.json | target-anysingertarget
```
