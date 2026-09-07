import streamlit as st
import json
import random

# Set Page Config
st.set_page_config(
    page_title="Nutanix NCP-MCI v6.10 备考模拟系统",
    page_icon="🟢",
    layout="wide"
)

# ── 数据集 (已内置 102 道真题、答案及技术解析) ──────────────────────────────
QUESTIONS = [
  {
    "num": 1,
    "question": "The team leads of a development environment want to limit developer access to a specific set of VMs What is the most efficient way to enable the team leads to directly manage these VMs?",
    "options": [
      "A. Create a Project for each team lead and assign access",
      "B. Create Security Policies to isolate users",
      "C. Create a VPC for each team lead and give them VPC Admin",
      "D. Create a role mapping for each team lead and assign appropriately"
    ],
    "answer": "A",
    "explanation": "Nutanix Projects in Prism Central provide a robust multi-tenant environment. By creating a Project for each team lead and assigning access, administrators can delegate direct management of a specific set of VMs to those team leads without exposing other project workloads.",
    "answer_clean": [
      "A"
    ],
    "is_multi": False
  },
  {
    "num": 2,
    "question": "What is supported for creating a VM Template?",
    "options": [
      "A. VM has disks located on RF2 containers",
      "B. VM is an agent or a Prism Central VM",
      "C. VM is protected by Protection Domain-based DR",
      "D. VM runs on the ESXi hypervisor"
    ],
    "answer": "A",
    "explanation": "Creating a VM template requires that the source VM's disks be placed on a storage container with a Replication Factor of 2 (RF2) or higher to ensure redundancy. Agent VMs, Prism Central VMs, and direct ESXi-managed VMs are not supported.",
    "answer_clean": [
      "A"
    ],
    "is_multi": False
  },
  {
    "num": 3,
    "question": "How can a VM of Volume Group (VG) be associated to a Storage Policy?",
    "options": [
      "A. Assign the Storage Policy directly on the VM or VG",
      "B. Assign the VM or VG directly on the Storage Policy",
      "C. Migrate the VM or VG to the Storage Container assigned to the Storage Policy",
      "D. Assign the VM or VG to the same Category as the Storage Policy"
    ],
    "answer": "D",
    "explanation": "Nutanix Storage Policies are applied at scale by leveraging Categories. Associating a VM or Volume Group (VG) with the target category instantly applies the rules managed by that Storage Policy.",
    "answer_clean": [
      "D"
    ],
    "is_multi": False
  },
  {
    "num": 4,
    "question": "What can be used to easily group a set of VMs?",
    "options": [
      "A. Labels",
      "B. Projects",
      "C. Tags",
      "D. Catalog Items"
    ],
    "answer": "A",
    "explanation": "Labels in Prism provide an easy, ad-hoc metadata grouping mechanism to filter and manage a collection of virtual machines, whereas Projects and Categories are used for more advanced RBAC and policy-driven control.",
    "answer_clean": [
      "A"
    ],
    "is_multi": False
  },
  {
    "num": 5,
    "question": "An administrator wants to live-migrate a vGPU-enabled VM from one host to another within the same cluster What requirements must be met before initiating the migration?",
    "options": [
      "A. The VM must be configured as an agent VM",
      "B. The vGPU profile needs to be changed",
      "C. The host affinity for the VM must be set to a specific host",
      "D. The target host has sufficient resources to support the VM"
    ],
    "answer": "D",
    "explanation": "For live-migrating a vGPU-enabled VM on AHV, the target physical host must have a compatible physical GPU and sufficient available vGPU slots/resources matching the VM's vGPU profile.",
    "answer_clean": [
      "D"
    ],
    "is_multi": False
  },
  {
    "num": 6,
    "question": "An administrator want to create a VM with memory overcommit features enabled in Nutanix environment Which statement best describes how the administrator will perform this VM creation?",
    "options": [
      "A. Memory overcommit can only be updated using the Prism Central console",
      "B. Memory overcommit can not be enabled for VM from the Prism Central console",
      "C. Memory overcommit can be enabled while creating a VM using Prism Element Web Console",
      "D. Memory overcommit can only be updated using the Prism Element Web Console once VM created"
    ],
    "answer": "A",
    "explanation": "AHV memory overcommit is configured and managed at the multi-cluster coordination level, which is why it can only be enabled or updated via the Prism Central console.",
    "answer_clean": [
      "A"
    ],
    "is_multi": False
  },
  {
    "num": 7,
    "question": "What guest customization options are available when creating a VM template?",
    "options": [
      "A. Custom Script - Guided Script",
      "B. Sysprep - Cloud-init",
      "C. Python - YAML",
      "D. Bash - Powershell"
    ],
    "answer": "B",
    "explanation": "Nutanix Guest Tools (NGT) and VM deployment leverage industry-standard customization tools: Sysprep for Windows operating systems and Cloud-init for Linux-based systems.",
    "answer_clean": [
      "B"
    ],
    "is_multi": False
  },
  {
    "num": 8,
    "question": "An administrator is tasked with optimizing a VM's storage to leverage compression features Currently, vDisks are in a storage container defaultcontainer-11111111111111 that has no optimization activated The administrator must move the VM's storage to the storage container Production What is the most efficient way to achieve this operation?",
    "options": [
      "A. Recreate VM in the Production storage container configuration and copy data",
      "B. Migrate VM to the Production storage container",
      "C. Recreate vDisk in the Production storage container configuration and copy data",
      "D. Migrate vDisks to the Production storage container"
    ],
    "answer": "D",
    "explanation": "The most efficient way to change the storage container of a VM's disks (vDisks) is to migrate the vDisks directly to the target storage container (Production) where compression is already active.",
    "answer_clean": [
      "D"
    ],
    "is_multi": False
  },
  {
    "num": 9,
    "question": "Which two entities can be categorized? (Choose two.)",
    "options": [
      "A. Alerts",
      "B. Storage Containers",
      "C. Virtual Machines",
      "D. ISO Images"
    ],
    "answer": "C, D",
    "explanation": "Categories in Prism Central can be assigned to multiple infrastructure entities. Virtual Machines and ISO Images can both be categorized to enforce backup, DR, security, and placement policies.",
    "answer_clean": [
      "C",
      "D"
    ],
    "is_multi": True
  },
  {
    "num": 10,
    "question": "An administrator has migrated a physical MySQL database from a legacy 3-Tier environment to a Nutanix cluster Post migration, the administrator finds that at peak load, the number of IOPS being generated is lower than expected, and latency is higher Which two steps should the administrator take to improve this behavior? (Choose two.)",
    "options": [
      "A. Create additional vDisks for SQL data",
      "B. Use LVM to stripe the SQL data across multiple vDisks",
      "C. Ensure that the SQL data vDisks are thin provisioned",
      "D. Ensure that the SQL data vDisks are thick provisioned"
    ],
    "answer": "A, B",
    "explanation": "MySQL and other database migrations to Nutanix perform best when I/O is parallelized. Creating multiple vDisks and striping them (e.g., using Logical Volume Manager in Linux) allows Nutanix's scale-out architecture to maximize IOPS and minimize latency.",
    "answer_clean": [
      "A",
      "B"
    ],
    "is_multi": True
  },
  {
    "num": 11,
    "question": "Which feature deploys a temporary VM to allow an administrator to login and apply OS patches to a VM template?",
    "options": [
      "A. Update Configuration",
      "B. Create VM from Template",
      "C. Update Guest OS",
      "D. Complete Guest OS Update"
    ],
    "answer": "C",
    "explanation": "The 'Update Guest OS' feature automatically deploys a temporary clone of the VM template, allowing the administrator to apply patches, and then seals and saves it back as the updated template.",
    "answer_clean": [
      "C"
    ],
    "is_multi": False
  },
  {
    "num": 12,
    "question": "An administrator needs to enable Windows Defender Credential Guard to comply with company policy New VM configurations desired by the company are:  Legacy BIOS  4 vCPU  8 GB Memory  Windows Server 2019 What must be changed in order to properly enable Windows Defender Credential Guard?",
    "options": [
      "A. Use Windows Server 2022",
      "B. Enable UEFI with Secure Boot",
      "C. Update vCPU to 8",
      "D. Update Memory to 16GB"
    ],
    "answer": "B",
    "explanation": "To run Windows Defender Credential Guard, the virtual machine must be configured with UEFI boot and Secure Boot enabled. Legacy BIOS is not supported for this security feature.",
    "answer_clean": [
      "B"
    ],
    "is_multi": False
  },
  {
    "num": 13,
    "question": "An administrator needs to create a storage container for VM disks The following conditions must be met for this container:  10 GiB of the total allocated space must not be used by other containers  The container must have a maximum storage capacity of 500 GiB What settings should the administrator configure while creating the storage container?",
    "options": [
      "A. Set Advertised Capacity to 10 GiB and Reserved Capacity to 500 GiB",
      "B. Set Advertised Capacity to 10 GiB",
      "C. Set Reserved Capacity to 500 GiB",
      "D. Set Reserved Capacity to 10 GiB and Advertised Capacity to 500 GiB"
    ],
    "answer": "D",
    "explanation": "To meet the criteria: Reserved Capacity is set to 10 GiB (guaranteeing that 10 GiB cannot be overcommitted), and Advertised Capacity is set to 500 GiB (limiting the maximum capacity of the storage container).",
    "answer_clean": [
      "D"
    ],
    "is_multi": False
  },
  {
    "num": 14,
    "question": "An administrator started an LCM upgrade of the AHV hosts and realized that the upgrades will continue beyond their planned maintenance window The administrator would like to prevent further updates at this point Which feature should be leveraged to prevent additional updates from occurring?",
    "options": [
      "A. Run the lcm_task_cleanup.py script",
      "B. Use the Stop Update feature in LCM",
      "C. Cancel the LCM tasks via the Ergon command line (ecli)",
      "D. Restart genesis on the cluster to restart the LCM service"
    ],
    "answer": "B",
    "explanation": "To prevent further software/firmware updates beyond a planned maintenance window without corrupting ongoing tasks, the administrator should leverage the graceful 'Stop Update' option in Life Cycle Manager.",
    "answer_clean": [
      "B"
    ],
    "is_multi": False
  },
  {
    "num": 15,
    "question": "Which two actions occur by default on a node which is placed in Maintenance Mode? (Choose two.)",
    "options": [
      "A. Non-migratable VMs are powered off",
      "B. Non-migratable VMs are powered off and restarted on other hosts in the cluster",
      "C. All eligible VMs on the host are powered off",
      "D. All eligible VMs on the host are migrated to other hosts in the cluster"
    ],
    "answer": "B, D",
    "explanation": "When an AHV host enters Maintenance Mode, eligible VMs are automatically live-migrated to other active hosts in the cluster, while non-migratable VMs (such as agent VMs or those with host affinity) are powered off.",
    "answer_clean": [
      "B",
      "D"
    ],
    "is_multi": True
  },
  {
    "num": 16,
    "question": "What is required to create a category?",
    "options": [
      "A. A name and a value",
      "B. A service and a scope",
      "C. A catalog and a template",
      "D. A policy and an entity"
    ],
    "answer": "A",
    "explanation": "A category is a Key-Value pair in Nutanix Prism Central, consisting of a key (name) and a value to group and enforce policies on various objects.",
    "answer_clean": [
      "A"
    ],
    "is_multi": False
  },
  {
    "num": 17,
    "question": "An administrator has been tasked with performing firmware upgrades for all their Nutanix sites When attempting to perform firmware upgrades via Life Cycle Manager (LCM) at a remote site with a single-node cluster deployed, no firmware updates are listed as being available The administrator confirmed the currently installed firmware is several revisions behind Why are there no firmware upgrades listed in LCM for this cluster?",
    "options": [
      "A. LCM does not have connectivity to the internet",
      "B. LCM cannot perform firmware upgrades on single-node clusters",
      "C. Single-node clusters only support one-click firmware upgrades",
      "D. LCM is not supported on single-node clusters"
    ],
    "answer": "A",
    "explanation": "If no updates are visible in LCM even though the local software is outdated, the most common cause is a lack of internet connectivity, preventing LCM from fetching the latest metadata catalog from the Nutanix portal.",
    "answer_clean": [
      "A"
    ],
    "is_multi": False
  },
  {
    "num": 18,
    "question": "Which task should be performed first when upgrading host memory?",
    "options": [
      "A. Execute \"shutdown -h now\" from the AHV command line interface",
      "B. Gracefully stop the host by using the out of band management interface",
      "C. Place node into the maintenance mode",
      "D. Remove node from the cluster"
    ],
    "answer": "C",
    "explanation": "Before performing physical hardware operations, such as adding memory, a node must be put into Maintenance Mode so that its VMs are safely evacuated to other nodes.",
    "answer_clean": [
      "C"
    ],
    "is_multi": False
  },
  {
    "num": 19,
    "question": "Which storage attributes do Storage Policies manage?",
    "options": [
      "A. Storage Containers and Volume Groups",
      "B. Replication Factor and Encryption",
      "C. Data protection and security",
      "D. Shares and Object stores"
    ],
    "answer": "B",
    "explanation": "Nutanix Storage Policies in Prism Central allow administrators to manage key storage attributes, specifically the Replication Factor (RF) and Encryption settings, at the VM level.",
    "answer_clean": [
      "B"
    ],
    "is_multi": False
  },
  {
    "num": 20,
    "question": "An administrator notices the message \"A newer version 2.7.1 of the framework is available\" when navigating to LCM from Prism Central Which action should the administrator take to update LCM to the latest version?",
    "options": [
      "A. Run an AHV upgrade",
      "B. Run an AOS upgrade",
      "C. Perform an Inventory",
      "D. Download and install the latest LCM version from a CVM"
    ],
    "answer": "C",
    "explanation": "Performing an Inventory scan in LCM triggers a metadata synchronization, which discovers the latest available LCM framework and allows upgrading the local LCM components.",
    "answer_clean": [
      "C"
    ],
    "is_multi": False
  },
  {
    "num": 21,
    "question": "An administrator, using a dark site deployment for LCM, is attempting to upgrade to the latest BIOS After completing an inventory, the administrator is not seeing the expected BIOS version available for upgrade What is the most likely reason the latest BIOS is not shown?",
    "options": [
      "A. The latest compatibility bundle has not been uploaded",
      "B. The BMC version needs to be upgraded first to show the latest BIOS",
      "C. The dark site webserver is not accessible",
      "D. AOS needs to be upgraded first to show the latest BIOS"
    ],
    "answer": "A",
    "explanation": "In a dark site deployment (no internet access), LCM depends on manual uploads. If expected firmware/BIOS versions are missing after an inventory, the administrator must upload the latest compatibility bundle.",
    "answer_clean": [
      "A"
    ],
    "is_multi": False
  },
  {
    "num": 22,
    "question": "An administrator has been tasked with creating a new storage container named TestData The TestData storage container must meeting the following conditions:  The container needs to have a Replication Factor of 1 (RF1)  Inline Compression must be enabled  Deduplication must be disabled  The container must have a maximum storage capacity of 100 GiB How should the administrator complete this task?",
    "options": [
      "A. Log into Prism Element and create the storage container with an Advertised Capacity of 100",
      "B. Log into Prism Element and create the storage container",
      "C. Log into Prism Central and create the storage container with a Reserved Capacity of 100 GiB",
      "D. Log into Prism Central and create the storage container"
    ],
    "answer": "A, B",
    "explanation": "Replication Factor 1 (RF1) is a cluster-level and container-level property that must be enabled and configured by logging directly into Prism Element, with Advertised Capacity acting as the storage limit.",
    "answer_clean": [
      "A",
      "B"
    ],
    "is_multi": True
  },
  {
    "num": 23,
    "question": "What additional step is required for LCM to upgrade an AHV host that has GPUs?",
    "options": [
      "A. Create an agent VM on each host that has GPU drivers installed",
      "B. Run LCM in dark site mode so it can update AHV independently",
      "C. Update NCC to the latest version and re-run Inventory",
      "D. Use Direct Uploads to upload appropriate driver bundles"
    ],
    "answer": "D",
    "explanation": "Upgrading host firmware or AHV components on GPU-equipped nodes requires manually uploading the GPU driver package to LCM using the Direct Uploads interface.",
    "answer_clean": [
      "D"
    ],
    "is_multi": False
  },
  {
    "num": 24,
    "question": "A security team asks an administrator to set up port mirroring of a specific source VM to a target VM What must the administrator ensure for this configuration to be possible?",
    "options": [
      "A. Source VM and Target VM are on the same subnet",
      "B. Source VM and Target VM are on the same host",
      "C. Source VM and Target VM are on the same VPC",
      "D. Source VM and Target VM are on the same VLAN"
    ],
    "answer": "B",
    "explanation": "AHV port mirroring utilizes local Open vSwitch (OVS) configurations, which restrict traffic capture to VMs running on the exact same physical host.",
    "answer_clean": [
      "B"
    ],
    "is_multi": False
  },
  {
    "num": 25,
    "question": "An administrator needs to apply a firmware upgrade to a host and wants to manually migrate VMs before executing an LCM upgrade All VMs but one are able to be live migrated Which action would fix the issue?",
    "options": [
      "A. Enable ADS (Acropolis Dynamic Scheduling) at cluster level",
      "B. Disable Agent VM within VM configuration options",
      "C. Update Link Layer Discovery Protocol (LLDP)",
      "D. Configure backplane portgroups that are assigned to CVM"
    ],
    "answer": "B",
    "explanation": "Agent VMs are pinned to their host by design to provide local cluster-level services. Disabling the 'Agent VM' flag is required before the VM can be live-migrated to another host.",
    "answer_clean": [
      "B"
    ],
    "is_multi": False
  },
  {
    "num": 26,
    "question": "In a scale-out Prism Central deployment what additional functionality does configuring an FQDN instead of a Virtual IP provide?",
    "options": [
      "A. Resiliency",
      "B. SSL Certificate",
      "C. Load balancing",
      "D. Segmentation"
    ],
    "answer": "C",
    "explanation": "Configuring a Fully Qualified Domain Name (FQDN) instead of a Virtual IP in scale-out Prism Central deployments enables DNS-based or external load balancers to distribute client requests across PC instances.",
    "answer_clean": [
      "C"
    ],
    "is_multi": False
  },
  {
    "num": 27,
    "question": "An administrator has been tasked by the company's leadership to justify and explain the decision to utilize the new Nutanix Disaster Recovery solution The environment contains:  100 workloads  Workloads have varying boot orders  Workloads span multiple subnets  Workloads span across different business units How should the administrator most efficiently organize and manage the workloads?",
    "options": [
      "A. Utilize a VM naming schema that allows sorting",
      "B. Utilize RESTful APIs to script creation of Recovery Plans",
      "C. Utilize a 1:10 ratio of Recovery-Plan to VMs",
      "D. Utilize Categories to organize VMs in Recovery Plans"
    ],
    "answer": "D",
    "explanation": "Nutanix Disaster Recovery recovery plans leverage Categories. By assigning VMs to categories, administrators can easily orchestrate large groups of workloads, boot orders, subnets, and failover targets.",
    "answer_clean": [
      "D"
    ],
    "is_multi": False
  },
  {
    "num": 28,
    "question": "An administrator is managing a 4-node cluster, based on intermixed hardware as follows:  Two G5 Nodes, 2 CPUs 12 Cores, 1 SSD 1.92 TB, 2 HHDs 4 TB  Two G7 Nodes, 2 CPUs 16 Cores, 2 SSD 1.92 TB, 4 HDDs, 4 TB G5 Nodes are going out of support and need to be replaced This cluster will be decommissioned from production and used for Disaster Recovery purposes with 1 hour RPO What is the supported configuration when swapping G5 nodes without compromising performance?",
    "options": [
      "A. New node must have at least 2 SSDs",
      "B. New node must be G7 or G8",
      "C. New node must have 2 CPUs with 12 cores",
      "D. New node must be hybrid"
    ],
    "answer": "A",
    "explanation": "To maintain optimal storage performance in a hybrid/all-flash intermixed cluster and prevent performance tier degradation, newly added nodes should have at least the same or greater solid-state drive (SSD) count as the existing nodes (G7 has 2 SSDs).",
    "answer_clean": [
      "A"
    ],
    "is_multi": False
  },
  {
    "num": 29,
    "question": "An administrator is responsible for resource planning and needs to plan for resiliency of a 10-node RF3 cluster The cluster has 100TB of storage How would the administrator plan for capacity in the event of future failures?",
    "options": [
      "A. Set Reserve Storage Capacity (%) to 20",
      "B. Set Reserve Memory Capacity (%) to 20",
      "C. Set Reserve Capacity For Failure to None",
      "D. Set Reserve Capacity For Failure to Auto Detect"
    ],
    "answer": "D",
    "explanation": "The most efficient way to ensure resiliency planning is to configure 'Reserve Capacity for Failure' to 'Auto Detect'. This allows the system to automatically compute and set aside the necessary compute and storage resources to tolerate host failures.",
    "answer_clean": [
      "D"
    ],
    "is_multi": False
  },
  {
    "num": 30,
    "question": "In an RF2 cluster, what is the minimum number of nodes required to allow a host removal?",
    "options": [
      "A. 2",
      "B. 3",
      "C. 4",
      "D. 5"
    ],
    "answer": "C",
    "explanation": "To safely remove a host in an RF2 cluster, the cluster must maintain at least 3 nodes post-removal to sustain RF2 metadata consensus. Thus, a minimum of 4 nodes is required to start the host removal process.",
    "answer_clean": [
      "C"
    ],
    "is_multi": False
  },
  {
    "num": 31,
    "question": "Which update in LCM can an administrator apply on a per-node basis?",
    "options": [
      "A. NCC",
      "B. AOS",
      "C. BMC",
      "D. AHV"
    ],
    "answer": "C",
    "explanation": "Out-of-band management controllers like the Baseboard Management Controller (BMC) can be updated individually on a per-node basis through LCM without impacting host clustering.",
    "answer_clean": [
      "C"
    ],
    "is_multi": False
  },
  {
    "num": 32,
    "question": "Due to application requirements, an administrator needs to modify an AHV VM in order to support a large number of distinct, concurrent connections The VM has the following configuration:  VCPUs: 4  RAM: 20 GB  Operating System: Microsoft Windows Server 2022 Which modification can the administrator make to improve network performance for network I/O-intensive applications running on this VM?",
    "options": [
      "A. Enabling AHV Turbo Technology",
      "B. Enabling RSS Virtio-Net Multi-Queue",
      "C. Adding more RAM",
      "D. Adding more VCPUs"
    ],
    "answer": "B",
    "explanation": "Receive Side Scaling (RSS) Virtio-Net Multi-Queue distributes incoming network traffic processing across multiple CPU cores, which is highly effective for high-performance and network-intensive applications on AHV VMs.",
    "answer_clean": [
      "B"
    ],
    "is_multi": False
  },
  {
    "num": 33,
    "question": "An administrator needs to configure NTP on Prism Central running on a Hyper-V cluster How should the administrator complete this task?",
    "options": [
      "A. Add a server with DNS hostname",
      "B. Add an external NTP server",
      "C. Add the DNS server IP",
      "D. Add the IP of the Domain Controller"
    ],
    "answer": "B",
    "explanation": "Time synchronization is vital. Nutanix recommends configuring Prism Central NTP settings with external, reliable NTP servers (IP addresses) rather than domain controllers or local DNS.",
    "answer_clean": [
      "B"
    ],
    "is_multi": False
  },
  {
    "num": 34,
    "question": "An administrator recently attempted to enable Data-in-Transit Encryption on a Scale-Out Prism Central cluster to ensure service level traffic is encrypted between the cluster nodes After attempting to enable this feature, the administrator noticed that it was not working correctly due to a firewall restriction Which CVM-specific port should be allowed through the firewall for Data-in-Transit Encryption?",
    "options": [
      "A. 2009",
      "B. 2010",
      "C. 2020",
      "D. 9440"
    ],
    "answer": "A",
    "explanation": "Port 2009 is the CVM-specific port that is used to encrypt and transport Data-in-Transit replication and synchronization traffic between Controller VMs.",
    "answer_clean": [
      "A"
    ],
    "is_multi": False
  },
  {
    "num": 35,
    "question": "An administrator is attempting to upgrade the NIC firmware on a Nutanix cluster and sees the error displayed in the exhibit Which log is the most appropriate to analyze the LCM precheck failure?",
    "options": [
      "A. lcm_wget.out",
      "B. catalog.out",
      "C. genesis.out",
      "D. lcm_ops.out"
    ],
    "answer": "D",
    "explanation": "The `lcm_ops.out` log file, located on the CVM, is the most appropriate log to review for details of LCM precheck operations, validations, and failures.",
    "answer_clean": [
      "D"
    ],
    "is_multi": False
  },
  {
    "num": 36,
    "question": "After upgrading Prism Central from pc.2022.1 to pc.2024.1, an administrator is unable to login to Prism Central with their IAM domain account What is the first thing the administrator should do?",
    "options": [
      "A. Login with a local admin account",
      "B. Ensure port 9441 is open in the firewall",
      "C. Validate trusted signing certificate of the organization",
      "D. Ping Domain Controller from CVM"
    ],
    "answer": "A",
    "explanation": "When IAM/Active Directory domain login fails after an upgrade, the first troubleshooting step is logging in with a local administrator account to check directory service and identity provider configuration.",
    "answer_clean": [
      "A"
    ],
    "is_multi": False
  },
  {
    "num": 37,
    "question": "An administrator would like to ensure that User VMs on their AHV hosts can take advantage of the bandwidth available beyond a single adapter in a bond Which uplink Bond Type should the administrator configure to accomplish this goal?",
    "options": [
      "A. Active-Active",
      "B. No Uplink Bond",
      "C. Active-Active With MAC pinning",
      "D. Active-Backup"
    ],
    "answer": "A, C",
    "explanation": "To aggregate bandwidth and allow User VMs to utilize network throughput beyond a single physical adapter's speed, the uplink bond type must be set to Active-Active (LACP).",
    "answer_clean": [
      "A",
      "C"
    ],
    "is_multi": True
  },
  {
    "num": 38,
    "question": "Which two URLs must be accessible from a Connected Site's Controller VMs in order to allow Life Cycle Manager (LCM) to download software updates? (Choose two.)",
    "options": [
      "A. my.nutanix.com",
      "B. release-api.nutanix.com",
      "C. download.nutanix.com",
      "D. portal.nutanix.com"
    ],
    "answer": "B, C",
    "explanation": "Prism Central/Prism Element LCM needs to reach `download.nutanix.com` (for downloading packages) and `release-api.nutanix.com` (to fetch metadata updates).",
    "answer_clean": [
      "B",
      "C"
    ],
    "is_multi": True
  },
  {
    "num": 39,
    "question": "When expanding a cluster, what is required to automatically discover nodes?",
    "options": [
      "A. New nodes have same hypervisor versions",
      "B. IPv6 multicast allowed on physical switches",
      "C. New nodes have same AOS versions",
      "D. IPv4 multicast allowed on physical switches"
    ],
    "answer": "B",
    "explanation": "During cluster expansion, Nutanix relies on IPv6 multicast (via mDNS) to automatically discover unconfigured nodes on the local physical network segment.",
    "answer_clean": [
      "B"
    ],
    "is_multi": False
  },
  {
    "num": 40,
    "question": "An administrator is trying to troubleshoot the environment after NCC raised an alert: \"Detailed information for remote_site_connectivity_check: Node x.x.x.x: WARN: Failed to connect to the remote site <remote_site>.\" Which two steps should an administrator follow to provide a solution? (Choose two.)",
    "options": [
      "A. If the remote site has been re-configured and the cluster has a new cluster incarnation ID,",
      "B. Confirm that the remote cluster is reachable, and ports 2009 and 2020 are open between the",
      "C. Check if ping packets with an MTU of 9000 reach the destination cluster",
      "D. Configure Network Address Translation performed by any device in between the two Nutanix clusters"
    ],
    "answer": "A, B",
    "explanation": "To resolve remote site connectivity warnings, verify physical network reachability on ports 2009/2020, and re-create the remote site mapping if a cluster reincarnation has occurred.",
    "answer_clean": [
      "A",
      "B"
    ],
    "is_multi": True
  },
  {
    "num": 41,
    "question": "An administrator is managing two clusters registered to two different Prism Central instances After configuring a Protection Policy for synchronous replication and verifying data replication, the administrator would like to create a new Recovery Plan with automatic failover However, the administrator finds that the Recovery Plan workflow offers only manual failure execution mode What configuration must be fixed to execute the failover automatically?",
    "options": [
      "A. Protection Policy must also have a local schedule",
      "B. Modify firewall to open 2030, 2036, 2073, 2090 ports on every local and remote CVMs",
      "C. Verify protected VM are not already part of another Recovery Plan",
      "D. Primary Location and Recovery Location must be in the same AZ"
    ],
    "answer": "D",
    "explanation": "In Nutanix Disaster Recovery (using Leap), automatic failover is only supported in a synchronous replication environment, which requires both the primary and recovery sites to be located within the same Availability Zone (AZ).",
    "answer_clean": [
      "D"
    ],
    "is_multi": False
  },
  {
    "num": 42,
    "question": "An administrator is trying to configure Metro Availability between Nutanix ESXi-based clusters However, the Compatible Remote Sites screen does not list all required storage containers Which two reasons could be a cause for this issue? (Choose two.)",
    "options": [
      "A. The destination storage container is not empty",
      "B. Source and destination hardware are from different vendors",
      "C. The remote site storage container has compression enabled",
      "D. Both storage containers must have the same name"
    ],
    "answer": "C, D",
    "explanation": "To enable Metro Availability replication between Nutanix ESXi clusters, the target storage container must have the exact same name as the source, and must not have conflict features like differing compression settings.",
    "answer_clean": [
      "C",
      "D"
    ],
    "is_multi": True
  },
  {
    "num": 43,
    "question": "An administrator wants to ensure that DR snapshots are protected from inadvertent or malicious deletion without notification What would be the best way to accomplish this?",
    "options": [
      "A. Create and Apply an Alert Policy",
      "B. Assign DR Admin Role to users",
      "C. Create and Apply an Approval Policy",
      "D. Create a Playbook to alert on event"
    ],
    "answer": "C",
    "explanation": "Approval Policies in Prism Central protect snapshots and administrative tasks from inadvertent or malicious actions by requiring secondary authorization before deletion.",
    "answer_clean": [
      "C"
    ],
    "is_multi": False
  },
  {
    "num": 44,
    "question": "An administrator is configuring a replication schedule on multiple remote locations deployed using a single-node cluster and would like to achieve the lowest RPO How should the administrator satisfy this requirement?",
    "options": [
      "A. Configure Async",
      "B. Configure NearSync",
      "C. Configure schedule for 16 minutes up to 59 minutes",
      "D. Configure schedule for one minute up to 15 minutes"
    ],
    "answer": "D",
    "explanation": "Nutanix NearSync provides the lowest RPO (1 to 15 minutes). Configuring a protection policy schedule within this range ensures the system uses NearSync replication.",
    "answer_clean": [
      "D"
    ],
    "is_multi": False
  },
  {
    "num": 45,
    "question": "An administrator is configuring Protection Policies to replicate VMs to a new Nutanix Cloud Cluster (NC2) connected via the Internet To comply with an organizational security policy, data sent via the Internet must be encrypted Which feature should be taken in account to be compliant?",
    "options": [
      "A. Enable Data-in-Transit Encryption",
      "B. Configure VMs to use UEFI secure boot",
      "C. Configure Data on a self encrypting drive",
      "D. Enable Data at Rest Encryption"
    ],
    "answer": "A",
    "explanation": "Data sent over the internet or untrusted networks must be encrypted. Enabling Data-in-Transit Encryption secures replicated storage traffic flowing between sites.",
    "answer_clean": [
      "A"
    ],
    "is_multi": False
  },
  {
    "num": 46,
    "question": "An administrator is protecting an application and its data stored on Volume Groups using protection domains During failover tests, all application VMs are restored successfully, however, the application data is completely missing In which two ways can the protection domain configuration be adjusted to avoid this issue in the future? (Choose two.)",
    "options": [
      "A. Place Volume Groups in a separate Protection Domain",
      "B. Use application consistent snapshots",
      "C. Manually add Volume Groups to Protected Entities",
      "D. Select the Auto protect related entities checkbox"
    ],
    "answer": "C, D",
    "explanation": "When protecting VMs with Volume Groups, you must either manually register the Volume Groups in the protection domain or check 'Auto protect related entities' to ensure they are replicated together.",
    "answer_clean": [
      "C",
      "D"
    ],
    "is_multi": True
  },
  {
    "num": 47,
    "question": "A Disaster Recovery administrator has setup a Protection Policy for 50 workloads - all configured in a similar fashion in terms of OS, storage, network, and performance The RPO is 60 minutes with a specified retention of 10 copies local, 5 copies remote, and crash consistency After configuring the Protection Policy and activating it, the administrator has noticed that recovery points are not showing up in DR Yet, everything within the Protection Policy looks correct and recovery points are showing up on production side What is the most likely issue?",
    "options": [
      "A. Nutanix NGT is not installed on the source VMs",
      "B. The storage container name of the protected VMs is not the same as the DR cluster storage container",
      "C. The storage container RF factor of the protected VMs is not the same as the RF factor in the DR cluster",
      "D. Windows updates need to be run on all the affected VMs"
    ],
    "answer": "A",
    "explanation": "For application-consistent snapshots to work and show recovery points at the DR site, Nutanix Guest Tools (NGT) must be installed and active in the guest operating system.",
    "answer_clean": [
      "A"
    ],
    "is_multi": False
  },
  {
    "num": 48,
    "question": "An administrator is working with a local network engineer to design the network architecture for a Disaster Recovery (DR) failover Because DNS is well designed and implemented, DR will utilize a different subnet from production To make the planning and execution easy to implement, the network engineer would like to utilize the same last octet in DR What is the best way to achieve this?",
    "options": [
      "A. Utilize Recovery Plan Offset-based IP mapping",
      "B. Utilize a custom script to update the IP address after instantiation in DR",
      "C. Log into the VMs after the DR event and update the IP address last octet",
      "D. Setup IPAM so the address can be dynamically assigned during DR"
    ],
    "answer": "A",
    "explanation": "Recovery Plan Offset-based IP mapping allows changing subnets during failover while keeping the last octet (host IP offset) identical, simplifying IP planning.",
    "answer_clean": [
      "A"
    ],
    "is_multi": False
  },
  {
    "num": 49,
    "question": "A company is evaluating Nutanix Disaster Recovery to protect multiple business-critical applications Some applications are built as 3-tier and have interdependencies An administrator has created a Protection Policy and Recovery Plan, added VMs, and defined all required network mappings After failover, the VM static IP address is retained However, DNS configuration is lost How should an administrator proceed?",
    "options": [
      "A. Configure a Protection Domain",
      "B. Configure Self-Service Restore",
      "C. Create custom in-guest scripts to preserve the statically assigned DNS IP addresses",
      "D. Install Network Manager command-line tool (nmcli) in the protected Windows VMs"
    ],
    "answer": "C",
    "explanation": "If VM static IP addresses are successfully retained during failover but DNS configuration is lost, custom in-guest pre/post scripts can be configured within the Recovery Plan to re-apply the correct DNS parameters.",
    "answer_clean": [
      "C"
    ],
    "is_multi": False
  },
  {
    "num": 50,
    "question": "An administrator is trying to delete a protected snapshot, but is unable to do so What is the most likely cause?",
    "options": [
      "A. The snapshot has been corrupted",
      "B. There is an active recovery occurring at that time",
      "C. There is an approval policy that was denied",
      "D. Ransomware has encrypted the snapshot"
    ],
    "answer": "B",
    "explanation": "Snapshots cannot be deleted if there is an active restoration or recovery operation actively reading or utilizing that snapshot.",
    "answer_clean": [
      "B"
    ],
    "is_multi": False
  },
  {
    "num": 51,
    "question": "A company is evaluating Nutanix DR to protect some business critical applications and tasked an administrator to find an optimal configuration providing highest resiliency and lowest RPO to the production environment The company's production environment is deployed on two physical sites with each hosting one AHV-based cluster What configuration will meet the company's requirements?",
    "options": [
      "A. Deploy Prism Central instance on one of the sites, configure Prism Central Disaster Recovery, and",
      "B. Deploy Prism Central instance on each site",
      "C. Configure Metro Availability using Protection Domains",
      "D. Deploy one Prism Central instance on each site and configure synchronous replication using"
    ],
    "answer": "D",
    "explanation": "For highest resiliency and lowest RPO, deploying one PC instance per site and leveraging synchronous replication via Protection Policies ensures zero-data-loss protection and site autonomy.",
    "answer_clean": [
      "D"
    ],
    "is_multi": False
  },
  {
    "num": 52,
    "question": "Deploy Prism Central instance on one of the sites Configure NearSync replication using Protection Domains An administrator has configured AHV Metro with Witness and wants to document different failover scenarios As a part of the failover tests, connection losses between these pairs were simulated:  Both the metro pair of clusters  Primary cluster and Prism Central However, Prism Central and the recovery cluster are still connected What are two expected system behaviors in this case? (Choose two.)",
    "options": [
      "A. Guest VMs continue to run on the primary cluster",
      "B. Guest VMs failover automatically to the recovery cluster",
      "C. Guest VM I/O operations pause (freeze) until the connectivity between the primary and recovery",
      "D. Guest VM I/O operations pause (freeze) until the connectivity between the primary and recovery"
    ],
    "answer": "A, D",
    "explanation": "In an AHV Metro environment with Witness, if connection is lost between the metro pair, VM IO will temporarily pause to prevent split-brain issues, while VMs continue running.",
    "answer_clean": [
      "A",
      "D"
    ],
    "is_multi": True
  },
  {
    "num": 53,
    "question": "An administrator configured a remote site for protection domain replication, but noticed that network performance and stability is impacted How can the remote site configuration be adjusted to fix the issue?",
    "options": [
      "A. Configure Network Address Translation between the two Nutanix clusters",
      "B. Configure Bandwidth Throttling Policy",
      "C. Configure Protection Domain with settings for many-to-many replication",
      "D. Configure remote Cluster VIP as proxy"
    ],
    "answer": "B",
    "explanation": "To resolve network performance issues and traffic impact during protection domain replication, setting a Bandwidth Throttling Policy limits replication traffic.",
    "answer_clean": [
      "B"
    ],
    "is_multi": False
  },
  {
    "num": 54,
    "question": "An administrator needs to setup a protection policy in preparation for a Disaster Recovery Test Which first step is required to satisfy this task?",
    "options": [
      "A. Convert the source cluster to AHV",
      "B. Create a recovery point of source VMs",
      "C. Create an Availability Zone between Production and DR",
      "D. Install NGT on VMs and assure that application consistent snapshots are supported"
    ],
    "answer": "C",
    "explanation": "To configure a protection policy and recovery plan for disaster recovery testing in Prism Central, the production and DR sites must first be registered as Availability Zones.",
    "answer_clean": [
      "C"
    ],
    "is_multi": False
  },
  {
    "num": 55,
    "question": "An administrator is responsible for Nutanix DR configuration and testing The administrator experiences a Recovery Plan Failure for a cross hypervisor (ESXi to AHV) DR Test The guest VMs do not recover at the DR location Which configuration is required for a successful event?",
    "options": [
      "A. Utilize delta disks",
      "B. Use raw device mappings",
      "C. Nutanix Guest Tools must be installed on source guest VMs",
      "D. Deploy Legacy BIOS boot on hosts within the cluster"
    ],
    "answer": "C",
    "explanation": "Cross-hypervisor DR (ESXi to AHV) requires Nutanix Guest Tools (NGT) installed on the source VMs to inject AHV VirtIO drivers during recovery at the target site.",
    "answer_clean": [
      "C"
    ],
    "is_multi": False
  },
  {
    "num": 56,
    "question": "An administrator has received complaints about VM performance After reviewing the VMs CPU Ready Time data shown in the exhibit, which step should the administrator take to diagnose the issue further?",
    "options": [
      "A. Check the number of vCPUs assigned to each CVM",
      "B. Enable VM memory oversubscription",
      "C. Assess cluster SSD capacity",
      "D. Review host CPU utilization"
    ],
    "answer": "D",
    "explanation": "High CPU Ready Time indicates VMs are waiting for CPU cycles. Reviewing host CPU utilization helps determine if the physical host processors are over-allocated or saturated.",
    "answer_clean": [
      "D"
    ],
    "is_multi": False
  },
  {
    "num": 57,
    "question": "An administrator is experiencing a storage problem on a single Microsoft Windows 2019 VMs configured as follows:  vCPU: 1  vRAM: 8  vSCSI: VirtIO SCSI Controller  vDisk: 2, first 100 GB, second 250 GB  vNIC: VirtIO Fast Ethernet The AHV cluster is healthy and other Windows VMs are performing much better Which configuration should be reviewed to enhance performances to the VM?",
    "options": [
      "A. Increase VM number of processors (vCPUs)",
      "B. Add a second virtual storage controller (vSCSI)",
      "C. Enable Balance TCP on bridge 0 (br0)",
      "D. Increase Controller VM (CVM) resources"
    ],
    "answer": "B",
    "explanation": "Adding multiple virtual storage controllers and spreading disks across them parallelizes I/O and enhances disk performance for high-throughput Windows VMs.",
    "answer_clean": [
      "B"
    ],
    "is_multi": False
  },
  {
    "num": 58,
    "question": "Due to application requirements, an administrator needs to support a multicast configuration in an AHV cluster Which AHV feature can be used to optimize network traffic such that multicast traffic is only forwarded to the VMs that need to receive it?",
    "options": [
      "A. Network Segmentation",
      "B. IGMP Snooping",
      "C. LLDP",
      "D. LACP"
    ],
    "answer": "B",
    "explanation": "IGMP Snooping is used in AHV networking to optimize multicast traffic by ensuring it is only forwarded to the ports/VMs that have actively subscribed to the multicast group.",
    "answer_clean": [
      "B"
    ],
    "is_multi": False
  },
  {
    "num": 59,
    "question": "A Linux VM provides services for multiple clients on a single large subnet The number of clients varies over time The clients consist of VMs and physical systems The administrator observed network performance problems on the Linux VM when going over 2,000 client connections Which action can be performed to mitigate the issue?",
    "options": [
      "A. Configure vNIC to operate in trunk mode",
      "B. Change VirtIO-Net vNIC to e1000 model",
      "C. Add multiple vNIC to the virtual machine",
      "D. Enable RSS VirtIO-Net Multi-Queue"
    ],
    "answer": "D",
    "explanation": "For a VM handling high numbers of concurrent client network connections, enabling RSS Virtio-Net Multi-Queue utilizes multiple vCPUs for network processing, resolving I/O bottlenecks.",
    "answer_clean": [
      "D"
    ],
    "is_multi": False
  },
  {
    "num": 60,
    "question": "An administrator needs to create two virtual machines: VM4 and VM5 that leverage the memory over-commit feature VM4 has the following configuration: 4 vCPU 32GB RAM Once VM4 is created and running, the administrator notices that it uses only 28GB of RAM What will be the maximum RAM that can be allocated to VM5 so that it can be powered on?",
    "options": [
      "A. 4GB",
      "B. 8GB",
      "C. 16GB",
      "D. 32GB"
    ],
    "answer": "B",
    "explanation": "Memory overcommit allows starting VMs. However, when VM4 uses 28GB of its 32GB allocation, 4GB remains unallocated. With overcommit, a maximum of 8GB can be safely allocated to VM5 to power on without starvation.",
    "answer_clean": [
      "B"
    ],
    "is_multi": False
  },
  {
    "num": 61,
    "question": "An administrator sees the alert: \"The cluster is using password bashed ssh access form the cvm ... Password-based remote login is enabled on the cluster It is recommended to use key-based ssh access instead of password-based ssh access for better security.\" What should the administrator do to ensure the nutanix user can no longer SSH to a CVM using a password?",
    "options": [
      "A. Rename the nutanix user",
      "B. Block port 22 on the CVM firewall",
      "C. Delete the nutanix user",
      "D. Enable Cluster Lockdown"
    ],
    "answer": "D",
    "explanation": "Enabling 'Cluster Lockdown' disables password-based SSH access to the CVMs and forces key-based authentication, fulfilling the security recommendation.",
    "answer_clean": [
      "D"
    ],
    "is_multi": False
  },
  {
    "num": 62,
    "question": "An administrator has successfully configured a Metro Availability protection domain After a couple of days the following NCC warning is raised: \"Detailed information for data_locality_check: Node x.x.x.20: WARN: Following VMs are accessing data from remote clusters VM-1 from remote cluster Remote-m1 Refer to KB 2093 for details on data_locality_check\" What is the first action an administrator must take to fix the issue?",
    "options": [
      "A. Run command ncli pd ls metro-avail-true |egnep “Protection Domain|Stretch|Role” |grep -B2 \"ACTIVE\" |",
      "B. Run command ncc health_checks metro_availability_checks data_locality_check --cvm_list=X.X.X.20",
      "C. Migrate the VM to its primary site and set appropriate rules for DRS and affinity",
      "D. Use \"must\" affinity rules to avoid automated VM migration to the standby datastore"
    ],
    "answer": "C",
    "explanation": "A data locality warning in Metro Availability indicates that a VM is running on the secondary site but accessing storage from the primary site. Migrating the VM back to the primary host restores data locality.",
    "answer_clean": [
      "C"
    ],
    "is_multi": False
  },
  {
    "num": 63,
    "question": "An administrator receives this alert: \"Storage Container <container_name> on cluster <cluster_name> will run out of storage resources in approximately 1 days.\" The cluster has plenty of space remaining Which configuration setting is causing the container to run out of space while the cluster has space remaining?",
    "options": [
      "A. Advertised Capacity is set too low",
      "B. Reserved Capacity is set too high",
      "C. Compression is set too low",
      "D. Replication Factor is set too high"
    ],
    "answer": "A",
    "explanation": "If a storage container reports running out of space while the physical cluster has ample space, the container's 'Advertised Capacity' (quota limit) was configured too low.",
    "answer_clean": [
      "A"
    ],
    "is_multi": False
  },
  {
    "num": 64,
    "question": "In a five-node cluster, an administrator noticed that three VMs are consuming too many resources on a single host Acropolis Dynamic Scheduling (ADS) is not able to migrate these VMs Which reason describes what is preventing ADS from migrating these VMs?",
    "options": [
      "A. VMs use external Network Attached Storage",
      "B. VMs use a Volume Group",
      "C. VM-VM anti-affinity policy is set",
      "D. VMs use GPU pass-through"
    ],
    "answer": "D",
    "explanation": "VMs using physical GPU pass-through are pinned to a specific host's hardware and cannot be live-migrated by Acropolis Dynamic Scheduling (ADS).",
    "answer_clean": [
      "D"
    ],
    "is_multi": False
  },
  {
    "num": 65,
    "question": "An administrator would like to ensure that VMs can be migrated and restarted on another node in the case of a single-host failure What action should be taken in Prism Element to meet this requirement?",
    "options": [
      "A. Configure an RF1 storage container",
      "B. Set Redundancy Factor to 3",
      "C. Configure a Protection Domain",
      "D. Enable HA Reservation"
    ],
    "answer": "D",
    "explanation": "Enabling HA Reservation in Prism Element guarantees that sufficient compute resources are set aside in the cluster to automatically restart VMs on surviving nodes during host failures.",
    "answer_clean": [
      "D"
    ],
    "is_multi": False
  },
  {
    "num": 66,
    "question": "An administrator observed an alert in Prism on a hybrid SSD/HDD cluster stating: Storage Pool SSD utilization consistently above 75% What is the potential impact of this condition?",
    "options": [
      "A. The cluster may be nearly out of storage for metadata",
      "B. The cluster is at risk of entering a read-only state",
      "C. Average IO latency in the cluster may increase",
      "D. The cluster is unable to sustain a SSD disk failure"
    ],
    "answer": "C",
    "explanation": "When SSD tier utilization exceeds 75%, hot data may spill over to the slower HDD tier (cold storage), resulting in higher average I/O latency for VM operations.",
    "answer_clean": [
      "C"
    ],
    "is_multi": False
  },
  {
    "num": 67,
    "question": "Which configuration option allows a VM to be powered on before the rest of the VMs when starting a host?",
    "options": [
      "A. Recovery Plan",
      "B. Host affinity",
      "C. High Availability",
      "D. Agent VM"
    ],
    "answer": "D",
    "explanation": "Configuring a VM as an 'Agent VM' ensures it is powered on first when a host starts up, before any user virtual machines are booted.",
    "answer_clean": [
      "D"
    ],
    "is_multi": False
  },
  {
    "num": 68,
    "question": "An administrator has been asked to calculate baseline Capacity Runway on a newly registered AHV cluster The cluster has been running for 16 days now, but no runway projections are being displayed Why are no Capacity Runway projections being displayed?",
    "options": [
      "A. Capacity Planning requires at least 3 months of data",
      "B. Capacity Planning requires at least 21 days of data",
      "C. Capacity Planning requires at least 30 days of data",
      "D. Capacity Planning requires at least 6 months of data"
    ],
    "answer": "C",
    "explanation": "Nutanix Intelligent Operations requires at least 30 days of historical cluster performance data to establish baselines and display accurate Capacity Runway projections.",
    "answer_clean": [
      "C"
    ],
    "is_multi": False
  },
  {
    "num": 69,
    "question": "After adding new workloads, why is Overall Runway below 365 days and the scenario still shows the cluster is in good shape?",
    "options": [
      "A. Because new workloads are sustainable",
      "B. Because Storage Runway is still good",
      "C. Because the Target is 1 month",
      "D. Because there are recommended resources"
    ],
    "answer": "B",
    "explanation": "The overall cluster runway can be affected by CPU or Memory, but if the storage space runway is still projected to be healthy, the capacity planning scenario will indicate the cluster is in good shape.",
    "answer_clean": [
      "B"
    ],
    "is_multi": False
  },
  {
    "num": 70,
    "question": "An administrator is experiencing performance issues within a VM and believes that more vCPU should be added to the specific VM The cluster as a whole appears to be performing well Which two metrics should be analyzed to determine if adding more vCPUs is warranted? (Choose two.)",
    "options": [
      "A. VM CPU Usage",
      "B. VM CPU Ready Time",
      "C. Host Memory Swap Out Rate",
      "D. Host CPU usage"
    ],
    "answer": "B, D",
    "explanation": "To justify adding vCPUs to a VM, analyze 'VM CPU Ready Time' (to check if the VM is waiting for physical CPU scheduling) and 'Host CPU usage' (to ensure physical cores are not fully saturated).",
    "answer_clean": [
      "B",
      "D"
    ],
    "is_multi": True
  },
  {
    "num": 71,
    "question": "The customer expects to maintain a cluster runway of 9 months The customer doesn't have budget for 6 months, but they want to add new workloads to the existing cluster Based on the exhibit, what is required to meet the customers budgetary time frame?",
    "options": [
      "A. Postpone the start of new workloads",
      "B. Add resources to the cluster",
      "C. Delete workloads running on the cluster",
      "D. Change the target to 9 months"
    ],
    "answer": "A",
    "explanation": "If there is no budget to add hardware resources within 6 months, postponing the start date of the new project workloads is required to maintain the targeted 9-month runway.",
    "answer_clean": [
      "A"
    ],
    "is_multi": False
  },
  {
    "num": 72,
    "question": "A user has created a report in the Intelligent Operations Analysis Dashboard, but forgot to download it However, after logging back into Prism Central, the administrator finds that the report is no longer available Which option explains this behavior?",
    "options": [
      "A. A user with Cluster Viewer role deleted the report",
      "B. The report is stored in the cluster's Prism Element",
      "C. Reports are automatically deleted after 24 hours",
      "D. The user-generated report was archived"
    ],
    "answer": "C",
    "explanation": "Prism Central generated reports are kept in the local history and by default are deleted after 24 hours if no retention policy is specified.",
    "answer_clean": [
      "C"
    ],
    "is_multi": False
  },
  {
    "num": 73,
    "question": "What feature allows receiving a weekly message about infrastructure Performance Summary?",
    "options": [
      "A. Admin Center Life Cycle Manager",
      "B. Prism Central syslog",
      "C. Infrastructrure VMs list",
      "D. Intelligent Operations Reports"
    ],
    "answer": "D",
    "explanation": "Intelligent Operations Reports allow scheduling and automating weekly infrastructure performance summaries sent directly via email.",
    "answer_clean": [
      "D"
    ],
    "is_multi": False
  },
  {
    "num": 74,
    "question": "A consultant is configuring syslog monitoring and wants to receive CRITICAL logs from the Audit module Which severity level setting should be configured to get the desired output?",
    "options": [
      "A. 0",
      "B. 2",
      "C. 5",
      "D. 7"
    ],
    "answer": "B",
    "explanation": "Syslog severity levels range from 0 to 7. Severity Level 2 (Critical) is the standard level for serious audit and system event logs.",
    "answer_clean": [
      "B"
    ],
    "is_multi": False
  },
  {
    "num": 75,
    "question": "An administrator wants to leverage VM Efficiency to clean up Inactive VMs The business requires that VMs have been powered off or have no measurable activity for 120 days before they are deleted A single Playbook was created to delete the Dead and Zombie VMs The administrator chose not to use a Branch Action The Playbook waits 99 days after VMs have been marked inactive before automatically deleting the Dead and Zombie VMs Which two responses show much time will have passed since the Dead and Zombie VMs were powered off or had no measurable activity before they are deleted? (Choose two.)",
    "options": [
      "A. For Dead VMs, the wait before deletion is 120 days",
      "B. For Zombie VMs, the wait before deletion is 129 days",
      "C. For Dead VMs, the wait before deletion is 129 days",
      "D. For Zombie VMs, the wait before deletion is 120 days"
    ],
    "answer": "A, B",
    "explanation": "A dead VM is inactive immediately. A Zombie VM has an extra verification period. Without branch actions, the waiting days are cumulative or set specifically by VM efficiency policies.",
    "answer_clean": [
      "A",
      "B"
    ],
    "is_multi": True
  },
  {
    "num": 76,
    "question": "An administrator is looking at the memory cluster runway diagram, as shown in the exhibit The environment is based on three hosts Each host is configured as follows:  CPU: 2x Intel Xeon Gold 8 cores at 2.6 GHz  RAM: 256 GB  Storage: 2x 1.92 GB SSD, 4 x 4 TB HDD The Intelligent Operations feature has been activated one month ago with no further configurations What does the dotted red line mean?",
    "options": [
      "A. It is the usable capacity based on cluster configuration options",
      "B. It is the maximum memory the administrator can assign to VMs",
      "C. It is the default trend analysis static threshold that can be manually set",
      "D. It is the calculated memory oversubscription limit for currently running VMs"
    ],
    "answer": "A",
    "explanation": "The dotted red line in runway diagrams represents the physical usable capacity boundary of the cluster after subtracting resiliency reservations (e.g. host rebuild capacity).",
    "answer_clean": [
      "A"
    ],
    "is_multi": False
  },
  {
    "num": 77,
    "question": "If an administrator creates a report with no retention policy configured, how many instances of the report are retained by default?",
    "options": [
      "A. 5",
      "B. 10",
      "C. 15",
      "D. 20"
    ],
    "answer": "B",
    "explanation": "In Prism Central, if no retention policy is explicitly configured for reports, the system retains a maximum of 10 instances of each report by default.",
    "answer_clean": [
      "B"
    ],
    "is_multi": False
  },
  {
    "num": 78,
    "question": "An administrator wants to enable application discovery on a Nutanix cluster to monitor applications An X-Large Prism Central instance is already configured and meets the licensing, CPU, and memory requirements Which two other prerequisites must be met before enabling application discovery? (Choose two.)",
    "options": [
      "A. Sufficient Prism Central VM resources",
      "B. Internet connection",
      "C. Network controller is enabled",
      "D. API key and key ID"
    ],
    "answer": "A, B",
    "explanation": "Enabling application discovery requires Prism Central to have internet connectivity to fetch signatures, and sufficient VM compute/memory resources to run the analytics engine.",
    "answer_clean": [
      "A",
      "B"
    ],
    "is_multi": True
  },
  {
    "num": 79,
    "question": "An administrator needs to create a single chart showing multiple storage bandwidth metrics a VM is consuming Which type of chart should the administrator create?",
    "options": [
      "A. Hypervisor Performance Chart",
      "B. Entity Chart",
      "C. Metric Chart",
      "D. VM Summary Chart"
    ],
    "answer": "B",
    "explanation": "An Entity Chart in Prism Central allows an administrator to plot and compare multiple different performance metrics for a single specific entity (such as a VM).",
    "answer_clean": [
      "B"
    ],
    "is_multi": False
  },
  {
    "num": 80,
    "question": "Which predefined view should be leveraged in Prism Central Intelligent Operations to determine which VM is consuming too many resources and causing other VMs to starve?",
    "options": [
      "A. Bully VMs List",
      "B. Constrained VMs List",
      "C. Overprovisioned VMs List",
      "D. Inactive VMs List"
    ],
    "answer": "A",
    "explanation": "The 'Bully VMs' view in Prism Central Intelligent Operations identifies resource-heavy VMs that are starving neighboring virtual machines of CPU or memory.",
    "answer_clean": [
      "A"
    ],
    "is_multi": False
  },
  {
    "num": 81,
    "question": "An administrator has deployed two Nutanix clusters and is now establishing synchronous replication between them However, the replication is failing immediately Which two responses show the reason and corrective action an administrator can take to resolve the issue? (Choose two.)",
    "options": [
      "A. If the primary and the recovery clusters are in different subnets, open the ports manually for",
      "B. If the primary and the recovery clusters are on the same subnet, open the ports manually for",
      "C. Use the command modify_firewall to open the ports on eth1 interface",
      "D. Use the command modify_firewall to open the ports on eth0 interface"
    ],
    "answer": "A, C",
    "explanation": "When replication fails immediately across subnets, ports must be opened manually, and if the backplane/secondary interface (eth1) is segmented, the firewall rules must be modified on eth1.",
    "answer_clean": [
      "A",
      "C"
    ],
    "is_multi": True
  },
  {
    "num": 82,
    "question": "An administrator manages multiple clusters at different geographic sites via a single Prism Central What should be configured to optimize image uploads to all locations?",
    "options": [
      "A. Image Placement Policy with Soft Enforcement",
      "B. Custom Image Upload Role",
      "C. Bandwidth Throttling Policy",
      "D. Image Placement Policy with Hard Enforcement"
    ],
    "answer": "A",
    "explanation": "Image Placement Policies with Soft Enforcement automatically replicate images across registered locations while allowing local overrides if bandwidth or storage is restricted.",
    "answer_clean": [
      "A"
    ],
    "is_multi": False
  },
  {
    "num": 83,
    "question": "An administrator is tasked with ensuring the resiliency of Tier-1 workloads As such, the administrator creates a Protection Policy with a crash-consistent snapshot period that meets RPO while maintaining 10 recovery points locally and 5 at DR location Since it is difficult to quantify how long a DR event will last, management wants the Tier-1 workloads to always have 10 recovery points locally How can this be achieved logically and most efficiently?",
    "options": [
      "A. Enable Reverse Retention within the Protection Policy Schedule",
      "B. Utilize a script that executes an API to take the required number of recovery points post-DR",
      "C. Post DR, recreate the Protection Policy with new/updated values",
      "D. Change retentions within the Protection Policy to be 10 at both locations and Save Schedule"
    ],
    "answer": "A",
    "explanation": "Enabling 'Reverse Retention' within the Protection Policy schedule ensures that local restore points are consistently maintained during a failover or disaster recovery event.",
    "answer_clean": [
      "A"
    ],
    "is_multi": False
  },
  {
    "num": 84,
    "question": "An administrator is receiving repeated approval requests to delete a protected snapshot that has already been approved What is the likely cause?",
    "options": [
      "A. There is an error with the SMTP server",
      "B. The Policy Engine wasn’t implemented",
      "C. The administrator is an approver on the approval policy",
      "D. There are multiple approvers on the approval policy"
    ],
    "answer": "C",
    "explanation": "If an administrator receives duplicate deletion approvals, it is usually because they are defined as a designated approver within the corresponding Prism Central approval policy.",
    "answer_clean": [
      "C"
    ],
    "is_multi": False
  },
  {
    "num": 85,
    "question": "What happens if an agent VM is powered off and then manually started on another host?",
    "options": [
      "A. Agent VM become unresponsive",
      "B. Agent VM cannot be migrated back to the original host",
      "C. Agent VM migrates back to the original host once it’s powered on",
      "D. Agent VM migrates to another host automatically"
    ],
    "answer": "C",
    "explanation": "AHV enforces host affinity for agent VMs. If an agent VM is manually started on another host, AHV will automatically live-migrate it back to its original host to preserve local services.",
    "answer_clean": [
      "C"
    ],
    "is_multi": False
  },
  {
    "num": 86,
    "question": "An administrator is managing an environment based on two different AHV-based and ESXi-based clusters Workloads are evenly distributed and in a healthy state A Linux VM running on ESXi is not performing well at the storage level and is configured as follows: vCPU: 8 VRAM: 32 vDisks: 3, first 100 GB, second 250 GB, third 260 GB What is the easiest way to test VM performance, while minimizing downtime?",
    "options": [
      "A. Increase the number of vCPUs",
      "B. Migrate the VM to the AHV cluster",
      "C. Enable vDisk sharding at AOS level",
      "D. Collapse the second and the third disk into a single one"
    ],
    "answer": "B",
    "explanation": "Migrating the guest VM from ESXi to AHV is the easiest way to test performance on the AHV native storage plane and utilize AHV Turbo features.",
    "answer_clean": [
      "B"
    ],
    "is_multi": False
  },
  {
    "num": 87,
    "question": "Which prerequisite should be met before any LCM updates are performed?",
    "options": [
      "A. Update AOS",
      "B. Update Foundation",
      "C. Update AHV",
      "D. Update BIOS"
    ],
    "answer": "B",
    "explanation": "Foundation is the installer tool in Nutanix. Upgrading Foundation to the latest version is a recommended prerequisite before applying LCM upgrades.",
    "answer_clean": [
      "B"
    ],
    "is_multi": False
  },
  {
    "num": 88,
    "question": "An administrator has been tasked with monitoring performance across a number of different entities in the Nutanix cluster The CIO has asked the administrator to provide Analysis charts that show performance as granularly as possible Given this request, what is the smallest preset time interval (in hours) that the administrator can select in a Metric or Entity Chart?",
    "options": [
      "A. 1",
      "B. 3",
      "C. 12",
      "D. 24"
    ],
    "answer": "A, C",
    "explanation": "Metric and Entity charts in Prism Central can display granular performance data down to a minimum preset interval of 1 hour.",
    "answer_clean": [
      "A",
      "C"
    ],
    "is_multi": True
  },
  {
    "num": 89,
    "question": "An administrator was tasked with configuring a Nutanix Disaster Recovery solution and has established synchronous replication between the sites For additional resiliency, each site is running its own Prism Central instance managing the local AHV cluster An administrator was notified that a failover is required for a planned datacenter maintenance on the primary site In which two ways should the administrator proceed? (Choose two.)",
    "options": [
      "A. Perform on-demand live migration between the clusters",
      "B. Conduct a planned failover from the standby site",
      "C. Conduct an unplanned failover from the primary site",
      "D. Conduct a planned failover from the primary site"
    ],
    "answer": "B, D",
    "explanation": "For scheduled data center maintenance, a planned failover gracefully replicates the latest changes and migrates workloads without data loss.",
    "answer_clean": [
      "B",
      "D"
    ],
    "is_multi": True
  },
  {
    "num": 90,
    "question": "Due to requirements from the network team, a Nutanix administrator must create User VMs on VLAN 10 on multiple AHV clusters What network configuration should the administrator consider in order to ensure consistent connectivity for User VMs on VLAN 10?",
    "options": [
      "A. Virtual Switch Configuration",
      "B. MTU",
      "C. MAC Address Prefix",
      "D. Bond Type"
    ],
    "answer": "A",
    "explanation": "When User VMs depend on specific VLAN tags (VLAN 10) across clusters, a consistent Virtual Switch configuration is required on all clusters to bridge traffic correctly.",
    "answer_clean": [
      "A"
    ],
    "is_multi": False
  },
  {
    "num": 91,
    "question": "An administrator has been tasked with developing a Prism Central Recovery Plan for 50 workloads that will be assigned new IP addresses and will need to utilize a new DNS server upon instantiation of workloads in the Disaster Recovery (DR) location What is the best way to accomplish this?",
    "options": [
      "A. Install Nutanix Guest Tools, this will allow Re-IP and automatically assign updated DNS",
      "B. Enable scripting within Recovery Sequence & utilize custom script per VM",
      "C. Utilize recovery Plan to bring VMs online at DR and then manually login to each VM and update IP",
      "D. Update DNS settings on production VMs prior to execution of Recovery Plan"
    ],
    "answer": "A",
    "explanation": "Nutanix Guest Tools (NGT) must be active inside the VMs to enable the orchestration engine to apply Re-IP configurations and inject new DNS settings in the DR site.",
    "answer_clean": [
      "A"
    ],
    "is_multi": False
  },
  {
    "num": 92,
    "question": "An administrator would like to create a Playbook where VM protection has failed for VMs in category: CriticalApps:Alerts The administrator needs to create an alert for only the VMs in the CriticalApps:Alerts category The alert must send a notification to the on-call personnel in the event that a VM Protection Failed Alert is triggered How should the administrator complete this task?",
    "options": [
      "A. Create a Playbook with a Manual trigger",
      "B. Create a Playbook with an Alert Matching Criteria trigger",
      "C. Create a Playbook with an Event-based trigger",
      "D. Create a Playbook with an Alert-based trigger"
    ],
    "answer": "D",
    "explanation": "An Alert-based trigger in Prism Playbooks allows capturing a specific failure alert (like VM Protection Failed) and automatically triggering a notification playbook.",
    "answer_clean": [
      "D"
    ],
    "is_multi": False
  },
  {
    "num": 93,
    "question": "A cluster has an RF3 storage container with many VMs Before the cluster runs out of space, the administrator has created a new RF2 storage container and would like to live migrate the vDisks Which check should be done before performing vDisk migration?",
    "options": [
      "A. Validate network latency is below 5 milliseconds",
      "B. Verify Multichannel Support is enabled",
      "C. Ensure storage optimization options match between storage containers",
      "D. Remove VMs from Protection Domains or Protection Policies"
    ],
    "answer": "D",
    "explanation": "Before migrating vDisks of protected VMs to a container with a different replication factor, they must be removed from protection domains to prevent snapshot replication metadata conflicts.",
    "answer_clean": [
      "D"
    ],
    "is_multi": False
  },
  {
    "num": 94,
    "question": "An administrator is planning for an upcoming maintenance window The administrator would like to minimize the chance of an upgrade failure during the maintenance window to ensure the updates will complete without issue What action should the administrator take to reduce the risk of any potential failures during an upgrade?",
    "options": [
      "A. Reboot each CVM one-at-a-time to ensure the reboots are successful",
      "B. Run an Upgrade Precheck from LCM",
      "C. Reboot each host one-at-a-time to ensure the reboots are successful",
      "D. Upgrade AOS to the latest version from LCM"
    ],
    "answer": "B",
    "explanation": "Running an LCM Upgrade Precheck evaluates cluster health, software compatibility, and network status, reducing the risk of failure during the maintenance window.",
    "answer_clean": [
      "B"
    ],
    "is_multi": False
  },
  {
    "num": 95,
    "question": "An administrator received a request to create a new storage container for persistent desktops Which storage optimization setting must the administrator set for the best possible capacity savings?",
    "options": [
      "A. Erasure Coding",
      "B. Inline compression with a delay of 0 minutes",
      "C. Inline Deduplication of Read Caches",
      "D. Post Process Deduplication"
    ],
    "answer": "B",
    "explanation": "For persistent VDI/desktops, inline compression with a 0-minute delay provides the highest capacity savings by compressing data immediately before it is written to disk.",
    "answer_clean": [
      "B"
    ],
    "is_multi": False
  },
  {
    "num": 96,
    "question": "An administrator is tasked with protection of a business critical application The application is running on a Linux VM and is using a custom DB that requires application-consistent snapshots for data integrity An administrator has written a pre_freeze and post_thaw scripts and placed them under /usr/local/sbin/ During protection domain scheduled run an alert is generated: Execution of the PostThaw Script Failed Which two resolution steps could an administrator conduct to fix the issue? (Choose two.)",
    "options": [
      "A. Ensure that scripts have nutanix user ownership and admin access",
      "B. Review the NGT logs under /usr/local/sbin/post_thaw",
      "C. Ensure NGT service is up and running",
      "D. Execute scripts manually and ensure they succeed"
    ],
    "answer": "C, D",
    "explanation": "If post_thaw script execution fails during consistent backup, check that the in-guest NGT daemon is active, and manually execute the scripts to troubleshoot syntax or execution issues.",
    "answer_clean": [
      "C",
      "D"
    ],
    "is_multi": True
  },
  {
    "num": 97,
    "question": "What happens when a VM is associated with multiple VM-Host affinity policies?",
    "options": [
      "A. The oldest policy is applied",
      "B. The newest policy takes precedence",
      "C. The VM is automatically removed from all policies",
      "D. All policies are applied simultaneously"
    ],
    "answer": "B",
    "explanation": "If a virtual machine is associated with multiple VM-Host affinity policies, conflict resolution rules specify that the newest policy takes precedence.",
    "answer_clean": [
      "B"
    ],
    "is_multi": False
  },
  {
    "num": 98,
    "question": "Within Intelligent Operations, Capacity Configurations have been set to Auto Detect for Reserve Capacity For Failure For an RF2 cluster with 10 nodes, what effect does this have on Capacity Runway?",
    "options": [
      "A. Reserves CPU, RAM and storage from the largest node to account for a single node failure",
      "B. Reserves 10% of CPU, memory and storage to account for a single node failure",
      "C. Reserves RAM and CPU from the fastest node to account for a single node failure",
      "D. Reserves storage and memory from the largest node to account for a single node failure"
    ],
    "answer": "D",
    "explanation": "Setting 'Reserve Capacity for Failure' to Auto Detect on a 10-node RF2 cluster reserves storage and compute resources equivalent to the largest node to survive a single node outage.",
    "answer_clean": [
      "D"
    ],
    "is_multi": False
  },
  {
    "num": 99,
    "question": "How can an administrator create a custom Intelligent Operations report, and run across multiple Prism Central instances?",
    "options": [
      "A. When creating the report, select the other Prism Central instances",
      "B. Export/import the report configuration in .rpt format",
      "C. Configure report sharing between Prism Central instances",
      "D. Manually recreate the report in each Prism Central instance"
    ],
    "answer": "B",
    "explanation": "To share and run custom Intelligent Operations reports across multiple independent Prism Central instances, export the configuration in `.rpt` format and import it into the other instances.",
    "answer_clean": [
      "B"
    ],
    "is_multi": False
  },
  {
    "num": 100,
    "question": "An administrator would like to plan for new project-related growth New project workload requirements have been included for a cluster named ClusterXYZ: 2 Medium Sized SQL Servers 10 VMs with 16GB RAM, 4 vCPU, 100GB Storage Which two additional information items should be added to the capacity planning scenario to provide a proper capacity runway expectation? (Choose two.)",
    "options": [
      "A. Storage compression ratio(s) for new workload",
      "B. Existing cluster hardware specifications",
      "C. Change in Demand percentage",
      "D. Date(s) workload(s) will be added"
    ],
    "answer": "A, D",
    "explanation": "When planning capacity runway, you must specify when the new workloads will be added and their estimated storage compression ratio to project accurate capacity depletion.",
    "answer_clean": [
      "A",
      "D"
    ],
    "is_multi": True
  },
  {
    "num": 101,
    "question": "An administrator is configuring a protection domain for business critical applications, including SQL, Oracle, and Exchange The administrator needs to evaluate the requirements and limitations for application-consistent snapshots What action should the administrator take while configuring application-consistent snapshots?",
    "options": [
      "A. Configure one consistency group for all VMs comprising an App",
      "B. Configure one consistency group for each VM",
      "C. Select application consistent snapshot checkbox in consistency group settings only",
      "D. Ensure that Windows VMs have in-guest mounted VHDX disks"
    ],
    "answer": "C",
    "explanation": "To take application-consistent snapshots, you must configure a consistency group containing the VMs and enable the 'application consistent snapshot' setting.",
    "answer_clean": [
      "C"
    ],
    "is_multi": False
  },
  {
    "num": 102,
    "question": "An administrator is executing a storage performance test between two Microsoft Windows VMs The first VM was deployed by using a template, while the second one was created from scratch Results show that VMs have very different metrics when using the same performance test The first VM reaches 8000 IOPS, while the second struggles reaching 500/800 IOPS Currently the AHV cluster is not under pressure How can the administrator determine why these results were produced?",
    "options": [
      "A. Compare vDisk bus type between VMs",
      "B. Enable AHV Turbo on the second VM",
      "C. Check number of vCPUs assigned to VMs",
      "D. Verify both VMs have installed Nutanix Guest Tools"
    ],
    "answer": "A",
    "explanation": "If a cloned VM achieves high IOPS but a manually built VM struggles, the difference is typically due to the disk bus controller type (e.g. high-performance VirtIO SCSI vs legacy SATA/IDE).",
    "answer_clean": [
      "A"
    ],
    "is_multi": False
  }
]

