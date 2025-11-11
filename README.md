# AWS Power System Demo

Demo of Amazon Web Services (AWS) for modern power system calculations.

---

## Tech Stack
- **AWS EC2 / Lambda** – for computation 
- **S3** – for data storage  
- **ECS** - for docker images
- **Python** – for algorithm development  

---

## 🛠️ EC2 with SSH

### 1️⃣ On AWS

1. Launch an EC2 instance

2. Allow SSH (port 22) in the security group

3. Key pair: download `.pem` file.


### 2️⃣ Upload files (from WSL Ubuntu)

1. Set key permission:

```bash
chmod 400 ~/.ssh/my-key.pem
```

2. Connect to EC2 via SSH

```bash
ssh -i ~/.ssh/my-key.pem ubuntu@<EC2_PUBLIC_IP>
```

3. Create project folder and exit
```bash
mkdir -p ~/aws_powerflow_demo
exit
```

4. Upload files from local machine

```bash
scp -i ~/.ssh/my-key.pem -r ./ ubuntu@<EC2_PUBLIC_IP>:~/aws_powerflow_demo/
```

**Recommended**: use `rsync` to skip steps 2-4

```bash
rsync -avz -e "ssh -i ~/.ssh/my_key.pem" --exclude '.git' --exclude '.venv' ./ ubuntu@<EC2_PUBLIC_IP>:~/aws_powerflow_demo/
```


### 3️⃣ Update Ubuntu and Install UV

Connect to EC2 via SSH:

```bash
ssh -i ~/.ssh/my-key.pem ubuntu@<EC2_PUBLIC_IP>
```
Install `uv`:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

If `curl` not available:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl
```

Reload shell and verify installation
```bash
source ~/.bashrc
uv --version
```

### 4️⃣ Install Python and dependencies
```bash
uv python pin 3.12
uv init
uv add grid-feedback-optimizer
```

or (with `.python-version`, `pyproject.toml` or `uv.lock`)

```bash
uv sync
```

### Run
```bash
uv run pf_ec2.py
```

### 5️⃣ Set up cron job (optional)

Edit
```bash
crontab -e
```
e.g.

```bash
* * * * * cd /home/ubuntu/aws_powerflow_demo && /home/ubuntu/aws_powerflow_demo/.venv/bin/python /home/ubuntu/aws_powerflow_demo/pf_ec2.py >> /home/ubuntu/aws_powerflow_demo/cron.log 2>&1
```

Check cron jobs
```bash
crontab -l
```

Check log
```bash
cat cron.log
```

Remove or comment out cronjob
```bash
crontab -r
```

---

## 🛠️ EC2 with S3

### 1️⃣ On AWS

1. Create a bucket `aws-powerflow-data`

2. Create *Access key* under security credentials

### 2️⃣ Install `AWS CLI` and upload files to `S3`

Install:
```bash
sudo apt update
sudo apt upgrade -y
sudo apt install curl unzip -y
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
aws --version
```

Configure credentials using created *Access key*:
```bash
aws configure
```

Upload files to `S3` bucket:
```bash
aws s3 cp ./data/grid.json s3://aws-powerflow-data/grid.json
aws s3 cp ./data/scenario.csv s3://aws-powerflow-data/scenario.csv
```

Remove by:
```bash
aws s3 rm s3://aws-powerflow-data/grid.json
aws s3 rm s3://aws-powerflow-data/scenario.csv
```

Alternatively, upload files by running `python`:
```python
import boto3

s3 = boto3.client('s3')
s3.upload_file('./data/scenario.csv', 'aws-powerflow-data', 'scenario.csv')
s3.upload_file('./data/grid.json', 'aws-powerflow-data', 'grid.json')
```

### 3️⃣ Create IAM Role and modify `EC2` IAM Role: e.g. `AmazonS3FullAccess` for testing

### 4️⃣ Run on local machine or on `EC2`:
```bash
uv run pf_ec2_s3.py
```

The script will read the input files from `S3`, run the simulation locally, and write `is_congested.json` back to `S3`.

---

## 🛠️ Lambda with S3

### 1️⃣ Create a `Dockerfile` and lambda handler function

Build Docker image:
```bash
Docker build -t pf_lambda_s3 .
```

### 2️⃣ Push to AWS ECR
1. Create an ECR repo:
```bash
aws ecr create-repository --repository-name pf_lambda_s3
```

2. Authenticate Docker:
```bash
aws ecr get-login-password --region <your-region> | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<region>.amazonaws.com
```

<!--
aws ecr get-login-password --region eu-north-1 | docker login --username AWS --password-stdin 513689973492.dkr.ecr.eu-north-1.amazonaws.com
-->

3. Tag and push:
```bash
docker tag pf_lambda_s3:latest <account-id>.dkr.ecr.<region>.amazonaws.com/pf_lambda_s3:latest
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/pf_lambda_s3:latest
```

<!--
docker tag pf_lambda_s3:latest 513689973492.dkr.ecr.eu-north-1.amazonaws.com/pf_lambda_s3:latest
docker push 513689973492.dkr.ecr.eu-north-1.amazonaws.com/pf_lambda_s3:latest
-->

### 3️⃣ On AWS `Lambda`
1. Create function using image
2. Configure memory, timeout
3. Add trigger using `S3`, set IAM role

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::aws-powerflow-data",
                "arn:aws:s3:::aws-powerflow-data/*"
            ]
        }
    ]
}
```

### 4️⃣ Test `Lambda` manually
```json
{
  "Records": [
    {
      "s3": {
        "bucket": { "name": "aws-powerflow-data" },
        "object": { "key": "scenario.csv" }
      }
    }
  ]
}

```

Test upload new `scenario.csv` with 
```bash
aws s3 cp data/scenario.csv s3://aws-powerflow-data/scenario.csv
```
and check `S3` to see if the function is triggered.


NB: If dependencies are small (less than 250 MB), one can also upload a `zip` file to `Lambda` rather than building a Docker image. Build with:
```bash
mkdir package
pip install -t package/ grid-feedback-optimizer
cp pf_lambda_s3.py package/
cd package
zip -r ../pf_lambda_s3.zip .
cd ..

```

---

## 📧 Author
**Sen Zhan**  
✉️ [sen.zhan@outlook.com](mailto:sen.zhan@outlook.com)

---

## 📝 License
This project is provided for demonstration purposes.  
Feel free to adapt or extend it with proper attribution.
