# GitHub GraphQL Wrapper

A delightful GraphQL wrapper around the GitHub GraphQL API, designed for use with APIsec testing.

When we run our server with `uv run uvicorn githubdata.main:app --reload`, it creates an endpoint we can queru with APIsec NG.

We are using the
We have created a GraphQL wrapper around it to:
  * Make it compatible for testing GraphQL with APIsec
  * Expose a GraphQL interface to their REST API
  * Generate SDL for current testing, and JSON introspection for future testing in APIsec

## Project Structure
```bash
githubdata/
├── githubdata/
│   ├── __init__.py
│   ├── main.py (FastAPI + Strawberry GraphQL app)
│   ├── schema/
│   │   └── types.py (GraphQL type definitions)
│   ├── resolvers/
│   │   └── launch_resolver.py (resolvers that call the REST API)
│   └── services/
│       └── github_api.py (handles REST API calls to api.githubdata.com)
└── scripts/
    └── generate_sdl.py (generates schema for APIsec)
```

## Setup

1. Create a virtual environment:
```bash
uv venv
```

2. Activate the virtual environment:
```bash
source .venv/bin/activate
```

3. Install dependencies:
```bash
# v1 did not package w pyproject.toml
#uv pip install -r requirements.txt
# v2 does
uv pip install -e .
```

## Running the Server

Start the server with:
```bash
uvicorn githubdata.main:app --reload
```

The GraphQL playground will be available at: http://localhost:8000/graphql

## Generating Schema

To generate the introspection schema for APIsec:
```bash
uv run python scripts/generate_schema.py
```

SDL Schema is generated as 'schema.graphql'
JSON Introspection Schema is generated as 'schema.json'

Note:  To generate just the SDL for APIsec:
```bash
uv run python scripts/generate_sdl.py
```

## EC2 Deployment
Based on the [list of common TCP and UDP port numbers](https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers) we chose 9070-9079 to deploy APIs on EC2.

### IAM User
```bash
ssh -vvv -o "IdentitiesOnly yes" -i "/Users/trust/.ssh/jonwilliams.pem" ec2-user@ec2-54-234-103-190.compute-1.amazonaws.com
```

## Deployment Status

The API is currently deployed and accessible at:
- Production: http://54.234.103.190:9070/graphql

### Deployment Information
- Hosting: AWS EC2
- Application Port: 9070
- Reverse Proxy: nginx
- Process Manager: systemd

## Local Development

### EC2 Configuration

We need asdf to manage Python
git clone https://github.com/asdf-vm/asdf.git --branch v0.16.0
git clone https://github.com/asdf-vm/asdf.git --branch v0.16.0

we need go (newer than what amazon has in yum)
wget https://go.dev/dl/go1.23.4.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.23.4.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin

sudo yum groupinstall "Development Tools"


  125  wget https://go.dev/dl/go1.23.4.linux-amd64.tar.gz
  127  sudo tar -C /usr/local -xzf go1.23.4.linux-amd64.tar.gz
  128  echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
  129  echo 'export GOPATH=$HOME/go' >> ~/.bashrc
  130  echo 'export PATH=$PATH:$GOPATH/bin' >> ~/.bashrc
  131  source ~/.bashrc
  132  go version
  133  pwd

  181  git clone https://github.com/asdf-vm/asdf.git --branch v0.16.0
  182  cd asdf
  183  make
  184  sudo cp ./asdf /usr/local/bin
  185  sudo chmod +x /usr/local/bin
  186  asdf
  187  asdf --version

but then python buiild fails
itried
sudo yum install -y gcc zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel tk-devel libffi-devel xz-devel

asdf uninstall python 3.11.11

asdf install python 3.11.11

  198  asdf install python 3.11.11
  199  asdf plugin add uv
  200  asdf plugin add nodejs
  201  asdf install nodejs latest
  202  asdf install uv latest

  [ec2-user@ip-172-31-29-43 asdf]$ asdf list
nodejs
  23.9.0
python
 *3.11.11
uv
  0.6.6

asdf set -u python 3.11.11
asdf set -u nodejs 23.9.0
asdf set -u uv 0.6.6

in local
git init
created empty repo at: https://github.com/kjon-life/apisec-graphql-github
git remote add origin https://github.com/kjon-life/apisec-graphql-github.git && git branch -M main && git push -u origin main

