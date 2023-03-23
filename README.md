# Python script to generate an AWS credentials report

Sample Python console script to generate the AWS credentials report and optionally open it in a spreadsheet application.

This script will also output diagnostics during run time for use by end user support in the case of an abnormal termination of the script. The diagnostics include:

- What platform the script is being run on.
- What version of Python the script is being run with.
- If the AWS CLI is installed and what version of the AWS CLI is installed.
- The version levels of the various packages that are used by the script
- The various input parameters supplied by the

## Requirements

- AWS CLI - this program will check to see if the AWS CLI has been installed. This program will pull the AWS credentials from the AWS CLI credentials files for the appropriately specified AWS CLI profile.
- Python 3 or higher is required to run this script
- The AWS user that is running this python script must have the following AWS IAM permissions:
  - iam:GenerateCredentialReport
  - iam:GetCredentialReport

```json
{
        "Version": "2012-10-17",
        "Statement": {
            "Effect": "Allow",
            "Action": [
                "iam:GenerateCredentialReport",
                "iam:GetCredentialReport"
            ],
            "Resource": "*"
        }
 }
```

## Parameters

This script will take the following parameters

`-r` or `--region` : The AWS region to execute this script in. The acceptable values are:

- af-south-1
- ap-east-1
- ap-northeast-1
- ap-northeast-2
- ap-south-1
- ap-south-2
- ap-southeast-1
- ap-southeast-2
- ap-southeast-3
- ap-southeast-4
- ca-central-1
- cn-north-1
- cn-northwest-1
- eu-central-1
- eu-central-2
- eu-north-1'
- eu-south-1
- eu-west-1
- eu-west-2
- eu-west-3
- me-south-1
- me-central-1
- sa-east-1
- us-east-1
- us-east-2
- us-gov-east-1
- us-gov-west-1
- us-west-1
- us-west-2

`-p` or `--profile`: The AWS CLI profile to get the AWS credentials from. Defaults to 'default'

`-f` or `--filename`: The name of the file the script will save the AWS credentials report to. Default is 'credentialsReport.csv'

`-o` or `--open`: The presence of this parameter will trigger the script to open the appropriate spreadsheet application for your platform.

## Example run

Using the following command this is the expected output you should see

`python3 ./generateCredentialsReport.py --region='us-east-1' --profile='default' --filename 'credentialsReport.csv' --open`

💻  Platform: macOS-13.2.1-arm64-arm-64bit
🐍  Python version: 3.11.2 (main, Feb 16 2023, 02:55:59) [Clang 14.0.0 (clang-1400.0.29.202)]
Python version is OK ✅
AWS CLI is installed ✅
🆗  AWS CLI version: 2.11.5
📦  Boto3 version: 1.26.93
📦  Requests version: 2.28.2
📦  Emoji version: 2.2.0
📦  Argparse version: 1.1
📦  Logging version: 0.5.1.2
📦  Platform version: 1.0.8
AWS Region: us-east-1
AWS CLI Profile: default
File name: credentialsReport.csv
Credential report being generated
Waiting for the credential report to be generated
Credential report ready
📂 Writing the credential report to credentialsReport.csv
📂 Opening credentialsReport.csv in Excel

## Security Notes

Bandit `#nosec` comments placed in code to acknowledge any security false positives in this script. Please review the code to see if the risks are acceptable to you before executing the script.
