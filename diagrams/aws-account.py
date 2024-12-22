from diagrams import Diagram, Cluster
from diagrams.aws.management import Organizations, ControlTower
from diagrams.aws.security import IAMRole, IAMPermissions
from diagrams.aws.general import User
from diagrams.aws.security import IdentityAndAccessManagementIamMfaToken as IAMMfaToken

# Create a diagram for the AWS Account Setup, User Access, and IAM RBAC
with Diagram("AWS Account Setup and IAM RBAC", show=False, direction="LR"):
    with Cluster("AWS Organization"):
        organizations = Organizations("AWS Organizations")
        control_tower = ControlTower("AWS Control Tower")
    
    root_account = User("Root Account")
    admin_role = IAMRole("Admin Role")
    user_role = IAMRole("User Role")
    
    with Cluster("IAM Access Setup"):
        root_mfa = IAMMfaToken("Root MFA Setup")
        admin_access = IAMPermissions("Admin Access Policy")
        user_access = IAMPermissions("User Access Policy")
        password_policy = IAMPermissions("Password Policy")

    # Connections
    root_account >> root_mfa
    organizations >> control_tower
    control_tower >> [admin_role, user_role]
    admin_role >> admin_access
    user_role >> user_access
    user_role >> password_policy
    admin_role >> password_policy