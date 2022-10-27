---
id: sorts
title: Sorts
sidebar_label: Sorts
slug: /development/sorts
---

Sorts is the product responsible
for helping End Users sort files in a Git repository
by its probability of containing security vulnerabilities.
It does so by using Machine Learning
and producing a Model that is then used by:

- End users, through:
  - <https://github.com/fluidattacks/ai-extension-docker>.
  - <https://github.com/fluidattacks/ai-extension-azuredevops>.
- Fluid Attacks internal systems,
  to update the priority in [Integrates](/development/integrates)
  of the source code
  that Fluid Attacks Hackers audit.

## Public Oath

None at the moment, Sorts is yet an experimental project.

## Architecture

1. Sorts uses a Machine Learning Pipeline architecture,
   namely,
   many models are trained and improved automatically
   as the data evolves,
   and the best model is chosen according to some predefined criteria
   set up by the Sorts Maintainer.

   At all points in time, we report statistics
   to the [Redshift cluster](/development/stack/aws/redshift)
   provided by [Observes](/development/observes),
   which allows us to monitor the progress of the model over time,
   and intervene in the pipeline if something doesn't go as planned.

1. The source data is taken from the vulnerabilities at [Integrates](/development/integrates)
   that human hackers at Fluid Attacks have found,
   which contain information
   like the [type of vulnerability](/criteria/vulnerabilities/),
   the name of the source code repository in which it was found,
   the path to the file where it was found,
   and the problematic line number.

1. Roughly, the pipeline consists of the following steps:

   - `/sorts/extract-features`:
     Whose purpose is to clone all source code repositories,
     and produce a CSV with the features for each file in the repository.
   - `/sorts/merge-features`:
     Which takes the features from the previous step,
     and merges them into a single CSV.
   - `/sorts/training-and-tune`:
     Who takes the CSV from the previous step
     and trains different models using
     [SageMaker by Amazon Web Services](/development/stack/aws/sagemaker).

     SageMaker takes the training data from the previous step
     and uploads the trained model to a bucket on
     [S3 by Amazon Web Services](/development/stack/aws/s3).

     Last but not least,
     the best model is selected automatically
     and uploaded to the same bucket,
     but in a constant location.

   This Best Model is the output of the pipeline.

1. `/sorts/execute`:
   Takes the "Best Model" and uses it to prioritize the files
   at [Integrates](/development/integrates).
1. `/sorts/association*`:
   This is an attempt to make Sorts recommend
   the [type of vulnerability](/criteria/vulnerabilities/)
   that a file may contain as well.

:::tip
You can right-click on the image below
to open it in a new tab,
or save it to your computer.
:::

![Architecture of Sorts](./sorts-arch.dot.svg)

## Contributing

Please read the
[contributing](/development/contributing) page first.

### Development Environment

Follow the steps
in the [Development Environment](/development/setup/environment) section of our documentation.

If prompted for an AWS role, choose `dev`,
and when prompted for a Development Environment, pick `sorts`.
