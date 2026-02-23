# Lab 18 — Reproducible Builds with Nix



## Build Reproducible Python App 

### Installation steps and verification output

```bash
curl --proto '=https' --tlsv1.2 -sSf -L https://install.determinate.systems/nix | sh -s -- install
```

```bash
info: downloading the Determinate Nix Installer
 INFO nix-installer v3.16.0
`nix-installer` needs to run as `root`, attempting to escalate now via `sudo`...
Password:
 INFO nix-installer v3.16.0
 INFO For a more robust Nix installation, use the Determinate package for macOS: https://dtr.mn/determinate-nix
Nix install plan (v3.16.0)
Planner: macos (with default settings)
...
 INFO Step: Install Determinate Nixd
 INFO Step: Create an encrypted APFS volume `Nix Store` for Nix on `disk3` and add it to `/etc/fstab` mounting on `/nix`
 INFO Step: Provision Nix
 INFO Step: Create build users (UID 351-382) and group (GID 350)
 INFO Step: Configure Time Machine exclusions
 INFO Step: Configure Nix
 INFO Step: Configuring zsh to support using Nix in non-interactive shells
 INFO Step: Create a `launchctl` plist to put Nix into your PATH
 INFO Step: Configure the Determinate Nix daemon
 INFO Step: Remove directory `/nix/temp-install-dir`
Nix was installed successfully!
To get started using Nix, open a new shell or run `. /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh`
```

---

```bash
nix --version
```

```bash
nix (Determinate Nix 3.16.0) 2.33.3
```

### `default.nix`

- **Import and function**: Defines a function with the `pkgs` argument

- **The main function of the assembly**: Uses a special function to build Python applications

- **Metadata**: Name, version, and sources

- **Dependencies**: Python packages required for the application to work

- **Build format**: Specifies the use of `setuptools`

- **Pre-build hook**: Creates a `setup.py` before assembly

- **Post-install hook**: Creates an executable script in `$out/bin/`, copies `app.py` in site-packages

- **Meta Information**: Description, license, and platforms for the package catalog

### Store path from multiple builds

```bash
nix-build
```

```bash
/nix/store/...
```

---

```bash
nix-build
```

```bash
/nix/store/...
```

### pip install vs Nix derivation

| Aspect | pip + requirements.txt | Nix derivation |
|--------|------------------------|----------------|
| Python version | System-dependent | Pinned in nixpkgs |
| Direct dependencies | Pinned in `requirements.txt` | Pinned in nixpkgs |
| Transitive dependencies | Drift over time | Pinned via nixpkgs revision |
| Build reproducibility | Different versions possible | Bit-for-bit identical |
| Cross-machine consistency | Varies | Same hash guaranteed |
| Cache | pip cache (not content-addressed) | `/nix/store` |

### Why does `requirements.txt` provide weaker guarantees than Nix?

- Pins only what install directly
- Transitive dependencies can change
- Different Python versions on different machines
- `pip install` without hashes can pull different versions
- No guarantee of reproducibility over time

### App running from Nix-built version

![app](screenshots/app.png)

### Nix store path format and what each part means

`/nix/store/<hash>-<name>-<version>`:

- **Hash**: SHA256 of all inputs (source, dependencies, build script)
- **Name**: Package name
- **Version**: Package version
- Same inputs -> Same hash -> Same store path

### Reflection

- **No "works on my machine" problems**

    - **pip**: Spend time debugging why the app works for me, but not for others
    - **Nix**: all developers have the same environment from the first launch

- **Dependency versioning**

    - **pip**: pip freeze, only direct dependencies
    - **Nix**: Nix locks everything - including 
    Python version and all transitive dependencies

- **Clean environments**

    - **pip**: virtualenv sometimes clashed with system packages
    - **Nix**: complete isolation, no conflicts

- **Caching of assemblies**

    - **pip**: pip install from scratch
    - **Nix**: Nix caches by content hash - repeated builds are instant

- **Documentation in the code**

    - **pip**: it was necessary to write a `README` about the versions
    - **Nix**: `default.nix` itself is the documentation



## Reproducible Docker Images

### `docker.nix`

- **Import and function**: Defines a function with the pkgs argument

- **Let binding**: Declares local variables for reuse in the derivation

- **app**: Imports the application derivation from `./default.nix`

- **Docker image build**: Uses `pkgs.dockerTools.buildImage` to create a Docker image

- **Image metadata**: Sets the image name to `devops-info-service-nix` and tag to `1.0.0`

- **Base image**: Uses `fromImage = null` to create a minimal image from scratch

- **Image contents**: Specifies what to include in the image

- **Extra filesystem commands**: Creates additional directories with proper ownership

### `Dockerfile` vs Nix `docker.nix`

| Aspect | Traditional Dockerfile | Nix dockerTools |
|--------|------------------|-----------------------|
| Base images | `python:3.9-slim` (changes over time) | No base image (pure derivations) |
| Timestamps | Different on each build | Fixed or deterministic
| Package installation | apt-get install + pip install | Declarative description in contents |
| Package installation | pip install at build time | Nix store paths (immutable) |
| Reproducibility | Same Dockerfile -> Different images | Same `docker.nix` -> Identical images |
| Build Caching | Layer-based (breaks on timestamp) | Content-addressable (perfect caching) |
| Image Size | 391.45MB with full base image | 1.6GB with minimal closure |
| Portability | Requires Docker | Requires Nix (then loads to Docker) |
| Security | Base image vulnerabilities | Minimal dependencies, easier auditing |

