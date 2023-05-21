
# Chargebee Integration with AWS Lambda

> The contents of this repository is currently a work in progress.

[Chargebee](https://www.chargebee.com/) is a recurring billing and subscription management tool that helps subscription businesses streamline their Revenue Operations. It offers a variety of functionality, including:
- Managing recurring billing and subscriptions seamlessly
- Supporting hybrid business models
- Enabling expansion of global footprint
- Automating self-serve workflows for all use-cases.

Chargebee also offers native reporting functionality, but there may be times where one might have more complex reporting needs than what is available on the platform by default. Fortunately, Chargebee also has a marketplace of third party tools that you can leverage to meet a variety of needs, and they also offer an API that you can use to build your own! This application is a custom exporting integration between Chargebee and Amazon Web Services (AWS).

# Table of Contents

1. [Pre-Requisites](#pre-requisites)
2. [Architecture Overview](#architecture-overview)
3. [Step-by-Step Tutorial](#step-by-step-tutorial)
4. [Deployment Instructions](#deployment-instructions)

## Pre-Requisites
- A free [AWS account](https://aws.amazon.com/free/)
- A free [Chargebee](https://www.chargebee.com/) account
- A [Chargebee API Key](https://www.chargebee.com/docs/2.0/api_keys.html)
  - It is recommended to follow the best practices of least privileges when assigning access to your API key.
- Sample customer data in Chargebee (dummy customer data has been provided in this repo)
- Programming fundamentals (if you require your own custom export lambda function logic)

## Architecture Overview

![Architecture Diagram](img/low-level-diagram.jpg)

The architecture for this solution is very straightforward. [AWS Lambda](https://aws.amazon.com/lambda/) will initiate an export API call to the Chargebee API. A secondary Lambda will download those files once they are ready. All of your exported Chargebee files will be stored in [Amazon S3](https://aws.amazon.com/s3/). [AWS Step Functions](https://aws.amazon.com/step-functions/) will orchestrate the entire workflow, and your Chargebee API key will be stored in (and referenced from) [AWS Systems Manager Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html). The parameter will be encrypted using [AWS Key Management Service](https://aws.amazon.com/kms/). An optional [Amazon EventBridge Scheduler](https://docs.aws.amazon.com/eventbridge/latest/userguide/scheduler.html) can trigger the workflow on a scheduled basis.

## Step-by-Step Tutorial

[This tutorial](https://toriancrane.github.io/chargebee-lambda-integration/) will walk you step by step on how you can build your own integration using AWS. More specifically, you will be able to ingest data from your Chargebee account into AWS and use that data for your own custom reporting workflows.

## Deployment Instructions

If you are already comfortable working with the services included in this architecture, you can deploy the templates in this repository to build the necessary AWS resources automatically. The sample code in the `chargebee-export.py` makes use of Chargebee's [Export Customers](https://apidocs.chargebee.com/docs/api/exports?prod_cat_ver=2#export_customers) to retrieve a list of all Chargebee customers. You are welcome to customize this function to meet whatever exporting needs you have (see the [Chargebee API Documentation](https://apidocs.chargebee.com/docs/api?prod_cat_ver=2) for more details on available APIs.).

TBD