# ── 样式定制 ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        color: #002B49;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 800;
        margin-bottom: 5px;
    }
    .sub-header {
        color: #2CBA00;
        font-weight: 600;
        margin-bottom: 25px;
    }
    .q-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 8px;
        border-left: 5px solid #002B49;
        margin-bottom: 20px;
    }
    .opt-card {
        padding: 10px 15px;
        background-color: #ffffff;
        border: 1px solid #e9ecef;
        border-radius: 5px;
        margin-bottom: 8px;
    }
    .explanation-box {
        background-color: #fafdf6;
        border-left: 5px solid #2CBA00;
        padding: 15px;
        border-radius: 5px;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# ── 初始化 Session State & Cookie/LocalStorage 进度校验 ────────────────────────
if 'started' not in st.session_state:
    st.session_state.started = False
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}  # dict of index -> list of selected letters, e.g., {0: ["A"]}
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'quiz_pool' not in st.session_state:
    st.session_state.quiz_pool = []
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'practice_answered' not in st.session_state:
    st.session_state.practice_answered = set() # Set of indices answered in practice mode
if 'selected_mode' not in st.session_state:
    st.session_state.selected_mode = "📝 章节练习 (Practice)"

# 🆕 进度加载器：检测 URL 中的 progress 参数
import streamlit.components.v1 as components_v5
query_progress = st.query_params.get("progress")
if query_progress:
    try:
        st.session_state.last_saved_progress = int(query_progress)
    except ValueError:
        st.session_state.last_saved_progress = 1
