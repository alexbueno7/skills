# Audaks Cloud API — referência de endpoints

Base: `https://api.audaks.com.br/api`. Auth: `Authorization: Bearer $AUDAKS_API_TOKEN`. Gerado dos Swagger `ceph.yaml`/`alto.yaml`.

Colunas: método, path, params (query/path), body (content-type + exemplo resumido).

## Alto (compute: VMs, storage, rede, LB, DNS, billing, conta)

### Authentication

- `POST /login` — Login  
  body: multipart/form-data
- `POST /reset-password` — Send Password Reset Link  
  body: multipart/form-data
- `POST /reset-password/{RESET_PASSWORD_TOKEN}` — Reset Password  
  params: RESET_PASSWORD_TOKEN(path)  
  body: multipart/form-data
- `POST /mfa/send-otp` — Send 2FA Verification OTP
- `POST /mfa/verify-otp` — 2FA Verification  
  body: multipart/form-data
### Registration

- `POST /register` — Customer Registration  
  body: multipart/form-data
### Dashboard

- `GET /analytics/account/services/counts` — Services Count
### Projects > Icons

- `GET /project-icons` — List Project Icons
### Projects > Project User

- `GET /projects/{PROJECT_SLUG}/users` — Project Users  
  params: include(query), PROJECT_SLUG(path)
- `POST /projects/{PROJECT_SLUG}/users` — Add User To Project  
  params: PROJECT_SLUG(path)  
  body (application/json): `{"users": ["9e131115-7367-40e5-97aa-7a3624c3e5a4"]}`
### Projects

- `GET /projects` — List Projects  
  params: include(query)
- `POST /projects` — Create Project  
  body: multipart/form-data
- `GET /projects/dashboard/{PROJECT_SLUG}/services` — Project Dashboard  
  params: PROJECT_SLUG(path)
- `PUT /projects/{PROJECT_SLUG}` — Update Project  
  params: PROJECT_SLUG(path)  
  body: multipart/form-data
### Virtual Machine > Virtual Machine Settings > Interfaces

- `POST /virtual-machines/{VIRTUAL_MACHINE_SLUG}/attach-network` — Add Network  
  params: VIRTUAL_MACHINE_SLUG(path)  
  body: multipart/form-data
- `POST /security-groups/{SECURITY_GROUP_SLUG}/attach-to-vm` — Attach Security Group  
  params: SECURITY_GROUP_SLUG(path)  
  body: multipart/form-data
- `POST /security-groups/{SECURITY_GROUP_SLUG}/detach-from-vm` — Detach Security Group  
  params: SECURITY_GROUP_SLUG(path)  
  body: multipart/form-data
- `POST /virtual-machines/{VIRTUAL_MACHINE_SLUG}/detach-network` — Detach Network  
  params: VIRTUAL_MACHINE_SLUG(path)  
  body: multipart/form-data
### Blockstorage

- `GET /blockstorages` — List Blockstorages  
  params: include(query)
- `POST /blockstorages` — Create Blockstorage  
  body: multipart/form-data
### Virtual Machine > Virtual Machine Settings

- `POST /virtual-machines/{VIRTUAL_MACHINE_SLUG}/change-label` — Change Hostname  
  params: VIRTUAL_MACHINE_SLUG(path)  
  body: multipart/form-data
- `GET /plans/service/Virtual Machine` — Change Plans  
  params: include(query), filter[cloud_provider](query), filter[region](query), cpu(query), memory(query), storage(query), filter[storage_category](query), template(query)
- `POST /virtual-machines/{VIRTUAL_MACHINE_SLUG}/change-plan` — Change Plan  
  params: Accept(header), VIRTUAL_MACHINE_SLUG(path)  
  body (application/json): `{"plan": "box2cm4", "slug": "vm-af1m8nf9-u", "vm": "vm-af1m8nf9-u", "template_type": "Operating System", "with_change_plan": true, "custom_plan": null, "billing_cycle": "hourly", "coupon": null, "is_free_trial_plan": false}`
### Virtual Machine

- `GET /virtual-machines` — List Virtual Machines  
  params: include(query)
