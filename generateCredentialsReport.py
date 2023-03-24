import argparse as argparse
import boto3 as boto3
import datetime as datetime
import emoji as emoji
import logging as logging
import os as os
import platform as platform
import requests as requests
import subprocess as subprocess  # nosec - B404:import_subprocess
import sys as sys
import time as time
from botocore.exceptions import ClientError
from shutil import get_terminal_size as get_terminal_size
from shutil import which as which

logger = logging.getLogger(__name__)


def main():
    """
    Take in the arguments and generate a credentials report.

    you must have the following AWS IAM permissions:

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

    """

    # Configure logging.
    logging.basicConfig(level=logging.ERROR,
                        format='%(levelname)s: %(message)s')

    # Add arguments to the parser.
    parser = argparse.ArgumentParser(exit_on_error=False)

    # The AWS region argument
    parser.add_argument('-r', '--region',
                        help='The AWS region you wish to execute the script in.',
                        default='us-east-1',
                        choices=(
                            'af-south-1',
                            'ap-east-1',
                            'ap-northeast-1',
                            'ap-northeast-2',
                            'ap-south-1',
                            'ap-south-2',
                            'ap-southeast-1',
                            'ap-southeast-2',
                            'ap-southeast-3',
                            'ap-southeast-4',
                            'ca-central-1',
                            'cn-north-1',
                            'cn-northwest-1',
                            'eu-central-1',
                            'eu-central-2',
                            'eu-north-1',
                            'eu-south-1',
                            'eu-west-1',
                            'eu-west-2',
                            'eu-west-3',
                            'me-south-1',
                            'me-central-1',
                            'sa-east-1',
                            'us-east-1',
                            'us-east-2',
                            'us-gov-east-1',
                            'us-gov-west-1',
                            'us-west-1',
                            'us-west-2'
                        )
                        )

    # The AWS CLI profile argument
    parser.add_argument('-p', '--profile',
                        help='AWS profile',
                        default='default')

    # The file name argument
    parser.add_argument('-f', '--filename',
                        help='The name of the file to download the report to.',
                        default='credentialsReport.csv')

    # The open in excel argument
    parser.add_argument('-o', '--open',
                        help='Open the file in Excel.',
                        action='store_true')

    # Parse the arguments.
    args = parser.parse_args()

    """ 
    The below outputs are for making the end user support staff lives easier;
    especially when dealing with end user PEBKAC & PICNIC issues.
    """

    # Display the computer platform that this script is running on.
    print(emoji.emojize(":computer:  Platform: {}",
          language='alias').format(platform.platform()))
    # Display the version of Python that this script is running with
    print(emoji.emojize(":snake:  Python version: {}",
          language='alias').format(sys.version))

    # Check that the Python version is 3 or higher.
    if sys.version_info[0] < 3:
        print(emoji.emojize(
            'You must use Python 3 or higher :cross_mark:',
            language='alias'))
        raise Exception("You must use Python 3 or higher")
    else:
        print(emoji.emojize(
            'Python version is OK :check_mark_button:',
            language='alias'))

    # Check that the AWS CLI is installed.
    if which('aws') is None:
        print(emoji.emojize(
            'AWS CLI is not installed :cross_mark:',
            language='alias'))
        raise Exception("AWS CLI is not installed")
    else:
        print(emoji.emojize(
            'AWS CLI is installed :check_mark_button:',
            language='alias'))
        # Get the version of the AWS CLI.
        aws_cli_version = subprocess.check_output(
            ['aws', '--version']).decode('utf-8').split(' ')[0]  # nosec B603 B607
        # Check that the AWS CLI version is less than verson 2.
        if int(aws_cli_version.split('/')[1].split('.')[0]) < 2:
            # Print an error message and raise an exception.
            print(emoji.emojize(
                'You must use AWS CLI version 2 or higher :heavy_exclamation_mark:',
                language='alias'))
            raise Exception("You must use AWS CLI version 2 or higher")
        else:
            # Display the version of the AWS CLI.
            print(emoji.emojize(":ok:  AWS CLI version: {}", language='alias').format(
                aws_cli_version.split('/')[1]))

    # Display the version of the Boto3 library.
    print(emoji.emojize(":package:  Boto3 version: {}",
          language='alias').format(boto3.__version__))
    # Display the version of the Requests library.
    print(emoji.emojize(":package:  Requests version: {}",
          language='alias').format(requests.__version__))
    # Display the version of the Emoji library.
    print(emoji.emojize(":package:  Emoji version: {}",
          language='alias').format(emoji.__version__))
    # Display the version of the Argparse library.
    print(emoji.emojize(":package:  Argparse version: {}",
          language='alias').format(argparse.__version__))
    # Display the version of the Logging library.
    print(emoji.emojize(":package:  Logging version: {}",
          language='alias').format(logging.__version__))
    # Display the version of the Platform library.
    print(emoji.emojize(":package:  Platform version: {}",
          language='alias').format(platform.__version__))

    # Display the values of the command-line arguments.
    print("AWS Region: {}".format(args.region))
    print("AWS CLI Profile: {}".format(args.profile))
    print("File name: {}".format(args.filename))

    # Create a Boto3 session using the specified profile and region.
    session = boto3.Session(profile_name=args.profile,
                            region_name=args.region)

    # Create a Boto3 client for Amazon IAM.
    s3_client = session.client('iam',
                               use_ssl=True,
                               verify=True
                               )
    # Generate the credential report.
    try:
        s3_client.generate_credential_report()
    except ClientError as e:
        print(e)
        raise Exception("Could not generate the credential report") from e
    else:
        print("Credential report being generated")

    # Wait for the credential report to be generated.
    print("Waiting for the credential report to be generated")
    while True:
        try:
            credential_report = s3_client.get_credential_report()
        except ClientError as e:
            print(e)
            raise Exception("Could not get the credential report") from e
        else:
            # Check if the credential report is ready.
            if credential_report['Content']:
                print("Credential report ready")
                break
            else:
                print("Credential report not ready yet. Waiting another 5 seconds")
                time.sleep(5)

    # Write the credential report to a file.
    print(emoji.emojize(
        ":open_file_folder: Writing the credential report to {}").format(args.filename))
    with open(args.filename, 'w') as f:
        f.write(credential_report['Content'].decode('utf-8'))

    if args.open:
        # determine if platform is Windows, Linux or Mac
        if platform.system() == 'Windows':
            # check if Excel is installed
            if which('excel.exe') is None:
                print(emoji.emojize(
                    'Excel is not installed :cross_mark:',
                    language='alias'))
                raise Exception("Excel is not installed")
            else:
                print(emoji.emojize(
                    ":open_file_folder: Opening {} in Excel in Windows").format(args.filename))
                # nosec B605: start is used to open a file with excel.exe
                os.system('start excel.exe {}'.format(args.filename))
        elif platform.system() == 'Linux':
            # check if LibreOffice is installed
            if which('libreoffice') is None:
                print(emoji.emojize(
                    'LibreOffice is not installed :cross_mark:',
                    language='alias'))
                raise Exception("LibreOffice is not installed")
            else:
                print(emoji.emojize(
                    ":open_file_folder: Opening {} in LibreOffice in Linux").format(args.filename))
                # nosec B605: libreoffice is used to open a file with LibreOffice
                os.system('libreoffice {}'.format(args.filename))
        elif platform.system() == 'Darwin':
            # check if Excel is installed
            if which('Microsoft Excel') is None:
                print(emoji.emojize(
                    'Excel is not installed :cross_mark:',
                    language='alias'))
                raise Exception("Excel is not installed")
            else:
                print(emoji.emojize(
                    ":open_file_folder: Opening {} in Excel in Mac").format(args.filename))
                # nosec B605: open is used to open a file with Microsoft Excel
                os.system('open -a "Microsoft Excel" {}'.format(args.filename))

    print(emoji.emojize(":white_check_mark:  Done :white_check_mark:"))


if __name__ == "__main__":
    main()
