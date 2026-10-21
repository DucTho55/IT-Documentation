# Báo cáo cài đặt và cấu hình Nextcloud, Keycloak (OIDC)

## 1. Mục tiêu

Thiết lập hệ thống Nextcloud chạy bằng Docker, xác thực người dùng thông
qua Keycloak sử dụng chuẩn OpenID Connect (OIDC). Người dùng đăng nhập
Nextcloud sẽ được chuyển hướng sang Keycloak để xác thực tập trung.

------------------------------------------------------------------------

## 2. Kiến trúc hệ thống

-   Ubuntu Server (VM)
-   Docker & Docker Compose
-   Nextcloud (container)
-   MariaDB/MySQL (container)
-   Keycloak (container)
-   Docker network dùng chung: `sso-net`

Luồng đăng nhập: Người dùng → Nextcloud → Keycloak → Nextcloud

------------------------------------------------------------------------

## 3. Cài đặt Docker trên Ubuntu
- Gỡ bỏ các bản cài đặt cũ (nếu có):
``` bash
sudo apt-get remove docker docker-engine docker.io containerd runc
```
- Cập nhật chỉ mục gói:
``` bash
sudo apt update
sudo apt install ca-certificates curl gnupg lsb-release
```
- Thêm GPG key chính thức của Docker
``` bash
sudo mkdir -m 0755 -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```
- Thiết lập kho lưu trữ (Repository)
``` bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
- Cài đặt Docker Engine
``` bash
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
- Kiểm tra cài đặt
``` bash
sudo docker run hello-world
```

Kiểm tra:

``` bash
docker --version
docker compose version
```

------------------------------------------------------------------------

## 4. Triển khai Nextcloud bằng Docker

### docker-compose.yml
```yaml
sudo nano docker-compose.yml
```

``` yaml
version: "3.8"

services:
  db:
    image: mariadb:10.11
    container_name: nextcloud_db
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: nextcloud
      MYSQL_USER: nextcloud
      MYSQL_PASSWORD: nextcloudpass
    volumes:
      - db:/var/lib/mysql

  app:
    image: nextcloud:latest
    container_name: nextcloud_app
    restart: always
    ports:
      - "8080:80"
    environment:
      MYSQL_HOST: db
      MYSQL_DATABASE: nextcloud
      MYSQL_USER: nextcloud
      MYSQL_PASSWORD: nextcloudpass
    volumes:
      - nextcloud:/var/www/html
    depends_on:
      - db

volumes:
  db:
  nextcloud:
```

Chạy:

``` bash
docker compose up -d
```

Truy cập: http://IP:8080

------------------------------------------------------------------------

## 5. Triển khai Keycloak bằng Docker

### docker-compose.yml

``` yaml
version: "3.8"

services:
  keycloak:
    image: quay.io/keycloak/keycloak:24
    container_name: keycloak
    command: start-dev
    ports:
      - "8090:8080"
    environment:
      KEYCLOAK_ADMIN: admin
      KEYCLOAK_ADMIN_PASSWORD: admin
```

Chạy:

``` bash
docker compose up -d
```

Truy cập: http://IP:8090/admin

------------------------------------------------------------------------

## 6. Kết nối Nextcloud và Keycloak vào cùng Docker network

``` bash
docker network create sso-net
docker network connect sso-net nextcloud_app
docker network connect sso-net keycloak
docker restart nextcloud_app keycloak
```

------------------------------------------------------------------------

## 7. Fix lỗi Discovery endpoint ( quan trọng )
### Bạn có setup như sau:

• Nextcloud chạy Docker container
• Keycloak chạy Docker container
• Discovery endpoint truy cập được từ host
• ❌ Nhưng Nextcloud chặn request HTTP nội bộ (local/private IP)

👉 Đây là cơ chế bảo mật mặc định của Nextcloud
Nó KHÔNG cho gọi OpenID Discovery tới IP LAN / HTTP, nên UI báo:

discovery endpoint is not reachable

Cho dù network OK.

#### B1. Cho phép Nextcloud gọi endpoint nội bộ

Chạy lệnh này trên host (rất quan trọng):
```yaml
docker exec -u www-data nextcloud_app php occ config:system:set allow_local_remote_servers --value=true
```
Kiểm tra lại:
```yaml
docker exec -u www-data nextcloud_app php occ config:system:get allow_local_remote_servers
```

Phải ra:
```yaml
true
```

#### B2. Restart container Nextcloud
```yaml
docker restart nextcloud_app
```
