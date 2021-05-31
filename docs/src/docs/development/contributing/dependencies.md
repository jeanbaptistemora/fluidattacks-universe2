---
id: dependencies
title: Dependencies
sidebar_label: Dependencies
slug: /development/contributing/dependencies
---

Below snippets should be added to the end of your `~/.bashrc`.
We highly recommend you to only use one snippet at a time because
different products can overlap with each other

Everytime you modify the `~/.bashrc` you should execute `$ source ~/.bashrc`,
otherwise changes won't be visible

All the programs and tools that you open from within the Bash Shell will
be able to see the configurations we made

### Forces
```bash
    cd /path/to/fluidattacks/product/repo \
&&  ./m makes.dev.forces \
&&  source out/makes-dev-forces
```

### Integrates

#### Back

```bash
# Replace the following values with real ones
export INTEGRATES_DEV_AWS_ACCESS_KEY_ID='test'
export INTEGRATES_DEV_AWS_SECRET_ACCESS_KEY='test'

    cd /path/to/fluidattacks/product/repo \
&&  ./m makes.dev.integrates.back \
&&  source out/makes-dev-integrates-back
```

### Melts
```bash
    cd /path/to/fluidattacks/product/repo \
&&  ./m makes.dev.melts \
&&  source out/makes-dev-melts
```

### Observes

#### Tap Mixpanel

```bash
    cd /path/to/fluidattacks/product/repo \
&&  ./m makes.dev.observes.tap-mixpanel \
&&  source out/makes-dev-observes-tap-mixpanel
```

### Skims

```bash
    cd /path/to/fluidattacks/product/repo \
&&  ./m makes.dev.skims \
&&  source out/makes-dev-skims
```
