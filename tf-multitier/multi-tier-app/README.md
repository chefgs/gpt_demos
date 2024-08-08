
### Implementing Infrastructure as Code (IaC) for a Multi-Tier Application Architecture on AWS Using Terraform

To demonstrate the implementation of IaC for a multi-tier application architecture on AWS using Terraform, we will go through the following steps:

1. **Define the Architecture:**
   - A VPC with public and private subnets
   - An internet gateway and NAT gateway
   - An EC2 instance in the public subnet
   - An auto-scaling group in the private subnets
   - An RDS instance in the private subnets
   - A load balancer to distribute traffic

2. **Install and Configure Terraform:**
   - Install Terraform on your local machine.
   - Configure AWS CLI with the necessary credentials.

3. **Create Terraform Configuration Files:**
   - Define variables, provider, VPC, subnets, internet gateway, NAT gateway, security groups, EC2 instances, auto-scaling group, RDS instance, and load balancer.

4. **Initialize and Apply Terraform Configuration:**
   - Initialize the Terraform configuration.
   - Apply the configuration to provision the infrastructure.

### Step-by-Step Guide

#### Step 1: Define the Architecture

A typical multi-tier architecture includes:
- A VPC with public and private subnets
- An internet gateway for internet access
- A NAT gateway for instances in private subnets to access the internet
- EC2 instances for the application layer
- An auto-scaling group to handle traffic
- An RDS instance for the database layer
- A load balancer to distribute incoming traffic

#### Step 2: Install and Configure Terraform

