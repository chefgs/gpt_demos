
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