elif "last_saved_progress" not in st.session_state:
    st.session_state.last_saved_progress = 1
    # 注入隐藏的 JS 脚本：如果本地 localStorage 存有进度，且 URL 中无 progress 参数，自动重定向父窗口以同步进度
    components_v5.html("""
    <script>
        try {
            const val = localStorage.getItem("ncp_mci_v4_progress");
            if (val && !window.parent.location.search.includes("progress=")) {
                const url = new URL(window.parent.location.href);
                url.searchParams.set("progress", val);
                window.parent.location.href = url.toString();
            }
        } catch (e) {
            console.error("读取本地进度失败:", e);
        }
    </script>
    """, height=0, width=0)

# ── 导航与页面布局 ────────────────────────────────────────────────────────
st.markdown("<h1 class='main-header'>🟢 Nutanix NCP-MCI v6.10 考试模拟器</h1>", unsafe_allow_html=True)
st.markdown("<h4 class='sub-header'>Nutanix Certified Professional - Multicloud Infrastructure 个人备考系统</h4>", unsafe_allow_html=True)

# ── 侧边栏设置 (仅在系统开始后作为一个快速控制和退出/重置区，避免配置功能在小屏幕下折叠找不到) ─────────────────
if st.session_state.started:
    st.sidebar.header("⚙️ 模拟器控制栏")
    st.sidebar.markdown(f"**当前模式：** {st.session_state.selected_mode}")
    if st.sidebar.button("🔄 退出并重置系统", use_container_width=True):
        st.session_state.started = False
        st.session_state.submitted = False
        st.rerun()

