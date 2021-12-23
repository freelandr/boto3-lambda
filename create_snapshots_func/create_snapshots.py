from datetime import datetime
import boto3

def lambda_handler(event, context):
    print("I've been deployed from Github!")
    ec2 = boto3.resource('ec2')

    # find instances with a tag of 'backup=true'
    search_filter = {'Name': 'tag:backup', 'Values': ['true']}
    instances_to_backup = ec2.instances.filter(Filters = [search_filter])
    
    timestamp = datetime.utcnow().replace(microsecond=0).isoformat()
    
    for i in instances_to_backup:
        for v in i.volumes.all():
            desc = f'Backup of {i.id}, volume {v.id} created {timestamp}'
            print(desc)
            snapshot = v.create_snapshot(Description=desc)
            print(f'Created snapshot {snapshot.id}')