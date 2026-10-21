# BÁO CÁO TRIỂN KHAI HỆ THỐNG XÁC THỰC TẬP TRUNG VỚI SAMBA AD DC, KEYCLOAK VÀ NEXTCLOUD

## 1. Thông tin chung

### 1.1. Tên đề tài
Triển khai hệ thống xác thực tập trung sử dụng **Samba AD DC** làm kho danh tính người dùng, **Keycloak** làm cổng xác thực tập trung, và **Nextcloud** làm ứng dụng sử dụng đăng nhập một lần thông qua Keycloak.

### 1.2. Mục tiêu
Mục tiêu của hệ thống là xây dựng một mô hình quản lý tài khoản tập trung, trong đó:

- **Samba AD DC** quản lý người dùng, mật khẩu, nhóm và các thuộc tính LDAP.
- **Keycloak** kết nối tới Samba AD bằng giao thức LDAP để dùng lại các tài khoản đã có.
- **Nextcloud** không xác thực trực tiếp với LDAP mà đăng nhập qua **Keycloak** theo chuẩn **OpenID Connect (OIDC)**.
- Người dùng chỉ cần **một tài khoản được tạo trong Samba** để đăng nhập vào Nextcloud thông qua Keycloak.

### 1.3. Kiến trúc tổng thể

```text
Samba AD DC
   │
   │ LDAP
   ▼
Keycloak
   │
   │ OpenID Connect (OIDC)
   ▼
Nextcloud
```

### 1.4. Thông tin hệ thống triển khai
Trong quá trình triển khai thực tế, hệ thống sử dụng các thông tin sau:

- Máy chủ Samba AD DC:
  - Hostname: `duy-Samba`
  - Domain: `hpa.local`
  - Base DN: `DC=hpa,DC=local`
  - Địa chỉ IP: `172.16.20.77`

- Máy chủ chạy ứng dụng:
  - Hostname: `duy-nextcloud`
  - Nextcloud chạy bằng Docker, container: `nextcloud_app`
  - Keycloak chạy bằng Docker, container: `keycloak-keycloak-1`

- Tên miền ứng dụng:
  - Keycloak: `https://id.km0.vn`
  - Nextcloud: `https://cloudnkd.km0.vn`

- Realm Keycloak sử dụng trong quá trình cấu hình:
  - `duy_keycloak`

---

## 2. Phần 1 - Cài đặt và cấu hình Samba AD DC, đồng thời tạo tài khoản người dùng

## 2.1. Giới thiệu
Samba AD DC là thành phần đóng vai trò như một máy chủ Active Directory. Hệ thống này cho phép quản lý tập trung:

- tài khoản người dùng,
- mật khẩu,
- nhóm người dùng,
- thông tin LDAP,
- Kerberos,
- DNS nội bộ của miền.

Trong mô hình này, Samba AD là **nguồn sự thật duy nhất** về người dùng. Tức là người dùng chỉ được tạo tại Samba, còn các hệ thống khác như Keycloak và Nextcloud chỉ dùng lại tài khoản này để xác thực.

---

## 2.2. Cài đặt các gói cần thiết

Trên máy chủ Ubuntu dùng để triển khai Samba AD DC, cài đặt các gói sau:

```bash
apt update
apt install samba krb5-config winbind smbclient ldap-utils -y
```

Giải thích:
- `samba`: cung cấp dịch vụ AD DC.
- `krb5-config`: cấu hình Kerberos.
- `winbind`: hỗ trợ xác thực và tích hợp domain.
- `smbclient`: tiện ích kiểm tra dịch vụ Samba.
- `ldap-utils`: hỗ trợ kiểm tra LDAP bằng `ldapsearch`, `ldapwhoami`.

---

## 2.3. Provision domain Samba AD

Thực hiện tạo domain mới bằng lệnh:

```bash
samba-tool domain provision --use-rfc2307 --interactive
```

Trong quá trình cấu hình, nhập các thông tin như sau:

- Realm: `HPA.LOCAL`
- Domain: `HPA`
- Server role: `dc`
- DNS backend: `SAMBA_INTERNAL`

Sau khi hoàn tất, Samba sẽ sinh ra cơ sở dữ liệu domain và file cấu hình.

---

## 2.4. Kích hoạt đúng dịch vụ Domain Controller

Dừng các dịch vụ Samba dạng file server thông thường nếu có:

```bash
systemctl stop smbd nmbd winbind
systemctl disable smbd nmbd winbind
```

Bật dịch vụ Samba AD DC:

```bash
systemctl unmask samba-ad-dc
systemctl enable samba-ad-dc
systemctl start samba-ad-dc
```

Kiểm tra trạng thái:

```bash
systemctl status samba-ad-dc
```

Kết quả mong muốn là trạng thái:

```text
Active: active (running)
```
<img width="738" height="516" alt="image" src="https://github.com/user-attachments/assets/985e719c-6fc0-4c05-82ee-d800ea97f8d8" />

---

## 2.5. Kiểm tra thông tin domain

### 2.5.1. Kiểm tra thông tin domain
```bash
samba-tool domain info 127.0.0.1
```

### 2.5.2. Kiểm tra functional level
```bash
samba-tool domain level show
```

### 2.5.3. Liệt kê user mặc định
```bash
samba-tool user list
```

Thông thường sẽ có:
- `Administrator`
- `Guest`
- `krbtgt`

---

## 2.6. Cấu hình DNS nội bộ cho Samba AD

Samba AD phụ thuộc rất lớn vào DNS. Nếu DNS không đúng, LDAP và Kerberos sẽ gặp lỗi.

### 2.6.1. Kiểm tra record LDAP SRV
```bash
host -t SRV _ldap._tcp.hpa.local 127.0.0.1
```

Kết quả đúng phải có dạng:

```text
_ldap._tcp.hpa.local has SRV record 0 100 389 duy-samba.hpa.local.
```


## 2.7. Cấu hình Kerberos

Trong một số trường hợp, file Kerberos mặc định của Ubuntu không trỏ đúng realm của domain mới tạo. Khi đó cần chỉnh lại `/etc/krb5.conf`.

Nội dung cấu hình chuẩn:

```conf
[libdefaults]
    default_realm = HPA.LOCAL
    dns_lookup_realm = false
    dns_lookup_kdc = true
    rdns = false
    forwardable = true
    proxiable = true
    ticket_lifetime = 24h
    renew_lifetime = 7d

[realms]
    HPA.LOCAL = {
        kdc = duy-samba.hpa.local
        admin_server = duy-samba.hpa.local
        default_domain = hpa.local
    }

[domain_realm]
    .hpa.local = HPA.LOCAL
    hpa.local = HPA.LOCAL
```

Sau đó kiểm tra Kerberos:

```bash
kdestroy
kinit Administrator@HPA.LOCAL
klist
```

Nếu thành công, `klist` sẽ hiển thị ticket Kerberos của Administrator.

---

## 2.8. Tạo tài khoản người dùng trong Samba AD

### 2.8.1. Tạo tài khoản mới
Ví dụ tạo tài khoản `nguyenkhanhduy`:

```bash
samba-tool user create nguyenkhanhduy
```

Hệ thống sẽ yêu cầu nhập mật khẩu.

### 2.8.2. Kiểm tra tài khoản đã tạo
```bash
samba-tool user list
```

<img width="377" height="99" alt="image" src="https://github.com/user-attachments/assets/145c83f0-869a-43a0-9175-e330a32bfa25" />

### 2.8.3. Xem thông tin chi tiết user
```bash
samba-tool user show nguyenkhanhduy
```
<img width="712" height="650" alt="image" src="https://github.com/user-attachments/assets/56ae606d-7390-4526-ac4a-ab874e6e9cd0" />


### 2.8.4. Gán email cho user
Để thuận tiện cho Keycloak và ứng dụng web, cần gán thuộc tính `mail`:

```bash
samba-tool user edit nguyenkhanhduy
```

Sau đó thêm dòng:

```text
mail: nguyenkhanhduy@hpa.local
```

Lưu file rồi kiểm tra lại:

```bash
samba-tool user show nguyenkhanhduy
```

### 2.8.5. Đổi mật khẩu user
```bash
samba-tool user setpassword nguyenkhanhduy
```

### 2.8.6. Reset mật khẩu Administrator
```bash
samba-tool user setpassword Administrator
```

---

## 2.9. Tạo group và phân quyền bằng group

### 2.9.1. Tạo group
Ví dụ tạo group dành cho Nextcloud:

```bash
samba-tool group add nextcloud-users
```

### 2.9.2. Thêm user vào group
```bash
samba-tool group addmembers nextcloud-users nguyenkhanhduy
```

### 2.9.3. Kiểm tra group membership
```bash
samba-tool group listmembers nextcloud-users
```
hoặc:

```bash
samba-tool user getgroups nguyenkhanhduy
```
<img width="527" height="38" alt="image" src="https://github.com/user-attachments/assets/641999ce-e1e8-487c-bd38-846e42caa627" />

---


## 3. Phần 2 - Tích hợp Samba LDAP với Keycloak

## 3.1. Mục tiêu
Phần này nhằm mục đích cấu hình Keycloak sử dụng Samba AD DC làm nguồn người dùng thông qua LDAP. Sau khi cấu hình xong:

- Keycloak đọc được user trong Samba,
- người dùng Samba đăng nhập được vào Keycloak,
- Keycloak trở thành cổng xác thực tập trung cho ứng dụng.

