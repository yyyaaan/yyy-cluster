from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
from boto3 import client as aws_client
from google.cloud import compute_v1, secretmanager
from json import dumps, loads
from logging import getLogger
from openstack import (
    connect as openstack_connect, 
    enable_logging as openstack_logging
)

logger = getLogger("FleetManager")


class FleetManager:
    """
    Generic VM management support on OpenStack, GCP, AWS and Azure
    """

    def __init__(self, vm_fleet=[]):
        name = "projects/yyyaaannn/secrets/ycrawl-credentials/versions/latest"
        gce_decoded = secretmanager \
            .SecretManagerServiceClient() \
            .access_secret_version(request={"name": name}) \
            .payload.data.decode("UTF-8")
        SECRET = loads(gce_decoded)

        self.vm_fleet = vm_fleet
        if vm_fleet is None or (len(vm_fleet) < 1):
            self.vm_fleet = self.__default_vm_fleet()

        # https://docs.openstack.org/openstacksdk/latest/user/proxies/compute.html
        openstack_logging(debug=False)
        self.openstack_conn = openstack_connect(cloud='openstack')
        self.gce_client = compute_v1.InstancesClient()
        self.aws_secrets = {
            "aws_access_key_id": SECRET['AWS_ACCESS_KEY'],
            "aws_secret_access_key": SECRET['AWS_SECRET']
        }
        self.ace_client = ComputeManagementClient(
            ClientSecretCredential(
                tenant_id=SECRET['AZURE_TENANT_ID'],
                client_id=SECRET['AZURE_CLIENT_ID'],
                client_secret=SECRET['AZURE_CLIENT_SECRET'],
            ),
            SECRET['AZURE_SUBSCRIPTION_ID']
        )
        return None

    def vm_list_all(self):
        n1, vms1 = self.list_instances_gcp()
        n2, vms2 = self.list_instances_azure()
        n3, vms3 = self.list_instances_aws()
        n4, vms4 = self.list_instances_csc()

        n_running, vm_list = n1+n2+n3+n4, vms1+vms2+vms3+vms4

        vm_list.sort(key=lambda x: x["header"])
        for i, x in enumerate(vm_list):
            x["icon"] = f"filter_{i+1}"

        return n_running, vm_list

    def vm_startup(self, vmid):
        if str(vmid)[:4] == "test":
            return True, f"start {vmid} passed"
        try:
            the_vm = [
                x for x in self.vm_fleet if x.get("vmid", "") == vmid
            ].pop(0)

            if not the_vm:
                return False, "VM not registered"
            if the_vm.provider == "GCP":
                return self.vm_startup_gcp(vmid=the_vm["vmid"], zone=the_vm["zone"])  # noqa: E501
            if the_vm.provider == "Azure":
                return self.vm_shutdown_azure(vmid=the_vm["vmid"], resource_group=the_vm["resourcegroup"])  # noqa: E501
            if the_vm.provider == "AWS":
                return self.vm_startup_aws(vmid=the_vm["vmid"], resourceId=the_vm["resourceId"], zone=the_vm["zone"])  # noqa: E501
            if the_vm.provider == "CSC":
                return self.vm_startup_csc(vmid=the_vm["vmid"])
        except Exception as e:
            return False, f"Error occurred: {str(e)}"

    def vm_shutdown(self, vmid):
        if str(vmid)[:4] == "test":
            return True, f"stop {vmid} passed"
        try:
            the_vm = [
                x for x in self.vm_fleet if x.get("vmid", "") == vmid
            ].pop(0)

            if not the_vm:
                return False, "VM not registered"
            if the_vm.provider == "GCP":
                return self.vm_shutdown_gcp(vmid=the_vm["vmid"], zone=the_vm["zone"])  # noqa: E501
            if the_vm.provider == "Azure":
                return self.vm_shutdown_azure(vmid=the_vm["vmid"], resource_group=the_vm["resourcegroup"])  # noqa: E501
            if the_vm.provider == "AWS":
                return self.vm_shutdown_aws(vmid=the_vm["vmid"], resourceId=the_vm["resourceId"], zone=the_vm["zone"])  # noqa: E501
            if the_vm.provider == "CSC":
                return self.vm_shutdown_csc(vmid=the_vm["vmid"])
        except Exception as e:
            return False, f"Error occurred: {str(e)}"

    # # #
    # Below are implementation for each cloud
    # # #
    def list_instances_csc(self):
        vm_names = [
            x.get("vmid", "") for x in self.vm_fleet
            if x.get("provider", "") == "CSC"
        ]

        out_list, n_running = [], 0
        for instance in self.openstack_conn.compute.servers():
            if str(instance.name) not in vm_names:
                logger.warn(f"CSC instance {instance.name} is not registered")
            out_list.append({
                "vmid": str(instance.name),
                "header": f"{instance.name} {instance.vm_state} (csc-nova)  {instance.flavor['original_name']}",  # noqa: E501
                "state": str(instance.vm_state),
                "size": str(instance.flavor['original_name']),
                "note": "",
                "content": dumps(str(instance)).replace(", ", ",<br/>").replace('\\"', '"')[1:-1],  # noqa: E501
            })
            if instance.vm_state == 'active':
                n_running += 1

        return n_running, out_list

    def vm_startup_csc(self, vmid):
        the_vm = [
            x for x in self.openstack_conn.compute.servers()
            if x.name == vmid
        ].pop()
        vm_status = str(the_vm.vm_state)

        if vm_status == "active":
            return False, f"{vmid} is already active, no action"
        try:
            self.openstack_conn.compute.unshelve_server(the_vm)
            return True, f"restarting {vmid} (was {vm_status})"
        except Exception as e:
            return False, f"starting {vmid} failed due to {str(e)}"

    def vm_shutdown_csc(self, vmid):
        the_vm = [
            x for x in self.openstack_conn.compute.servers() 
            if x.name == vmid
        ][0]

        if the_vm.vm_state != "active":
            return False, f"{vmid} is not running, no action."
        try:
            self.openstack_conn.compute.shelve_server(the_vm)
            return True, f"shutting down {vmid}"
        except Exception as e:
            return False, f"shutting down {vmid} failed due to {str(e)}"

    def list_instances_gcp(self):
        zones = [
            x.get("zone", "") for x in self.vm_fleet
            if x.get("provider", "") == "GCP"
        ]
        out_list, n_running = [], 0

        for zone in set(zones):
            for instance in self.gce_client.list(project="yyyaaannn", zone=zone):  # noqa: E501
                restricted = "(Restricted Restart) " if instance.start_restricted else ""  # noqa: E501
                out_list.append({
                    "vmid": str(instance.name),
                    "header": f"{instance.name} {instance.status} {restricted} ({instance.zone.split('/')[-1]})  {instance.machine_type.split('/')[-1]}",  # noqa: E501
                    "state": str(instance.status),
                    "size": instance.machine_type.split('/')[-1],
                    "note": restricted,
                    "content": dumps(str(instance)).replace("\\n", "<br/>").replace('\\"', '"')[1:-1],  # noqa: E501
                })
                if instance.status == 'RUNNING':
                    n_running += 1

        return n_running, out_list

    def vm_startup_gcp(self, vmid, zone):
        vm_check = [
            x for x in self.gce_client.list(project="yyyaaannn", zone=zone) 
            if x.name == vmid
        ]
        vm_status = [x.status for x in vm_check][0]
        vm_restricted = [x.start_restricted for x in vm_check][0]

        if vm_status == "RUNNING":
            return False, f"{vmid} is already active, no action"
        if vm_restricted:
            return False, f"{vmid}({vm_status}) is restricted."
        try:
            self.gce_client.start_unary(project="yyyaaannn", zone=zone, instance=vmid)  # noqa: E501
            return True, f"restarting {vmid} (was {vm_status})"
        except Exception as e:
            return False, f"starting {vmid} failed due to {str(e)}"

    def vm_shutdown_gcp(self, vmid, zone):
        vm_check = [
            x for x in self.gce_client.list(project="yyyaaannn", zone=zone)
            if x.name == vmid
        ]
        vm_status = [x.status for x in vm_check][0]

        if vm_status != "RUNNING":
            return False, f"{vmid} is not running, no action."
        try:
            self.gce_client.stop_unary(project="yyyaaannn", zone=zone, instance=vmid)  # noqa: E501
            return True, f"shutting down {vmid}"
        except Exception as e:
            return False, f"shutting down {vmid} failed due to {str(e)}"

    def list_instances_azure(self):
        resource_groups = [
            x.get("resourcegroup", "") for x in self.vm_fleet
            if x.get("provider", "") == "Azure"
        ]
        out_list, n_running = [], 0

        for group in set(resource_groups):
            instance_list = self.ace_client.virtual_machines.list(group)
            for instance in instance_list:

                vm_status = self.ace_client.virtual_machines.get(
                    group, instance.name, expand='instanceView'
                ).instance_view.statuses[1].display_status
                out_list.append({
                    "vmid": str(instance.name),
                    "header": f"{instance.name} {vm_status.upper().replace(' ', '')} ({instance.location}) {instance.hardware_profile.vm_size}",  # noqa: E501
                    "state":vm_status,
                    "size": str(instance.hardware_profile.vm_size),
                    "note": "",
                    "content": dumps(str(instance)).replace(", '", ",<br/>'")[2:-2]  # noqa: E501
                })
                if vm_status == 'VM running':
                    n_running += 1

        return n_running, out_list

    def vm_startup_azure(self, vmid, resource_group):
        vm_status = self.ace_client.virtual_machines.get(
            resource_group, vmid, expand='instanceView'
        ).instance_view.statuses[1].display_status

        if vm_status == "VM running":
            return False, f"{vmid} is already active, no action"
        try:
            self.ace_client.virtual_machines.begin_start(resource_group, vmid)
            return True, f"restarting {vmid} (was {vm_status.upper().replace(' ', '')})"  # noqa: E501
        except Exception as e:
            return False, f"restart {vmid} failed due to {str(e)}"

    def vm_shutdown_azure(self, vmid, resource_group):
        vm_status = self.ace_client.virtual_machines.get(
            resource_group, vmid, expand='instanceView'
        ).instance_view.statuses[1].display_status
        # Azure: power off is billable, must be deallocated

        if vm_status != "VM running":
            return False, f"{vmid} is not running, no action"
        try:
            self.ace_client.virtual_machines.begin_deallocate(resource_group, vmid)  # noqa: E501
            return True, f"shutting down {vmid}"
        except Exception as e:
            logger.info(f"Completion noted: shutting down failed due to {str(e)}")  # noqa: E501
            return False, f"shutting down {vmid} failed due to {str(e)}"

    def __get_aws_client(self, instance_id):
        # client is region-bind, so need to determine proper client
        the_zones = [
            x.get("zone", "") for x in self.vm_fleet
            if x.get("resourceId", "") == instance_id
        ]

        return aws_client(
            "ec2",
            region_name=the_zones[0],
            **self.aws_secrets
        )

    def list_instances_aws(self):
        instance_ids = [
            x.get("resourceId", "") for x in self.vm_fleet
            if x.get("provider", "") == "AWS"
        ]
        out_list, n_running = [], 0

        try:
            instance_list = [
                self.__get_aws_client(one_id).describe_instances(InstanceIds=[one_id])  # noqa: E501
                for one_id in instance_ids
            ]
            for instance_info in instance_list:
                instance = instance_info['Reservations'][0]['Instances'][0]
                out_list.append({
                    "vmid": str(instance['Tags'][0]['Value']),
                    "header": f"{instance['Tags'][0]['Value']} {instance['State']['Name'].upper()} ({instance['Placement']['AvailabilityZone']}) {instance['InstanceType']}",  # noqa: E501
                    "state": instance['State']['Name'],
                    "size": instance['InstanceType'],
                    "note": "",
                    "content": dumps(str(instance)).replace(", '", ",<br/>'")[2:-2]  # noqa: E501
                })
                if instance['State']['Name'] == 'running':
                    n_running += 1
        except Exception as e:
            logger.error(str(e))

        return n_running, out_list

    def vm_startup_aws(self, vmid, instance_id):
        ec2_client = self.__get_aws_client(instance_id)
        vm_status = ec2_client.describe_instances(InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]['State']['Name'].upper()  # noqa: E501

        if vm_status == "RUNNING":
            return False, f"{vmid} is already active, no action"
        try:
            ec2_client.start_instances(InstanceIds=[instance_id])
            return True, f"restarting {vmid} (was {vm_status.upper().replace(' ', '')})"  # noqa: E501
        except Exception as e:
            return False, f"starting {vmid} failed due to {str(e)}"

    def vm_shutdown_aws(self, vmid, instance_id):
        ec2_client = self.__get_aws_client(instance_id)
        vm_status = ec2_client.describe_instances(InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]['State']['Name'].upper()  # noqa: E501

        if vm_status != "RUNNING":
            return False, f"{vmid} is not running, no action"
        try:
            ec2_client.stop_instances(InstanceIds=[instance_id])
            return True, f"shutting down {vmid}"
        except Exception as e:
            return False, f"shutting down failed due to {str(e)}"

    def __default_vm_fleet(self):
        self.vm_fleet = [
            {
                "vmid": "ycrawl-9-csc",
                "provider": "CSC",
                "project": "yCrawl",
                "batchn": 8
            },
            {
                "vmid": "ycrawl-8-csc",
                "provider": "CSC",
                "project": "yCrawl",
                "batchn": 7
            },
            {
                "vmid": "ycrawl-7-csc",
                "provider": "CSC",
                "project": "yCrawl",
                "batchn": 6
            },
            {
                "vmid": "ycrawl-6r-nl",
                "provider": "Azure",
                "project": "yCrawl",
                "batchn": 5,
                "resourcegroup": "westeurope"
            },
            {
                "vmid": "ycrawl-5r-ie",
                "provider": "Azure",
                "project": "yCrawl",
                "batchn": 4,
                "resourcegroup": "northeurope"
            },
            {
                "vmid": "ycrawl-4-fr",
                "provider": "AWS",
                "project": "yCrawl",
                "batchn": 3,
                "resourceId": "i-07a9cb47522f26bf8",
                "zone": "eu-west-3b"
            },
            {
                "vmid": "ycrawl-3-se",
                "provider": "AWS",
                "project": "yCrawl",
                "batchn": 2,
                "resourceId": "i-05baaec0fe7fe4d66",
                "zone": "eu-north-1c"
            },
            {
                "vmid": "ycrawl-2-fi",
                "provider": "GCP",
                "project": "yCrawl",
                "batchn": 1,
                "zone": "europe-north1-b"
            },
            {
                "vmid": "ycrawl-1-pl",
                "provider": "GCP",
                "project": "yCrawl",
                "batchn": 0,
                "zone": "europe-central2-b"
            },
            {
                "vmid": "yan-us-server",
                "provider": "GCP",
                "project": "main",
                "batchn": 999,
                "zone": "us-east1-b"
            },
            {
                "vmid": "yan-main",
                "provider": "CSC",
                "project": "main",
                "batchn": 999
            },
            {
                "vmid": "yan-fi-v2",
                "provider": "GCP",
                "project": "transition",
                "batchn": 999,
                "zone": "europe-north1-c"
            }
        ]
