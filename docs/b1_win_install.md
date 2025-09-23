# Prepare the environment

## Terraform provisioning
* Spin up an EC2 instance with Windows server 2022
* Ensure AWS SSM Agent is installed and running. 
* The EC2 instance needs to have an instance profile allowing Session Manager activities. SAP doesn't support all instance types availabe in AWS checkout the documentation and ensure using a supported one.

# silent install of components

`D:\hana-media\DATA_UNITS\SAP HANA STUDIO 2.0 FOR B1\NT_X64\SAP_HANA_STUDIO\hdbinst.exe -b --path="c:\Program files\SAP\hdbstudio`

`D:\hana-media\DATA_UNITS\SAP HANA CLIENT 2.0 FOR B1\NT_X64\SAP_HANA_CLIENT\hdbinst.exe -b --path="c:\Program files\SAP\hdbclient`

`D:\hana-media\DATA_UNITS\SAP HANA CLIENT 2.0 FOR B1\NT_I386\SAP_HANA_CLIENT\hdbinst.exe -b --path="c:\Program files (x86)\SAP\hdbclient`

# Handover to manual process

Run the manual installer for the b1 media

# Add license files

finally a license needs to be requested and applied to the instance