### SHA256 hash comparison proving Nix reproducibility

```bash
docker images devops-info-service-nix:1.0.0
```

```bash
sha256:30814fbcf817b93c5413170fb6ee0c32a28ac68bdadcf0b2ffad355aaafffd9c
```

---

```bash
nix-store --delete /nix/store/*
rm result
docker images devops-info-service-nix:1.0.0
```

```bash
sha256:30814fbcf817b93c5413170fb6ee0c32a28ac68bdadcf0b2ffad355aaafffd9c
```

### Image size comparison with analysis

- **Dockerfile**: 391.45MB
- **Nix dockerTools**: 1.6GB

**Nix image**:

- There is no base image with extra OS files
- Only the minimum necessary dependencies
- Python is included as part of closure, not as a separate layer

### `docker history`

```bash
docker history lab2-app:v1
```

```bash
IMAGE          CREATED          CREATED BY                                      SIZE      COMMENT
0df4ab8345f9   59 minutes ago   CMD ["python" "app.py"]                         0B        buildkit.dockerfile.v0
<missing>      59 minutes ago   HEALTHCHECK &{["CMD-SHELL" "curl -f http://l…   0B        buildkit.dockerfile.v0
<missing>      59 minutes ago   EXPOSE map[5050/tcp:{}]                         0B        buildkit.dockerfile.v0
<missing>      59 minutes ago   USER appuser                                    0B        buildkit.dockerfile.v0
<missing>      59 minutes ago   RUN /bin/sh -c mkdir -p /data && chown appus…   0B        buildkit.dockerfile.v0
<missing>      59 minutes ago   RUN /bin/sh -c useradd -m -u 1000 appuser &&…   23.6kB    buildkit.dockerfile.v0
<missing>      59 minutes ago   COPY app.py . # buildkit                        14.6kB    buildkit.dockerfile.v0
<missing>      59 minutes ago   RUN /bin/sh -c pip install --no-cache-dir -r…   17.3MB    buildkit.dockerfile.v0
<missing>      59 minutes ago   COPY requirements.txt . # buildkit              93B       buildkit.dockerfile.v0
<missing>      59 minutes ago   WORKDIR /app                                    0B        buildkit.dockerfile.v0
<missing>      59 minutes ago   RUN /bin/sh -c apt-get update && apt-get ins…   227MB     buildkit.dockerfile.v0
<missing>      3 months ago     CMD ["python3"]                                 0B        buildkit.dockerfile.v0
<missing>      3 months ago     RUN /bin/sh -c set -eux;  for src in idle3 p…   36B       buildkit.dockerfile.v0
<missing>      3 months ago     RUN /bin/sh -c set -eux;   savedAptMark="$(a…   42.8MB    buildkit.dockerfile.v0
<missing>      3 months ago     ENV PYTHON_SHA256=00e07d7c0f2f0cc002432d1ee8…   0B        buildkit.dockerfile.v0
<missing>      3 months ago     ENV PYTHON_VERSION=3.9.25                       0B        buildkit.dockerfile.v0
<missing>      3 months ago     ENV GPG_KEY=E3FF2839C048B25C084DEBE9B26995E3…   0B        buildkit.dockerfile.v0
<missing>      3 months ago     RUN /bin/sh -c set -eux;  apt-get update;  a…   3.86MB    buildkit.dockerfile.v0
<missing>      3 months ago     ENV LANG=C.UTF-8                                0B        buildkit.dockerfile.v0
<missing>      3 months ago     ENV PATH=/usr/local/bin:/usr/local/sbin:/usr…   0B        buildkit.dockerfile.v0
<missing>      4 months ago     # debian.sh --arch 'arm64' out/ 'trixie' '@1…   101MB     debuerreotype 0.16
```

---

```bash
docker history devops-info-service-nix:1.0.0
```

```bash
IMAGE          CREATED   CREATED BY   SIZE      COMMENT
30814fbcf817   N/A                    1.6GB
```

### Containers running simultaneously

```bash
docker ps
```

```bash
CONTAINER ID   IMAGE         COMMAND           CREATED             STATUS                       PORTS                    NAMES
b14353656bf4   devops-info-service-nix:1.0.0   "/nix/store/.../dev..."   About an hour ago   Up About an hour (healthy)   0.0.0.0:5052->5050/tcp   nix-container
1183a33d3a1c   lab2-app:v1   "python app.py"   About an hour ago   Up About an hour (healthy)   0.0.0.0:5051->5050/tcp   lab2-container
```

---

```bash
curl http://localhost:5051/health
curl http://localhost:5052/health
```

```bash
{"status":"healthy","timestamp":"2026-02-23T11:19:21Z","uptime_seconds":537}
{"status":"healthy","timestamp":"2026-02-23T11:19:23Z","uptime_seconds":539}
```

