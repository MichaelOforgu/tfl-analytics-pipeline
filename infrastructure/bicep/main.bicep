targetScope = 'subscription'

@description('The Azure region where resources will be deployed')
param location string = 'uksouth'

@description('Environment name (e.g., dev, test, prod)')
param environment string = 'dev'

@description('Base name for resources')
param baseName string = 'analytics'

@description('Storage Account SKU')
@allowed([
  'Standard_LRS'
  'Standard_ZRS'
  'Standard_GRS'
])
param storageAccountSku string = 'Standard_LRS'

@description('Enable hierarchical namespace for ADLS Gen2')
param enableHierarchicalNamespace bool = true

@description('Databricks workspace pricing tier')
@allowed([
  'standard'
  'premium'
])
param databricksPricingTier string = 'premium'

@description('Enable public IP for Databricks')
param disablePublicIp bool = true

// Variables
var resourceGroupName = 'rg-${baseName}-${environment}'

// Create Resource Group
resource resourceGroup 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: resourceGroupName
  location: location
  tags: {
    Environment: environment
    ManagedBy: 'Bicep'
    Purpose: 'DataPlatform'
    Organization: 'TransportForLondon'
    Project: 'Analytics-Pipeline'
  }
}

// Deploy resources into the resource group using a module
module resources 'resources.bicep' = {
  name: 'resources-deployment'
  scope: resourceGroup
  params: {
    location: location
    environment: environment
    baseName: baseName
    storageAccountSku: storageAccountSku
    enableHierarchicalNamespace: enableHierarchicalNamespace
    databricksPricingTier: databricksPricingTier
    disablePublicIp: disablePublicIp
  }
}

// Outputs
output resourceGroupName string = resourceGroup.name
output storageAccountName string = resources.outputs.storageAccountName
output storageAccountPrimaryDfsEndpoint string = resources.outputs.storageAccountPrimaryDfsEndpoint
output dataFactoryName string = resources.outputs.dataFactoryName
output accessConnectorName string = resources.outputs.accessConnectorName
output accessConnectorId string = resources.outputs.accessConnectorId
output databricksWorkspaceName string = resources.outputs.databricksWorkspaceName
output databricksWorkspaceUrl string = resources.outputs.databricksWorkspaceUrl
