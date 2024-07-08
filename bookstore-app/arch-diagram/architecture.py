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