from diagrams import Diagram, Cluster
from diagrams.aws.management import Organizations, ControlTower
from diagrams.aws.security import IAMRole, IAMPermissions
from diagrams.aws.general import User
from diagrams.aws.security import IdentityAndAccessManagementIamMfaToken as IAMMfaToken

# Create a diagram for the AWS Account Setup, User Access, and IAM RBAC
with Diagram("AWS Account Setup and IAM RBAC with Users", show=False, direction="LR"):
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

    with Cluster("Admin Users"):
        admin_user1 = User("Admin User 1")
        # admin_user2 = User("Admin User 2")
        admin_mfa1 = IAMMfaToken("Admin User 1 MFA")
        # admin_mfa2 = IAMMfaToken("Admin User 2 MFA")

    with Cluster("Regular Users"):
        user1 = User("User 1")
        # user2 = User("User 2")
        user_mfa1 = IAMMfaToken("User 1 MFA")
        # user_mfa2 = IAMMfaToken("User 2 MFA")

    # Connections
    root_account >> root_mfa
    organizations >> control_tower
    control_tower >> [admin_role, user_role]
    admin_role >> admin_access
    user_role >> user_access
    user_role >> password_policy
    admin_role >> password_policy

    admin_role >> [admin_user1]
    admin_user1 >> admin_mfa1
    admin_user1 >> admin_access
    

    user_role >> [user1]
    user1 >> user_mfa1
    user1 >> user_access
    user1 >> password_policy