- `POST /virtual-machines` — Create Virtual Machine  
  body (application/json): `{"name": "vm-o0gnt0yaht", "cloud_provider": "alto", "server": "cloud-compute", "project": "default-126", "region": "frankfurt", "networks": [], "network_type": "Input is not a string.", "billing_cycle": "hourly", "template": "ubuntu-2204-1", "instance_confirm_password": null, "instance_password": nu…`
- `GET /virtual-machines/{VIRTUAL_MACHINE_SLUG}` — Show Virtual Machine  
  params: include(query), VIRTUAL_MACHINE_SLUG(path)
- `PUT /virtual-machines/{VIRTUAL_MACHINE_SLUG}/stop` — Stop Virtual Machine  
  params: VIRTUAL_MACHINE_SLUG(path)
- `PUT /virtual-machines/{VIRTUAL_MACHINE_SLUG}/start` — Start Virtual Machine  
  params: VIRTUAL_MACHINE_SLUG(path)
- `PUT /virtual-machines/{VIRTUAL_MACHINE_SLUG}/reset` — Reset Virtual Machine  
  params: VIRTUAL_MACHINE_SLUG(path)
- `GET /loggers/service/VirtualMachine/{VIRTUAL_MACHINE_SLUG}` — Virtual Machine Activity Logs  
  params: VIRTUAL_MACHINE_SLUG(path)
### Blockstorage

- `POST /blockstorages/{BLOCK_STORAGE_SLUG}/attach` — Blockstorage Attach VM  
  params: BLOCK_STORAGE_SLUG(path)  
  body: multipart/form-data
- `POST /blockstorages/{BLOCK_STORAGE_SLUG}/detach` — Blockstorage Detach VM  
  params: BLOCK_STORAGE_SLUG(path)
- `POST /blockstorages/{BLOCK_STORAGE_SLUG}/resize` — Resize Blockstorage  
  params: BLOCK_STORAGE_SLUG(path)  
  body: multipart/form-data
### Snapshot > Block Storage Snapshot

- `GET /blockstorages/snapshots` — List Snapshots  
  params: include(query)
- `POST /blockstorages/{BLOCK_STORAGE_SLUG}/snapshots` — Create Snapshot  
  params: BLOCK_STORAGE_SLUG(path)  
  body: multipart/form-data
### Backups > Blockstorage Backup

- `GET /blockstorages/backups` — Blockstorage Backups
- `POST /blockstorages/{BLOCK_STORAGE_SLUG}/backups` — Create Blockstorage Backup  
  params: BLOCK_STORAGE_SLUG(path)  
  body: multipart/form-data
- `DELETE /blockstorages/backups/{BLOCK_STORAGE_BACKUP_SLUG}` — Destroy Blockstorage Backup  
  params: BLOCK_STORAGE_BACKUP_SLUG(path)
- `POST /blockstorages/backups/{BLOCK_STORAGE_BACKUP_SLUG}/restore` — Restore Blockstorage Backup  
  params: BLOCK_STORAGE_BACKUP_SLUG(path)
### Loadbalancer

- `GET /load-balancers` — List Loadbalancers  
  params: include(query)
- `POST /load-balancers` — Create Loadbalancer  
  body (application/json): `{"cloud_provider": "alto", "network": "sm26-vn-01", "region": "istanbul", "project": "default-108", "rules": [{"virtual_machines": [], "protocol": "UDP", "enable_tls_protocol": false, "enable_proxy_protocol": false, "algorithm": "roundrobin", "name": "Test Rule", "public_port": "80", "private_port":…`
- `POST /load-balancers/{LOADBALANCER_SLUG}/load-balancer-rules` — Create Load Balancer Rule  
  params: LOADBALANCER_SLUG(path)  
  body (application/json): `{"rules": [{"name": "Test Rule", "public_port": "80", "private_port": "44", "protocol": "UDP", "algorithm": "roundrobin", "virtual_machines": [{"slug": "vm-e5ljf4bnvg", "ipaddress": ""}], "cloud_provider_name": "alto", "enable_tls_protocol": false, "enable_proxy_protocol": false}]}`
- `POST /load-balancers/{LOADBALANCER_SLUG}/load-balancer-rules/{LOADBALANCER_RULE_ID}/attach` — Load Balancer Rule Attach VM  
  params: LOADBALANCER_SLUG(path), LOADBALANCER_RULE_ID(path)  
  body (application/json): `{"virtual_machines": ["vm-e5ljf4bnvg"], "cloud_provider": "alto", "region": "istanbul", "project": "default-108"}`
