# Hướng dẫn sử dụng SecureCRT cho người mới

> Tài liệu này hướng dẫn cách cài đặt và sử dụng SecureCRT để kết nối tới **Linux Server, Switch, Router, Firewall** bằng SSH/Telnet/Serial, quản lý nhiều phiên làm việc và truyền file bằng SFTP.

> **Lưu ý để ảnh hiển thị trên GitHub:** hãy upload `README.md` và toàn bộ 5 file `.png` bên dưới vào **cùng một thư mục**. Không upload riêng mỗi `README.md`.


---

## 1. SecureCRT là gì?

**SecureCRT** là phần mềm terminal client dùng để truy cập và quản trị thiết bị từ xa. Phần mềm hỗ trợ nhiều giao thức như:

- **SSH2**: giao thức nên dùng khi quản trị server và thiết bị mạng.
- **Telnet**: giao thức cũ, không mã hóa; chỉ nên dùng trong lab hoặc thiết bị cũ.
- **Serial**: kết nối Console qua cổng COM/USB-to-Serial.
- **SFTP**: truyền file an toàn qua kết nối SSH.
- Có thể mở nhiều **Session** dưới dạng tab và lưu cấu hình để dùng lại.

Trang chính thức: https://www.vandyke.com/products/securecrt/

Trang tải chính thức: https://www.vandyke.com/cgi-bin/releases.php?product=securecrt

---

## 2. Giao diện SecureCRT

![Giao diện SecureCRT](./01-giao-dien-securecrt.png)

Các khu vực chính:

| Khu vực | Chức năng |
|---|---|
| **Session Manager** | Lưu, tìm kiếm và sắp xếp các kết nối |
| **Tab Session** | Mở nhiều server/switch/router cùng lúc |
| **Terminal** | Nhập lệnh trên thiết bị từ xa |
| **Menu/Toolbar** | Tạo kết nối, cấu hình, log, SFTP, script... |

---

## 3. Cài đặt SecureCRT trên Windows

### Bước 1: Tải SecureCRT

Truy cập trang tải chính thức:

```text
https://www.vandyke.com/cgi-bin/releases.php?product=securecrt
```

Chọn bản dành cho Windows 64-bit nếu máy của bạn đang dùng Windows 64-bit.

### Bước 2: Cài đặt

1. Chạy file cài đặt `.exe`.
2. Chọn **Next**.
3. Đồng ý điều khoản sử dụng.
4. Chọn thư mục cài đặt.
5. Chọn **Install**.
6. Sau khi cài xong, mở **SecureCRT**.

> SecureCRT là phần mềm thương mại. Hãy sử dụng license hợp lệ hoặc bản đánh giá do VanDyke cung cấp.

---

## 4. Tạo kết nối SSH tới Server/Switch/Router

Ví dụ cần SSH tới thiết bị:

```text
IP: 192.168.1.10
Port: 22
Username: admin
```

![Tạo Session SSH](./02-tao-session-ssh.png)

### Bước 1: Mở Session Manager

Chọn:

```text
File → Connect...
```

hoặc mở **Session Manager** ở cạnh trái.

### Bước 2: Tạo Session mới

Chọn:

```text
New Session
```

### Bước 3: Chọn giao thức

Chọn:

```text
SSH2
```

Sau đó bấm **Next**.

### Bước 4: Nhập thông tin thiết bị

Nhập:

```text
Hostname: 192.168.1.10
Port: 22
Username: admin
```

Trong đó:

- **Hostname**: IP hoặc domain của thiết bị.
- **Port**: SSH mặc định là `22`.
- **Username**: tài khoản đăng nhập.

### Bước 5: Đặt tên Session

Ví dụ:

```text
SW-Core-01
```

Sau đó chọn:

```text
Finish
```

### Bước 6: Kết nối

Double-click vào Session vừa tạo hoặc chọn:

```text
Connect
```

