# Nullbyte-Ticketing-System


## Setup

<details>
<summary>STEP 1: Active Directory Domain Controller</summary>

+ Install virtualbox
+ Install latest iso of [Windows Server 2022](https://www.microsoft.com/en-us/evalcenter/download-windows-server-2022?msockid=17947612fb4a6b212c776314fae76acd) or spawn one from any of your favorite service provider
+ Skip Unattended installation.
+ Configure network to use bridge adapter and use default settings
+ Install Ansible from python
+ Set the following environmental variables before executing the playbook

```bash
export DC_GATEWAY='your_gateway'             # Set the gateway address
export DOMAIN='domain_name_to_setup'          # Specify the domain name to be configured
export CURRENT_IP='current_windows_server_ip'  # Current IP address of the Windows server
export SERVER_IP='new_ip_for_domain_controller' # IP address to assign to the Domain Controller
export DC_PASSWORD='domain_controller_password' # Password for the Domain Controller configuration
export RECOVERY_PASSWORD='recovery_password'   # Recovery password for the Domain
export CURRENT_DC_PASSWORD='existing_dc_password' # Current password for the Domain Controller

```
+ Run ansible playbook to deploy configure and promote the server to AD-DC

```bash
cd deployment/configs/
ansible-playbook ansible-playbook Setup-DC.yml 
```
</details>

<details>
<summary>STEP 2: Starting Docker Services</summary>

```bash
docker compose up -d # To start all services
docker compose down --rmi # To stop services
```
or
```bash
sudo docker-compose down
sudo docker-compose up --build
```

Connect to database :
```bash
mysql -h 127.0.0.1 -P 3306 -u nullbyteadmin -p
>rootpassword
```

</details>