- `POST /load-balancers/{LOADBALANCER_SLUG}/load-balancer-rules/{LOADBALANCER_RULE_ID}/detach` — Loadbalancer Rule Detach VM  
  params: LOADBALANCER_SLUG(path), LOADBALANCER_RULE_ID(path)
- `DELETE /load-balancers/{LOADBALANCER_SLUG}/load-balancer-rules/{LOADBALANCER_RULE_ID}` — Delete Loadbalancer Rule  
  params: LOADBALANCER_SLUG(path), LOADBALANCER_RULE_ID(path)
### Apps

- `GET /marketplace-apps` — Apps List  
  params: filter[region](query), include(query)
### Monitoring

- `GET /monitoring/global` — Monitoring Resources
- `GET /monitoring/{VIRTUAL_MACHINE_SLUG}/cpu-usage` — CPU Usage  
  params: vm(query), chart(query), virtual_machine(query), monitoring_chart(query), filter_by(query), hours(query), VIRTUAL_MACHINE_SLUG(path)
- `GET /monitoring/{VIRTUAL_MACHINE_SLUG}/disk-read-write` — Disk Read Write  
  params: vm(query), chart(query), virtual_machine(query), monitoring_chart(query), filter_by(query), hours(query), VIRTUAL_MACHINE_SLUG(path)
- `GET /monitoring/{VIRTUAL_MACHINE_SLUG}/memory-usage` — Memory Usage  
  params: vm(query), chart(query), virtual_machine(query), monitoring_chart(query), filter_by(query), hours(query), VIRTUAL_MACHINE_SLUG(path)
- `GET /monitoring/{VIRTUAL_MACHINE_SLUG}/network-traffic` — Network Traffic  
  params: vm(query), chart(query), virtual_machine(query), monitoring_chart(query), filter_by(query), hours(query), VIRTUAL_MACHINE_SLUG(path)
- `GET /monitoring/{VIRTUAL_MACHINE_SLUG}/disk-io-read-write` — Disk IO Read  
  params: vm(query), chart(query), virtual_machine(query), monitoring_chart(query), filter_by(query), hours(query), VIRTUAL_MACHINE_SLUG(path)
- `GET /monitoring/charts` — Charts  
  params: filter[os_family](query), filter[virtual_machine](query)
### Networks > Categories

- `GET /network/categories` — List Network Categories
### Networks > Virtual Network > Subnet

- `GET /networks/{NETWORK_SLUG}/subnet` — Subnets List  
  params: NETWORK_SLUG(path)
- `POST /networks/{NETWORK_SLUG}/subnet` — Add Subnet  
  params: NETWORK_SLUG(path)  
  body (application/json): `{"name": "Test", "size": "30", "cidr": "10.0.0.0", "cloud_provider": "alto", "ipVersion": 4, "dns_nameservers": ["8.8.8.8"], "gateway_ip": "198.2.0.1"}`
- `DELETE /networks/{NETWORK_SLUG}/subnet/{SUBNET_ID}` — Delete Subnet  
  params: NETWORK_SLUG(path), SUBNET_ID(path)
### Networks > Virtual Network > Port

- `GET /networks/{NETWORK_SLUG}/ports` — List network Ports  
  params: NETWORK_SLUG(path)
- `DELETE /networks/{NETWORK_SLUG}/ports/{NETWORK_PORT_ID}` — Delete Network Port  
  params: NETWORK_SLUG(path), NETWORK_PORT_ID(path)
### Networks > Virtual Network

- `GET /networks` — List Networks  
  params: include(query)
- `POST /networks` — Create Network  
  body: multipart/form-data
### Networks > Virtual Router

- `GET /virtual-routers` — List Virtual Routers
- `POST /virtual-routers` — Create Virtual Router  
  body: multipart/form-data
- `PUT /virtual-routers/{VIRTUAL_ROUTER_SLUG}/reboot` — Revert Virtual Router  
  params: VIRTUAL_ROUTER_SLUG(path)
### Networks > IP Address

- `GET /ipaddresses` — List IP Addresses  
  params: filter[is_internal](query), sort(query), page(query), limit(query), include(query)