---

## 3.2. Truy cập giao diện quản trị Keycloak

Đăng nhập giao diện quản trị Keycloak bằng tài khoản admin.

Chọn realm sử dụng cho hệ thống, ví dụ:

```text
duy_keycloak
```
<img width="1919" height="916" alt="image" src="https://github.com/user-attachments/assets/7e50c21e-d7f6-44e1-99ac-3cc88508f480" />

---

## 3.3. Thêm LDAP provider

Đi tới:

```text
User federation → Add provider → LDAP
```

---

## 3.4. Cấu hình kết nối LDAP

### 3.4.1. Connection settings
Thiết lập như sau:

<img width="1919" height="907" alt="image" src="https://github.com/user-attachments/assets/ac5f0daf-0de5-41c3-8378-e69781370c86" />

- Vendor: `Active Directory`
- Connection URL: `ldap://172.16.20.77`
- Enable StartTLS: bật nếu Samba yêu cầu mã hóa qua cổng 389
- Use Truststore SPI: `Never` nếu đang dùng certificate nội bộ/self-signed
- Connection pooling: bật

<img width="1919" height="735" alt="image" src="https://github.com/user-attachments/assets/c66c0df7-ceca-4d9f-8290-99a55bd1d61e" />


### 3.4.2. Authentication settings
- Bind type: `simple`
- Bind DN:
  ```text
  CN=Administrator,CN=Users,DC=hpa,DC=local
  ```
- Bind credential: mật khẩu của Administrator

<img width="1919" height="915" alt="image" src="https://github.com/user-attachments/assets/9a2d3609-97ad-43a8-be4f-389fe3d027db" />

### 3.4.3. LDAP searching and updating
- Users DN:
  ```text
  CN=Users,DC=hpa,DC=local
  ```
- Edit mode: `READ_ONLY`
- Username LDAP attribute: `sAMAccountName`
- RDN LDAP attribute: `cn`
- UUID LDAP attribute: `objectGUID`
- User object classes:
  ```text
  person, organizationalPerson, user
  ```

---

## 3.5. Test kết nối và xác thực

### Cấu hình Samba config
- Tắt StartTLS
  - Mở Samba config:
   ```
   sudo nano /etc/samba/smb.conf
   ```
  - Trong phần `[global]` thêm dòng:
   ```
   ldap server require strong auth = no
   ```
  - Lưu lại rồi restart:
   ```
   sudo systemctl restart samba-ad-dc
   ```
<img width="926" height="877" alt="image" src="https://github.com/user-attachments/assets/c04a5898-c36d-409d-bd04-c50afd7cea1d" />

Sau khi nhập cấu hình, thực hiện:

- `Test connection`
- `Test authentication`

<img width="1916" height="916" alt="image" src="https://github.com/user-attachments/assets/0aca980a-bcdc-4ed3-9427-25161f486fcf" />


Nếu `Test connection` thành công nhưng `Test authentication` thất bại, cần kiểm tra:
- Bind DN có đúng không,
- mật khẩu của Administrator có đúng không,
- domain DN có đúng là `DC=hpa,DC=local` không.

Trong quá trình triển khai thực tế, lỗi này đã xuất hiện khi dùng nhầm DN `DC=km0,DC=vn`. Sau khi sửa về đúng DN `DC=hpa,DC=local`, quá trình test thành công.

---

## 3.6. Kiểm tra user trong Keycloak

Sau khi LDAP federation hoạt động, vào:

```text
Users
```

Tìm các user như:
- `Administrator`
- `nguyenkhanhduy`

Nếu Keycloak hiển thị được các user này, chứng tỏ LDAP federation đã hoạt động đúng.

Ngoài ra, có thể đăng nhập thử Keycloak bằng:
- `Administrator`
- `nguyenkhanhduy`

Nếu đăng nhập thành công, phần tích hợp Samba LDAP với Keycloak coi như hoàn tất.

<img width="1919" height="748" alt="image" src="https://github.com/user-attachments/assets/d8340343-bcae-4c46-b5f2-217a75105b93" />


---


## 4. Phần 3 - Dùng tài khoản tạo ở Samba để đăng nhập vào Nextcloud thông qua Keycloak

## 4.1. Mục tiêu
Phần này nhằm cấu hình Nextcloud dùng Keycloak làm nhà cung cấp OpenID Connect. Người dùng được tạo tại Samba sẽ:

1. được Keycloak xác thực qua LDAP,
2. nhận token OpenID Connect,
3. đăng nhập vào Nextcloud.

---

## 4.2. Chuẩn bị Nextcloud

Nextcloud được triển khai bằng Docker với container:

```text
nextcloud_app
```

Kiểm tra container:

```bash
docker ps
```

Kiểm tra trạng thái Nextcloud:

