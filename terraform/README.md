# FinPilot Terraform Infrastructure

## Resources Created
- **VPC** with DNS support
- **2 Public Subnets** across availability zones
- **2 Private Subnets** for EKS worker nodes
- **Internet Gateway** for public access
- **NAT Gateway** for private subnet outbound access
- **EKS Cluster** (Kubernetes 1.29)
- **Managed Node Group** (t3.medium, 2 nodes default)
- **IAM Roles** for EKS cluster and worker nodes

## Cost Warning
⚠️ Running this infrastructure incurs AWS charges:
- **EKS Control Plane**: ~$0.10/hour (~$73/month)
- **NAT Gateway**: ~$0.045/hour + data (~$33/month)
- **t3.medium nodes** (x2): ~$0.042/hour each (~$61/month)
- **Estimated total**: ~$170/month

**Always run `terraform destroy` after evaluation.**

## Usage
```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values

terraform init
terraform fmt -check
terraform validate
terraform plan
terraform apply     # Requires approval
terraform output

# Cleanup
terraform destroy   # Requires approval
```