- `POST /ipaddresses` — Create IP Address  
  body: multipart/form-data
- `POST /virtual-machines/{VIRTUAL_MACHINE_SLUG}/attach-public-network` — Attach VM  
  params: VIRTUAL_MACHINE_SLUG(path)  
  body: multipart/form-data
- `DELETE /ipaddresses/{IP_ADDRESS}` — Release IP Address  
  params: IP_ADDRESS(path)
### Networks > VPN

- `GET /vpns` — VPN List
- `POST /vpns` — Create VPN  
  body (application/json): `{"ike_policy": {"cloud_provider": "alto", "phase1_negotiation_mode": "main", "auth_algorithm": "sha1", "encryption_algorithm": "aes-128", "pfs": "group5", "lifetime": {"units": "seconds", "value": 3600}, "ike_version": "v2", "name": "Test", "description": "this is description", "slug": "create_new",…`
- `DELETE /vpn-users/{VPN_USER_SLUG}` — Delete VPN User  
  params: VPN_USER_SLUG(path)
- `PUT /vpns/ipsec-site-connections/{VPN_SLUG}` — Update VPN  
  params: VPN_SLUG(path)  
  body (application/json): `{"project": "default-126", "region": "istanbul", "cloud_provider": "alto", "site_connections": {"psk": "example-password", "initiator": "bi-directional", "mtu": 1500, "dpd": {"action": "hold", "interval": 30, "timeout": 120}, "peer_address": "10.0.0.10", "peer_id": "", "name": "Test", "description"…`
### Networks > Security Groups

- `GET /security-groups` — List Security Groups  
  params: filter[provider](query), sort(query), page(query), limit(query)
- `POST /security-groups` — Create Security Group  
  body: multipart/form-data
- `DELETE /security-groups/{SECURITY_GROUP_SLUG}` — Delete Security Group  
  params: provider(query), SECURITY_GROUP_SLUG(path)
- `POST /security-groups/{SECURITY_GROUP_SLUG}/add-rule` — Security Group Add Rule  
  params: SECURITY_GROUP_SLUG(path)  
  body (application/json): `{"provider": "alto", "rules": [{"direction": "egress", "ethertype": "IPv4", "id": "b1619fed-3b26-4f9b-8582-5cd4b0099490", "portRangeMax": null, "portRangeMin": null, "protocol": null, "remoteGroupId": null, "remoteIpPrefix": "0.0.0.0/0", "securityGroupId": "4bb80ff7-87b1-49f6-b695-639b7f840f23", "te…`
- `POST /security-groups/{SECURITY_GROUP_SLUG}/delete-rule/{SECURITY_GROUP_RULE_ID}` — Delete Security Group Rule  
  params: SECURITY_GROUP_SLUG(path), SECURITY_GROUP_RULE_ID(path)
### Billing > Subscriptions

- `GET /billing/service-cancel-requests` — List Scheduled Subscriptions  
  params: sort(query), page(query), limit(query), include(query)
### Service Cancellation Request

- `POST /billing/service-cancel-requests/{SERVICE_SLUG}` — Service Cancel Request  
  params: SERVICE_SLUG(path)  
  body: multipart/form-data
### DNS

- `GET /dns/domains` — DNS Domain List  
  params: include(query)
- `POST /dns/domains` — Create DNS Domain  
  body: multipart/form-data
- `GET /dns/domains/{DNS_SLUG}` — Show DNS Domain Details  
  params: dns_provider(query), DNS_SLUG(path)
- `DELETE /dns/domains/{DNS_SLUG}` — Delete DNS Domain  
  params: DNS_SLUG(path)
- `POST /dns/domains/{DNS_SLUG}/records` — Create DNS Domain Record  
  params: DNS_SLUG(path)  
  body: multipart/form-data
- `DELETE /dns/domains/{DNS_SLUG}/records` — Delete DNS Domain Record  
  params: DNS_SLUG(path)
### Billing > Subscriptions

- `GET /billing/subscriptions/active` — List Active Subscriptions  
  params: sort(query), page(query), limit(query), includes(query)
- `GET /billing/subscriptions/inactive` — List Inactive Subscriptions  
  params: sort(query), page(query), limit(query), includes(query)