Nhập mật khẩu khi SecureCRT yêu cầu.

---

## 5. Xử lý Host Key khi kết nối SSH lần đầu

Lần đầu SSH tới một thiết bị, SecureCRT có thể hỏi có tin cậy SSH Host Key hay không.

![Host Key](./03-host-key.png)

Bạn nên kiểm tra fingerprint trước khi chọn lưu.

Nếu đúng thiết bị:

```text
Accept & Save
```

Nếu fingerprint thay đổi bất ngờ so với trước đây, hãy kiểm tra nguyên nhân trước khi tiếp tục.

---

## 6. Quick Connect – kết nối nhanh không cần tạo Session trước

Có thể dùng:

```text
File → Quick Connect
```

hoặc phím tắt tùy phiên bản/cấu hình.

Nhập:

```text
Protocol: SSH2
Hostname: 192.168.1.10
Port: 22
Username: admin
```

Sau đó chọn **Connect**.

Quick Connect phù hợp khi bạn chỉ cần truy cập nhanh một thiết bị. Nếu thường xuyên dùng thiết bị đó, nên lưu thành Session.

---

## 7. Quản lý nhiều Session

Bạn có thể tạo thư mục trong **Session Manager** để quản lý thiết bị.

Ví dụ:

```text
Sessions
├── Linux-Servers
│   ├── Web-01
│   ├── DB-01
│   └── Backup-01
│
├── Switch
│   ├── SW-Core-01
│   └── SW-Access-01
│
└── Firewall
    ├── FortiGate-HQ
    └── MikroTik-HQ
```

Cách tạo Folder:

```text
Right-click Sessions → New Folder
```

Sau đó kéo Session vào từng thư mục tương ứng.

---

## 8. Mở nhiều thiết bị bằng Tab

SecureCRT cho phép mở nhiều kết nối trong cùng một cửa sổ.

Ví dụ:

```text
[Ubuntu-01] [Core-Switch] [Firewall] [Router]
```

Việc này rất tiện khi phải:

- kiểm tra nhiều switch;
- cấu hình firewall;
- theo dõi nhiều server;
- so sánh kết quả lệnh giữa các thiết bị.

---

## 9. Kết nối Telnet

Nếu thiết bị cũ chỉ hỗ trợ Telnet:

```text
Protocol: Telnet
Port: 23
```

Sau đó nhập IP thiết bị và kết nối.

> **Cảnh báo:** Telnet không mã hóa username, password và dữ liệu. Không nên dùng Telnet trên Internet hoặc mạng không tin cậy. Hãy ưu tiên SSH.

---

## 10. Kết nối Console/Serial tới Switch hoặc Router

Nếu bạn dùng dây Console USB/Serial:

### Bước 1

Kết nối dây Console với máy tính.

### Bước 2

Mở **Device Manager** trên Windows và kiểm tra cổng COM.

Ví dụ:

```text
COM3
```

### Bước 3

Trong SecureCRT tạo Session mới và chọn:

```text
Protocol: Serial
```

### Bước 4

Cấu hình thông số theo thiết bị.

Ví dụ phổ biến:

```text
Port: COM3
Baud rate: 9600
Data bits: 8
Parity: None
Stop bits: 1
Flow control: None
```

Một số thiết bị sử dụng:

```text
115200 baud
```

Nếu màn hình hiển thị ký tự rác, hãy kiểm tra lại **Baud rate**.

---

## 11. Copy và Paste trong SecureCRT

Trong terminal Linux, tổ hợp `Ctrl+C` thường dùng để dừng tiến trình đang chạy, vì vậy không nên mặc định coi `Ctrl+C` là lệnh Copy.

Có thể dùng menu:

```text
Edit → Copy
Edit → Paste
```

Hoặc cấu hình phím tắt theo nhu cầu trong:

```text
Options / Global Options
```

---

## 12. Truyền file bằng SFTP

