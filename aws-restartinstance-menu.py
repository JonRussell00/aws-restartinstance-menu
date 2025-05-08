#!/usr/bin/env python

import sys
import time
import argparse
import boto3
from boto3 import Session
import botocore.exceptions

def list_profiles():
    #Return a list of configured AWS profiles.
    session = boto3.session.Session()
    return session.available_profiles

def select_from_menu(options, prompt):
    #Display a menu of options and return the user's selection.
    for idx, option in enumerate(options, start=1):
        print(f"{idx}. {option}")
    while True:
        try:
            choice = int(input(f"{prompt} (1-{len(options)}): "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
        except (ValueError, IndexError):
            print("Invalid selection, please try again.")

def list_instances(ec2):
    #List instances for the given EC2 client.
    instances = []
    response = ec2.describe_instances()
    for r in response['Reservations']:
        for i in r['Instances']:
            instance_name = next((tag["Value"] for tag in i.get("Tags", []) if tag["Key"] == "Name"), "Unnamed")
            instances.append({"id": i['InstanceId'], "name": instance_name, "state": i['State']['Name']})
    return instances

def main():
    parser = argparse.ArgumentParser(description="Stop and start an AWS EC2 instance.")
    parser.add_argument("profile", nargs='?', help="The AWS profile to use for the connection.")
    parser.add_argument("--instance", help="The ID of the EC2 instance to restart.")
    parser.add_argument("--region", default="eu-west-2", help="The AWS region of the instance. Default is 'eu-west-2'.")
    args = parser.parse_args()

    # If no profile is provided, show a menu of available profiles
    if not args.profile:
        profiles = list_profiles()
        if not profiles:
            print("No AWS profiles found. Please configure AWS credentials.")
            sys.exit(1)
        print("Available AWS Profiles:")
        args.profile = select_from_menu(profiles, "Select a profile")

    # Initialize EC2 client
    try:
        session = Session(profile_name=args.profile, region_name=args.region)
        ec2 = session.client('ec2')
    except botocore.exceptions.ProfileNotFound as e:
        print(f"Error: {e}")
        sys.exit(1)

    # If no instance ID is provided, show a menu of available instances
    if not args.instance:
        instances = list_instances(ec2)
        if not instances:
            print("No instances found.")
            sys.exit(0)
        print("Available Instances:")
        selected_instance = select_from_menu(
            [f"{instance['id']} ({instance['name']})" for instance in instances],
            "Select an instance"
        )
        args.instance = instances[[f"{i['id']} ({i['name']})" for i in instances].index(selected_instance)]['id']

    # Restart the selected instance
    print(f"Restarting instance {args.instance} in profile {args.profile}...")
    try:
        # Stop the instance
        print(f"Stopping instance: {args.instance}")
        ec2.stop_instances(InstanceIds=[args.instance])
        
        # Wait until the instance is stopped
        print("Waiting for instance to stop...")
        waiter = ec2.get_waiter('instance_stopped')
        waiter.wait(InstanceIds=[args.instance])
        print(f"Instance {args.instance} is now stopped.")

        # Start the instance again
        print(f"Starting instance: {args.instance}")
        ec2.start_instances(InstanceIds=[args.instance])
        
        # Wait until the instance is running
        print("Waiting for instance to start...")
        waiter = ec2.get_waiter('instance_running')
        waiter.wait(InstanceIds=[args.instance])
        print(f"Instance {args.instance} is now running.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()


