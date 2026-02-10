# Lab 6 — Advanced Ansible & CI/CD



## Refactor with Blocks & Tags

### Selective execution with `--tags`

```bash
ansible-playbook playbooks/provision.yml --tags "docker"
```

```bash
PLAY [Provision web servers] ***********************************************************************************************************************************

TASK [Gathering Facts] *****************************************************************************************************************************************
ok: [info-service]

TASK [common : Log package installation completion] ************************************************************************************************************
ok: [info-service] => {
    "msg": "Package installation block completed"
}

TASK [common : Create completion timestamp] ********************************************************************************************************************
changed: [info-service]

TASK [common : User management completed] **********************************************************************************************************************
ok: [info-service] => {
    "msg": "User management block finished"
}

TASK [docker : Docker role execution started] ******************************************************************************************************************
ok: [info-service] => {
    "msg": "Starting Docker role execution"
}

TASK [docker : Install Docker prerequisites] *******************************************************************************************************************
ok: [info-service]

TASK [docker : Add Docker GPG key] *****************************************************************************************************************************
ok: [info-service]

TASK [docker : Add Docker repository] **************************************************************************************************************************
ok: [info-service]

TASK [docker : Update apt cache after repository setup] ********************************************************************************************************
changed: [info-service]

TASK [docker : Install Docker packages] ************************************************************************************************************************
ok: [info-service]

TASK [docker : Install Docker Python SDK] **********************************************************************************************************************
ok: [info-service]

TASK [docker : Ensure Docker service is running] ***************************************************************************************************************
ok: [info-service]

TASK [docker : Add users to docker group] **********************************************************************************************************************
ok: [info-service] => (item=ubuntu)
ok: [info-service] => (item=ubuntu)

TASK [docker : Create docker-compose directory] ****************************************************************************************************************
ok: [info-service]

TASK [docker : Verify Docker installation] *********************************************************************************************************************
ok: [info-service]

TASK [docker : Display Docker version] *************************************************************************************************************************
ok: [info-service] => {
    "msg": "Docker version: Docker version 29.2.1, build a5c7197"
}

PLAY RECAP *****************************************************************************************************************************************************
info-service               : ok=16   changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```





```bash
ansible-playbook playbooks/provision.yml --skip-tags "common"
```

```bash
PLAY [Provision web servers] ***********************************************************************************************************************************

TASK [Gathering Facts] *****************************************************************************************************************************************
ok: [info-service]

TASK [docker : Docker role execution started] ******************************************************************************************************************
ok: [info-service] => {
    "msg": "Starting Docker role execution"
}

TASK [docker : Install Docker prerequisites] *******************************************************************************************************************
ok: [info-service]

TASK [docker : Add Docker GPG key] *****************************************************************************************************************************
ok: [info-service]

TASK [docker : Add Docker repository] **************************************************************************************************************************
ok: [info-service]

TASK [docker : Update apt cache after repository setup] ********************************************************************************************************
changed: [info-service]

TASK [docker : Install Docker packages] ************************************************************************************************************************
ok: [info-service]

TASK [docker : Install Docker Python SDK] **********************************************************************************************************************
ok: [info-service]

TASK [docker : Ensure Docker service is running] ***************************************************************************************************************
ok: [info-service]

TASK [docker : Add users to docker group] **********************************************************************************************************************
ok: [info-service] => (item=ubuntu)
ok: [info-service] => (item=ubuntu)

TASK [docker : Create docker-compose directory] ****************************************************************************************************************
ok: [info-service]

TASK [docker : Verify Docker installation] *********************************************************************************************************************
ok: [info-service]

TASK [docker : Display Docker version] *************************************************************************************************************************
ok: [info-service] => {
    "msg": "Docker version: Docker version 29.2.1, build a5c7197"
}

PLAY RECAP *****************************************************************************************************************************************************
info-service               : ok=13   changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```





```bash
ansible-playbook playbooks/provision.yml --tags "packages"
```

```bash
PLAY [Provision web servers] ***********************************************************************************************************************************

TASK [Gathering Facts] *****************************************************************************************************************************************
ok: [info-service]

TASK [common : Update apt cache] *******************************************************************************************************************************
ok: [info-service]

TASK [common : Install common packages] ************************************************************************************************************************
ok: [info-service]

TASK [common : Upgrade system packages] ************************************************************************************************************************
skipping: [info-service]

TASK [common : Log package installation completion] ************************************************************************************************************
ok: [info-service] => {
    "msg": "Package installation block completed"
}

TASK [common : Create completion timestamp] ********************************************************************************************************************
changed: [info-service]

TASK [common : User management completed] **********************************************************************************************************************
ok: [info-service] => {
    "msg": "User management block finished"
}

TASK [docker : Install Docker packages] ************************************************************************************************************************
ok: [info-service]

PLAY RECAP *****************************************************************************************************************************************************
info-service               : ok=7    changed=1    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0 
```