### Billing > Payment Transactions

- `GET /account/payments` — List Payment Transactions  
  params: sort(query), page(query), limit(query), include(query)
### Billing > Account Statement

- `GET /billing/invoices-count` — Invoices Count
- `GET /billing/invoices` — List Invoices  
  params: filter[created_between](query), sort(query), page(query), limit(query), include(query)
- `GET /billing/account/usage` — List Usage Details  
  params: include(query), sort(query), page(query), limit(query), filter[created_between](query)
- `GET /account/free-credits` — List Free Credits Usage  
  params: sort(query), page(query), limit(query), include(query)
- `GET /billing/subscriptions/service-contracts` — List Service Contracts  
  params: sort(query), page(query), limit(query), include(query)
- `GET /billing/subscriptions/service-trials` — List Service(Free) Trials  
  params: sort(query), page(query), limit(query), include(query)
### Billing > Coupons

- `GET /account/coupons` — Redeem Coupons
- `POST /account/coupons` — Redeem Coupon  
  body: multipart/form-data
### Billing > Budget Alert Setting

- `GET /billing/budget-alert-settings` — Budget Alert Setting
- `POST /billing/budget-alert-settings` — Create Or Update Budget Alert Setting  
  body: multipart/form-data
### Billing

- `GET /analytics/services/costs` — Cost Per Service
- `GET /account/balance` — Account Balance
- `GET /analytics/month-wise-usage` — Monthly Usage
- `GET /billing/credit-limit` — Credit Limit
### Profile > KYC

- `GET /profile/account/kyc-verification` — KYC Documents
- `POST /profile/account/kyc-verification` — KYC Upload Document  
  body: multipart/form-data
- `DELETE /profile/account/kyc-verification` — Delete KYC Document
- `GET /kyc-settings` — KYC Required Document Details
### Profile > Authentication > Change Password

- `POST /users/change-password` — Change Password  
  body: multipart/form-data
### Profile > Authentication

- `POST /mfa/enable/verify-otp` — Enable 2FA  
  body: multipart/form-data
- `POST /mfa/enable/send-otp` — Send 2FA Enable OTP  
  body: multipart/form-data
- `POST /mfa/disable/verify-otp` — Disable 2FA
- `POST /mfa/disable/send-otp` — Send 2FA Disable OTP  
  body: multipart/form-data
- `POST /account/enforce2fa` — Enable/Disable Enforce 2fa  
  params: Accept(header)  
  body: multipart/form-data
### Profile > Users

- `POST /api/users` — Create User  
  body (application/json): `{"name": "Sub User ", "email": "subuser@gmail.com", "auth_user": "customer", "is_user_password": true, "password": null, "is_partner": false, "is_blocked": 0, "role": "owner", "projects": ["default-126"]}`
- `PUT /api/users/{USER_ID}` — Update User  
  params: USER_ID(path)  
  body (application/json): `{"name": "Sub User", "email": "subuser@gmail.com", "auth_user": "customer", "is_user_password": false, "is_partner": false, "is_blocked": 1, "role": "owner", "projects": ["default-126", "review"]}`
- `POST /users/re-invite/{USER_ID}` — Re Invite Email  
  params: USER_ID(path)
- `DELETE /users/{USER_ID}` — Delete User  
  params: USER_ID(path)
### Profile > API

- `POST /profile/api/enable` — Enable API  
  body: multipart/form-data
- `DELETE /profile/api/disable` — Disable API
- `GET /profile/swagger-doc-links` — Doc Url
- `GET /profile/api/access-token` — Access Token
### Profile > Date & Time

- `POST /profile/time-settings` — Update Setting  
  params: Accept(header)  
  body: multipart/form-data
### Profile > Activity Logs

- `GET /loggers/{CRN}` — Login Activity  
  params: CRN(path)
- `GET /loggers/activity/{CRN}` — Activity Logs  
  params: CRN(path)
### Profile

- `GET /profile` — Get User Profile
- `PUT /profile` — Update User Profile  
  body (application/json): `{"registration_type": "Organization", "name": "Jane Doe", "email": "jane.doe@example.com", "billing_address": {"postal_code": "431001", "country": "India", "state": "Maharashtra", "city": "Achalpur", "line_1": "123 Example Street", "billing_name": "", "billing_email": ""}, "_me…`
