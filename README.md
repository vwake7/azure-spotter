## Azure spotter
Convert OnDemand VMs to Spot VMs in Azure Virtual Machine Scalesets
1. Covers all Virtual Machine Scalesets within a Subscription, but that can be controlled with environment variable - CONVERT_TO_SPOT and tags 
2. For each VMSS, converts all OD VMs to Spot VMs except one OD VM
3. Azure credentials needs to be provided as environment variables
4. CONVERT_TO_SPOT variable can accept three values
   * ALL - This will convert all Virtual Machine Scaleset regardless of its tag 
   * TRUE - This will convert only Virtual Machine Scalesets with tag - convert_to_spot = True
   * FALSE - Virtual Machine Scalesets with tag convert_to_spot = False will be skipped, everything else will be converted
5. This task is scheduled to run every hour at the first minute

## Getting started using Docker
### 1. Clone the repo 
`git clone https://github.com/vwake7/azure-spotter`
      
### 2. Traverse to the azure-spotter directory
`cd azure-spotter`

### 3. Build the Docker image
 docker build -t azurespot-local-image .`

### 4. If you have another container running with the same name, delete it
 docker rm --force azurespot-local`

### 5. Run your docker image
```
 docker run -d --name azurespot-local \
-e AZURE_TENANT_ID="tenant_id" \
-e AZURE_CLIENT_ID="client_id" \
-e AZURE_CLIENT_SECRET="secret" \
-e AZURE_SUBSCRIPTION_ID="subscription_id" \
-e CONVERT_TO_SPOT="ALL" \
azurespot-local-image
```
<!-- 
## Contributing
Please read [CONTRIBUTING.md]() for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning
We use [SemVer](https://semver.org/) for versioning. For the versions available, see the tags on this repository.
-->
## License
This project is licensed under the Apache-2.0 License - see the [LICENSE](https://github.com/vwake7/azure-spotter/blob/main/LICENSE) file for details.

## Acknowledgments
* This project is built with [stackql](https://stackql.io/) as the IaC tool and this has helped to simplify the code to a great extent
* This project is inspired by [AutoSpotting](https://github.com/LeanerCloud/AutoSpotting)