```bash
ansible-playbook playbooks/provision.yml --tags "docker" --check
```

```bash
PLAY [Provision web servers] ***********************************************************************************************************************************

TASK [Gathering Facts] *****************************************************************************************************************************************
ok: [info-service]

TASK [common : Log package installation completion] ************************************************************************************************************
ok: [info-service] => {
    "msg": "Package installation block completed"
}

TASK [common : Create completion timestamp] ********************************************************************************************************************
changed: [info-service]

TASK [common : User management completed] **********************************************************************************************************************
ok: [info-service] => {
    "msg": "User management block finished"
}

TASK [docker : Docker role execution started] ******************************************************************************************************************
ok: [info-service] => {
    "msg": "Starting Docker role execution"
}

TASK [docker : Install Docker prerequisites] *******************************************************************************************************************
ok: [info-service]

TASK [docker : Add Docker GPG key] *****************************************************************************************************************************
ok: [info-service]

TASK [docker : Add Docker repository] **************************************************************************************************************************
ok: [info-service]

TASK [docker : Update apt cache after repository setup] ********************************************************************************************************
changed: [info-service]

TASK [docker : Install Docker packages] ************************************************************************************************************************
ok: [info-service]

TASK [docker : Install Docker Python SDK] **********************************************************************************************************************
ok: [info-service]

TASK [docker : Ensure Docker service is running] ***************************************************************************************************************
ok: [info-service]

TASK [docker : Add users to docker group] **********************************************************************************************************************
ok: [info-service] => (item=ubuntu)
ok: [info-service] => (item=ubuntu)

TASK [docker : Create docker-compose directory] ****************************************************************************************************************
ok: [info-service]

TASK [docker : Verify Docker installation] *********************************************************************************************************************
skipping: [info-service]

TASK [docker : Display Docker version] *************************************************************************************************************************
ok: [info-service] => {
    "msg": "Docker version: "
}

PLAY RECAP *****************************************************************************************************************************************************
info-service               : ok=15   changed=2    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
```





```bash
ansible-playbook playbooks/provision.yml --tags "docker_install"
```

```bash
PLAY [Provision web servers] ***********************************************************************************************************************************

TASK [Gathering Facts] *****************************************************************************************************************************************
ok: [info-service]

TASK [common : Log package installation completion] ************************************************************************************************************
ok: [info-service] => {
    "msg": "Package installation block completed"
}

TASK [common : Create completion timestamp] ********************************************************************************************************************
changed: [info-service]

TASK [common : User management completed] **********************************************************************************************************************
ok: [info-service] => {
    "msg": "User management block finished"
}

TASK [docker : Install Docker prerequisites] *******************************************************************************************************************
ok: [info-service]

TASK [docker : Add Docker GPG key] *****************************************************************************************************************************
ok: [info-service]

TASK [docker : Add Docker repository] **************************************************************************************************************************
ok: [info-service]

TASK [docker : Update apt cache after repository setup] ********************************************************************************************************
changed: [info-service]

TASK [docker : Install Docker packages] ************************************************************************************************************************
ok: [info-service]

TASK [docker : Install Docker Python SDK] **********************************************************************************************************************
ok: [info-service]

PLAY RECAP *****************************************************************************************************************************************************
info-service               : ok=10   changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0 
```

### List of all available tags

- app_user
- apt
- block_config
- block_install
- block_packages
- block_repository
- block_users
- common
- config
- containers
- debug
- directories
- docker
- docker_config
- docker_install
- gpg, hostname
- packages
- prerequisites
- python
- repository
- service
- ssh
- sudo
- system
- timezone
- upgrade
- users



## Upgrade to Docker Compose

### Docker Compose deployment success

```bash
--ask-vault-pass
```