Khi SSH server hỗ trợ SFTP, SecureCRT có thể mở SFTP tab.

Chọn:

```text
Transfer → Open SFTP Tab
```

![SFTP SecureCRT](./04-sftp.png)

Một số lệnh SFTP thường dùng:

### Xem thư mục hiện tại trên server

```bash
pwd
```

### Xem thư mục hiện tại trên máy tính

```bash
lpwd
```

### Liệt kê file

```bash
ls
```

### Đổi thư mục trên server

```bash
cd /var/log
```

### Đổi thư mục trên máy tính Windows

```text
lcd C:\Users\User\Desktop
```

### Tải file từ server về máy

```bash
get server.log
```

### Upload file từ máy lên server

```bash
put backup.cfg
```

---

## 13. Đăng nhập bằng SSH Key

SSH Key an toàn và tiện hơn việc nhập mật khẩu liên tục.

Trong SecureCRT có thể tạo hoặc sử dụng private key đã có.

Thông thường bạn sẽ cấu hình trong:

```text
Session Options
→ Connection
→ SSH2
→ Authentication
```

Sau đó ưu tiên phương thức:

```text
PublicKey
```

Private key cần được bảo vệ bằng passphrase nếu có thể.

> Không đưa private key, mật khẩu hoặc file chứa credential lên GitHub.

---

## 14. Bật UTF-8 nếu tiếng Việt hoặc ký tự bị lỗi

Mở:

```text
Session Options
→ Terminal
→ Appearance
```

Tìm mục:

```text
Character encoding
```

Chọn:

```text
UTF-8
```

Sau đó kết nối lại Session.

---

## 15. Lưu log phiên làm việc

SecureCRT có thể ghi lại nội dung terminal để phục vụ kiểm tra lỗi hoặc lưu lịch sử cấu hình.

Có thể sử dụng:

```text
File → Log Session
```

Hoặc cấu hình cố định tại:

```text
Session Options → Log File
```

Khi làm việc với thiết bị mạng, log rất hữu ích để lưu:

- lệnh đã chạy;
- kết quả `show`;
- lỗi SSH;
- debug;
- cấu hình trước/sau thay đổi.

---

## 16. Một số lệnh thường dùng khi SSH vào Linux

### Kiểm tra IP

```bash
ip addr
```

### Kiểm tra route

```bash
ip route
```

### Ping

```bash
ping 8.8.8.8
```

### Kiểm tra DNS

```bash
nslookup google.com
```

hoặc:

```bash
dig google.com
```

### Kiểm tra port đang mở

```bash
ss -tulpn
```

### Kiểm tra dung lượng

```bash
df -h
```

### Kiểm tra RAM

```bash
free -h
```

### Kiểm tra CPU/process

```bash
top
```

---

## 17. Ví dụ dùng SecureCRT với thiết bị mạng

### Cisco

```text
show ip interface brief
show running-config
show vlan brief
show interfaces status
```

### FortiGate CLI

```text
get system status
get system interface
get router info routing-table all
diagnose ip address list
```

### MikroTik CLI

```text
/ip address print
/ip route print
/interface print
```

> Các lệnh phụ thuộc model, phiên bản firmware và quyền của tài khoản.

---

## 18. Các lỗi thường gặp

![Các lỗi SecureCRT thường gặp](./05-loi-thuong-gap.png)

### 18.1 Connection timed out

Nguyên nhân có thể:

- sai IP;
- không có route;
- VPN chưa thông;
- firewall chặn;
- port 22 chưa mở;
- thiết bị tắt.

Kiểm tra từ Windows:

```powershell
ping 192.168.1.10
```

Kiểm tra port SSH:

```powershell
Test-NetConnection 192.168.1.10 -Port 22
```

---

### 18.2 Connection refused

Có thể thiết bị vẫn ping được nhưng SSH chưa chạy.

Linux:

```bash
sudo systemctl status ssh
```

hoặc:

```bash
sudo systemctl status sshd
```

Kiểm tra port:

```bash
ss -tulpn | grep :22
```

---

### 18.3 Authentication failed

Kiểm tra:

```text
Username
Password
SSH Key
Quyền đăng nhập
Authentication method
```

---

### 18.4 Host key has changed

Không nên xóa cảnh báo ngay lập tức.

Hãy xác minh:

- server có vừa cài lại hệ điều hành không;
- SSH host key có được tạo lại không;
- IP có trỏ nhầm sang thiết bị khác không;
- có khả năng bị Man-in-the-Middle hay không.

---

### 18.5 Ký tự hiển thị bị lỗi

Kiểm tra:

```text
Character encoding = UTF-8
```

và Terminal Emulation phù hợp, thường là:

```text
Xterm
```

hoặc:

```text
VT100
```

---

## 19. Mẹo sử dụng SecureCRT hiệu quả

- Tạo Folder để phân loại server/switch/firewall.
- Đặt Session Name theo quy tắc dễ tìm.
- Không lưu password quản trị vào tài liệu GitHub.
- Ưu tiên SSH thay vì Telnet.
- Dùng SSH Key cho server quan trọng.
- Bật logging khi troubleshoot.
- Dùng tab để quản lý nhiều thiết bị.
- Đặt mô tả Session để biết IP, vị trí và chức năng thiết bị.

Ví dụ cách đặt tên:

```text
HN-FW-FortiGate-01
HN-SW-Core-01
HN-SW-Access-T8
HN-Linux-Web-01
```

---

## 20. Bài thực hành cho người mới

### Bài 1 – SSH vào Linux

Thông tin giả lập:

```text
IP: 192.168.1.10
Port: 22
User: admin
```

Thực hiện:

1. Tạo SSH2 Session.
2. Kết nối server.
3. Chạy:

```bash
ip addr
ip route
ping 8.8.8.8
df -h
```

---

### Bài 2 – SSH vào Switch

Thông tin giả lập:

```text
IP: 192.168.1.2
Port: 22
User: admin
```

Thực hiện:

1. Tạo Folder `Switch`.
2. Tạo Session `SW-Core-01`.
3. SSH vào switch.
4. Kiểm tra interface/VLAN theo dòng thiết bị.

---

### Bài 3 – Tải log bằng SFTP

1. SSH vào Linux.
2. Mở SFTP Tab.
3. Chạy:

```bash
cd /var/log
ls
get syslog
```

---

## 21. Sơ đồ cách SecureCRT hoạt động

```text
┌─────────────────────┐
│ Máy tính Windows    │
│ SecureCRT           │
└──────────┬──────────┘
           │
           │ SSH TCP/22
           │
     ┌─────▼─────┐
     │   LAN /   │
     │   VPN /   │
     │ Internet  │
     └─────┬─────┘
           │
    ┌──────┴───────────────┐
    │                      │
┌───▼───────┐        ┌─────▼──────┐
│ Linux     │        │ Switch /   │
│ Server    │        │ Router / FW│
└───────────┘        └────────────┘
```

---

## 22. Tài liệu tham khảo

- VanDyke SecureCRT: https://www.vandyke.com/products/securecrt/
- SecureCRT Download: https://www.vandyke.com/cgi-bin/releases.php?product=securecrt
- SecureCRT Videos: https://www.vandyke.com/products/securecrt/securecrt-video.html
- SecureCRT Tips: https://www.vandyke.com/support/tips/

---

## Tóm tắt nhanh

Để SSH tới một thiết bị bằng SecureCRT:

```text
New Session
→ SSH2
→ Nhập IP
→ Port 22
→ Username
→ Đặt tên Session
→ Connect
→ Kiểm tra Host Key
→ Nhập Password
```

Sau khi đăng nhập thành công, bạn có thể quản trị server, switch, router hoặc firewall trực tiếp trong Terminal của SecureCRT.
