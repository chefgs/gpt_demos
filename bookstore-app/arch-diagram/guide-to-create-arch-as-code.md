## **How to Create Architecture Diagram as Code for a 2-Tier Bookstore Application**

Creating architecture `diagrams as code` is a modern approach that offers numerous benefits over traditional diagramming methods, including architecture diagram automation, and consistency. This approach allows for version-controlled, easily reproducible, and modifiable diagrams that can evolve alongside your application.

This article will guide you through the process of creating an architecture diagram for a 2-tier bookstore application in AWS Cloud using `Python` and its [`diagrams`] library.

## Why Diagrams as Code?

Diagrams as code offer several advantages over traditional diagramming tools:

- **Version Control**: Changes to diagrams can be tracked over time.
- **Automation**: Diagrams can be automatically updated as part of your CI/CD pipeline.
- **Consistency**: Ensures uniformity in the presentation of your architecture.

Diagram as code makes it easy to **Architects** and **Developers** to update their architecture diagram, and use version control to maintain various versions of the Architecture.

## Tools & Technology Used

We'll use the [`diagrams`] Python library, which allows for creating cloud system architecture diagrams using code. It supports various providers, including **AWS, GCP, Azure**, and many more.

## Prerequisites

- Python 3.x installed on your system
- Basic understanding of Python programming
- Familiarity with virtual environments in Python

## Sample Application: Bookstore 2-Tier Architecture

Our sample application is a simple bookstore with a 2-tier architecture consisting of a frontend and a backend, along with a database. It also includes a CI/CD pipeline and monitoring services.

To run the Python code that generates an architecture diagram for a bookstore application, follow these detailed steps. These steps include setting up a virtual environment, installing dependencies, and running the script.

### Step 1: Setting Up a Python Virtual Environment

First, you need to create a virtual environment. A virtual environment is a self-contained directory that contains a Python installation for a particular version of Python, plus a number of additional packages.

1. Open your terminal.
2. Navigate to the directory where you want to store your project.
3. Run the following command to create a virtual environment named `venv`:

```bash
python3 -m venv venv
```

### Activate the Virtual Environment

Activate the virtual environment to use it for your project.

- On macOS and Linux:

```bash
source venv/bin/activate
```

- On Windows:

```bash
.\venv\Scripts\activate
```

### Install the Required Libraries

With the environment activated, install the `diagrams` library, which enables you to generate architecture diagrams using Python code.

```bash
pip install diagrams graphviz
```

## Step 2: Writing the Diagram Code

Create a new Python file named [`architecture.py`] and open it in your favorite text editor. 
Copy the following code into the file. This code defines the architecture of a simple bookstore application with a 2-tier architecture, including a frontend, a backend, a database, a CI/CD pipeline, and monitoring services.

```python
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB, Route53
from diagrams.aws.general import Client
from diagrams.onprem.network import Internet
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.programming.framework import React
from diagrams.custom import Custom

graph_attr = {'ranksep': '1.0'} #, 'rankdir': 'TB'}

with Diagram("Two Tier Application Architecture", show=False, graph_attr=graph_attr):
	with Cluster("User Network"):
		client = Client("User")
		internet = Internet("Internet")

	with Cluster("CI/CD Pipeline"):
		with Cluster("Source Code"):
			react = React("React")
			terraform = Custom("Terraform", "./tf.png")
		github_actions = Custom("GitHub Actions", "./ghactions.png")

	with Cluster("AWS Cloud"):
		with Cluster("VPC"):
			with Cluster("Public Subnet"):
				dns = Route53("DNS")
				lb = ELB("Load Balancer")
				# public_subnet = Subnet("Public Subnet")
				dns >> lb

			with Cluster("Private Subnet for Backend"):
				# private_subnet_backend = Subnet("Private Subnet")
				backend = EC2("Backend (Node.js)")
				db = RDS("Database (MongoDB)")
				backend >> db

			with Cluster("Private Subnet for Frontend"):
				# private_subnet_frontend = Subnet("Private Subnet")
				frontend = EC2("Frontend (React)")
				# private_subnet_frontend >> frontend

		with Cluster("Monitoring"):
			prometheus = Prometheus("Prometheus")
			grafana = Grafana("Grafana")

	client >> internet >> dns
	react >> github_actions
	terraform >> github_actions
	lb >> Edge(label="HTTP/HTTPS") >> frontend
	lb >> Edge(label="HTTP/HTTPS") >> backend
	backend >> Edge(label="Database Connection") >> db
	backend >> prometheus
	frontend >> prometheus
	db >> prometheus
	prometheus >> grafana

	# Connecting CI/CD Pipeline to AWS Cloud
	github_actions >> Edge(color="blue", style="dashed", label="Deploy to AWS Cloud") >> dns
	
# Creating Custom Node 
# Custom Node: We can create a custom node to represent the subnet. 
# The diagrams library allows you to create custom nodes with your own images, 
# which can be useful for representing components that are not available as predefined classes.
# from diagrams import Node
# class Subnet(Node):
#    _icon_dir = "path/to/custom/icons"
#    _icon = "subnet.png"
```