```bash
PLAY [Deploy application] ********************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************
ok: [info-service]

TASK [docker : Install Docker prerequisites] *************************************************************************************************************************
ok: [info-service]

TASK [docker : Add Docker GPG key] ***********************************************************************************************************************************
changed: [info-service]

TASK [docker : Add Docker repository] ********************************************************************************************************************************
ok: [info-service]

TASK [docker : Update apt cache after repository setup] **************************************************************************************************************
changed: [info-service]

TASK [docker : Install Docker packages] ******************************************************************************************************************************
ok: [info-service]

TASK [docker : Install Docker Python SDK] ****************************************************************************************************************************
changed: [info-service]

TASK [docker : Ensure Docker service is running] *********************************************************************************************************************
changed: [info-service]

TASK [docker : Add users to docker group] ****************************************************************************************************************************
changed: [info-service] => (item=ubuntu)
changed: [info-service] => (item=appuser)

TASK [docker : Create docker-compose directory] **********************************************************************************************************************
changed: [info-service]

TASK [docker : Verify Docker installation] ***************************************************************************************************************************
ok: [info-service]

TASK [docker : Display Docker version] *******************************************************************************************************************************
ok: [info-service] => {
    "msg": "Docker version: Docker version 29.2.1, build a5c7197"
}

TASK [common : Update apt cache] *************************************************************************************************************************************
changed: [info-service]

TASK [common : Install common packages] ******************************************************************************************************************************
changed: [info-service]

TASK [common : Upgrade system packages] ******************************************************************************************************************************
skipping: [info-service]

TASK [common : Log package installation completion] ******************************************************************************************************************
ok: [info-service] => {
    "msg": "Package installation block completed"
}

TASK [common : Create completion timestamp] **************************************************************************************************************************
changed: [info-service]

TASK [common : Create application user] ******************************************************************************************************************************
changed: [info-service]

TASK [common : Ensure SSH directory exists for app user] *************************************************************************************************************
changed: [info-service]

TASK [common : Add users to sudo group] ******************************************************************************************************************************
skipping: [info-service]

TASK [common : User management completed] ****************************************************************************************************************************
ok: [info-service] => {
    "msg": "User management block finished"
}

TASK [common : Set timezone] *****************************************************************************************************************************************
changed: [info-service]

TASK [common : Configure hostname] ***********************************************************************************************************************************
changed: [info-service]

TASK [common : Configure SSH hardening] ******************************************************************************************************************************
ok: [info-service] => (item={'key': 'PasswordAuthentication', 'value': 'no'})
ok: [info-service] => (item={'key': 'PermitRootLogin', 'value': 'no'})
ok: [info-service] => (item={'key': 'ClientAliveInterval', 'value': '300'})

TASK [web_app : Login to Docker Hub] *********************************************************************************************************************************
ok: [info-service]

TASK [web_app : Pull Docker image] ***********************************************************************************************************************************
ok: [info-service]

TASK [web_app : Check if container exists] ***************************************************************************************************************************
ok: [info-service]

TASK [web_app : Stop existing container if running] ******************************************************************************************************************
changed: [info-service]

TASK [web_app : Remove old container if exists] **********************************************************************************************************************
changed: [info-service]

TASK [web_app : Create application directory] ************************************************************************************************************************
changed: [info-service]

TASK [web_app : Deploy application container] ************************************************************************************************************************
changed: [info-service]

TASK [web_app : Wait for application to start] ***********************************************************************************************************************
ok: [info-service]

TASK [web_app : Check application health endpoint] *******************************************************************************************************************
ok: [info-service]

TASK [web_app : Display health check result] *************************************************************************************************************************
ok: [info-service] => {
    "msg": "Application is healthy! Response: {'status': 'healthy', 'timestamp': '2026-02-10T13:06:04.889120+00:00', 'uptime_seconds': 13}"
}

TASK [Show running containers] ***************************************************************************************************************************************
changed: [info-service]

TASK [Display container status] **************************************************************************************************************************************
ok: [info-service] => {
    "msg": [
        "NAMES          IMAGE                              STATUS          PORTS",
        "info-service   scruffyscarf/info-service:latest   Up 17 seconds   0.0.0.0:8000->5000/tcp"
    ]
}

PLAY RECAP ***********************************************************************************************************************************************************
info-service               : ok=34   changed=19   unreachable=0    failed=0    skipped=2    rescued=0    ignored=0
```

### Idempotency

```bash
ansible-playbook playbooks/deploy.yml --ask-vault-pass
```