# ── 主体渲染 ─────────────────────────────────────────────────────────────
if not st.session_state.started:
    # 1. 考试说明卡片
    st.markdown("""
    <div class='q-card'>
        <h3>💡 备考系统说明</h3>
        <p>此模拟网页基于您的 NCP-MCI v6.10 PDF 题库开发，包含 102 道真实技术考题、高亮答案与深度技术架构解析。本系统提供以下两种学习模式：</p>
        <ul>
            <li><b>📝 章节练习模式 (Practice Mode)：</b>逐题进行练习。每答完一题即可提交并查看该题的正确答案及详细技术分析，适合边学边背、查漏补缺。</li>
            <li><b>🏆 模拟考试模式 (Mock Exam Mode)：</b>在无即时反馈的环境下一次性完成所有题目，答题结束后统一提交。系统会自动打分并为您归纳出所有<b>错题汇总与深度技术解析</b>。</li>
        </ul>
        <p><i>请在下方完成配置并点击【🚀 启动模拟系统】开始备考！</i></p>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. 将配置选项直接放在主页中心，防止移动端或窄屏下 sidebar 折叠导致用户找不到！
    st.markdown("### 🛠️ 第一步：系统初始化配置")
    setup_col1, setup_col2 = st.columns(2)
    with setup_col1:
        mode_select = st.radio(
            "📚 选择答题模式", 
            ["📝 章节练习 (Practice)", "🏆 模拟考试 (Mock Exam)"],
            help="章节练习：做一题对一题并即时展示官方技术解析。模拟考试：在无即时反馈下连续答题，提交后统一生成错题本。"
        )
    with setup_col2:
        shuffle_opt = st.checkbox(
            "🔀 随机打乱题目顺序", 
            value=True, 
            help="开启：打乱并随机抽取指定数量的题；关闭：可自定义选择顺序练习的题号区间（例如刷第20-50题，系统已自动定位您上次的进度）。"
        )
        if shuffle_opt:
            num_questions = st.slider(
                "❓ 随机抽取题目数量", 
                min_value=5, 
                max_value=len(QUESTIONS), 
                value=20, 
                help="默认抽取 20 道题，您可自由拖动滑块至最多 102 道全套题。"
            )
            range_opt = None
        else:
            # 🆕 自动应用上次进度
            default_start = st.session_state.get("last_saved_progress", 1)
            default_start = max(1, min(default_start, len(QUESTIONS)))
            default_end = min(default_start + 19, len(QUESTIONS))
            if default_end < default_start:
                default_end = len(QUESTIONS)
                
            range_opt = st.slider(
                "🎯 选择顺序练习的题号范围（从第几题到第几题）",
                min_value=1,
                max_value=len(QUESTIONS),
                value=(default_start, default_end),
                step=1,
                help=f"指定您要按顺序练习的题号区间。系统已为您自动将起点设为上次结束进度：第 {default_start} 题。"
            )
            num_questions = range_opt[1] - range_opt[0] + 1
        
    st.markdown("---")
    start_btn = st.button("🚀 启动模拟系统 (Start Exam)", type="primary", use_container_width=True)
    
    # 🆕 清除进度交互按钮
    if st.session_state.get("last_saved_progress", 1) > 1:
        st.write("")
        reset_progress_btn = st.button("🧹 清除历史进度 (从第 1 题重新开始)", use_container_width=True)
        if reset_progress_btn:
            st.session_state.last_saved_progress = 1
            st.query_params["progress"] = "1"
            components_v5.html("""
            <script>
                try {
                    localStorage.removeItem("ncp_mci_v4_progress");
                } catch (e) {
                    console.error("清除本地进度失败:", e);
                }
            </script>
            """, height=0, width=0)
            st.success("历史进度已清除，已恢复至第 1 题！")
            st.rerun()
            
    if start_btn:
        st.session_state.shuffle_opt = shuffle_opt
        if shuffle_opt:
            pool = list(range(len(QUESTIONS)))
            random.shuffle(pool)
            st.session_state.quiz_pool = pool[:num_questions]
        else:
            # 顺序抽取指定范围的题目
            start_idx = range_opt[0] - 1  # 题号转为 0-based 索引
            end_idx = range_opt[1]        # range_opt[1] 是包含的
            st.session_state.quiz_pool = list(range(start_idx, end_idx))
        st.session_state.selected_mode = mode_select
        st.session_state.started = True
        st.session_state.current_index = 0
        st.session_state.user_answers = {}
        st.session_state.submitted = False
        st.session_state.practice_answered = set()
        st.session_state.score = 0
        
        # 🆕 如果是顺序练习，启动时自动在 URL 中打上进度标记
        if mode_select == "📝 章节练习 (Practice)" and not shuffle_opt:
            initial_q_num = st.session_state.quiz_pool[0] + 1
            st.query_params["progress"] = str(initial_q_num)
            
        st.rerun()
else:
    mode = st.session_state.selected_mode
    pool_indices = st.session_state.quiz_pool
    current_q_idx = pool_indices[st.session_state.current_index]
    q_data = QUESTIONS[current_q_idx]
    
    # 🆕 自动保存进度到 Cookie/LocalStorage（仅在顺序章节练习模式下触发）
    if mode == "📝 章节练习 (Practice)" and not st.session_state.get("shuffle_opt", True):
        current_global_num = current_q_idx + 1
        st.session_state.last_saved_progress = current_global_num
        st.query_params["progress"] = str(current_global_num)
        
        # 写入浏览器 LocalStorage，防止会话丢失
        components_v5.html(f"""
        <script>
            try {{
                localStorage.setItem("ncp_mci_v4_progress", "{current_global_num}");
            }} catch (e) {{
                console.error("保存本地进度失败:", e);
            }}
        </script>
        """, height=0, width=0)
    
    total_q = len(pool_indices)
    curr_num = st.session_state.current_index + 1
    
    st.sidebar.markdown(f"**当前进度：** {curr_num} / {total_q} 题")
    st.sidebar.progress(curr_num / total_q)
    
    if mode == "📝 章节练习 (Practice)":
        # ── 练习模式 (逐题反馈) ──────────────────────────────────────────
        st.markdown(f"### 第 {curr_num} 题 / 共 {total_q} 题")
        
        # 渲染题目内容
        st.markdown(f"<div class='q-card'><b>[题目]</b> {q_data['question']}</div>", unsafe_allow_html=True)
        
        # 解析选项
        options_list = q_data['options']
        
        user_sel = []
        is_multi = q_data['is_multi']
        
        # 答题交互
        st.write("**请选择您的答案：** (Choose two 为多选题)" if is_multi else "**请选择您的答案：**")
        
        # 获取之前保存的答案
        saved_ans = st.session_state.user_answers.get(st.session_state.current_index, [])
        
        if is_multi:
            # 多选题，渲染复选框
            for opt in options_list:
                letter = opt[0] if len(opt) > 0 else ""
                checked = letter in saved_ans
                val = st.checkbox(opt, value=checked, key=f"p_check_{st.session_state.current_index}_{letter}")
                if val:
                    user_sel.append(letter)
        else:
            # 单选题，渲染单选框
            default_idx = None
            if saved_ans:
                for idx, opt in enumerate(options_list):
                    if opt[0] == saved_ans[0]:
                        default_idx = idx
                        break
            
            choice = st.radio(
                "请选择：", 
                options_list, 
                index=default_idx if default_idx is not None else 0,
                label_visibility="collapsed",
                key=f"p_radio_{st.session_state.current_index}"
            )
            if choice:
                user_sel = [choice[0]]
                
        st.session_state.user_answers[st.session_state.current_index] = user_sel
        
        # 提交按钮
        is_answered = st.session_state.current_index in st.session_state.practice_answered
        
        col1, col2 = st.columns([1, 4])
        with col1:
            submit_btn = st.button("🗳️ 提交并查看解析", disabled=is_answered, use_container_width=True)
            
        if submit_btn or is_answered:
            st.session_state.practice_answered.add(st.session_state.current_index)
            
            # 校验答案
            correct_set = set(q_data['answer_clean'])
            user_set = set(user_sel)
            
            correct_str = ", ".join(q_data['answer_clean'])
            
            if user_set == correct_set:
                st.success(f"🎉 恭喜！回答正确！(正确答案：{correct_str})")
            else:
                user_str = ", ".join(user_set) if user_set else "未作答"
                st.error(f"❌ 回答错误。您的选择：{user_str} | 正确答案：{correct_str}")
                
            # 显示解析
            st.markdown(f"""
            <div class='explanation-box'>
                <h5 style='color:#2CBA00;margin-top:0;'>💡 Nutanix 技术架构专家解析：</h5>
                <p>{q_data['explanation']}</p>
            </div>
            """, unsafe_allow_html=True)
            
        # 翻题按钮
        st.write("---")
        nav_col1, nav_col2, nav_col3 = st.columns([1, 1, 3])
        with nav_col1:
            if st.button("⬅️ 上一题", disabled=st.session_state.current_index == 0, use_container_width=True):
                st.session_state.current_index -= 1
                st.rerun()
        with nav_col2:
            if st.button("下一题 ➡️", disabled=st.session_state.current_index == total_q - 1, use_container_width=True):
                st.session_state.current_index += 1
                st.rerun()
                
    elif mode == "🏆 模拟考试 (Mock Exam)":
        # ── 模拟考试模式 (统一交卷) ──────────────────────────────────────
        if not st.session_state.submitted:
            st.markdown(f"### 第 {curr_num} 题 / 共 {total_q} 题")
            st.markdown(f"<div class='q-card'><b>[题目]</b> {q_data['question']}</div>", unsafe_allow_html=True)
            
            options_list = q_data['options']
            user_sel = []
            is_multi = q_data['is_multi']
            
            st.write("**请选择您的答案：** (Choose two 为多选题)" if is_multi else "**请选择您的答案：**")
            
            # 获取已经保存的值
            saved_ans = st.session_state.user_answers.get(st.session_state.current_index, [])
            
            if is_multi:
                for opt in options_list:
                    letter = opt[0] if len(opt) > 0 else ""
                    checked = letter in saved_ans
                    val = st.checkbox(opt, value=checked, key=f"m_check_{st.session_state.current_index}_{letter}")
                    if val:
                        user_sel.append(letter)
            else:
                default_idx = None
                if saved_ans:
                    for idx, opt in enumerate(options_list):
                        if opt[0] == saved_ans[0]:
                            default_idx = idx
                            break
                choice = st.radio(
                    "请选择：", 
                    options_list, 
                    index=default_idx if default_idx is not None else 0,
                    label_visibility="collapsed",
                    key=f"m_radio_{st.session_state.current_index}"
                )
                if choice:
                    user_sel = [choice[0]]
                    
            st.session_state.user_answers[st.session_state.current_index] = user_sel
            
            st.write("---")
            nav_col1, nav_col2, nav_col3 = st.columns([1, 1, 3])
            with nav_col1:
                if st.button("⬅️ 上一题", disabled=st.session_state.current_index == 0, use_container_width=True):
                    st.session_state.current_index -= 1
                    st.rerun()
            with nav_col2:
                if st.session_state.current_index == total_q - 1:
                    submit_exam = st.button("🏁 提交试卷", type="primary", use_container_width=True)
                    if submit_exam:
                        st.session_state.submitted = True
                        st.rerun()
                else:
                    if st.button("下一题 ➡️", use_container_width=True):
                        st.session_state.current_index += 1
                        st.rerun()
                        
            # 答题导航快速面板
            st.markdown("### 🗺️ 答题卡快速跳转")
            cols = st.columns(10)
            for idx, q_idx in enumerate(pool_indices):
                col_i = idx % 10
                is_answered = idx in st.session_state.user_answers and len(st.session_state.user_answers[idx]) > 0
                btn_label = f"{idx+1}"
                if idx == st.session_state.current_index:
                    style_type = "primary"
                else:
                    style_type = "secondary"
                    
                if cols[col_i].button(btn_label, key=f"nav_btn_{idx}", type=style_type, use_container_width=True):
                    st.session_state.current_index = idx
                    st.rerun()
        else:
            # ── 提交后的成绩结算页面 ──────────────────────────────────────────
            st.markdown("### 📊 模拟考试成绩报告")
            
            # 计算总得分
            correct_count = 0
            wrong_list = []
            
            for idx, q_idx in enumerate(pool_indices):
                orig_q = QUESTIONS[q_idx]
                user_ans = set(st.session_state.user_answers.get(idx, []))
                correct_ans = set(orig_q['answer_clean'])
                
                if user_ans == correct_ans:
                    correct_count += 1
                else:
                    wrong_list.append({
                        "num_label": idx + 1,
                        "orig_num": orig_q['num'],
                        "question": orig_q['question'],
                        "options": orig_q['options'],
                        "user_ans": ", ".join(user_ans) if user_ans else "未答",
                        "correct_ans": ", ".join(correct_ans),
                        "explanation": orig_q['explanation']
                    })
                    
            score_pct = (correct_count / total_q) * 100
            
            # 显示看板
            col_m1, col_m2, col_m3 = st.columns(3)
            col_m1.metric("答对题数", f"{correct_count} / {total_q} 题")
            col_m2.metric("得分率", f"{score_pct:.1f}%")
            
            is_passed = score_pct >= 50.0
            if is_passed:
                col_m3.success("🏆 通过考试 (PASS)")
            else:
                col_m3.error("❌ 未通过 (FAIL) — 需加油！")
                
            st.markdown("---")
            
            # 如果有错题，展示错题汇总和解析
            if len(wrong_list) > 0:
                st.markdown(f"### 🔍 错题本与专家解析 (共 {len(wrong_list)} 道错题)")
                st.write("请针对以下做错的题目进行专项深度强化复习：")
                
                for w in wrong_list:
                    with st.expander(f"第 {w['num_label']} 题（原卷第 {w['orig_num']} 题）：{w['question'][:80]}...", expanded=True):
                        st.markdown(f"**[完整问题]** {w['question']}")
                        st.write("**[选项]**")
                        for opt in w['options']:
                            st.write(f"- {opt}")
                            
                        # 用户选择与正确答案
                        w_col1, w_col2 = st.columns(2)
                        w_col1.markdown(f"❌ **您的答案：** `{w['user_ans']}`")
                        w_col2.markdown(f"✔ **正确答案：** `{w['correct_ans']}`")
                        
                        # 解析
                        st.markdown(f"""
                        <div class='explanation-box' style='margin-top:5px;'>
                            <h6 style='color:#2CBA00;margin-top:0;'>💡 Nutanix 官方技术解析：</h6>
                            <p>{w['explanation']}</p>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.balloons()
                st.success("🎉 太不可思议了！您完成了满分答卷！100% 正确！已完美掌握该阶段所有考点。")
                
            # 重新开始
            if st.button("🔄 重新开始新的考试", type="primary"):
                st.session_state.started = False
                st.session_state.submitted = False
                st.rerun()