1. **Install Terraform:**
   Download Terraform from the [official site](https://www.terraform.io/downloads.html) and follow the installation instructions for your operating system.

2. **Configure AWS CLI:**
   Ensure you have AWS CLI installed and configured with the necessary access credentials.
   ```bash
   aws configure
   ```

#### Step 3: Create Terraform Configuration Files

Create a directory for your Terraform configuration files, e.g., `multi-tier-app/`.

##### 1. **Variables File: `variables.tf`**

```hcl
variable "region" {
  default = "us-west-2"
}

variable "vpc_cidr" {
  default = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  default = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnet_cidrs" {
  default = ["10.0.3.0/24", "10.0.4.0/24"]
}

variable "db_subnet_cidrs" {
  default = ["10.0.5.0/24", "10.0.6.0/24"]
}
```

##### 2. **Provider Configuration File: `provider.tf`**

```hcl
provider "aws" {
  region = var.region
}
```

##### 3. **VPC and Subnets File: `network.tf`**

```hcl
resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr
  enable_dns_support = true
  enable_dns_hostnames = true
  tags = {
    Name = "main-vpc"
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "main-igw"
  }
}

resource "aws_subnet" "public" {
  count = length(var.public_subnet_cidrs)
  vpc_id = aws_vpc.main.id
  cidr_block = element(var.public_subnet_cidrs, count.index)
  map_public_ip_on_launch = true
  tags = {
    Name = "public-subnet-${count.index + 1}"
  }
}

resource "aws_subnet" "private" {
  count = length(var.private_subnet_cidrs)
  vpc_id = aws_vpc.main.id
  cidr_block = element(var.private_subnet_cidrs, count.index)
  tags = {
    Name = "private-subnet-${count.index + 1}"
  }
}

resource "aws_subnet" "db" {
  count = length(var.db_subnet_cidrs)
  vpc_id = aws_vpc.main.id
  cidr_block = element(var.db_subnet_cidrs, count.index)
  tags = {
    Name = "db-subnet-${count.index + 1}"
  }
}
```

##### 4. **Security Groups File: `security_groups.tf`**

```hcl
resource "aws_security_group" "web_sg" {
  vpc_id = aws_vpc.main.id
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name = "web-sg"
  }
}

resource "aws_security_group" "app_sg" {
  vpc_id = aws_vpc.main.id
  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name = "app-sg"
  }
}

resource "aws_security_group" "db_sg" {
  vpc_id = aws_vpc.main.id
  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name = "db-sg"
  }
}
```

##### 5. **EC2 Instances and Auto-Scaling Group File: `instances.tf`**

```hcl
resource "aws_launch_configuration" "app_lc" {
  name          = "app-lc"
  image_id      = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  security_groups = [aws_security_group.app_sg.id]

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_autoscaling_group" "app_asg" {
  desired_capacity     = 2
  max_size             = 3
  min_size             = 1
  vpc_zone_identifier  = aws_subnet.private[*].id
  launch_configuration = aws_launch_configuration.app_lc.id
  tags = [
    {
      key                 = "Name"
      value               = "app-instance"
      propagate_at_launch = true
    },
  ]
}
```

##### 6. **RDS Instance File: `rds.tf`**

```hcl
resource "aws_db_subnet_group" "db_subnet_group" {
  name       = "db-subnet-group"
  subnet_ids = aws_subnet.db[*].id

  tags = {
    Name = "db-subnet-group"
  }
}

resource "aws_db_instance" "db" {
  identifier              = "mydb"
  allocated_storage       = 20
  engine                  = "mysql"
  engine_version          = "5.7"
  instance_class          = "db.t2.micro"
  name                    = "mydatabase"
  username                = "admin"
  password                = "password"
  db_subnet_group_name    = aws_db_subnet_group.db_subnet_group.name
  vpc_security_group_ids  = [aws_security_group.db_sg.id]
  skip_final_snapshot     = true

  tags = {
    Name = "mydb"
  }
}
```

##### 7. **Load Balancer File: `load_balancer.tf`**

```hcl
resource "aws_elb" "web_elb" {
  name               = "web-elb"
  availability_zones = ["${aws_subnet.public[*].availability_zone}"]
  security_groups    = [aws_security_group.web_sg.id]
  listener {
    instance_port     = 8080
    instance_protocol = "HTTP"
    lb_port           = 80
    lb_protocol       = "HTTP"
  }

  health_check {
    target              = "HTTP:8080/"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }

  tags = {
    Name = "web-elb"
  }
}
```

#### Step 4: Initialize and Apply Terraform Configuration

1. **Initialize the Terraform configuration:**
   ```bash
   terraform init
   ```

2. **Apply the Terraform configuration:**
   ```bash
   terraform apply
   ```

   Confirm the action by typing `yes` when prompted.

### Directory Structure

Here’s an example of how the directory structure should look:

```
multi-tier-app/
├── variables.tf
├── provider.tf
├── network

.tf
├── security_groups.tf
├── instances.tf
├── rds.tf
├── load_balancer.tf
└── outputs.tf
```

### Detailed Explanation

1. **`variables.tf`:** Defines the input variables for the Terraform configuration.
2. **`provider.tf`:** Configures the AWS provider with the specified region.
3. **`network.tf`:** Creates the VPC, subnets, internet gateway, and NAT gateway.
4. **`security_groups.tf`:** Defines security groups for the web, application, and database layers.
5. **`instances.tf`:** Sets up the EC2 instances and auto-scaling group for the application layer.
6. **`rds.tf`:** Configures the RDS instance with the necessary subnet group and security group.
7. **`load_balancer.tf`:** Creates a load balancer to distribute traffic to the application instances.



### Modularising the code with Remote Backend

To enhance the Terraform configuration by using modules and a remote backend with dynamic locking, follow these steps:

1. **Set Up Remote Backend:**
   - Configure Terraform to use an S3 bucket for storing state files and DynamoDB for state locking and consistency.

2. **Create Terraform Modules:**
   - Split the configuration into reusable modules for VPC, EC2 instances, RDS, and Load Balancer.

3. **Main Terraform Configuration:**
   - Utilize the modules in the main configuration file and configure the remote backend.

### Step-by-Step Guide

#### Step 1: Set Up Remote Backend

1. **Create an S3 Bucket and DynamoDB Table:**
   - S3 bucket: Store the Terraform state files.
   - DynamoDB table: Manage state locks.

**S3 Bucket and DynamoDB Configuration (AWS CLI or Console):**

```bash
aws s3 mb s3://my-terraform-state-bucket
aws dynamodb create-table \
    --table-name terraform-lock-table \
    --attribute-definitions AttributeName=LockID,AttributeType=S \
    --key-schema AttributeName=LockID,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
```

#### Step 2: Create Terraform Modules

Create the following directory structure for modules:

```
modules/
├── vpc/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── ec2/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── rds/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
└── lb/
    ├── main.tf
    ├── variables.tf
    └── outputs.tf
```


#### Step 3: Main Terraform Configuration


### Directory Structure

Here’s an example of how the directory structure should look:

```
multi-tier-app/
├── main.tf
├── variables.tf
├── modules/
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── ec2/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── rds/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── lb/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
```

### Detailed Explanation

1. **Remote Backend:**
   Configures Terraform to use an S3 bucket for state storage and a DynamoDB table for state locking to ensure consistency and avoid conflicts during concurrent operations.

2. **Modules:**
   Encapsulates different infrastructure components (VPC, EC2, RDS, Load Balancer) into reusable modules, promoting modularity and reusability.

3. **Main Configuration:**
   Utilizes the modules to build the complete infrastructure. Variables are defined for customizable parameters, and outputs from each module are used as inputs for others, ensuring seamless integration.

By following this steps, we can set up a robust, scalable, and secure multi-tier application architecture on AWS using Terraform modules and a remote backend. This modular approach promotes reusability, maintainability, and ensures that your infrastructure is consistently and efficiently managed.
This IaC setup automates the provisioning of infrastructure components, ensuring consistency and repeatability across different environments.

## Pre-requisites

To create the S3 bucket and DynamoDB table required for the Terraform backend, you can use the AWS CLI. Here are the steps:

### Step-by-Step Instructions

1. **Open Terminal**:
   - Open the terminal in Visual Studio Code or your preferred terminal application.

2. **Create S3 Bucket**:
   - Use the following command to create an S3 bucket. 
   ```sh
   aws s3api create-bucket --bucket my-terraform-state-bucket --region us-west-2 --create-bucket-configuration LocationConstraint=us-west-2
   ```

3. **Enable Versioning on S3 Bucket**:
   - Enable versioning on the S3 bucket to keep track of the state file versions.
   ```sh
   aws s3api put-bucket-versioning --bucket my-terraform-state-bucket --versioning-configuration Status=Enabled
   ```

4. **Create DynamoDB Table**:
   - Use the following command to create a DynamoDB table for state locking.
   ```sh
   aws dynamodb create-table --table-name terraform-lock-table --attribute-definitions AttributeName=LockID,AttributeType=S --key-schema AttributeName=LockID,KeyType=HASH --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 --region us-west-2
   ```

### Summary of Commands

```sh
# Create S3 bucket
aws s3api create-bucket --bucket gs-multi-tier-infra --region us-west-2 --create-bucket-configuration LocationConstraint=us-west-2

# Enable versioning on S3 bucket
aws s3api put-bucket-versioning --bucket gs-multi-tier-infra --versioning-configuration Status=Enabled

# Create DynamoDB table
aws dynamodb create-table --table-name gs-terraform-lock-table --attribute-definitions AttributeName=LockID,AttributeType=S --key-schema AttributeName=LockID,KeyType=HASH --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 --region us-west-2
```