```bash
PLAY [Deploy application] ********************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************
ok: [info-service]

TASK [docker : Install Docker prerequisites] *************************************************************************************************************************
ok: [info-service]

TASK [docker : Add Docker GPG key] ***********************************************************************************************************************************
ok: [info-service]

TASK [docker : Add Docker repository] ********************************************************************************************************************************
ok: [info-service]

TASK [docker : Update apt cache after repository setup] **************************************************************************************************************
changed: [info-service]

TASK [docker : Install Docker packages] ******************************************************************************************************************************
ok: [info-service]

TASK [docker : Install Docker Python SDK] ****************************************************************************************************************************
ok: [info-service]

TASK [docker : Ensure Docker service is running] *********************************************************************************************************************
ok: [info-service]

TASK [docker : Add users to docker group] ****************************************************************************************************************************
ok: [info-service] => (item=ubuntu)
ok: [info-service] => (item=appuser)

TASK [docker : Create docker-compose directory] **********************************************************************************************************************
ok: [info-service]

TASK [docker : Verify Docker installation] ***************************************************************************************************************************
ok: [info-service]

TASK [docker : Display Docker version] *******************************************************************************************************************************
ok: [info-service] => {
    "msg": "Docker version: Docker version 29.2.1, build a5c7197"
}

TASK [common : Update apt cache] *************************************************************************************************************************************
ok: [info-service]

TASK [common : Install common packages] ******************************************************************************************************************************
ok: [info-service]

TASK [common : Upgrade system packages] ******************************************************************************************************************************
skipping: [info-service]

TASK [common : Log package installation completion] ******************************************************************************************************************
ok: [info-service] => {
    "msg": "Package installation block completed"
}

TASK [common : Create completion timestamp] **************************************************************************************************************************
changed: [info-service]

TASK [common : Create application user] ******************************************************************************************************************************
ok: [info-service]

TASK [common : Ensure SSH directory exists for app user] *************************************************************************************************************
ok: [info-service]

TASK [common : Add users to sudo group] ******************************************************************************************************************************
skipping: [info-service]

TASK [common : User management completed] ****************************************************************************************************************************
ok: [info-service] => {
    "msg": "User management block finished"
}

TASK [common : Set timezone] *****************************************************************************************************************************************
ok: [info-service]

TASK [common : Configure hostname] ***********************************************************************************************************************************
ok: [info-service]

TASK [common : Configure SSH hardening] ******************************************************************************************************************************
ok: [info-service] => (item={'key': 'PasswordAuthentication', 'value': 'no'})
ok: [info-service] => (item={'key': 'PermitRootLogin', 'value': 'no'})
ok: [info-service] => (item={'key': 'ClientAliveInterval', 'value': '300'})

TASK [web_app : Login to Docker Hub] *********************************************************************************************************************************
ok: [info-service]

TASK [web_app : Pull Docker image] ***********************************************************************************************************************************
ok: [info-service]

TASK [web_app : Check if container exists] ***************************************************************************************************************************
ok: [info-service]

TASK [web_app : Stop existing container if running] ******************************************************************************************************************
changed: [info-service]

TASK [web_app : Remove old container if exists] **********************************************************************************************************************
changed: [info-service]

TASK [web_app : Create application directory] ************************************************************************************************************************
ok: [info-service]

TASK [web_app : Deploy application container] ************************************************************************************************************************
changed: [info-service]

TASK [web_app : Wait for application to start] ***********************************************************************************************************************
ok: [info-service]

TASK [web_app : Check application health endpoint] *******************************************************************************************************************
ok: [info-service]

TASK [web_app : Display health check result] *************************************************************************************************************************
ok: [info-service] => {
    "msg": "Application is healthy! Response: {'status': 'healthy', 'timestamp': '2026-02-10T13:06:04.889120+00:00', 'uptime_seconds': 13}"
}

TASK [Show running containers] ***************************************************************************************************************************************
changed: [info-service]

TASK [Display container status] **************************************************************************************************************************************
ok: [info-service] => {
    "msg": [
        "NAMES          IMAGE                              STATUS          PORTS",
        "info-service   scruffyscarf/info-service:latest   Up 17 seconds   0.0.0.0:8000->5000/tcp"
    ]
}

PLAY RECAP ***********************************************************************************************************************************************************
info-service               : ok=34   changed=6    unreachable=0    failed=0    skipped=2    rescued=0    ignored=0
```

### Application running and accessible

```bash
curl http://localhost:8000/health
```

```bash
{"status":"healthy","timestamp":"2026-02-10T13:35:52.669019+00:00","uptime_seconds":1801}
```

### Contents of templated docker compose

```bash
docker-compose.yml.j2
```