- `PUT /profile/company-details` — Update Company Details  
  body (application/json): `{"organization_name": "IT Solution", "tax_number": "", "billing_address": {"country": "Malaysia", "state": "Kedah", "city": "Alor Setar", "line_1": "Pune", "line_2": "", "website": "https://www.google.com", "postal_code": "411001", "billing_name": "Billing", "billing_email": "test@gmail.com", "addit…`
### Support > Ticket Feedback

- `GET /support/ticket-feedbacks/{TICKET_ID}` — Ticket Feedbacks  
  params: TICKET_ID(path)
- `POST /support/ticket-feedbacks/{TICKET_ID}` — Ticket Feedback  
  params: TICKET_ID(path)  
  body: multipart/form-data
### Support

- `GET /support/tickets` — Ticket List  
  params: filter[status](query)
- `POST /support/tickets` — Create Ticket  
  body: multipart/form-data
- `GET /services/Ticket/summary` — Tickets Count
- `GET /support/tickets/{TICKET_ID}` — Show Ticket  
  params: include(query), TICKET_ID(path)
- `DELETE /support/tickets/{TICKET_ID}` — Delete Ticket  
  params: TICKET_ID(path)
- `POST /support/tickets-reply/{TICKET_ID}` — Ticket Reply  
  params: TICKET_ID(path)  
  body: multipart/form-data
- `GET /support/tickets-reply/{TICKET_ID}` — Ticket Replies  
  params: TICKET_ID(path)
- `GET /faqs` — Faqs
### Plans

- `GET /admin/plans/service/Virtual Machine` — List Virtual Machine Plans  
  params: include(query), filter[cloud_provider](query), filter[region](query), filter[storage_category](query), planable(query)
- `GET /plans/service/Virtual Router` — List Virtual Router Plans  
  params: ?sort(query), page(query), limit(query), include(query), filter[cloud_provider](query), filter[region](query), filter[storage_category](query)
- `GET /plans/service/Block Storage` — List Block Storage Plans  
  params: include(query), filter[cloud_provider](query), filter[region](query), filter[storage_category](query)
- `GET /plans/service/Load Balancer` — List Load Balancer Plans  
  params: include(query), filter[cloud_provider](query), filter[region](query)
- `GET /plans/service/Kubernetes` — List Kubernetes Plans  
  params: include(query), filter[region](query), filter[cloud_provider](query), filter[storage_category](query)
- `GET /plans/service/IP Address` — List IP Address Plans  
  params: include(query), filter[cloud_provider](query), filter[region](query)
- `GET /plans/service/Virtual Machine Snapshot` — List  Snapshot Plans  
  params: include(query), filter[cloud_provider](query), filter[region](query)
- `GET /plans/service/My Template` — List  Template Plans  
  params: sort(query), page(query), limit(query), include(query), filter[region](query), filter[cloud_provider](query)
- `GET /plans/service/ISO` — List ISO Plans  
  params: include(query), filter[cloud_provider](query), filter[region](query)
- `GET /plans/service/Backups` — List Backup Plans  
  params: sort(query), page(query), limit(query), include(query), filter[cloud_provider](query), filter[region](query)
- `GET /unit-pricings` — List Unit Pricings Plans  
  params: sort(query), page(query), limit(query), include(query)
### Currencies

- `GET /currencies` — List Currencies
### Billing Cycles

- `GET /billing-cycles` — List Billing Cycles
### Regions

- `GET /regions` — List Regions  
  params: include(query), filter[service](query)
### Templates

- `GET /templates` — List Templates  
  params: filter[region](query), include(query)
### Cloud Providers

- `GET /cloud-providers` — List Cloud Providers  
  params: include(query)
### Servers

- `GET /servers` — List Servers
### Account

- `GET /account/taxations/{COUNTRY}` — List Tax Percentage  
  params: COUNTRY(path)
### Storage Categories

- `GET /storage-categories` — Storage Categories  
  params: filter[cloud_provider](query), filter[region](query), include(query)

> Ceph compartilha os endpoints de conta/projeto/billing/suporte acima; abaixo só os exclusivos.

## Ceph (object storage: conta, projetos, billing, suporte)