Full source code has been available in GitHub. Please [check it out here](https://github.com/chefgs/gpt_demos/tree/main/bookstore-app/arch-diagram).

## Python Code Break down of the Architecture Diagram 
Let's break down the Python code used to generate the architecture diagram step-by-step:

```python
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB, Route53
from diagrams.aws.devtools import Codepipeline, Codebuild
from diagrams.aws.general import Client
from diagrams.onprem.network import Internet
from diagrams.onprem.container import Docker
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.programming.language import Python
```

### Imports

- **Diagram, Cluster, Edge**: Core components from the `diagrams` library to create diagrams, group components, and define connections.
- **AWS Components**: Various AWS components (`EC2`, `RDS`, `ELB`, `Route53`, `Codepipeline`, `Codebuild`, `Client`) to represent different parts of the architecture.
- **On-Prem Components**: Components for non-cloud (on-prem) services (`Internet`, `Docker`, `Prometheus`, `Grafana`).
- **Programming Language**: Represents GitHub Actions with a generic programming language icon (`Python`).

### Creating the Diagram

```python
with Diagram("Two Tier Application Architecture", show=False, graph_attr=graph_attr):
	with Cluster("User Network"):
		client = Client("User")
		internet = Internet("Internet")
```

- **Diagram**: The main context for the diagram, with the title "Bookstore Application Architecture". `show=False` prevents the diagram from being immediately displayed.
- **Client**: Represents the user accessing the application.
- **DNS**: Uses Route53 to represent the DNS service.

### CI/CD Pipeline

```python
	with Cluster("CI/CD Pipeline"):
		with Cluster("Source Code"):
			react = React("React")
			terraform = Custom("Terraform", "./tf.png")
		github_actions = Custom("GitHub Actions", "./ghactions.png")
```

- **Cluster**: Groups components logically. Here, it groups the CI/CD pipeline components.
- **GitHub Actions**: Represented using a generic programming language user uploaded icon (`ghactions.png`).
- **React and Custom**: MERN code and Terraform code representation (with user uploaded Terraform icon). They are integrated with the GitHub action workflow for CICD deployment.

### AWS Cloud & Monitoring Components

```python
	with Cluster("AWS Cloud"):
		with Cluster("VPC"):
			with Cluster("Public Subnet"):
				dns = Route53("DNS")
				lb = ELB("Load Balancer")
				# public_subnet = Subnet("Public Subnet")
				dns >> lb

			with Cluster("Private Subnet for Backend"):
				# private_subnet_backend = Subnet("Private Subnet")
				backend = EC2("Backend (Node.js)")
				db = RDS("Database (MongoDB)")
				backend >> db

			with Cluster("Private Subnet for Frontend"):
				# private_subnet_frontend = Subnet("Private Subnet")
				frontend = EC2("Frontend (React)")
				# private_subnet_frontend >> frontend

		with Cluster("Monitoring"):
			prometheus = Prometheus("Prometheus")
			grafana = Grafana("Grafana")
```

- **AWS Cloud Cluster**: Groups all AWS cloud components.
- **Load Balancer (ELB) and DNS**: Distributes traffic between frontend and backend services. DNS used to be exposed to the public internet.
- **VPC Cluster**: VPC cluster has been created to indicate private and public subnet networks for UI layer and backend layer.
- **Backend Service Cluster**: Contains the backend server (Node.js on EC2) and the database (MongoDB on RDS).
- **Frontend Service Cluster**: Contains the frontend server (React on EC2).
- **Monitoring Cluster**: Contains Prometheus for metrics collection and Grafana for visualization.

### Defining Connections

```python
	client >> internet >> dns
	react >> github_actions
	terraform >> github_actions
	lb >> Edge(label="HTTP/HTTPS") >> frontend
	lb >> Edge(label="HTTP/HTTPS") >> backend
	backend >> Edge(label="Database Connection") >> db
	backend >> prometheus
	frontend >> prometheus
	db >> prometheus
	prometheus >> grafana
```

- **Connections**: Represented using `>>` operator, defining the flow and connections between components.
- **client >> internet >> dns**: The user accesses the DNS service, via public internet.
- **react >> github_actions**: Represents the CI/CD pipeline flow from MERN Code into integration GitHub Actions.
- **terraform >> github_actions**: Represents the CI/CD pipeline flow from Terraform infra deployment code into integration GitHub Actions.
- **lb >> Edge(label="HTTP/HTTPS") >> frontend**: The load balancer directs traffic to the frontend services.
- **lb >> Edge(label="HTTP/HTTPS") >> backend**: The load balancer directs traffic to the backend services.
- **backend >> Edge(label="Database Connection") >> db**: The backend service connects to the MongoDB database.
- **backend >> prometheus** and **frontend >> prometheus**: Both frontend and backend services send metrics to Prometheus.
- **prometheus >> grafana**: Prometheus metrics are visualized using Grafana.
- **github_actions >> Edge(color="blue", style="dashed", label="Deploy to AWS Cloud") >> dns**: Depicts to connection from GitHub Action to AWS Cloud infra deployment and code deployment into servers

### Summary of Diagram Breakdown

The Python script leverages the `diagrams` library to create a structured, version-controlled architecture diagram. It groups related components into clusters, defines the interactions between them using directed edges, and ensures the entire infrastructure is visually represented in a clear, consistent manner. This approach makes it easy to update and maintain the architecture diagram as the application evolves.

### Adding custom node for user-defined components

Let us see how to create a custom node in Python using the `diagrams` library. This library allows developers to visually represent their infrastructure and systems.

The purpose of creating a custom node is to represent a user-defined architecture component and ICON/logo. 

Method 1: Defining the `from diagrams.custom import Custom` Diagrams Custom module, and using this section along with the valid logo/ICON PNG image of the architecture component.
For example, we have added Terraform Icon using this method.

We need to store the license free PNG image for this purpose.
```
from diagrams.custom import Custom

terraform = Custom("Terraform", "./tf.png")
```

Method 2:
As depicted on the _commented out_ example, a custom node definition for subnet has been added.

A subnet is part of VPC architecture &, and is a logical subdivision of an IP network. The ability to create custom nodes is particularly useful when the predefined classes provided by the `diagrams` library do not cover all the components you need to represent in your architecture diagrams.

- The code snippet begins by importing the `Node` class from the `diagrams` library.
- This `Node` class is the base class for all diagram nodes, and custom nodes can be created by subclassing it. 
- The subclass shown in the example is named `Subnet`, indicating its intended use to represent subnetworks.

Within the `Subnet` class, two class attributes are defined:
- `_icon_dir`: This attribute specifies the directory path where custom icons are stored. In this example, it's set to `"path/to/custom/icons"`, which should be replaced with the actual path to the directory containing the icon files.
- `_icon`: This attribute specifies the filename of the icon image that will be used to visually represent the node in the diagram. Here, it is set to `"subnet.png"`, indicating that an image file named `subnet.png` in the specified directory will be used as the icon for the subnet node.

By defining these attributes, the `Subnet` class tells the `diagrams` library where to find the custom icon and which icon to use when rendering the subnet node in a diagram. This allows for a more customized and visually accurate representation of the system's architecture.

## Step 3: Generating the Diagram

Ensure the Python script ([`architecture.py`] is saved in your project directory.

Run the script to generate the architecture diagram. Ensure your virtual environment is activated, then execute:

```bash
python architecture.py
```

This command executes the script, which generates a PNG image named `Bookstore Application Architecture.png` in the same directory, illustrating the architecture of the bookstore application.

### Understanding the Diagram `Bookstore Application Architecture.png`

- **User Network**: Represents the entry point for users, connecting through the internet to our application.
- **CI/CD Pipeline**: Showcases the automation for deploying our React frontend and Terraform configurations.
- **AWS Cloud**: Hosts our application, including the load balancer, DNS service, backend service (Node.js), frontend service (React), and database (MongoDB).
- **Monitoring**: Utilizes Prometheus for monitoring and Grafana for visualization.

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/edqzic58yebbm0s1un8e.png)

## Step 4: Deactivating the Virtual Environment

Once you're done working in the virtual environment, you can deactivate it by running:

```bash
deactivate
```

This command returns you to the system’s default Python interpreter with all its installed libraries.

By following these steps, you've successfully set up a virtual environment, installed necessary dependencies, and run a Python script to generate an architecture diagram for a bookstore application.

## Benefits & Use-cases of Diagram as code

Diagrams as code offer numerous benefits in real-time project scenarios, providing a powerful and efficient way to manage and visualize complex system architectures. Here are some typical use-cases:

1. Documentation and Communication
Architecture Documentation: Automatically generate up-to-date diagrams that accurately reflect the current state of the system architecture. This ensures that documentation is always current and avoids the pitfalls of manually maintained diagrams.
Team Communication: Facilitate better communication among team members by providing a clear and consistent visualization of the architecture, which can be easily shared and discussed.

2. Infrastructure as Code (IaC) Integration
IaC Synchronization: Use diagrams as code to keep architecture diagrams in sync with the actual infrastructure managed by tools like Terraform, CloudFormation, or Ansible. This provides a visual representation of the infrastructure that matches the code.
Automated Updates: Automatically update architecture diagrams as part of the CI/CD pipeline whenever changes are made to the IaC scripts. This ensures that diagrams reflect the latest infrastructure changes.

3. CI/CD Pipeline Integration
Pipeline Visualization: Visualize the CI/CD pipeline stages and the flow of code from development to production. This helps in understanding the deployment process and identifying potential bottlenecks.
Deployment Architecture: Generate diagrams that show the architecture of the deployed application, including microservices, databases, and other components. This can be especially useful for troubleshooting and optimizing deployment strategies.

4. Microservices and Distributed Systems
Service Dependencies: Visualize the dependencies and interactions between microservices in a distributed system. This helps in understanding the overall system behavior and identifying potential points of failure.
Dynamic Environments: Automatically generate diagrams for dynamic environments where services and dependencies may frequently change. This ensures that the architecture diagram remains accurate and up-to-date.

## Conclusion

You've now successfully created an architecture diagram as code for a 2-tier bookstore application. This method allows for easy updates, version control, and integration into CI/CD pipelines, making it an efficient tool for modern software development practices.

## Docs Reference
[Python Diagrams](https://diagrams.mingrammer.com/)

[Installation](https://diagrams.mingrammer.com/docs/getting-started/installation)

[Examples](https://diagrams.mingrammer.com/docs/getting-started/examples)

Share your views about creating Architecture Diagrams as code.