```bash
version: '{{ compose_version }}'

services:
  {{ app_name }}:
    image: {{ docker_image }}:{{ docker_tag }}
    container_name: {{ app_name }}_{{ app_name }}
    hostname: {{ app_name }}
    
    ports:
      - "{{ app_port }}:{{ app_internal_port }}"
    
    environment:
      {% for key, value in app_environment.items() %}
      - {{ key }}={{ value }}
      {% endfor %}
      
      - APP_SECRET_KEY={{ app_secret_key | default('change_me_in_production') }}
    
    env_file:
      - .env
    
    volumes:
      - {{ data_volume }}:/app/data
      - {{ log_volume }}:/app/logs
      - ./config:/app/config:ro
    
    networks:
      - {{ network_name }}
    
    restart: {{ service_restart_policy }}
    
    healthcheck:
      test: {{ service_healthcheck.test | to_json }}
      interval: {{ service_healthcheck.interval }}
      timeout: {{ service_healthcheck.timeout }}
      retries: {{ service_healthcheck.retries }}
      start_period: {{ service_healthcheck.start_period }}
    
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
    
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    
    labels:
      - "maintainer=DevOps Team"
      - "version={{ app_version }}"
      - "description={{ app_description }}"

networks:
  {{ network_name }}:
    driver: {{ network_driver }}
    name: {{ network_name }}

volumes:
  {{ data_volume }}:
    name: {{ data_volume }}
  {{ log_volume }}:
    name: {{ log_volume }}

```



## Wipe Logic Implementation

### Output of Scenario 1

```bash
ansible-playbook playbooks/deploy.yml --ask-vault-pass
```

```bash
PLAY [Deploy application] ********************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************
ok: [info-service]

TASK [docker : Install Docker prerequisites] *************************************************************************************************************************
ok: [info-service]

TASK [docker : Add Docker GPG key] ***********************************************************************************************************************************
ok: [info-service]

TASK [docker : Add Docker repository] ********************************************************************************************************************************
ok: [info-service]

TASK [docker : Update apt cache after repository setup] **************************************************************************************************************
changed: [info-service]

TASK [docker : Install Docker packages] ******************************************************************************************************************************
ok: [info-service]

TASK [docker : Install Docker Python SDK] ****************************************************************************************************************************
ok: [info-service]

TASK [docker : Ensure Docker service is running] *********************************************************************************************************************
ok: [info-service]

TASK [docker : Add users to docker group] ****************************************************************************************************************************
ok: [info-service] => (item=ubuntu)
ok: [info-service] => (item=appuser)

TASK [docker : Create docker-compose directory] **********************************************************************************************************************
ok: [info-service]

TASK [docker : Verify Docker installation] ***************************************************************************************************************************
ok: [info-service]

TASK [docker : Display Docker version] *******************************************************************************************************************************
ok: [info-service] => {
    "msg": "Docker version: Docker version 29.2.1, build a5c7197"
}

TASK [common : Update apt cache] *************************************************************************************************************************************
ok: [info-service]

TASK [common : Install common packages] ******************************************************************************************************************************
ok: [info-service]

TASK [common : Upgrade system packages] ******************************************************************************************************************************
skipping: [info-service]

TASK [common : Log package installation completion] ******************************************************************************************************************
ok: [info-service] => {
    "msg": "Package installation block completed"
}

TASK [common : Create completion timestamp] **************************************************************************************************************************
changed: [info-service]

TASK [common : Create application user] ******************************************************************************************************************************
ok: [info-service]

TASK [common : Ensure SSH directory exists for app user] *************************************************************************************************************
ok: [info-service]

TASK [common : Add users to sudo group] ******************************************************************************************************************************
skipping: [info-service]

TASK [common : User management completed] ****************************************************************************************************************************
ok: [info-service] => {
    "msg": "User management block finished"
}

TASK [common : Set timezone] *****************************************************************************************************************************************
ok: [info-service]

TASK [common : Configure hostname] ***********************************************************************************************************************************
ok: [info-service]

TASK [common : Configure SSH hardening] ******************************************************************************************************************************
ok: [info-service] => (item={'key': 'PasswordAuthentication', 'value': 'no'})
ok: [info-service] => (item={'key': 'PermitRootLogin', 'value': 'no'})
ok: [info-service] => (item={'key': 'ClientAliveInterval', 'value': '300'})

TASK [web_app : Include wipe tasks] **********************************************************************************************************************************
included: /Users/scruffyscarf/DevOps-Core-Course/ansible/roles/web_app/tasks/wipe.yml for info-service

TASK [web_app : Wipe web application - confirmation check] ***********************************************************************************************************
skipping: [info-service]

TASK [web_app : Check if Docker Compose project exists] **************************************************************************************************************
ok: [info-service]

TASK [web_app : Stop and remove Docker Compose project] **************************************************************************************************************
skipping: [info-service]

TASK [web_app : Remove application directory] ************************************************************************************************************************
ok: [info-service]

TASK [web_app : Remove Docker images] ********************************************************************************************************************************
skipping: [info-service]

TASK [web_app : Verify wipe completion] ******************************************************************************************************************************
[ERROR]: Task failed: Action failed.
Origin: /Users/scruffyscarf/DevOps-Core-Course/ansible/roles/web_app/tasks/wipe.yml:65:7

63         - images
64
65     - name: Verify wipe completion
         ^ column 7

fatal: [info-service]: FAILED! => {"changed": false, "cmd": "docker ps -a --filter \"name=info-service\" --format \"{{.Names}}\"\n", "delta": "0:00:00.033141", "end": "2026-02-10 18:46:55.273423", "failed_when_result": true, "msg": "", "rc": 0, "start": "2026-02-10 18:46:55.240282", "stderr": "", "stderr_lines": [], "stdout": "info-service", "stdout_lines": ["info-service"]}

PLAY RECAP ***********************************************************************************************************************************************************
info-service               : ok=25   changed=2    unreachable=0    failed=1    skipped=5    rescued=0    ignored=0
```

