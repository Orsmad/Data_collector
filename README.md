
# Data Collector for Non-Compliant EC2 Instances [SSM.3]
## Amazon EC2 instances managed by Systems Manager should have an association compliance status of COMPLIANT
This Python project identifies and returns **non-compliant EC2 instances** in an AWS environment using the AWS CLI and boto3. The project analyzes resource compliance summaries and logs the details of non-compliant instances.
More information about this here:
https://docs.aws.amazon.com/securityhub/latest/userguide/ssm-controls.html#ssm-3

Severity: Low

Resource type: AWS::SSM::AssociationCompliance

AWS Config rule: ec2-managedinstance-association-compliance-status-check

---

## Features

- Connects to AWS via boto3.
- Retrieves compliance summaries using the AWS SSM API.
- Filters and identifies non-compliant EC2 instances.
- Provides detailed logs of non-compliance.

---

## Prerequisites

Before running the project, ensure you have the following:

1. **Python**: Version 3.8 or later.
2. **AWS CLI**: Configured with the necessary permissions to access SSM and EC2 services.
3. **Virtual Environment**: For dependency management.
4. **Environment Variables**: Use a `.env` file to store your AWS credentials and other configurations.

---

## Setup Instructions

### 1. Create a Virtual Environment

Create and activate a virtual environment to manage dependencies:

```bash
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```

### 2. Install Dependencies

Install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the project directory with the following content:

```bash
AWS_ACCESS_KEY_ID=<your-aws-access-key-id>
AWS_SECRET_ACCESS_KEY=<your-aws-secret-access-key>
AWS_REGION=<your-aws-region>
SHARD_SIZE=<desired-shard-size>
MAX_WORKERS=<number-of-threads>
```

### 4. Run the Application

Execute the main Python script to run the application:

```bash
python main.py
```

### 5. AWS CLI Commands

You can use the following AWS CLI commands to interact with EC2 and SSM:

```bash
aws ec2 describe-instances 
aws ssm list-resource-compliance-summaries --region <your-region>
```

---

