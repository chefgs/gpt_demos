from diagrams import Diagram, Cluster
from diagrams.aws.management import Organizations, ControlTower
from diagrams.aws.security import IAMPermissions, IAMRole
from diagrams.aws.general import User
from diagrams.aws.compute import Lambda
from diagrams.aws.integration import StepFunctions
from diagrams.aws.security import IdentityAndAccessManagementIamMfaToken as IAMMfaToken

# Create a diagram for the AWS Account Creation Flow
with Diagram("AWS Account Creation Flow", show=False, direction="LR"):
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

    with Cluster("Automation"):
        step_functions = StepFunctions("Account Creation Workflow")
        provisioning_lambda = Lambda("Provisioning Function")
        # compliance_check_lambda = Lambda("Compliance Check Function")

    # Connections
    root_account >> root_mfa
    organizations >> control_tower >> step_functions
    # step_functions >> provisioning_lambda >> compliance_check_lambda
    provisioning_lambda >> [admin_role, user_role]
    admin_role >> admin_access
    user_role >> user_access

    # Connection back to organizations for governance
    [admin_role, user_role] >> organizations