### Output of Scenario 2

```bash
ansible-playbook playbooks/deploy.yml --ask-vault-pass \
  -e "web_app_wipe=true" \
  --tags web_app_wipe
```

```bash
PLAY [Deploy application] ********************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************
ok: [info-service]

TASK [common : Log package installation completion] ******************************************************************************************************************
ok: [info-service] => {
    "msg": "Package installation block completed"
}

TASK [common : Create completion timestamp] **************************************************************************************************************************
changed: [info-service]

TASK [common : User management completed] ****************************************************************************************************************************
ok: [info-service] => {
    "msg": "User management block finished"
}

TASK [web_app : Include wipe tasks] **********************************************************************************************************************************
included: /Users/scruffyscarf/DevOps-Core-Course/ansible/roles/web_app/tasks/wipe.yml for info-service

TASK [web_app : Wipe web application - confirmation check] ***********************************************************************************************************
ok: [info-service] => {
    "msg": "===========================================\nWIPE OPERATION INITIATED\n\nThis will remove:\n1. Docker containers for info-service\n2. Docker volumes for info-service\n3. Application directory: /opt/info-service\n4. Docker images (optional)\n\nWipe variable: true\nTag: web_app_wipe\n===========================================\n"
}

TASK [web_app : Check if Docker Compose project exists] **************************************************************************************************************
ok: [info-service]

TASK [web_app : Stop and remove Docker Compose project] **************************************************************************************************************
skipping: [info-service]

TASK [web_app : Remove application directory] ************************************************************************************************************************
ok: [info-service]

TASK [web_app : Remove Docker images] *********************************************************************************************************************
skipping: [info-service]

TASK [web_app : Verify wipe completion] ******************************************************************************************************************************
ok: [info-service]

TASK [web_app : Display wipe results] ********************************************************************************************************************************
ok: [info-service] => {
    "msg": "===========================================\nWIPE OPERATION COMPLETED\n\nCompose file existed: False\nDirectory removed: False\n\nRemaining containers:\nNone - all containers removed successfully\n\nApplication directory exists: False\n===========================================\n"
}

PLAY RECAP ***********************************************************************************************************************************************************
info-service               : ok=10   changed=1    unreachable=0    failed=0    skipped=2    rescued=0    ignored=0
```

### Output of Scenario 3

```bash
ansible-playbook playbooks/deploy.yml --ask-vault-pass \
  -e "web_app_wipe=true"
```