we can also update the remote to use ssh
git remote set-url origin git@github.com:kjon-life/apisec-graphql-github.git && git branch -M main && git push -u origin main

so we have an environment on EC2
[ec2-user@ip-172-31-29-43 asdf]$ uv --version
uv 0.6.6
[ec2-user@ip-172-31-29-43 asdf]$ python --version
Python 3.11.11
[ec2-user@ip-172-31-29-43 asdf]$ node --version
v23.9.0

and the git repo to clone
git@github.com:kjon-life/apisec-graphql-github.git

./scripts/deploy.sh
writes to the app directory to ~/apps/githubdata
The repository URL uses SSH
Uses $USER instead of hardcoded ec2-user
We sudo for commands that require root access
Updated domain to githubdata.kjon.life

copy my key to the server
scp my deploy.sh to the server
chmod +x on deploy.sh

sudo yum install -y nginx
sudo yum install -y nginx && sudo systemctl start nginx && sudo systemctl enable nginx && ./deploy.sh
please note that deploy.sh is idempotent

(I had to run it twice because I forgot to install nginx)
Created symlink /etc/systemd/system/multi-user.target.wants/githubdata.service → /etc/systemd/system/githubdata.service.
[2025-03-12 17:51:49] Deployment completed successfully!
[2025-03-12 17:51:49] Next steps:
[2025-03-12 17:51:49] 1. Configure AWS security group to allow traffic on port 9070
[2025-03-12 17:51:49] 2. Set up SSL certificate with Let's Encrypt

let's check the current NETWORK
sudo ss -tulpn | grep -E ':80|:443|:9070'

check the status of the appllication
systemctl status githubdata

why did it fail to start?
journalctl -u githubdata.service -n 50 | cat

systemd was configured to run main:app from the root dir not the apps/githubdata
sudo sed -i 's/main:app/githubdata.main:app/' /etc/systemd/system/githubdata.service && sudo systemctl daemon-reload && sudo systemctl restart githubdata && systemctl status githubdata

now we check if it is listeing on the port 9070
ss -tulpn | grep 9070

so I can configure this with DNS
http://githubdata.kjon.life
http://githubdata.kjon.life:9070

but for now we will
http://54.234.103.190:9070
http://54.234.103.190

we need the instance-id for EC2
curl http://54.234.108.190/latest/meta-data/instance-id


In the EC2 console, select the running instance
`sg-0c8ce9629b0959a93 - launch-wizard-2`
In the "Security" tab, click on the security group link
Click "Edit inbound rules"
Click "Add rule"
Set the following values:

Type: Custom TCP
Protocol: TCP
Port range: 9070
Source: Anywhere (0.0.0.0/0) for public access or your specific IP
Description: GitHubdata

```bash
http://54.234.103.190:9070/graphql
```

now we go to NG
https://cst.dev.apisecapps.com/
jon+dev@apisec.ai (CST DEV in pwSafe)

Add the application `GitHubdata` with Host URL:
```
http://54.234.103.190:9070/
```
image.png

## Production Deployment

The application is deployed using a custom deployment script. To deploy:

1. SSH into the EC2 instance:
```bash
ssh -i "<key>.pem" ec2-user@54.234.103.190
```

2. Run the deployment script:
```bash
cd ~/apps/githubdata
./scripts/deploy.sh
```

### Service Management

The application runs as a systemd service. Common commands:

```bash
# Check service status
sudo systemctl status githubdata

# Restart service
sudo systemctl restart githubdata

# View logs
journalctl -u githubdata -f
```

### Monitoring

The application can be monitored through:
- systemd service status
- nginx access logs: `/var/log/nginx/access.log`
- nginx error logs: `/var/log/nginx/error.log`
- Application logs: via journalctl

# Appendix

### Getting started



## EC2 Configuration

We need asdf to manage Python
git clone https://github.com/asdf-vm/asdf.git --branch v0.16.0

we need go (newer than what amazon has in yum)
wget https://go.dev/dl/go1.23.4.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.23.4.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin

sudo yum groupinstall "Development Tools"


  125  wget https://go.dev/dl/go1.23.4.linux-amd64.tar.gz
  127  sudo tar -C /usr/local -xzf go1.23.4.linux-amd64.tar.gz
  128  echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
  129  echo 'export GOPATH=$HOME/go' >> ~/.bashrc
  130  echo 'export PATH=$PATH:$GOPATH/bin' >> ~/.bashrc
  131  source ~/.bashrc
  132  go version
  133  pwd

  181  git clone https://github.com/asdf-vm/asdf.git --branch v0.16.0
  182  cd asdf
  183  make
  184  sudo cp ./asdf /usr/local/bin
  185  sudo chmod +x /usr/local/bin
  186  asdf
  187  asdf --version

but then python buiild fails
itried
sudo yum install -y gcc zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel tk-devel libffi-devel xz-devel

asdf uninstall python 3.11.11

asdf install python 3.11.11

  198  asdf install python 3.11.11
  199  asdf plugin add uv
  200  asdf plugin add nodejs
  201  asdf install nodejs latest
  202  asdf install uv latest

  [ec2-user@ip-172-31-29-43 asdf]$ asdf list
nodejs
  23.9.0
python
 *3.11.11
uv
  0.6.6

asdf set -u python 3.11.11
asdf set -u nodejs 23.9.0
asdf set -u uv 0.6.6

in local
git init
created empty repo at: https://github.com/kjon-life/apisec-graphql-github
git remote add origin https://github.com/kjon-life/apisec-graphql-github.git && git branch -M main && git push -u origin main

we can also update the remote to use ssh
git remote set-url origin git@github.com:kjon-life/apisec-graphql-github.git && git branch -M main && git push -u origin main

so we have an environment on EC2
[ec2-user@ip-172-31-29-43 asdf]$ uv --version
uv 0.6.6
[ec2-user@ip-172-31-29-43 asdf]$ python --version
Python 3.11.11
[ec2-user@ip-172-31-29-43 asdf]$ node --version
v23.9.0

and the git repo to clone
git@github.com:kjon-life/apisec-graphql-github.git

./scripts/deploy.sh
writes to the app directory to ~/apps/githubdata
The repository URL uses SSH
Uses $USER instead of hardcoded ec2-user
We sudo for commands that require root access
Updated domain to githubdata.kjon.life

copy my key to the server
scp my deploy.sh to the server
chmod +x on deploy.sh

sudo yum install -y nginx
sudo yum install -y nginx && sudo systemctl start nginx && sudo systemctl enable nginx && ./deploy.sh
please note that deploy.sh is idempotent

(I had to run it twice because I forgot to install nginx)
Created symlink /etc/systemd/system/multi-user.target.wants/githubdata.service → /etc/systemd/system/githubdata.service.
[2025-03-12 17:51:49] Deployment completed successfully!
[2025-03-12 17:51:49] Next steps:
[2025-03-12 17:51:49] 1. Configure AWS security group to allow traffic on port 9070
[2025-03-12 17:51:49] 2. Set up SSL certificate with Let's Encrypt

let's check the current NETWORK
sudo ss -tulpn | grep -E ':80|:443|:9070'

check the status of the appllication
systemctl status githubdata

why did it fail to start?
journalctl -u githubdata.service -n 50 | cat

systemd was configured to run main:app from the root dir not the apps/githubdata
sudo sed -i 's/main:app/githubdata.main:app/' /etc/systemd/system/githubdata.service && sudo systemctl daemon-reload && sudo systemctl restart githubdata && systemctl status githubdata

now we check if it is listeing on the port 9070
ss -tulpn | grep 9070

so I can configure this with DNS
http://githubdata.kjon.life
http://githubdata.kjon.life:9070

but for now we will
http://54.234.103.190:9070
http://54.234.103.190

we need the instance-id for EC2
curl http://54.234.108.190/latest/meta-data/instance-id


In the EC2 console, select the running instance
`sg-0c8ce9629b0959a93 - launch-wizard-2`
In the "Security" tab, click on the security group link
Click "Edit inbound rules"
Click "Add rule"
Set the following values:

Type: Custom TCP
Protocol: TCP
Port range: 9070
Source: Anywhere (0.0.0.0/0) for public access or your specific IP
Description: GitHubdata

```bash
http://54.234.103.190:9070/graphql
```

now we go to NG
https://cst.dev.apisecapps.com/
jon+dev@apisec.ai (CST DEV in pwSafe)

Add the application `GitHubdata` with Host URL:
```
http://54.234.103.190:9070/
```
image.png

# Credits
- GitHub GraphQL API
- APIsec NG
- EC2
- made with ❤️ kjon-life ©2025