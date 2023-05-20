---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: default

accordion: 
  - title: Step 0. [Optional] Import Sample Data to Chargebee
    content: You may already have sample data to work with in your Chargebee environment, and you are welcome to use that for this tutorial. If you do not have sample data, feel free to use the sample data provided in the [chargebee-sample-customer-data.csv](https://github.com/toriancrane/chargebee-lambda-integration/blob/main/chargebee-sample-customer-data.csv) file. Follow the steps found in Chargebee's [Bulk Operations documentation](https://www.chargebee.com/docs/2.0/bulk-operations.html) to pre-load this data before continuing on.
  - title: Step 1. Select a Region
    content: This application can be deployed in any AWS region that supports all the services used in this application (see the Architecture Overview section). You can refer to the [region table](https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/) to see which regions support these services. For the purpose of this guide, we will be creating resources in the **US East (N. Virginia)** region. You can select this region from the dropdown in the upper right corner of the [AWS Management Console](https://console.aws.amazon.com/console/home).
  - title: Step 2. Create AWS Systems Manager Parameters
    content: |-
        AWS Systems Manager (SSM) Parameter Store provides the ability to securely store data such as passwords, database strings, and license codes as parameter values. 

        In this step, you will use the AWS console to create SSM Parameters that will store the values of your Chargebee Site name and API key. We will later reference these values in our Lambda function code that will invoke the Chargebee API call.
        
        
        ---
        
        <br>
        a. In the AWS Console, navigate to the **AWS Systems Manager** service. The click the `Parameter Store` link in the left hand menu. Then click `Create parameter`.
        
        <p align="center">
            <video autoplay loop muted height="90%" width="90%">
            	<source src="video/initiate-ssm-param-creation.mp4" type="video/mp4">
            </video>
        </p>
        <br>
        
        b. On the **Create parameter** page, provide a unique name for your parameter. For the purpose of this guide, we will use `chargebee-apikey` as the name. Keep the default Tier of `Standard` selected.
        
        c. Under **Type**, select the `SecureString` radio button. This will apply encryption to the value that is stored in the parameter. Under the **KMS Key ID** section, a default KMS key will auto-populate. This will be the key that is used to encrypt the parameter data.
        
        d. In the **Value** text box, enter the value of your Chargebee API key. Then click the `Create parameter` button to create your parameter.
        
        <p align="center">
            <video autoplay loop muted height="90%" width="90%">
            	<source src="video/create-new-ssm-param.mp4" type="video/mp4">
            </video>
        </p>
        <br>
        
        e. Repeat steps A through E to create another parameter and store the value of your Chargebee Site name. You should see the following in the SSM Parameter Store console upon successful creation of both parameters:
        
        <p align="center"><img src="img/ssm-param-created.png" alt="SSM Parameter Created image" width="90%" height="90%"></p>
  - title: Step 3. Create an S3 Bucket to store the export files
    content: |-
        In this step, you'll create a new S3 bucket that will be used to hold all of the downloaded Chargebee files.
        
        ---
        
        <br>
        a. In the AWS Management Console, navigate to the **S3** service. Then click the `Create bucket` button on the right hand side of the screen.
        
        <p align="center"><img src="img/s3-create-bucket.png" alt="S3 Create Bucket image" width="90%" height="90%"></p>
        <br>
        
        b. On the **Create bucket** page, provide a globally unique name for your bucket such as `chargebee-to-aws-workshop`. If you get an error that your bucket name already exists, try adding additional numbers or characters until you find an unused name. Also, make sure the Region you've chosen to use for this workshop is selected in the dropdown.
        
        <p align="center"><img src="img/s3-create-bucket-name.png" alt="S3 Create Bucket Name image" width="90%" height="90%"></p>
        <br>        

        c. Choose `Create` in the lower left corner of this page, leaving the remaining default options.
        
        <p align="center"><img src="img/s3-create-bucket-final.png" alt="S3 Create Bucket Button image" width="90%" height="90%"></p>
        
        You should see the following in the S3 console upon successful creation:
        
        <p align="center"><img src="img/s3-bucket-created.png" alt="S3 Bucket Created image" width="90%" height="90%"></p>
        
  - title: Step 4. Create an IAM Role for your Lambda Functions
    content: |-
        In this step, we will create a Lambda Execution role for our Lambda functions. This role defines what other AWS services the function is allowed to interact with (see [Lambda Execution Role](https://docs.aws.amazon.com/lambda/latest/dg/lambda-intro-execution-role.html)).
        
        For the purposes of this workshop, we'll need to create an IAM role that grants your Lambda functions the following permissions:
        
        a. write logs to Amazon CloudWatch Logs
        
        b. read parameter values from Systems Manager Parameter Store
        
        c. write files to an S3 bucket

        ---
        
        <br>
        
        a. In the AWS Management Console, navigate to the **IAM** service. Then click the `Roles` link in the left hand menu.
        
        <p align="center"><img src="img/iam-create-role.png" alt="IAM Create Role image" width="90%" height="90%"></p>
        <br>
        
        b. Then click the `Create role` button.
        
        <p align="center"><img src="img/iam-create-role-button.png" alt="IAM Create Role image" width="90%" height="90%"></p>
        <br>
        
        c. In the **Select trusted entity** page, keep the default selection of `AWS Service`.
        
        <p align="center"><img src="img/iam-create-role-trust.png" alt="IAM Create Role image" width="90%" height="90%"></p>
        <br>
        
        d. Under the **Use case** section further down the page, select the radio button next to `Lambda`. Then click the `Next` button.
        
        <p align="center"><img src="img/iam-create-role-use-case.png" alt="IAM Create Role Use Case image" width="90%" height="90%"></p>
        <br>
        
        e. In the **Add permissions** page, under the **Permissions policies** section, search for and select the following Policy names:
        
        `AWSLambdaBasicExecutionRole`
        
        `AmazonSSMReadOnlyAccess`
        
        <br>
        
        Then click `Next`.
        
        <p align="center"><img src="img/iam-create-role-perms.png" alt="IAM Create Role Permissions image" width="90%" height="90%"></p>
        <br>
        
        f. On the **Name, review, and create** page, provide a name for your IAM role such as `ChargebeeExportExecutionRole`. Then click the `Create role` button at the bottom of the page.
        
        <p align="center"><img src="img/iam-create-role-name.png" alt="IAM Create Role Name image" width="90%" height="90%"></p>
        <br>
        
        <p align="center"><img src="img/iam-create-role-final.png" alt="IAM Role Create Role image" width="90%" height="90%"></p>
        <br>
        
        g. You will be redirected to the **Roles** page once the role has finished creating. In the search box of this page, enter the name of the role you just created (Ex: `ChargebeeExportExecutionRole`) and click the role's link.
        
        <p align="center"><img src="img/iam-role-search.png" alt="IAM Role Search image" width="90%" height="90%"></p>
        <br>
        
        h. Under the **Permissions policies** section, click the `Add permissions` dropdown, and select `Create inline policy`.
        
        <p align="center"><img src="img/iam-create-inline-policy.png" alt="IAM Create Inline Policy image" width="90%" height="90%"></p>
        <br>
        
        i. Select `Choose a service`. Type in `S3` into the **Find a service** search box and select **S3** when it appears.
        
        <p align="center"><img src="img/iam-policy-select-s3.png" alt="IAM Policy Select S3 image" width="90%" height="90%"></p>
        <br>
        
        j. Under **Actions - Specify the actions allowed in S3**, search for and select the following permissions:
        
        `ListBucket`
        
        `ListAllMyBuckets`
        
        `PutObject`
        
        `PutObjectTagging`
        
        `PutObjectVersionTagging`
        
        `PutObjectAcl`
        
        <p align="center"><img src="img/iam-policy-select-actions.png" alt="IAM Policy Select Actions image" width="90%" height="90%"></p>
        <br>
        
        h. Select the **Resources** section. Keeping the `Specific` option selected, click the `Add ARN` link in the **bucket** section.
        
        <p align="center"><img src="img/iam-policy-select-resources.png" alt="IAM Policy Select Resources image" width="90%" height="90%"></p>
        <br>
        
        g. In the **Add ARN(s)** pop-up modal, type in the name of the S3 bucket you created earlier in this guide. Then click `Add`.
        
        <p align="center"><img src="img/iam-policy-select-bucket.png" alt="IAM Policy Select Bucket image" width="90%" height="90%"></p>
        <br>
        
        h. Under **Resources** next to the **object** section, select the check box next to `Any`. Then click `Review policy`.
        
        <p align="center"><img src="img/iam-policy-review.png" alt="IAM Policy Review image" width="90%" height="90%"></p>
        <br>
        
        i. On the **Review policy** page, give a name to your policy such as `ChargebeeS3WriteAccess`. Then click `Create policy`.
        
        <p align="center"><img src="img/iam-policy-create-final.png" alt="IAM Policy Create image" width="90%" height="90%"></p>
        <br>
        
        You should see the following inline policy in the **Permissions policies** section of your IAM Role.
        
        <p align="center"><img src="img/iam-policy-created.png" alt="IAM Policy Created image" width="90%" height="90%"></p>
  - title: Step 6. Create a Lambda Layer for your Lambda Functions
    content: |-
        [Lambda layers](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html) are a convenient way to package libraries and other dependencies that you can use with your Lambda functions. For this particular integration, we will need the Chargebee API library as well as the [Requests](https://pypi.org/project/requests/) library.

        In this step, we will upload a pre-made Lambda Layer that includes both the Chargebee and Requests libraries. Creating one from scratch is outside of the scope of this tutorial, but you can find more details about this process in the [Creating layer content](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html#configuration-layers-upload) section of the official AWS documentation.
        
        ---
        
        <br>
        a. Download the [chargebee-requests-lambda-layer](https://github.com/toriancrane/chargebee-lambda-integration/blob/main/aws/chargebee-requests-lambda-layer.zip) from the application repo. In the AWS Management Console, navigate to the Lambda service and select the `Layers` link in the left hand menu. Then click the `Create layer` button on the right hand side.
        
        <p align="center"><img src="img/lambda-layer-create.png" alt="Create Lambda Layer image" width="90%" height="90%"></p>
        <br>
        
        b. On the **Create layer** page, provide a name for your Lambda Layer such as `chargebee-requests-layer`. With `Upload a .zip file` selected, click the `Upload` button and select the zip file downloaded in the previous step.
        
        <p align="center"><img src="img/lambda-layer-create-name.png" alt="Create Lambda Layer Name image" width="90%" height="90%"></p>
        <br>
        
        c. In the **Compatible architectures** section, select the check box next to `x86_64`. In the **Compatible runtimes** section, select the latest supported `Python` runtime (`Python 3.10` as of the time of this guide's creation) from the dropdown. 
        
        > You can learn more about these configuration settings in the [Creating a layer](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html#configuration-layers-create) AWS documentation.
        
        Then click `Create`.
        
        <p align="center"><img src="img/lambda-layer-create-final.png" alt="Create Lambda Layer image" width="90%" height="90%"></p>
        <br>
        
        You should see the following screen once the Lambda Layer has been successfully created.
        
        <p align="center"><img src="img/lambda-layer-created.png" alt="Create Lambda Layer image" width="90%" height="90%"></p>
        
  - title: Step 7. Create Lambda Functions to initiate and download an Export from Chargebee
    content: |-
        In this step, we will be making use of the [Chargebee API](https://apidocs.chargebee.com/docs/api?prod_cat_ver=2) to build the core functionality of exporting of data from Chargebee and storing it in AWS. The Chargebee API supports a number of programming languages. You'll want to make sure you select both the Product Catalog version that is relevant to the version of Chargebee you are using as well as your supported programming language of choice to make sure you are seeing the correct documentation for your environment. 

        <p align="center"><img src="img/chargebee-api-docs.png" alt="Chargebee API Docs image" width="90%" height="90%"></p>
        <br>
        
        For the purpose of this tutorial, we will be using the `Product Catalog 2.0` version and the `Python` language of the documentation, and we will be specifically making use of the [Export Customers API](https://apidocs.chargebee.com/docs/api/exports?prod_cat_ver=2#export_customers).
        
        We will be creating a total of two lambda functions, one that will initiate the export from Chargebee, and one that will download the data once the export is ready for download.
        
         ---
        
        <br>
        a. In the AWS Management Console, navigate to the **Lambda** service. Then click the `Create function` button on the top right side of the screen.
        
        <p align="center"><img src="img/lambda-create-function.png" alt="Lambda Create Function image" width="90%" height="90%"></p>
        <br>
        
        b. On the **Create function** page, provide a unique name for the first "export" Lambda function such as `chargebee-export-function`. Under **Runtime**, select the latest supported `Python` runtime (make sure it matches the same runtime as the one that was selected during the Lambda Layer creation process). Leave the default value selected under **Architecture**.
        
        <p align="center"><img src="img/lambda-create-function-name.png" alt="Lambda Create Function Name image" width="90%" height="90%"></p>
        <br>
        
        c. Click the `Change default execution role` and select `Use an existing role`. In the **Existing Role** dropwdown, select the IAM role you created in the previous step. Then click the `Create function` button at the bottom right hand side of the page.
        
        <p align="center"><img src="img/lambda-create-function-final.png" alt="Lambda Create Function Button image" width="90%" height="90%"></p>
        <br>
        
        d. In the lambda function console, scroll all the way to the bottom of the page until you see the **Layers** section. Click `Add a layer`.
        
        <p align="center"><img src="img/lambda-add-layer.png" alt="Lambda Add Layer image" width="90%" height="90%"></p>
        <br>
        
        e. In the **Add layer** page in the **Choose a layer** section, select the `Custom layers` option under **Layer source**. Then select the lambda layer created in the previous section under the **Custom layers** dropdown. Select the latest version of the lambda layer in the **Version** dropdown. Then click `Add`.
        
        <p align="center"><img src="img/lambda-add-layer-config.png" alt="Lambda Add Layer Configuration image" width="90%" height="90%"></p>
        <br>
        
        f. In the **Code Source** section of the lambda function, copy and paste the code in [this file](https://github.com/toriancrane/chargebee-lambda-integration/blob/main/aws/lambda/export.py) into `lambda_function.py`. Then click `Deploy`.
        
        <p align="center"><img src="img/lambda-add-code.png" alt="Lambda Add Export Code image" width="90%" height="90%"></p>
        <br>
        
        g. Repeat steps A through F in this section for the second "download" lambda function. (Make sure to provide a unique name for it such as `chargebee-download-function`). Use the code provided in [this file](https://github.com/toriancrane/chargebee-lambda-integration/blob/main/aws/lambda/download.py) for the contents of this lambda function.
        
        <p align="center"><img src="img/lambda-add-code-2.png" alt="Lambda Add Download Code image" width="90%" height="90%"></p>
        <br>
  - title: Step 8. Create a State Machine to Orchestrate the Chargebee Export Workflow
    content: |-
        Now that we have all of our core resources created, this next step will bring the entire workflow together in an organized and procedural way. We will do this by leveraging [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html), a serverless visual orchestration service.

        ---
        
        <br>
        a. In the AWS Management Console, navigate to the **Step Functions** service and click the `State machines` link in the left hand menu. Then click `Create state machine`.
        
        <p align="center"><img src="img/state-machine-create.png" alt="Create State Machine image" width="90%" height="90%"></p>
        <br>
        
        b. In the **Choose authoring method** page, keep the default value of `Design your workflow visually`, and keep the default value of `Standard` under the **Type** section. Then click `Next`.
        
        > Defining your orchestration workflow as code is outside of the scope of this guide, but you can refer to the [Amazon States Language](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-amazon-states-language.html) for more information on this topic.
        
        <p align="center"><img src="img/state-machine-authoring-method.png" alt="State Machine Configuration image" width="90%" height="90%"></p>
        <br>
        
        
        c. The next page is the Step Functions Workflow Studio.
        
        <p align="center"><img src="img/state-machine-workflow-designer.png" alt="Architecture Diagram" width="90%" height="90%"></p>
        <br>
        
        We will use this visual designer to create workflow as shown in the highlighted `AWS Step Functions workflow` part of architecture diagram below.
        
        <p align="center"><img src="img/architecture-workflow-highlight.png" alt="Workflow Designer image" width="90%" height="90%"></p>
        <br>
        
        The first step we will add to our workflow is the "Export" lambda function we created in a previous step. We will do this by dragging and dropping the `AWS Lambda Invoke` action from the left menu into the designer form space.
        <p align="center">
            <video autoplay loop muted height="90%" width="90%">
            	<source src="video/add-export-lambda-invoke.mp4" type="video/mp4">
            </video>
        </p>
                
---

> The contents of this tutorial are currently a work in progress.

[Chargebee](https://www.chargebee.com/) is a recurring billing and subscription management tool that helps subscription businesses streamline their Revenue Operations. It offers a variety of functionality, including:
- Managing recurring billing and subscriptions seamlessly
- Supporting hybrid business models
- Enabling expansion of global footprint
- Automating self-serve workflows for all use-cases.

Chargebee also offers native reporting functionality, but there may be times where one might have more complex reporting needs than what is available on the platform by default. Fortunately, Chargebee also has a marketplace of third party tools that you can leverage to meet a variety of needs, and they also offer an API that you can use to build your own!

This guide will walk you through one option for how you can build your own integration using Amazon Web Services (AWS). More specifically, you will be able to ingest data from your Chargebee account into AWS and use that data for your own custom reporting workflows.

## Pre-Requisites

- A free [AWS account](https://aws.amazon.com/free/)
- A free [Chargebee](https://www.chargebee.com/) account
- [Chargebee API Key](https://www.chargebee.com/docs/2.0/api_keys.html)
  - It is recommended to follow the best practices of least privileges when assigning access to your API key.
- Programming Fundamentals

> It is highly recommended that the steps followed in this guide are done in your Test environment in Chargebee and a development account in AWS.

## Architecture Overview

<p align="center"><img src="img/architecture.jpg" alt="Architecture Diagram" width="90%" height="90%"></p>

The architecture for this guide is very straightforward. [AWS Lambda](https://aws.amazon.com/lambda/) will initiate an export API call to the Chargebee API. A secondary Lambda will download those files once they are ready. All of your exported Chargebee files will be stored in [Amazon S3](https://aws.amazon.com/s3/). [AWS Step Functions](https://aws.amazon.com/step-functions/) will orchestrate the entire workflow, and your Chargebee Site name and API key will be stored in (and referenced from) [AWS Systems Manager Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html). The parameters will be encrypted using [AWS Key Management Service](https://aws.amazon.com/kms/). An optional [Amazon EventBridge Scheduler](https://docs.aws.amazon.com/eventbridge/latest/userguide/scheduler.html) can trigger the workflow on a scheduled basis.  

<br>

---

<br>

## Implementation Instructions

Follow the step-by-step instructions below to create the integration. Click on each step number to expand the section.

{% include accordion.html %}