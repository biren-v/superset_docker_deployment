# Superset Docker Deployment

Apache Superset deployment configured for Azure Container Instances with PostgreSQL database and Redis cache.

## Repository Structure

```
superset_docker_deployment/
├── .env                    # Environment variables (not in repo - create from .env.example)
├── .env.example            # Template for environment variables
├── .gitignore             # Git ignore rules
├── Dockerfile             # Docker image configuration for Superset
├── docker-compose.yml     # Docker Compose configuration
├── entrypoint.sh          # Startup script for Superset container
├── requirements.txt       # Python dependencies (python-dotenv)
├── superset_config.py     # Superset configuration with env variables
└── README.md              # This file
```

## Prerequisites

- Azure CLI installed and configured
- Docker installed locally (for building images)
- Azure Container Registry (ACR)
- Azure PostgreSQL Database
- Azure Cache for Redis

## Environment Configuration

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Update `.env` with your actual values:
   ```env
   # Database Configuration
   DB_USER=your_postgres_username
   DB_PASSWORD=your_postgres_password
   DB_HOST=your-postgres-server.postgres.database.azure.com
   DB_PORT=5432
   DB_NAME=superset

   # Secret Key (generate a secure random key)
   SECRET_KEY=your_secret_key_here

   # Redis Configuration
   REDIS_HOST=your-redis.redis.cache.windows.net
   REDIS_PORT=6380
   REDIS_PASSWORD=your_redis_password
   REDIS_SSL=true
   ```

## Azure Container Instances Deployment

### Step 1: Build and Push Docker Image

1. Create an Azure Container Registry (if not exists):
   ```bash
   az acr create --resource-group myResourceGroup \
                 --name myregistryname \
                 --sku Basic
   ```

2. Login to ACR:
   ```bash
   az acr login --name myregistryname
   ```

3. Build the Docker image:
   ```bash
   docker build -t superset:latest .
   ```

4. Tag the image for ACR:
   ```bash
   docker tag superset:latest myregistryname.azurecr.io/superset:latest
   ```

5. Push to ACR:
   ```bash
   docker push myregistryname.azurecr.io/superset:latest
   ```

### Step 2: Create Azure Container Instance

1. Create a YAML deployment file `aci-deployment.yaml`:
   ```yaml
   apiVersion: 2021-07-01
   name: superset-container-group
   properties:
     containers:
     - name: superset
       properties:
         image: myregistryname.azurecr.io/superset:latest
         resources:
           requests:
             cpu: 2
             memoryInGb: 4
         ports:
         - port: 8088
         environmentVariables:
         - name: DB_USER
           value: "your_db_user"
         - name: DB_PASSWORD
           secureValue: "your_db_password"
         - name: DB_HOST
           value: "your-postgres.postgres.database.azure.com"
         - name: DB_PORT
           value: "5432"
         - name: DB_NAME
           value: "superset"
         - name: SECRET_KEY
           secureValue: "your_secret_key"
         - name: REDIS_HOST
           value: "your-redis.redis.cache.windows.net"
         - name: REDIS_PORT
           value: "6380"
         - name: REDIS_PASSWORD
           secureValue: "your_redis_password"
         - name: REDIS_SSL
           value: "true"
     osType: Linux
     ipAddress:
       type: Public
       ports:
       - protocol: tcp
         port: 8088
     imageRegistryCredentials:
     - server: myregistryname.azurecr.io
       username: myregistryname
       password: "registry_password"
   location: eastus
   ```

2. Deploy using Azure CLI:
   ```bash
   az container create --resource-group myResourceGroup \
                       --file aci-deployment.yaml
   ```

### Alternative: Deploy with Azure CLI directly

```bash
az container create \
    --resource-group myResourceGroup \
    --name superset-container \
    --image myregistryname.azurecr.io/superset:latest \
    --cpu 2 \
    --memory 4 \
    --port 8088 \
    --ip-address public \
    --registry-login-server myregistryname.azurecr.io \
    --registry-username myregistryname \
    --registry-password <registry-password> \
    --environment-variables \
        DB_HOST=your-postgres.postgres.database.azure.com \
        DB_PORT=5432 \
        DB_NAME=superset \
        REDIS_HOST=your-redis.redis.cache.windows.net \
        REDIS_PORT=6380 \
        REDIS_SSL=true \
    --secure-environment-variables \
        DB_USER=your_db_user \
        DB_PASSWORD=your_db_password \
        SECRET_KEY=your_secret_key \
        REDIS_PASSWORD=your_redis_password
```

### Step 3: Access Superset

1. Get the public IP address:
   ```bash
   az container show --resource-group myResourceGroup \
                     --name superset-container \
                     --query ipAddress.ip \
                     --output tsv
   ```

2. Access Superset at: `http://<public-ip>:8088`

3. Default login credentials:
   - Username: `admin`
   - Password: `admin`
   
   **Important**: Change the admin password immediately after first login.

## Configuration Details

### Superset Features Enabled
- Alert Reports
- Embedded Superset
- Dashboard Thumbnails (cached)
- Template Processing
- Native Dashboard Filters
- Dashboard Caching
- Chart Export

### Security Configuration
- CORS enabled for all origins (configure for production)
- Proxy fix enabled
- Session timeout: 1 hour (configurable via SESSION_TIMEOUT env var)

### Performance Configuration
- Redis caching for queries, dashboards, and filters
- High row limits for large datasets (1 billion rows)
- Configurable cache timeouts

## Monitoring and Logs

View container logs:
```bash
az container logs --resource-group myResourceGroup \
                  --name superset-container
```

Monitor container status:
```bash
az container show --resource-group myResourceGroup \
                  --name superset-container \
                  --query instanceView.state
```

## Scaling Considerations

For production deployments, consider:

1. **Azure Kubernetes Service (AKS)**: For better scaling and orchestration
2. **Azure Application Gateway**: For SSL termination and load balancing
3. **Azure Key Vault**: For secure secret management
4. **Managed Identity**: For secure access to Azure resources
5. **Azure Monitor**: For comprehensive logging and monitoring

## Troubleshooting

### Common Issues

1. **Container fails to start**: Check logs for database connection issues
2. **Redis connection errors**: Verify Redis SSL settings and firewall rules
3. **PostgreSQL connection failed**: Ensure PostgreSQL firewall allows Azure services

### Debug Commands

```bash
# Check container state
az container show --resource-group myResourceGroup \
                  --name superset-container \
                  --query instanceView.events

# Restart container
az container restart --resource-group myResourceGroup \
                     --name superset-container

# Delete and recreate container
az container delete --resource-group myResourceGroup \
                    --name superset-container --yes
```

## Security Best Practices

1. Never commit `.env` file to repository
2. Use Azure Key Vault for production secrets
3. Enable SSL/TLS for all connections
4. Configure network security groups appropriately
5. Regularly update Superset and dependencies
6. Use managed identities when possible
7. Enable Azure Defender for container security

## Support

For issues or questions:
- Check Superset documentation: https://superset.apache.org/
- Azure Container Instances docs: https://docs.microsoft.com/en-us/azure/container-instances/

## License

Apache License 2.0 (inherited from Apache Superset)