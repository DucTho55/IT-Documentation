# Báo cáo khái niệm mạng cơ bản

## 1. IP Address

### IP là gì

IP (Internet Protocol Address) là địa chỉ định danh của một thiết bị
trong mạng.\
Mỗi thiết bị khi tham gia vào mạng đều phải có một IP để có thể gửi và
nhận dữ liệu.

Ví dụ:

    192.168.1.10
    8.8.8.8

IPv4 có độ dài 32 bit và thường được viết dưới dạng 4 số thập phân.

------------------------------------------------------------------------

## 2. Private IP và Public IP

### Private IP

Private IP là địa chỉ IP dùng trong mạng nội bộ (LAN).\
Các IP này không được định tuyến trên Internet.

Các dải Private IP theo chuẩn RFC1918:

    10.0.0.0 – 10.255.255.255      (10.0.0.0/8)
    172.16.0.0 – 172.31.255.255    (172.16.0.0/12)
    192.168.0.0 – 192.168.255.255  (192.168.0.0/16)

Ví dụ:

    192.168.1.10
    10.0.0.5
    172.16.1.20

Đặc điểm: - Chỉ hoạt động trong mạng nội bộ - Có thể bị trùng giữa các
mạng khác nhau - Thường được cấp bởi DHCP của router

------------------------------------------------------------------------

### Public IP

Public IP là địa chỉ IP có thể truy cập từ Internet toàn cầu.

Ví dụ:

    8.8.8.8
    1.1.1.1
    142.250.190.78

Đặc điểm: - Duy nhất trên Internet - Được cấp bởi ISP hoặc datacenter -
Có thể truy cập trực tiếp từ Internet

Ví dụ hệ thống:

    Laptop (Private IP)      192.168.1.10
    Router (Public IP)       113.190.45.82
    Internet

------------------------------------------------------------------------

# 3. CIDR và Subnet

CIDR cho biết bao nhiêu bit của địa chỉ IP được dùng cho phần mạng.

Ví dụ:

    192.168.1.0/24

/24 nghĩa là 24 bit đầu là network.

------------------------------------------------------------------------

## /24

Subnet mask:

    255.255.255.0

Host:

    254 host

Ví dụ:

    Network      192.168.1.0
    Host range   192.168.1.1 – 192.168.1.254
    Broadcast    192.168.1.255

------------------------------------------------------------------------

## /25

Subnet mask:

    255.255.255.128

Host:

    126 host

------------------------------------------------------------------------

## /26

Subnet mask:

    255.255.255.192

Host:

    62 host

------------------------------------------------------------------------

## /27

Subnet mask:

    255.255.255.224

Host:

    30 host

------------------------------------------------------------------------

## /28

Subnet mask:

    255.255.255.240

Host:

    14 host

------------------------------------------------------------------------

## /29

Subnet mask:

    255.255.255.248

Host:

    6 host

------------------------------------------------------------------------

# 4. Gateway

Gateway là thiết bị cho phép các thiết bị trong mạng LAN đi ra mạng khác
hoặc Internet.

Ví dụ:

    PC        192.168.1.10
    Gateway   192.168.1.1
    Internet

Khi PC muốn truy cập Internet, dữ liệu sẽ gửi đến gateway trước.

------------------------------------------------------------------------

# 5. DHCP

DHCP (Dynamic Host Configuration Protocol) là giao thức cấp phát IP tự
động cho thiết bị trong mạng.

DHCP cấp các thông tin sau:

-   IP address
-   Subnet mask
-   Gateway
-   DNS

Ví dụ DHCP cấp:

    IP       192.168.1.101
    Subnet   255.255.255.0
    Gateway  192.168.1.1
    DNS      8.8.8.8

------------------------------------------------------------------------

# 6. DNS

DNS (Domain Name System) là hệ thống chuyển đổi tên miền thành địa chỉ
IP.

Ví dụ:

    google.com → 142.250.190.78

DNS server phổ biến:

    8.8.8.8
    1.1.1.1

------------------------------------------------------------------------

# 7. NAT

NAT (Network Address Translation) là kỹ thuật chuyển đổi địa chỉ IP khi gói tin đi qua router hoặc firewall.
Nó thường được dùng để cho phép các thiết bị có IP private truy cập Internet bằng IP public.

Ví dụ:

    Laptop          192.168.1.10
    Router NAT      113.190.45.82
    Internet

Luồng:

    192.168.1.10
    ↓
    NAT
    ↓
    113.190.45.82
    ↓
    Internet

Một IP public có thể phục vụ nhiều thiết bị trong LAN.

------------------------------------------------------------------------

# 8. Default Route

Default route là đường đi mặc định khi thiết bị không biết gửi packet đi
đâu.

Ví dụ:

    0.0.0.0/0 → 192.168.1.1

Điều này có nghĩa:

Mọi địa chỉ ngoài mạng nội bộ sẽ gửi đến gateway.

------------------------------------------------------------------------

# 9. Địa chỉ MAC

MAC Address là địa chỉ vật lý của card mạng.

Ví dụ:

    3C:52:82:4A:1F:20

MAC hoạt động ở Layer 2 của mô hình OSI.

IP hoạt động ở Layer 3.

Ví dụ thiết bị:

    IP   192.168.1.10
    MAC  AA:BB:CC:DD:EE:01

Switch dùng MAC address để chuyển dữ liệu trong mạng LAN.
