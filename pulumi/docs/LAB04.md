# Lab 4 — Infrastructure as Code (Terraform & Pulumi)

## Programming language - Python

- **Clarity** — easy-managed
- **Simplicity** — straightforward syntax
- **Speed** — fast start

## pulumi version

v3.219.0

## pulumi preview

```bash
     Type                              Name                         Plan       Info
 +   pulumi:pulumi:Stack               info-service-dev             create     2 messages
 +   ├─ pulumi:providers:yandex        yc                           create     
 +   ├─ yandex:index:VpcNetwork        info-service-network         create     
 +   ├─ yandex:index:VpcSubnet         info-service-subnet          create     
 +   ├─ yandex:index:VpcSecurityGroup  info-service-security-group  create     
 +   └─ yandex:index:ComputeInstance   info-service-vm              create 
```

## pulumi up

```bash
     Type                              Name                         Status              Info
 +   pulumi:pulumi:Stack               info-service-dev             created (49s)       2 messages
 +   ├─ pulumi:providers:yandex        yc                           created (0.24s)     
 +   ├─ yandex:index:VpcNetwork        info-service-network         created (3s)        
 +   ├─ yandex:index:VpcSubnet         info-service-subnet          created (0.76s)     
 +   ├─ yandex:index:VpcSecurityGroup  info-service-security-group  created (1s)        
 +   └─ yandex:index:ComputeInstance   info-service-vm              created (40s)

Outputs:
    public_ip: "89.169.*.*" 
```

## VM Public IP address

`89.169.*.*`

## SSH connection

`ssh ubuntu@89.169.*.*`
```bash
The authenticity of host '89.169.*.* (89.169.*.*)' can't be established.
ED25519 key fingerprint is SHA256:0M8....

ubuntu@fhm...:~$
```

## Resources

- info-service-dev
- info-service-vm
- info-service-subnet
- info-service-security-group
- info-service-network
- yc

## pulumi destroy

```bash
     Type                              Name                         Status              
 -   pulumi:pulumi:Stack               info-service-dev             deleted (0.31s)     
 -   ├─ yandex:index:ComputeInstance   info-service-vm              deleted (31s)       
 -   ├─ yandex:index:VpcSubnet         info-service-subnet          deleted (6s)        
 -   ├─ yandex:index:VpcSecurityGroup  info-service-security-group  deleted (1s)        
 -   ├─ yandex:index:VpcNetwork        info-service-network         deleted (1s)        
 -   └─ pulumi:providers:yandex        yc                           deleted (0.53s)     

Outputs:
  - public_ip: "89.169.*.*"

The resources in the stack have been deleted, but the history and configuration associated with the stack are still maintained. 
If you want to remove the stack completely, run `pulumi stack rm dev`.
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