```bash
docker exec -u www-data -it nextcloud_app php occ status
```

---

## 4.3. Cài và bật app OIDC trong Nextcloud

Kiểm tra danh sách app:

```bash
docker exec -u www-data -it nextcloud_app php occ app:list
```

Bật app `user_oidc`:

```bash
docker exec -u www-data -it nextcloud_app php occ app:enable user_oidc
```

Nếu cần vô hiệu LDAP trực tiếp để tránh xung đột:
```bash
docker exec -u www-data -it nextcloud_app php occ app:disable user_ldap
```

---

## 4.4. Tạo client Nextcloud trong Keycloak

Trong Keycloak:

```text
Clients → Create client
```

Tạo client với các thông tin:

- Client ID: `nextcloud`

<img width="1919" height="478" alt="image" src="https://github.com/user-attachments/assets/fd0dcbeb-aba6-447b-8a3a-0d8fab120a2d" />

### 4.4.1. Cấu hình client
Thiết lập:
- Root URL:
  ```text
  https://cloudnkd.km0.vn/
  ```
- Home URL:
  ```text
  https://cloudnkd.km0.vn/
  ```
- Valid redirect URIs:
  ```text
  https://cloudnkd.km0.vn/*
  ```
- Web origins:
  ```text
  https://cloudnkd.km0.vn
  ```
- Client authentication: bật
- Standard flow: bật

<img width="1919" height="919" alt="image" src="https://github.com/user-attachments/assets/efa1c22b-4764-46d8-a204-4c7271ffe89c" />


### 4.4.2. Lấy Client Secret
Vào tab `Credentials` để lấy `Client Secret`.

<img width="1919" height="762" alt="image" src="https://github.com/user-attachments/assets/6a940dc4-d71e-4506-adda-35057930f58c" />

---

## 4.5. Kiểm tra Client Scopes và Mappers trong Keycloak

Để Nextcloud nhận diện đúng người dùng, Keycloak phải phát đủ claim:

- `preferred_username`
- `email`
- `name`

Kiểm tra `Client Scopes` của client `nextcloud`:
- `profile`
- `email`

Nếu thiếu, cần thêm vào.

Kiểm tra mappers:
- `preferred_username` phải map từ thuộc tính `username`
- `email` phải map từ thuộc tính email của user
- `name` có thể map từ first name + last name

Đây là bước rất quan trọng. Trong thực tế, khi thiếu `preferred_username`, Nextcloud sẽ báo lỗi:
- `Unexpected error when handling authentication request to identity provider`
- hoặc `Internal Server Error`

---

## 4.6. Cấu hình OpenID Connect trong Nextcloud

Vào:

```text
Settings → OpenID Connect
```
<img width="1919" height="903" alt="image" src="https://github.com/user-attachments/assets/6be10100-31e2-4742-ab46-bed58583cc8c" />

Tạo provider mới.

### 4.6.1. Các thông số cấu hình
- Identifier: ví dụ `duykeycloak`
- Discovery endpoint:
  ```text
  https://id.km0.vn/realms/duy_keycloak/.well-known/openid-configuration
  ```
- Client ID: `nextcloud`
- Client secret: lấy từ Keycloak
- Scope:
  ```text
  openid profile email
  ```
- User ID mapping:
  ```text
  preferred_username
  ```

<img width="808" height="843" alt="image" src="https://github.com/user-attachments/assets/0a94eccd-603b-494c-8cda-8c317a04ad55" />


### 4.6.2. Giải thích
- `preferred_username` là claim dùng để định danh user trong Nextcloud.
- Nếu đặt nhầm `sub`, `email` hoặc `name`, hệ thống có thể không tạo được user hoặc không login được.

---

## 4.7. Đăng nhập bằng tài khoản Samba qua Keycloak

Quy trình hoạt động:

1. Người dùng truy cập `https://cloudnkd.km0.vn`
2. Chọn `Login with Keycloak`
3. Trình duyệt chuyển sang Keycloak
4. Người dùng nhập tài khoản Samba, ví dụ:
   - `nguyenkhanhduy`
   - hoặc `nguyenkhanhduy@hpa.local`

<img width="1919" height="933" alt="image" src="https://github.com/user-attachments/assets/c4111d3d-5ff0-4d19-bc91-77444e88c1ad" />

5. Keycloak xác thực user thông qua LDAP tới Samba AD
6. Nếu thành công, Keycloak trả token OIDC cho Nextcloud
7. Nextcloud lấy `preferred_username` để tạo hoặc ánh xạ user
8. Người dùng đăng nhập thành công vào Nextcloud

<img width="1919" height="942" alt="image" src="https://github.com/user-attachments/assets/09642d24-f7b7-4f94-9c9b-c8034cf3363d" />

---
