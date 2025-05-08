# aws-restartinstance-menu.py
A python script, using the Boto3 library and AWS API, to list all AWS instances, and allows you to select one to forcibly restart.

This is useful if an instance stops responding, or crashes, and you cannot connect to it remotely. 

Usually you would need to log in to the AWS Console, find the instance and force a restart, then monitor it to ensure it successfully restarts.

This script achieves the same using the AWS API, but without the need to log in to the console.

The script lists all the profiles defined in your `~/.aws/credentials` file and allows you to select one for the connection.

The `~/.aws/credentials` file should have the following format:

    [default]
    aws_access_key_id = AA_ACCESS_KEY_AA
    aws_secret_access_key = AA_SECRET_KEY_AA

    [projectA]
    aws_access_key_id = AA_ACCESS_KEY_AA
    aws_secret_access_key = AA_SECRET_KEY_AA

    [projectB]
    aws_access_key_id = BB_ACCESS_KEY_BB
    aws_secret_access_key = BB_SECRET_KEY_BB

    [projectC]
    aws_access_key_id = CC_ACCESS_KEY_CC
    aws_secret_access_key = CC_SECRET_KEY_CC`

# Usage
    ./aws-restartinstance-menu.py --help
    usage: aws-restartinstance-menu.py [-h] [--instance INSTANCE] [--region REGION] [profile]

    Stop and start an AWS EC2 instance.

    positional arguments:
      profile              The AWS profile to use for the connection.

    options:
      -h, --help           show this help message and exit
      --instance INSTANCE  The ID of the EC2 instance to restart.
      --region REGION      The AWS region of the instance. Default is 'eu-west-2'.

# Typical output
    $ ./aws-restartinstance-menu.py 
    Available AWS Profiles:
    1. default
    2. projectA
    3. projectB
    4. projectC
    Select a profile (1-4): 3
    Available Instances:
    1. i-1234567890abcdef1 (Web_Server_1)
    2. i-1234567890abcdef2 (Web_Server_2)
    3. i-1234567890abcdef3 (Database_Server)
    4. i-1234567890abcdef4 (App_Server_1)
    5. i-1234567890abcdef5 (App_Server_2)
    6. i-1234567890abcdef6 (Dev_Server)
    Select an instance (1-6): 4
    Restarting instance i-1234567890abcdef4 in profile projectB...
    Stopping instance: i-1234567890abcdef4
    Waiting for instance to stop...
    Instance i-1234567890abcdef4 is now stopped.
    Starting instance: i-1234567890abcdef4
    Waiting for instance to start...
    Instance i-1234567890abcdef4 is now running.


