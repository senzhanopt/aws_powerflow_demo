# AWS Power System Demo

Demo of AWS for modern power system calculations.

---

## 🛠️ Tech Stack
- **AWS EC2 / Lambda** – for computation 
- **S3** – for data storage  
- **Python** – for algorithm development  

---

## EC2 with SSH

### On AWS

1. Launch an EC2 instance

2. Allow SSH (port 22) in the security group

3. Key pair: download `.pem` file.


### SSH (from Git Bash)

1. Set key permission

```bash
chmod 400 ~/.ssh/my-key.pem
```

e.g.
```bash
chmod 400 /d/aws_powerflow_demo/powerflow_demo.pem
```

2. Connect to EC2 via SSH

```bash
ssh -i "~/.ssh/my-key.pem" ubuntu@<EC2_PUBLIC_IP>
```

e.g.
```bash
ssh -i /d/aws_powerflow_demo/powerflow_demo.pem ubuntu@13.60.189.133
```

3. Create project folder and exit
```bash
mkdir -p ~/project
exit
```

e.g.
```bash
mkdir -p ~/aws_powerflow_demo
exit
```

4. Upload files from local machine

```bash
scp -i "~/.ssh/my-key.pem" -r ./project ubuntu@<EC2_PUBLIC_IP>:~/project
```

e.g.
```bash
scp -i /d/aws_powerflow_demo/powerflow_demo.pem -r /d/aws_powerflow_demo/data /d/aws_powerflow_demo/main.py /d/aws_powerflow_demo/.python-version /d/aws_powerflow_demo/pyproject.toml ubuntu@13.60.189.133:~/aws_powerflow_demo/
```



### Update Ubuntu and Install UV



```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

If `curl` or `git` not available:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl git
```

Reload shell and verify installation
```bash
source ~/.bashrc
uv --version
```

### Install Python and dependencies
```bash
uv python pin 3.12
uv init
uv add grid-feedback-optimizer
```

or

```bash
uv sync
```

### Run
```bash
uv run main.py
```

### Set up cron job when useful

Edit
```bash
crontab -e
```
e.g.

```bash
* * * * * cd /home/ubuntu/aws_powerflow_demo && /home/ubuntu/aws_powerflow_demo/.venv/bin/python /home/ubuntu/aws_powerflow_demo/main.py >> /home/ubuntu/aws_powerflow_demo/cron.log 2>&1
```

Check cron jobs
```bash
crontab -l
```

Check log
```bash
cat cron.log
```
---

## 📧 Author
**Sen Zhan**  
✉️ [sen.zhan@outlook.com](mailto:sen.zhan@outlook.com)

---

## 📝 License
This project is provided for demonstration purposes.  
Feel free to adapt or extend it with proper attribution.
