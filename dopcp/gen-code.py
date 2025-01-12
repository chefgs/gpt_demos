import os

# Define the folder structure
project_structure = {
    "project-root": {
        "backend": {
            "src": {
                "controllers": {},
                "models": {},
                "routes": {},
                "services": {},
                "utils": {}
            },
            ".env": None,
            "server.js": None,
        },
        "frontend": {
            "pages": {
                "api": {},
                "dashboard.js": None,
                "login.js": None,
                "onboarding.js": None
            },
            "components": {},
            "styles": {},
            "next.config.js": None,
            ".env.local": None,
        },
        "deploy": {
            "terraform": {},
            "docker": {},
            "aws-cdk": {},
            "README.md": None,
        },
        "README.md": None,
        "package.json": None,
        ".gitignore": None,
        ".prettierrc": None,
    }
}

# Create the folder structure
def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            with open(path, "w") as f:
                if name == "README.md":
                    f.write(generate_readme())
                elif name in [".env", ".env.local"]:
                    f.write(generate_env_content())
                elif name == "server.js":
                    f.write(generate_server_js())
                elif name == "next.config.js":
                    f.write(generate_next_config())
                elif name == "dashboard.js":
                    f.write(generate_dashboard_page())
                elif name == "login.js":
                    f.write(generate_login_page())
                elif name == "onboarding.js":
                    f.write(generate_onboarding_page())
                elif name == "package.json":
                    f.write(generate_package_json())
                elif name == ".gitignore":
                    f.write(generate_gitignore())
                elif name == ".prettierrc":
                    f.write("{}")

# Generate content for README.md
def generate_readme():
    return """
# DevOps & Cloud Automation Platform

## Overview
This project is a web application for DevOps and cloud automation. It enables users to:
- Authenticate using GitHub OAuth.
- Integrate and manage repositories.
- Deploy applications to AWS.

## Setup Instructions

### 1. GitHub OAuth App Setup
1. Navigate to [GitHub Developer Settings](https://github.com/settings/developers).
2. Under **OAuth Apps**, click **New OAuth App**.
3. Fill out the details:
   - **Application Name**: DevOps Cloud Platform
   - **Homepage URL**: `http://localhost:3000`
   - **Authorization Callback URL**: `http://localhost:3000/api/auth/callback/github`
4. After registration, note the **Client ID** and generate a **Client Secret**.

### 2. Environment Variables
- Backend (`backend/.env`):
  ```env
  MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/mydb
  JWT_SECRET=your_jwt_secret
  GITHUB_CLIENT_ID=your_client_id
  GITHUB_CLIENT_SECRET=your_client_secret
  AWS_ACCESS_KEY_ID=your_aws_access_key
  AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
  PORT=5000
  ```
- Frontend (`frontend/.env.local`):
  ```env
  NEXT_PUBLIC_BACKEND_URL=http://localhost:5000
  NEXTAUTH_SECRET=your_nextauth_secret
  GITHUB_CLIENT_ID=your_client_id
  GITHUB_CLIENT_SECRET=your_client_secret
  ```

### 3. Run Locally
- **Backend**:
  ```bash
  cd backend
  npm install
  npm start
  ```
- **Frontend**:
  ```bash
  cd frontend
  npm install
  npm run dev
  ```
- Access the application at `http://localhost:3000`.

### 4. Deploy to AWS
1. Configure AWS CLI:
   ```bash
   aws configure
   ```
2. Navigate to the Terraform directory:
   ```bash
   cd deploy/terraform
   terraform init
   terraform apply
   ```
3. SSH into the EC2 instance and deploy the backend and frontend.

---

### Technologies Used
- Next.js (Frontend)
- Node.js (Backend)
- MongoDB (Database)
- AWS (Cloud Deployment)
- Terraform (Infrastructure as Code)

## License
MIT
"""

# Generate content for .env files
def generate_env_content():
    return "# Add your environment variables here\n"

# Generate content for server.js
def generate_server_js():
    return """const express = require('express');
const mongoose = require('mongoose');
require('dotenv').config();

const app = express();
app.use(express.json());

// MongoDB connection
mongoose.connect(process.env.MONGO_URI, { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => console.log('Connected to MongoDB'))
    .catch(err => console.error('Failed to connect to MongoDB:', err));

app.get('/', (req, res) => res.send('Backend is running'));

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
"""

# Generate content for next.config.js
def generate_next_config():
    return """module.exports = {
    reactStrictMode: true,
};
"""

# Generate content for dashboard.js
def generate_dashboard_page():
    return """import React from 'react';

const Dashboard = () => {
    return <h1>Dashboard</h1>;
};

export default Dashboard;
"""

# Generate content for login.js
def generate_login_page():
    return """import React from 'react';

const Login = () => {
    return <h1>Login Page</h1>;
};

export default Login;
"""

# Generate content for onboarding.js
def generate_onboarding_page():
    return """import React from 'react';

const Onboarding = () => {
    return <h1>Onboarding Page</h1>;
};

export default Onboarding;
"""

# Generate content for package.json
def generate_package_json():
    return """{
  "name": "devops-cloud-platform",
  "version": "1.0.0",
  "scripts": {
    "start": "node server.js",
    "dev": "next dev"
  },
  "dependencies": {
    "express": "^4.18.2",
    "mongoose": "^6.10.2",
    "next": "^13.0.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0"
  }
}
"""

# Generate content for .gitignore
def generate_gitignore():
    return """
# Node modules
node_modules/

# Environment files
.env
.env.local

# Logs
logs/
*.log
"""

# Run the generator
if __name__ == "__main__":
    base_path = os.getcwd()
    create_structure(base_path, project_structure)
    print("Project structure generated successfully.")
