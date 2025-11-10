# AWS Power System Demo

Demo of Amazon Web Services (AWS) for modern power system calculations.

---

## Tech Stack
- **AWS EC2 / Lambda** – for computation 
- **S3** – for data storage  
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
uv run main.py
```

### 5️⃣ Set up cron job (optional)

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

Remove or comment out cronjob
```bash
crontab -r
```
---

## 📧 Author
**Sen Zhan**  
✉️ [sen.zhan@outlook.com](mailto:sen.zhan@outlook.com)

---

## 📝 License
This project is provided for demonstration purposes.  
Feel free to adapt or extend it with proper attribution.
