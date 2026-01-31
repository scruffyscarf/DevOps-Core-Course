# LAB02



## Docker Best Practices Applied

### Non-root User
The application runs inside the container using a non-root user instead of root. Running containers as root increases security risks. If the application is compromised, the attacker would gain elevated privileges inside the container. Using a non-root user limits the potential impact.

```bash
RUN adduser devopsuser
USER devopsuser
```

### Layer Caching

Dependencies are installed before copying the application source code. Docker caches image layers. When only application code changes, dependency layers are reused, which significantly speeds up rebuilds.

```bash
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```

### Minimal Base Image

A slim Python base image is used. Slim images reduce image size, build time, and attack surface while still providing the required runtime environment.

```bash
FROM python:3.13-slim
```

### .dockerignore
A `.dockerignore` file is used to exclude unnecessary files from the build context. Excluding files such as virtual environments, caches, and git metadata reduces build context size, speeds up builds, and prevents accidental inclusion of development artifacts.



## Image Information & Decisions

### Base Image Choice
Base image: `python:3.13-slim`. The image matches the Python version used locally, is smaller than full Python images, and is officially maintained.

### Final Image Size
The final image size is significantly smaller than a full Python image due to the use of a slim base image and exclusion of unnecessary files. This size is appropriate for production use.

### Layer Structure Explanation
1. Base Python image
2. Dependency installation layer
3. Application source code layer
4. Runtime configuration (non-root user, startup command)

### Optimization Choices
- Slim base image
- Proper layer ordering
- .dockerignore usage
- Non-root user execution



## Build & Run Process

### Image Build Output
```bash
docker build -t info-service .
```
```bash
View build details: docker-desktop://dashboard/build/desktop-linux/desktop-linux/ve0ypxkglj3os1i0cu5naitlc
```

### Running Container
```bash
docker run -p 5000:5000 info-service
```
```bash
* Serving Flask app 'app'
 * Debug mode: off
2026-01-31 18:28:21,077 [INFO] WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://172.17.0.2:5000
2026-01-31 18:28:21,077 [INFO] Press CTRL+C to quit
```

### Testing Endpoints

```bash
curl http://localhost:5000
```
```bash
{"service":{"name":"devops-info-service","version":"1.0.0","description":"DevOps course info service","framework":"net/http"},"system":{"hostname":"bd7afeeb7b00","platform":"linux","platform_version":"unknown","architecture":"amd64","cpu_count":8,"python_version":"python3.14"},"runtime":{"uptime_seconds":128,"uptime_human":"0 hour(s), 2 minute(s)","current_time":"2026-01-31T19:22:51Z","timezone":"UTC"},"request":{"client_ip":"172.17.0.1:59016","user_agent":"curl/8.7.1","method":"GET","path":"/"},"endpoints":[{"path":"/","method":"GET","description":"Service information"},{"path":"/health","method":"GET","description":"Health check"}]}
```
```bash
curl http://localhost:5000/health
```
```bash
{"status":"healthy","timestamp":"2026-01-31T19:22:42Z","uptime_seconds":119}
```

### Docker Hub Repository
```bash
https://hub.docker.com/repository/docker/scruffyscarf/info-service/tags/first/sha256-98ddc0a8908218f935dd65fd91618e41983c861c7ffa2b5fb96c2309c5f206b2
```



## Technical Analysis

### Why the Dockerfile Works This Way

`Dockerfile` is structured to follow Docker best practices for security, performance, and maintainability by minimizing image size and maximizing cache reuse.

### Effect of Changing Layer Order
If application files were copied before installing dependencies, Docker would reinstall dependencies on every code change, resulting in slower builds.

### Security Considerations
- Application runs as a non-root user
- Minimal base image reduces attack surface
- No sensitive or development files included in the image

### Role of .dockerignore
The `.dockerignore` file prevents unnecessary files from being sent to the Docker daemon, improving build speed and reducing image size.