```bash
PLAY [Deploy application] ********************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************
ok: [info-service]

TASK [docker : Install Docker prerequisites] *************************************************************************************************************************
ok: [info-service]

TASK [docker : Add Docker GPG key] ***********************************************************************************************************************************
ok: [info-service]

TASK [docker : Add Docker repository] ********************************************************************************************************************************
ok: [info-service]

TASK [docker : Update apt cache after repository setup] **************************************************************************************************************
changed: [info-service]

TASK [docker : Install Docker packages] ******************************************************************************************************************************
ok: [info-service]

TASK [docker : Install Docker Python SDK] ****************************************************************************************************************************
ok: [info-service]

TASK [docker : Ensure Docker service is running] *********************************************************************************************************************
ok: [info-service]

TASK [docker : Add users to docker group] ****************************************************************************************************************************
ok: [info-service] => (item=ubuntu)
ok: [info-service] => (item=appuser)

TASK [docker : Create docker-compose directory] **********************************************************************************************************************
ok: [info-service]

TASK [docker : Verify Docker installation] ***************************************************************************************************************************
ok: [info-service]

TASK [docker : Display Docker version] *******************************************************************************************************************************
ok: [info-service] => {
    "msg": "Docker version: Docker version 29.2.1, build a5c7197"
}

TASK [common : Update apt cache] *************************************************************************************************************************************
ok: [info-service]

TASK [common : Install common packages] ******************************************************************************************************************************
ok: [info-service]

TASK [common : Upgrade system packages] ******************************************************************************************************************************
skipping: [info-service]

TASK [common : Log package installation completion] ******************************************************************************************************************
ok: [info-service] => {
    "msg": "Package installation block completed"
}

TASK [common : Create completion timestamp] **************************************************************************************************************************
changed: [info-service]

TASK [common : Create application user] ******************************************************************************************************************************
ok: [info-service]

TASK [common : Ensure SSH directory exists for app user] *************************************************************************************************************
ok: [info-service]

TASK [common : Add users to sudo group] ******************************************************************************************************************************
skipping: [info-service]

TASK [common : User management completed] ****************************************************************************************************************************
ok: [info-service] => {
    "msg": "User management block finished"
}

TASK [common : Set timezone] *****************************************************************************************************************************************
ok: [info-service]

TASK [common : Configure hostname] ***********************************************************************************************************************************
ok: [info-service]

TASK [common : Configure SSH hardening] ******************************************************************************************************************************
ok: [info-service] => (item={'key': 'PasswordAuthentication', 'value': 'no'})
ok: [info-service] => (item={'key': 'PermitRootLogin', 'value': 'no'})
ok: [info-service] => (item={'key': 'ClientAliveInterval', 'value': '300'})

TASK [web_app : Include wipe tasks] **********************************************************************************************************************************
included: /Users/scruffyscarf/DevOps-Core-Course/ansible/roles/web_app/tasks/wipe.yml for info-service

TASK [web_app : Wipe web application - confirmation check] ***********************************************************************************************************
ok: [info-service] => {
    "msg": "===========================================\nWIPE OPERATION INITIATED\n\nThis will remove:\n1. Docker containers for info-service\n2. Docker volumes for info-service\n3. Application directory: /opt/info-service\n4. Docker images (optional)\n\nWipe variable: true\nTag: web_app_wipe\n===========================================\n"
}

TASK [web_app : Check if Docker Compose project exists] **************************************************************************************************************
ok: [info-service]

TASK [web_app : Stop and remove Docker Compose project] **************************************************************************************************************
skipping: [info-service]

TASK [web_app : Remove application directory] ************************************************************************************************************************
ok: [info-service]

TASK [web_app : Remove Docker images] ********************************************************************************************************************************
skipping: [info-service]

TASK [web_app : Verify wipe completion] ******************************************************************************************************************************
ok: [info-service]

TASK [web_app : Display wipe results] ********************************************************************************************************************************
ok: [info-service] => {
    "msg": "===========================================\nWIPE OPERATION COMPLETED\n\nCompose file existed: False\nDirectory removed: False\n\nRemaining containers:\nNone - all containers removed successfully\n\nApplication directory exists: False\n===========================================\n"
}

TASK [web_app : Login to Docker Hub] *********************************************************************************************************************************
ok: [info-service]

TASK [web_app : Pull Docker image] ***********************************************************************************************************************************
ok: [info-service]

TASK [web_app : Check if container exists] ***************************************************************************************************************************
ok: [info-service]

TASK [web_app : Stop existing container if running] ******************************************************************************************************************
skipping: [info-service]

TASK [web_app : Remove old container if exists] **********************************************************************************************************************
ok: [info-service]

TASK [web_app : Create application directory] ************************************************************************************************************************
changed: [info-service]

TASK [web_app : Deploy application container] ************************************************************************************************************************
changed: [info-service]

TASK [web_app : Wait for application to start] ***********************************************************************************************************************
ok: [info-service]

TASK [web_app : Check application health endpoint] *******************************************************************************************************************
ok: [info-service]

TASK [web_app : Display health check result] *************************************************************************************************************************
ok: [info-service] => {
    "msg": "Application is healthy! Response: {'status': 'healthy', 'timestamp': '2026-02-10T16:23:37.762844+00:00', 'uptime_seconds': 12}"
}

TASK [Show running containers] ***************************************************************************************************************************************
changed: [info-service]

TASK [Display container status] **************************************************************************************************************************************
ok: [info-service] => {
    "msg": [
        "NAMES          IMAGE                              STATUS          PORTS",
        "info-service   scruffyscarf/info-service:latest   Up 16 seconds   0.0.0.0:8000->5000/tcp"
    ]
}

PLAY RECAP ***********************************************************************************************************************************************************
info-service               : ok=39   changed=5    unreachable=0    failed=0    skipped=5    rescued=0    ignored=0 
```

