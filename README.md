# Customer Onboarding Terraform
## Technology Used

* Python for GUI
* Ansible for configuration management
* GitHub as code repository and pipeline runner 
* Terraform as Infrastructure as Code to provision AWS resources
* Packer to create golden images (refer to [ami-factory](https://github.com/SapphireSystems/ami-factory))


## Deployment Pipeline

The deployment pipeline runs using GitHub Actions. Workflows are created per customer by copying and updating the `template.yml` file in `./github/workflows/` directory.


### GitHub Workflow Jobs
The following runs on: _pull_request_
1. Checkov - to apply static code analysis
2. Infracost - to see cloud costs before launching resources
3. Terraform Plan - to show changes required by the current configuration

The following runs on: _push_
1. Terraform Apply - to finaly create or update infrastructure
2. Configure Servers - to configure the provisioned servers using Ansible


## Development Tools

| Tool                                                                                          | Use              |
| --------------------------------------------------------------------------------------------- |------------------|
| [Visual Studio Code](https://code.visualstudio.com/download)                                  |Code editor|
| [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)      |To enable assume role via terminal while running Terraform code locally
| [Python](https://www.python.org/downloads)                                               |Python v3.13 or later is required|
| [Terraform](https://www.terraform.io/downloads)                                               |To enable running of Terraform code locally|
| [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html) |To enable running of Ansible playbooks locally|
| [AWS Cloud 9](https://eu-west-2.console.aws.amazon.com/cloud9/home/product)                   |Cloud-based IDE for Windows users who need to perform Ansible-related tasks
| [Git](https://git-scm.com/downloads)                                                          |Version Control System|
| [AWS Tools for PowerShell on Windows](https://docs.aws.amazon.com/powershell/latest/userguide/pstools-getting-set-up-windows.html)                                                          |To assume roles when working with Terraform locally|


## IAM Roles

| Role ARN                                              | Use                                                       | Session Duration |
| ----------------------------------------------------- |-----------------------------------------------------------|------------------|
|`arn:aws:iam::<customeraccount#>:role/SSMInstanceProfile`|the instance role profile used by provisioned EC2 instances|2 Hours
|`arn:aws:iam::<customeraccount#>:role/github-oidc`|the role used by GitHub Actions to permit AWS configuration on configure_servers job; primarily used when running AWS commands on CLI|2 Hours
|`arn:aws:iam::<customeraccount#>:role/AWSAFTExecution`|the role assumed by Terraform to permit AWS configuration|2 Hours
|`arn:aws:iam::<customeraccount#>:role/github-oidc`|the role used during terraform_apply and terraform_plan job|2 Hours
|`arn:aws:iam::812224207958:role/AWSAFTExecution`|the role assumed by Terraform to use resources on shared services account|1 Hour


## Install Dependencies

* (Required) Windows x64
```sh
curl -L -o vc_redist.x64.exe https://aka.ms/vs/17/release/vc_redist.x64.exe
start /wait vc_redist.x64.exe /install /quiet /norestart
del vc_redist.x64.exe
```

* Check python version (should be v3.13 or later)
```sh
python3 --version || python --version
```

* Upgrade pip
```sh
python3 -m pip install --upgrade pip wheel setuptools || python -m pip install --upgrade pip wheel setuptools
```

* Install python libraries
```sh
pip install -r requirements.txt
```
- or
```sh
pip install awsume boto3 botocore paramiko pandas numpy pillow pyqt6 pyside6 pyinstaller
```


## Instructions

* Clone this repo    
```sh
git clone git@github.com:SapphireSystems/customer-onboarding-terraform.git
```

* Create your branch
```sh
git checkout -b feat/<AWS_ACCOUNT_NAME>
```

* Awsume to your AWS Account
```sh
awsume <AWS_ACCOUNT_NAME>
```

* Build & Run application
```sh
python3 build_app.py || python build_app.py
```

* Run application
```sh
python3 start_app.py || python start_app.py
```

* Commit and push changes
```sh
git add .
```
```sh
git commit -m "onboarding account"
```
```sh
git push
```

* Create pull request to main branch

* Go to Github Actions to check pipeline

* After pipeline is done, select reviewer/approver

* When approved, squash and merge

* Go to Github Actions again and check pipeline


## Tags-Rename (Manual)

### This is used when renaming EBS Volume Tags

* Awsume to AWS Account
```sh
awsume <AWS_ACCOUNT>
```

* Looks for comments "# change this value to rename tag" in tags_rename.py and change to the proper value.
* Leave blank "" if don't want to change any.

* Run Tags Rename Script
```sh
python3 tags_rename.py || python tags_rename.py
```


## Modify and Apply Terraform for an existing AWS Account

* Create your branch
```sh
git checkout -b feat/<AWS_ACCOUNT_NAME>
```

* Awsume to AWS Account
```sh
awsume <AWS_ACCOUNT_NAME>
```

* Navigate to AWS Account TF Folder
```sh
cd terraform/<AWS_ACCOUNT_NAME>
```

* Make necessary changes to TF files
* Most of the specifications are location in variables.tf

* Terraform Init (Correct details can be found in S3 Bucket)
```sh
terraform init \
-backend-config="region=<AWS_ACCOUNT_REGION>" \
-backend-config="bucket=tf-customer-onboarding--<AWS_ACCOUNT_NAME>-<AWS_ACCOUNT_ID>" \
-backend-config="key=ansible-runner.tfstate" \
-backend-config="dynamodb_table=tf-state-lock--<AWS_ACCOUNT_NAME>-<AWS_ACCOUNT_ID>" \
-backend-config="encrypt=true" 
```

* Change IAM Role trust polices (check below)

* Terraform Plan
```sh
terraform plan
```

* Terraform Apply
```sh
terraform apply
```

* Revert trust policy changes to maintain security

> NOTE: Don't make any changes to workflow file (.github/workflows/<AWS_ACCOUNT_NAME>.yml) to prevent pipeline from running during Pull Request.

* Create pull request to main branch

* When approved, squash and merge



### When encountering errors during plan and apply check trust policies in IAM Roles for current AWS_ACCOUNT and aft-mgmt account

> IAM Roles (only change trust policies):
AWSAFTExecution
SSMInstanceProfile
OrganizationAccountAccessRole

### Example error (using financeit as AWS_ACCOUNT)
> │ Error: operation error STS: AssumeRole, https response error StatusCode: 403, RequestID: 8aee7e44-a9ab-4b24-aa71-9b2a25d9b140, api error
│ AccessDenied: User: arn:aws:sts::905418122674:assumed-role/OrganizationAccountAccessRole/financeit is not authorized to perform: sts:AssumeRole on
│ resource: arn:aws:iam::231639157514:role/AWSAFTExecution

* Go to aft-mgmt (231639157514) AWS account and modify IAM Role trust policies for AWSAFTExecution
* Add "arn:aws:sts::905418122674:assumed-role/OrganizationAccountAccessRole/financeit" to "AWS Principal list"

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": [
                    "arn:aws:iam::231639157514:role/AWSAFTAdmin",
                    "arn:aws:sts::231639157514:assumed-role/AWSAFTAdmin/AWSAFT-Session",
                    "arn:aws:sts::886436937679:assumed-role/github-oidc/actionsrolesession",
                    "arn:aws:sts::905418122674:assumed-role/OrganizationAccountAccessRole/financeit"
                ]
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

### Example error
> │ Error: operation error STS: AssumeRole, https response error StatusCode: 403, RequestID: b5d08260-da06-4274-a9f2-eaa786277f6f, api error
│ AccessDenied: User: arn:aws:sts::905418122674:assumed-role/OrganizationAccountAccessRole/financeit is not authorized to perform: sts:AssumeRole on
│ resource: arn:aws:iam::905418122674:role/AWSAFTExecution

* Go to financeit (905418122674) AWS account and modify IAM Role trust policies for AWSAFTExecution
* Add "arn:aws:sts::905418122674:assumed-role/OrganizationAccountAccessRole/financeit" to "AWS Principal list"

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": [
                    "arn:aws:sts::231639157514:assumed-role/AWSAFTAdmin/AWSAFT-Session",
                    "arn:aws:sts::905418122674:assumed-role/OrganizationAccountAccessRole/financeit"
                ]
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

### Example error
> │ Error: operation error STS: AssumeRole, https response error StatusCode: 403, RequestID: f6e623ba-6295-4973-9d72-2626bea19ae5, api error 
│ AccessDenied: User: arn:aws:sts::905418122674:assumed-role/OrganizationAccountAccessRole/financeit is not authorized to perform: sts:AssumeRole on 
│ resource: arn:aws:iam::905418122674:role/SSMInstanceProfile

* Go to financeit (905418122674) AWS account and modify IAM Role trust policies for SSMInstanceProfile
* Add "arn:aws:sts::905418122674:assumed-role/OrganizationAccountAccessRole/financeit" to "AWS Principal list"

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:sts::905418122674:assumed-role/OrganizationAccountAccessRole/financeit",
                "Service": "ec2.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```