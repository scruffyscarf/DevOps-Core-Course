"""A Python Pulumi program"""

import pulumi
import pulumi_yandex as yc

# ======================
# CONFIG
# ======================

config = pulumi.Config()

cloud_id = config.require("cloud_id")
folder_id = config.require("folder_id")
ssh_public_key = config.require("ssh_public_key")
zone = "ru-central1-a"
ssh_cidr = "192.145.30.13/32"
vm_name = "info-service-vm"

# ======================
# PROVIDER
# ======================

provider = yc.Provider(
    "yc",
    cloud_id=cloud_id,
    folder_id=folder_id,
    zone=zone,
    service_account_key_file=config.get("serviceAccountKeyFile"),
)

# ======================
# NETWORK
# ======================

network = yc.VpcNetwork(
    "info-service-network",
    name="info-service-network",
    opts=pulumi.ResourceOptions(provider=provider),
)

subnet = yc.VpcSubnet(
    "info-service-subnet",
    name="info-service-subnet",
    zone=zone,
    network_id=network.id,
    v4_cidr_blocks=["10.0.0.0/24"],
    opts=pulumi.ResourceOptions(provider=provider),
)

# ======================
# SECURITY GROUP
# ======================

security_group = yc.VpcSecurityGroup(
    "info-service-security-group",
    name="info-service-security-group",
    network_id=network.id,
    ingresses=[
        yc.VpcSecurityGroupIngressArgs(
            protocol="TCP",
            port=22,
            v4_cidr_blocks=[ssh_cidr],
        ),
        yc.VpcSecurityGroupIngressArgs(
            protocol="TCP",
            port=80,
            v4_cidr_blocks=["0.0.0.0/0"],
        ),
        yc.VpcSecurityGroupIngressArgs(
            protocol="TCP",
            port=5000,
            v4_cidr_blocks=["0.0.0.0/0"],
        ),
    ],
    egresses=[
        yc.VpcSecurityGroupEgressArgs(
            protocol="ANY",
            v4_cidr_blocks=["0.0.0.0/0"],
        )
    ],
    opts=pulumi.ResourceOptions(provider=provider),
)

# ======================
# COMPUTE INSTANCE
# ======================

instance = yc.ComputeInstance(
    "info-service-vm",
    name=vm_name,
    zone=zone,
    resources=yc.ComputeInstanceResourcesArgs(
        cores=2,
        memory=1,
        core_fraction=20,
    ),
    boot_disk=yc.ComputeInstanceBootDiskArgs(
        initialize_params=yc.ComputeInstanceBootDiskInitializeParamsArgs(
            image_id="fd8i5gvlr8t2tcesgf2g",  # Ubuntu 22.04
            size=10,
        )
    ),
    network_interfaces=[
        yc.ComputeInstanceNetworkInterfaceArgs(
            subnet_id=subnet.id,
            nat=True,
            security_group_ids=[security_group.id],
        )
    ],
    metadata={
        "ssh-keys": f"ubuntu:{ssh_public_key}"
    },
    opts=pulumi.ResourceOptions(provider=provider),
)

# ======================
# OUTPUTS
# ======================

pulumi.export(
    "public_ip",
    instance.network_interfaces[0].nat_ip_address,
)
