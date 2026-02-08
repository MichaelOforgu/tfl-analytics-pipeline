# Deploy RG and provision resources.
az deployment sub create \
    --location uksouth \
    --template-file ./infrastructure/bicep/main.bicep \
    --parameters ./infrastructure/parameters/dev.parameters.json