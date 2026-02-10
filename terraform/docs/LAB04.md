# Lab 4 — Infrastructure as Code (Terraform & Pulumi)



## Cloud Provider - Yandex Cloud

- **Accessibility** — no problems with access and payment
- **Tariff** — 4000 rubles from start
- **Good documentation** — simplifies learning

## terraform version

Terraform v1.14.4

## terraform init

```bash
Initializing the backend...
Initializing provider plugins...
- Finding latest version of yandex-cloud/yandex...
- Installing yandex-cloud/yandex v0.184.0...
- Installed yandex-cloud/yandex v0.184.0 (self-signed, key ID E40...)
Partner and community providers are signed by their developers.
If you'd like to know more about provider signing, you can read about it here:
https://developer.hashicorp.com/terraform/cli/plugins/signing
Terraform has created a lock file .terraform.lock.hcl to record the provider
selections it made above. Include this file in your version control repository
so that Terraform can guarantee to make the same selections by default when
you run "terraform init" in the future.

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
```

## terraform plan

```bash
Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # yandex_compute_instance.vm will be created
  + resource "yandex_compute_instance" "vm" {
      + created_at                = (known after apply)
      + folder_id                 = (known after apply)
      + fqdn                      = (known after apply)
      + gpu_cluster_id            = (known after apply)
      + hardware_generation       = (known after apply)
      + hostname                  = (known after apply)
      + id                        = (known after apply)
      + maintenance_grace_period  = (known after apply)
      + maintenance_policy        = (known after apply)
      + metadata                  = {
          + "ssh-keys" = <<-EOT
...
```

## terraform apply

```bash
yandex_vpc_network.this: Creating...
yandex_vpc_network.this: Creation complete after 2s [id=enpkn4h3jfsactmlsjbe]
yandex_vpc_subnet.this: Creating...
yandex_vpc_security_group.this: Creating...
yandex_vpc_subnet.this: Creation complete after 1s [id=e9bn6kss7d6fond1rlpp]
yandex_vpc_security_group.this: Creation complete after 2s [id=enp80v7buefldcri6bhg]
yandex_compute_instance.vm: Creating...
yandex_compute_instance.vm: Still creating... [10s elapsed]
yandex_compute_instance.vm: Still creating... [20s elapsed]
yandex_compute_instance.vm: Still creating... [30s elapsed]
yandex_compute_instance.vm: Still creating... [40s elapsed]
yandex_compute_instance.vm: Creation complete after 45s [id=fhm...]

Apply complete! Resources: 4 added, 0 changed, 0 destroyed.

Outputs:

public_ip = "93.77.*.*"
```

## VM Public IP address

`93.77.*.*`

## SSH connection

`ssh ubuntu@93.77.*.*`
```bash
The authenticity of host '93.77.*.* (93.77.*.*)' can't be established.
ED25519 key fingerprint is SHA256:6hk....

ubuntu@fhm...:~$
```

## Resources

- info-service
- info-service-network
- info-service-security-groups
- info-service-subnet

## terraform destroy

```bash
yandex_compute_instance.vm: Destroying... [id=fhm6ue6tlbqaps0ajb9k]
yandex_compute_instance.vm: Still destroying... [id=fhm6ue6tlbqaps0ajb9k, 00m10s elapsed]
yandex_compute_instance.vm: Still destroying... [id=fhm6ue6tlbqaps0ajb9k, 00m20s elapsed]
yandex_compute_instance.vm: Still destroying... [id=fhm6ue6tlbqaps0ajb9k, 00m30s elapsed]
yandex_compute_instance.vm: Destruction complete after 31s
yandex_vpc_subnet.this: Destroying... [id=e9b923runku4pks1jhao]
yandex_vpc_security_group.this: Destroying... [id=enp8sg70v6kdketes7fg]
yandex_vpc_security_group.this: Destruction complete after 0s
yandex_vpc_subnet.this: Destruction complete after 5s
yandex_vpc_network.this: Destroying... [id=enpqmv18bdjd65ja03o7]
yandex_vpc_network.this: Destruction complete after 0s

Destroy complete! Resources: 4 destroyed.
```

## Terraform vs Pulumi

Advantages of HCL:

- Declarative syntax
- A single standard for all providers
- Good readability for infrastructure
- Extensive community and documentation

Advantages of Pulumi:

- A full-fledged programming language
- Typing and auto-completion in the IDE
- The ability to use functions, loops, classes
- It's easier to reuse the code

## Preferable tool - Terraform

- Super-stable infrastructures
- Collaboration with external teams
- Enterprise features
- Stability

## tflint

`No output`

## GitHub repository import process

```bash
export GITHUB_TOKEN="..."
terraform init
terraform import github_repository.course_repo "DevOps-Core-Course"
terraform plan
terraform apply

Terraform has been successfully initialized!

github_repository.course_repo: Importing from ID "DevOps-Core-Course"
github_repository.course_repo: Import prepared!
  Prepared github_repository for import
github_repository.course_repo: Refreshing state... [id=DevOps-Core-Course]

Import successful!
```

## Why importing matters

- **A single source of truth**: All resources are managed through a single tool
- **Consistency**: Eliminates configuration drift
- **Change Security**: Terraform shows the difference before applying
- **Documentation**: The code becomes the documentation of the infrastructure
- **Recovery**: Easy infrastructure recovery in case of failures

## Benefits for managing repos with IaC

- **Reproducibility**: Identical repositories can be created for different environments.
- **Versioning**: The history of settings changes in Git
- **Code Review**: Repository settings are reviewed as code
- **Automating**: Massive changes across multiple repositories
- **Security**: Standardized security settings
