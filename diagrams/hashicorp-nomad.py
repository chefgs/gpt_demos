from diagrams import Diagram, Cluster
from diagrams.onprem.compute import Nomad
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.network import Nginx
from diagrams.generic.os import Ubuntu

with Diagram("HashiCorp Nomad High-Level Architecture", show=False):
    with Cluster("Nomad Cluster"):
        server = Nomad("Nomad Server")
        
        with Cluster("Nomad Clients"):
            client1 = Ubuntu("Nomad Client 1")
            client2 = Ubuntu("Nomad Client 2")
        
        with Cluster("Applications"):
            nginx = Nginx("Nginx")
            postgres = PostgreSQL("PostgreSQL")
            
        server >> [client1, client2]
        client1 >> nginx
        client2 >> postgres
        
    monitoring = Prometheus("Monitoring")
    dashboard = Grafana("Dashboard")
    
    server >> monitoring
    monitoring >> dashboard
