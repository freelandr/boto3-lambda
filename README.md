# Python / AWS Boto3 project
Lambda functions for creating and pruning EBS volume snapshots.
Snapshots are created for for all EC2 instances with tag backup=true.
A push to the main branch on this repository automatically triggers re-deployment of the Lambda code.
