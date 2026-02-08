@description('The Azure region where resources will be deployed')
param location string

@description('Environment name')
param environment string

@description('Base name for resources')
param baseName string

@description('Storage Account SKU')
param storageAccountSku string

@description('Enable hierarchical namespace for ADLS Gen2')
param enableHierarchicalNamespace bool

@description('Databricks workspace pricing tier')
param databricksPricingTier string

@description('Enable public IP for Databricks')
param disablePublicIp bool

// Variables
var storageAccountName = toLower('st${baseName}${environment}${uniqueString(resourceGroup().id)}')
var adfName = toLower('adf-${baseName}-${environment}')
var accessConnectorName = toLower('ac-databricks-${baseName}-${environment}')
var databricksWorkspaceName = toLower('dbw-${baseName}-${environment}')
var managedResourceGroupName = 'databricks-rg-${databricksWorkspaceName}-${uniqueString(databricksWorkspaceName, resourceGroup().id)}'
var managedResourceGroupId = subscriptionResourceId('Microsoft.Resources/resourceGroups', managedResourceGroupName)
var storageBlobDataContributorRoleId = 'ba92f5b4-2d11-453d-a403-e96b0029c9fe'

// Create Storage Account
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: storageAccountSku
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
    isHnsEnabled: enableHierarchicalNamespace
  }
}

// Configure Settings for Blobs
resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2023-05-01' = {
  parent: storageAccount
  name: 'default'
  properties: {
    deleteRetentionPolicy: {
      enabled: true
      days: 7
    }
    containerDeleteRetentionPolicy: {
      enabled: true
      days: 7
    }
  }
}

// Create Data Factory
resource dataFactory 'Microsoft.DataFactory/factories@2018-06-01' = {
  name: adfName
  location: location
}

// Create Access Connector for Databricks
resource accessConnector 'Microsoft.Databricks/accessConnectors@2026-01-01' = {
  name: accessConnectorName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
}

// Create Databricks Workspace 
resource databricksWorkspace 'Microsoft.Databricks/workspaces@2023-02-01' = {
  name: databricksWorkspaceName
  location: location
  sku: {
    name: databricksPricingTier
  }
  properties: {
    managedResourceGroupId: managedResourceGroupId
    parameters: {
      enableNoPublicIp: {
        value: disablePublicIp
      }
    }
  }
  dependsOn: [
    accessConnector  // Ensure access connector is fully created first
  ]  
}

// Role Assignment for Storage Account
resource storageAccountRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(storageAccount.id, 'Storage Blob Data Contributor')
  scope: storageAccount
  properties: {
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      storageBlobDataContributorRoleId)
    principalId: accessConnector.identity.principalId
  }
  dependsOn: [
    databricksWorkspace  // Wait for Databricks to be fully created
  ]
}

// Outputs
output storageAccountName string = storageAccount.name
output storageAccountId string = storageAccount.id
output storageAccountPrimaryDfsEndpoint string = storageAccount.properties.primaryEndpoints.dfs
output dataFactoryName string = dataFactory.name
output accessConnectorName string = accessConnector.name
output accessConnectorId string = accessConnector.id
output databricksWorkspaceName string = databricksWorkspace.name
output databricksWorkspaceUrl string = databricksWorkspace.properties.workspaceUrl