### Output of Scenario 4

```bash
ansible-playbook playbooks/deploy.yml --tags web_app_wipe
```

```bash
PLAY [Deploy application] ********************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************
ok: [info-service]

TASK [common : Log package installation completion] ******************************************************************************************************************
ok: [info-service] => {
    "msg": "Package installation block completed"
}

TASK [common : Create completion timestamp] **************************************************************************************************************************
changed: [info-service]

TASK [common : User management completed] ****************************************************************************************************************************
ok: [info-service] => {
    "msg": "User management block finished"
}

TASK [web_app : Include wipe tasks] **********************************************************************************************************************************
included: /Users/scruffyscarf/DevOps-Core-Course/ansible/roles/web_app/tasks/wipe.yml for info-service

TASK [web_app : Wipe web application - confirmation check] ***********************************************************************************************************
ok: [info-service] => {
    "msg": "===========================================\nWIPE OPERATION INITIATED\n\nThis will remove:\n1. Docker containers for info-service\n2. Docker volumes for info-service\n3. Application directory: /opt/info-service\n4. Docker images (optional)\n\nWipe variable: False\nTag: web_app_wipe\n===========================================\n"
}

TASK [web_app : Check if Docker Compose project exists] **************************************************************************************************************
ok: [info-service]

TASK [web_app : Stop and remove Docker Compose project] **************************************************************************************************************
skipping: [info-service]

TASK [web_app : Remove application directory] ************************************************************************************************************************
changed: [info-service]

TASK [web_app : Remove Docker images] ********************************************************************************************************************************
skipping: [info-service]

TASK [web_app : Verify wipe completion] ******************************************************************************************************************************
ok: [info-service]

TASK [web_app : Display wipe results] ********************************************************************************************************************************
ok: [info-service] => {
    "msg": "===========================================\nWIPE OPERATION COMPLETED\n\nCompose file existed: False\nDirectory removed: True\n\nRemaining containers:\ne765a2ecee53   scruffyscarf/info-service:latest   \"python app.py\"   4 minutes ago   Up 4 minutes   0.0.0.0:8000->5000/tcp   info-service\n\nApplication directory exists: False\n===========================================\n"
}

PLAY RECAP ***********************************************************************************************************************************************************
info-service               : ok=10   changed=2    unreachable=0    failed=0    skipped=2    rescued=0    ignored=0
```

### Application running after clean reinstall

```bash
curl http://localhost:8000/health
```

```bash
{"status":"healthy","timestamp":"2026-02-10T16:28:44.844433+00:00","uptime_seconds":319}
```

### Research

- Use both variable AND tag (Double safety mechanism)

**Safety and flexibility:** The variable (`web_app_wipe`) controls the logic, the tag (`web_app_wipe`) controls the execution. Double protection against accidental deletion:  must explicitly specify both the =true variable and the tag. This prevents accidental wipe during normal deployment.

- Difference between never tag and this approach

**`never` tag:** Tasks with the `never` tag are never performed automatically, only if `--tags never` is explicitly specified.  
**Approach:** Tasks are executed when `web_app_wipe=true` And the tag `web_app_wipe` is present. More controllable:  can run wipe without changing the playbook, just via `-e "web_app_wipe=true"'.

- Wipe logic come BEFORE deployment in main.yml (Clean reinstall scenario)

**Sequence of operations:** Wipe -> Deploy = clean reinstall. If wipe occurs after deployment, it will delete the newly deployed application. The "delete old -> install new" order is critical for the clean reinstallation scenario.

- Clean reinstallation vs. rolling update

**Clean reinstallation:**  
- Migration of versions with breaking changes  
- Correction of the corrupted state  
- Changing the application architecture  
- Testing from a clean state  

**Rolling update:**  
- Minor updates without downtime  
- Hotfixes in production  
- Saving state/data  
- Blue-green deployments

- Extend wipe Docker images and volumes

**Add tasks:**
```bash
- name: Clean unused Docker resources
  shell: docker system prune -af
```



## CI/CD with GitHub Actions

### 