# Lab 2 — Docker Containerization



## Docker Best Practices Applied

### Non-root User
The application runs inside the container using a non-root user instead of root. Running containers as root increases security risks. If the application is compromised, the attacker would gain elevated privileges inside the container. Using a non-root user limits the potential impact.

```bash
RUN adduser -D appuser
USER appuser
```

### .dockerignore
A `.dockerignore` file is used to exclude unnecessary files from the build context. Excluding files such as virtual environments, caches, and git metadata reduces build context size, speeds up builds, and prevents accidental inclusion of development artifacts.



## Image Information & Decisions

### Base Image Choice
Base image: `golang:1.22`.

### Layer Structure Explanation
1. Base Go image
2. Dependency installation layer
3. Application source code layer
4. Runtime configuration (non-root user, startup command)

### Optimization Choices
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

### Testing Endpoints

```bash
curl http://localhost:5000
```
```bash
{"service":{"name":"devops-info-service","version":"1.0.0","description":"DevOps course info service","framework":"net/http"},"system":{"hostname":"bd7afeeb7b00","platform":"linux","platform_version":"unknown","architecture":"amd64","cpu_count":8,"go_version":"go1.22.12"},"runtime":{"uptime_seconds":128,"uptime_human":"0 hour(s), 2 minute(s)","current_time":"2026-01-31T19:22:51Z","timezone":"UTC"},"request":{"client_ip":"172.17.0.1:59016","user_agent":"curl/8.7.1","method":"GET","path":"/"},"endpoints":[{"path":"/","method":"GET","description":"Service information"},{"path":"/health","method":"GET","description":"Health check"}]}
```
```bash
curl http://localhost:5000/health
```
```bash
{"status":"healthy","timestamp":"2026-01-31T19:22:42Z","uptime_seconds":119}
```

### Docker Hub Repository
```bash
https://hub.docker.com/repository/docker/scruffyscarf/info-service/tags/go/sha256:c52e55316458d88f37d8ead47f2dc625ba7b0094a1f728d777f100e352b2fa99
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
