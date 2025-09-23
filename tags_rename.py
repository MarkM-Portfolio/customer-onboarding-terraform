import boto3, json, os, platform, subprocess, time

class EC2Instance:
    def __init__(self, instance_id, instance_name, volume_info):
        self.instance_id = instance_id
        self.instance_name = instance_name
        self.volume_info = volume_info

class TagsRename():
    def __init__(self):
        self.os_name = platform.system()

        self.AWS_ALIAS = ''
        self.AWS_ACCT = ''
        self.AWS_RGN = ''
        self.AWS_REGNAME = None
        self.AWS_HOSTID = ''
        self.AWS_ENV = ''
        self.EC2_CLIENT = ''
        self.EC2 = []

        self.init_account()
        self.get_instances()
        self.volume_tags_rename()

    def init_account(self):
        try:
            ACCT_NAME = boto3.client('sts').get_caller_identity()['UserId'].split(':')[1]
        except (Exception) as e:
            errorMsg = 'No awsumed account.<br>Please set one now!'
            print(errorMsg)
            self.end(1)
        else:
            try:
                self.AWS_ACCT = boto3.client('sts').get_caller_identity()["Account"]
                cmd = f"awsume sapphire-payer && aws organizations list-tags-for-resource --resource-id { self.AWS_ACCT } --output json"
                result = subprocess.run(f"{ '.' if self.os_name != 'Windows' else '' } { cmd }", shell=True, capture_output=True, text=True)
            except (Exception) as e:
                errorMsg = f'[ERROR]: Account ({ ACCT_NAME }) has no tag CustomerID. Please set one now!'
                print(errorMsg)
                self.end(1)
            else:
                self.AWS_ALIAS = boto3.client('sts').get_caller_identity()['UserId'].split(':')[1]

                tags = json.loads(result.stdout).get('Tags')
                for obj in tags:
                    if obj.get('Key') == 'CustomerID':
                        self.AWS_HOSTID = obj.get('Value')
                    if obj.get('Key') == 'Environment':
                        self.AWS_ENV = obj.get('Value')

                self.AWS_RGN = boto3.Session().region_name
                self.AWS_REGNAME = self.get_region_name()

                print(f'\nAccount ID: { self.AWS_ACCT }')
                print(f'\nAccount Name: { self.AWS_ALIAS }')
                print(f'\nAccount Region: { self.AWS_RGN } ({ self.AWS_REGNAME })')
                print(f'\nCustomer ID: { self.AWS_HOSTID }')
                print(f'\nEnvironment: { self.AWS_ENV }')

    def get_region_name(self):
        if 'eu-west-2' in self.AWS_RGN:
            return "London"
        elif 'us-east-2' in self.AWS_RGN:
            return 'Ohio'
        else:
            return 'N/A'
        
    def get_instances(self):
        self.EC2_CLIENT = boto3.client('ec2', region_name=self.AWS_RGN)
        response = self.EC2_CLIENT.describe_instances(
            Filters=[{
                'Name': 'tag:' + 'CustomerID',
                'Values': [ self.AWS_HOSTID ]
            }]
        )

        instances = []

        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instances.append(instance)

        for instance in instances:
            instance_name = self.get_instance_name(instance.get('Tags', [])) 
            volume_info = self.get_volume_ids_and_tags(instance.get('BlockDeviceMappings', []), instance['InstanceId']) 

            ec2_instance = EC2Instance(
                instance_id=instance['InstanceId'],
                instance_name=instance_name,
                volume_info=volume_info
            )
            
            self.EC2.append(ec2_instance)

        print(f'\n{"-":>1}----------------------------------')
        print(f"Total # EC2 Instances: { len(self.EC2) }")

    def get_instance_name(self, tags):
        for tag in tags:
            if tag['Key'] == 'Name':
                return tag['Value']
        return 'N/A' 
    
    def get_volume_ids_and_tags(self, block_device_mappings, instance_id):
        volume_info = []

        for device in block_device_mappings:
            volume_id = device['Ebs']['VolumeId']
            device_name = device['DeviceName']
            
            tags = self.get_volume_tags(volume_id)
            
            volume_info.append({
                'VolumeId': volume_id,
                'DeviceName': device_name,
                'Tags': tags,
                'InstanceId': instance_id
            })
        
        return volume_info

    def get_volume_tags(self, volume_id):
        response = self.EC2_CLIENT.describe_tags(
            Filters = [
                {'Name': 'resource-id', 'Values': [ volume_id ]},
                {'Name': 'resource-type', 'Values': [ 'volume' ]}
            ])
        
        tags = response.get('Tags', [])
        return tags

    def volume_tags_rename(self):
        updated_volumes = [] 

        for ec2_instance in self.EC2:
            print(f'{"-":>1}----------------------------------')
            print(f"Instance Name: { ec2_instance.instance_name }")
            for vol in ec2_instance.volume_info:
                volume_id = vol['VolumeId']
                dev_name = vol['DeviceName']
                instance_id = vol['InstanceId']

                ansible_group_value = next((tag['Value'] for tag in vol['Tags'] if tag['Key'] == 'ansible_group'), None)

                if ansible_group_value:
                    box_type = "DC" if ansible_group_value.endswith("-dc") else "HANA" if ansible_group_value == "sap_hana_db" else "HM" if ansible_group_value == "sap_hana_win" else \
                        "VDA" if ansible_group_value.startswith("citrix") else "RDS" if ansible_group_value.startswith("rds") else \
                        "INT" if ansible_group_value.startswith("integration") else "SQL" if ansible_group_value.startswith("sql") else None
                    patch_group = "Windows" if ansible_group_value.endswith("-dc") else "Linux" if ansible_group_value == "sap_hana_db" else "Windows" if ansible_group_value.endswith("_win") else None

                if box_type and self.AWS_HOSTID and self.AWS_ENV:
                    new_instance_name = f"{ self.AWS_HOSTID }{ box_type }{ self.AWS_ENV[0] }{ ec2_instance.instance_name[-2:] if ec2_instance.instance_name[-2:].isdigit() else '01' }"

                updated_tags = []
                
                for tag in vol['Tags']:
                    if tag['Key'] == 'Name':
                        new_tag_name = f"{ new_instance_name if new_instance_name else tag['Value'] }/{ dev_name[5:].replace('a', '') if dev_name.startswith('/dev/sda1') else dev_name }"
                        updated_tags.append({ 'Key': 'Name', 'Value': new_tag_name if new_tag_name else tag['Value'] })
                        print(f"    { tag['Key']}: { tag['Value'] } ~> { new_tag_name if new_tag_name else tag['Value'] }")
                    elif tag['Key'] == 'Environment':
                        new_tag_env = "PROD" if not self.AWS_ENV else self.AWS_ENV
                        updated_tags.append({ 'Key': 'Environment', 'Value': new_tag_env if new_tag_env else tag['Value'] })
                        print(f"    { tag['Key']}: { tag['Value'] } ~> { new_tag_env if new_tag_env else tag['Value'] }")
                    elif tag['Key'] == 'CustomerName':
                        new_tag_customer_name = self.AWS_ALIAS
                        updated_tags.append({ 'Key': 'CustomerName', 'Value': new_tag_customer_name if new_tag_customer_name else tag['Value'] })
                        print(f"    { tag['Key']}: { tag['Value'] } ~> { new_tag_customer_name if new_tag_customer_name else tag['Value'] }")
                    elif tag['Key'] == 'CustomerID':
                        new_tag_customer_id = self.AWS_HOSTID
                        updated_tags.append({ 'Key': 'CustomerID', 'Value': new_tag_customer_id if new_tag_customer_id else tag['Value'] })
                        print(f"    { tag['Key']}: { tag['Value'] } ~> { new_tag_customer_id if new_tag_customer_id else tag['Value'] }")
                    elif tag['Key'] == 'Patch Group':
                        new_tag_patch = patch_group
                        updated_tags.append({ 'Key': 'Patch Group', 'Value': new_tag_patch if new_tag_patch else tag['Value'] })
                        print(f"    { tag['Key']}: { tag['Value'] } ~> { new_tag_patch if new_tag_patch else tag['Value'] }")
                    elif tag['Key'] == 'ansible_group':
                        new_tag_ansible = ansible_group_value
                        updated_tags.append({ 'Key': 'ansible_group', 'Value': new_tag_ansible if new_tag_ansible else tag['Value'] })
                        print(f"    { tag['Key']}: { tag['Value'] } ~> { new_tag_ansible if new_tag_ansible else tag['Value'] }")
                    elif tag['Key'] == 'FinanceCode':
                        new_tag_financecode = "" # change this value to rename tag
                        updated_tags.append({ 'Key': 'FinanceCode', 'Value': new_tag_financecode if new_tag_financecode else tag['Value'] })
                        print(f"    { tag['Key']}: { tag['Value'] } ~> { new_tag_financecode if new_tag_financecode else tag['Value'] }")
                    elif tag['Key'] == 'map-migrated':
                        new_tag_map_migrated = "" # change this value to rename tag
                        updated_tags.append({ 'Key': 'map-migrated', 'Value': new_tag_map_migrated if new_tag_map_migrated else tag['Value'] })
                        print(f"    { tag['Key']}: { tag['Value'] } ~> { new_tag_map_migrated if new_tag_map_migrated else tag['Value'] }")
                    elif tag['Key'] == 'scheduler:ebs-snapshot':
                        new_tag_scheduler = "Yes" # change this value to rename tag
                        updated_tags.append({ 'Key': 'scheduler:ebs-snapshot', 'Value': new_tag_scheduler if new_tag_scheduler else tag['Value'] })
                        print(f"    { tag['Key']}: { tag['Value'] } ~> { new_tag_scheduler if new_tag_scheduler else tag['Value'] }")
                    else:
                        updated_tags.append(tag) # keep the other tags unchanged

                # DEBUG
                # updated_tags = [tag for tag in updated_tags if tag['Key'] not in ['ResourceId', 'ResourceType']]
                # print(updated_tags)

                if updated_tags:
                    updated_volumes.append((volume_id, updated_tags, instance_id))

        if updated_volumes:
            user_input = input("\nDo you want to apply changes to all volumes? (y/n): ").strip().lower()

            if user_input in ['yes', 'y']:
                print("\nApplying tag changes...\n")
                for volume_id, tags, instance_id in updated_volumes:
                    try:
                        self.EC2_CLIENT.create_tags(
                            Resources=[volume_id],
                            Tags=tags
                        )
                        instance_name = next((instance.instance_name for instance in self.EC2 if instance.instance_id == instance_id), "Unknown Instance")
                        print(f"Successfully renamed tags for Instance: { instance_name } | Volume ID: { volume_id }")
                    except Exception as e:
                        print(f"Error renaming tags for Instance: { instance_name } | Volume ID { volume_id }: { e }")
                        self.end(1)
                self.end(0)
            elif user_input in ['no', 'n']:
                print("No changes will be applied.")
            else:
                print("Invalid input. Please respond with 'yes', 'no', 'y', or 'n'.")
        else:
            print("No volumes had any tag updates.")

    def end(self, exit_code):
        print('\n\nD O N E !!!' if exit_code == 0 else f"\n\nExited with non-zero error status ({ exit_code }).")

        time.sleep(1)
        os._exit(exit_code)


if __name__ == '__main__':
    try:
        TagsRename()
    except (KeyboardInterrupt):
        print("\n\n[ERROR]: Program interrupted by the user (Ctrl+C)")