### Analysis

- Timestamps

    - Each Docker layer gets a timestamp of creation
    - Even with the same content, timestamps are different -> different hashes

- Base image tags

    - `FROM python:3.9-slim` points to the floating tag
    - In a month `python:3.9-slim` may point to a different image

- `apt-get install`

    - Downloads the "latest" versions of packages from repositories
    - Repositories are updated -> packages are changed

- `pip install`

    - Even with pinned versions, downloads wheel files
    - Wheels can be rebuilt with different optimizations

- Build context

    - `.dockerignore` can skip different files
    - The order of copying affects the layers

- Network

    - Different mirrors may give different versions
    - CDN caching may affect downloaded files

### Reflection

- **Use Nix for Python dependencies**

    - **pip**: `requirements.txt` + `pip install`
    - **Nix**: Guarantees the same versions everywhere

- **Create a minimal image from the very beginning**

    - **pip**: `python:3.9-slim`
    - **Nix**:  Build an image with only what really need

- **Automate reproducibility testing**

    - **pip**: Catch problems before they get into the prod
    - **Nix**: In CI, check that nix-build gives the same hash

- **Document the dependencies in one place**

    - **pip**: Dependencies in `requirements.txt` + `Dockerfile` + `README`
    - **Nix**: All in one declarative file

- **Use assembly caching**

    - **pip**: Each build downloads everything as a new
    - **Nix**: Binary cache speeds up builds

### Practical scenarios where Nix's reproducibility matters

- **CI/CD Pipelines**: The deployment should be predictable. If it's assembled today and it's working, tomorrow it should work the same way

- **Security Audits**: For compliance, need to know the exact versions of the entire stack, including transitive dependencies

- **Rollbacks**: Instant rollback to any previous version, even if it was not launched in the registry

- **Multi-team collaboration**: "Works on my machine" disappears. What works on local - works for everyone

- **Release engineering**: Legal requirements for long-term support (LTS) releases



## Modern Nix with Flakes

### `flake.nix`

- **inputs**: External dependencies

- **outputs**: A function that returns the results of an assembly

- **flake-utils.lib.eachDefaultSystem**: Works automatically on all platforms

- **let ... in**: Local variables and definitions

- **packages**: Exported packages

- **apps**: Executable applications

- **devShells.default**: Development environment

### `flake.lock`

```yaml
...
"nixpkgs": {
    "locked": {
    "lastModified": 1751274312,
    "narHash": "sha256-/bVBlRpECLVzjV19t5KMdMFWSwKLtb5RyXdjz3LJT+g=",
    "owner": "NixOS",
    "repo": "nixpkgs",
    "rev": "50ab793786d9de88ee30ec4e4c24fb4236fc2674",
    "type": "github"
    },
    "original": {
    "owner": "NixOS",
    "ref": "nixos-24.11",
    "repo": "nixpkgs",
    "type": "github"
...
```

### `nix build`

```bash
warning: Git tree '/Users/scruffyscarf/DevOps-Core-Course' has uncommitted changes
```

### Builds are identical across time

```bash
nix build .
readlink result
```

```bash
/nix/store/lbc4c0r0q4pzclh0qlgp52yyxwphxvd6-devops-info-service-1.0.0
```

---

```bash
nix-store --delete /nix/store/lbc4c0r0q4pzclh0qlgp52yyxwphxvd6-devops-info-service-1.0.0
nix build .
readlink result
```

```bash
/nix/store/lbc4c0r0q4pzclh0qlgp52yyxwphxvd6-devops-info-service-1.0.0
```

### Dev shell experience

```bash
source venv/bin/activate
```

```bash
Python: 3.13.1 # depends on the system
Flask: 3.1.3 # can update
```

---

```bash
nix develop
```
```bash
Python: 3.12.3 # always the same
Flask: 3.0.3 # always the same
```

### `values.yaml` vs `flake.nix`

| Aspect | Helm `values.yaml` | Nix `flake.nix` |
|--------|---------------------------|---------------------|
| **Locks Python version** | Uses image Python | Pinned in flake |
| **Locks dependencies** | Only image tag | Exact hashes |
| **Locks build tools** | No | Yes |
| **Reproducibility** | Tag-based | Cryptographic |
| **Cross-machine** | Depends on image | Identical |
| **Dev environment** | No | Yes |
| **Time-stable** | Tags can change | Locked forever |

### Reflection

- **Complete closure**: All dependencies are removed, including compilers and utilities
- **Cryptographic verification**: Hashes guarantee integrity
- **Determinism**: Same input -> same output
- **Divisibility**: Link to specific GitHub commits
- **Dev/prod parity**: Development environment = Production

### Practical scenarios where `flake.lock` prevented a "works on my machine" problem

| Scenario | Without `flake.lock` | With `flake.lock` |
|----------|-------------------|-----------------|
| New developer joins the team | Full day of environment setup | a few minutes |
| Python version update | May break the application | No impact |
| CVE in transitive dependency | Unknown which version is used | Exactly know the version |
| Deployment after a month | May fail to build | Builds identically |
| Dependency audit | Manual information gathering | Automatic from lock file |
