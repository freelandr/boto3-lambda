import boto3

def lambda_handler(event, context):
    print("I'm the new function!")
    ec2_client = boto3.client('ec2')
    
    account_id = boto3.client('sts').get_caller_identity().get('Account')

    response = ec2_client.describe_snapshots(OwnerIds=[account_id])
    snapshots = response['Snapshots']

    # keep only the most recent snapshot for each volume
    sorted_snaps = sorted(snapshots, key=lambda snapshot: (snapshot["SnapshotId"], snapshot["VolumeId"]), reverse=True)
    
    [print(f'{snapshot.get("SnapshotId")=}, {snapshot.get("VolumeId")=}, {snapshot.get("StartTime").ctime()=}') for snapshot in sorted_snaps]
    
    retained_volumes = []
    
    for snapshot in sorted_snaps:
        if snapshot["VolumeId"] in retained_volumes:
            # we already have a more recent snapshot, so delete this one...
            try:
                print(f'Deleting snapshot: {snapshot["SnapshotId"]}')
                ec2_client.delete_snapshot(SnapshotId=snapshot["SnapshotId"])
            except Exception as e:
                if 'InvalidSnapshot.InUse' in e.message:
                    print(f'Snapshot {snapshot["SnapshotId"]} in use, skipping')
                    continue
        else:
            # this is the most recent snapshot - retain
            retained_volumes.append(snapshot["VolumeId"])