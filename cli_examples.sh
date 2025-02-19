#!/bin/zsh

# create the database account
az cosmosdb create --name mdwintertest4321 --kind GlobalDocumentDB --resource-group DataAcademyWinter2025

# list accounts (shows document endpoint uri)
az cosmosdb list -g DataAcademyWinter2025 -o table

# create the database
az cosmosdb sql database create --account-name mdwintertest4321 --name "iot" --resource-group DataAcademyWinter2025

# create the container
az cosmosdb sql container create --account-name mdwintertest4321 --database-name "iot" --name "monitoring" --partition-key-path "/id" --throughput 400 --resource-group DataAcademyWinter2025

# show the database keys
az cosmosdb keys list --name mdwintertest4321 --resource-group DataAcademyWinter2025

# show the database connection strings
az cosmosdb keys list --type connection-strings --name mdwintertest4321 --resource-group DataAcademyWinter2025