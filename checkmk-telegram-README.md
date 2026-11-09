# CheckMK 2.4 Docker + Proxmox + Windows + Telegram

> Tài liệu thực hành dựa trên quá trình cấu hình thực tế, ảnh chụp màn hình và kết quả kiểm tra ngày 09/11/2026.  
> **Mục đích:** triển khai giám sát hạ tầng với CheckMK 2.4, tự động thông báo qua Telegram, và hạn chế cảnh báo lặp.

[![CheckMK](https://img.shields.io/badge/CheckMK-2.4.0p18-20a090)](https://checkmk.com/) ![Docker](https://img.shields.io/badge/Deployment-Docker-2496ED) ![Guide](https://img.shields.io/badge/Language-Ti%E1%BA%BFng%20Vi%E1%BB%87t-blue)

## Mục lục

1. [Kiến trúc và kết quả](#1-kiến-trúc-và-kết-quả)
2. [Kiểm tra CheckMK Docker](#2-kiểm-tra-checkmk-docker)
3. [Thêm Proxmox vào CheckMK](#3-thêm-proxmox-vào-checkmk)
4. [Tạo Bot và tích hợp Telegram](#4-tạo-bot-và-tích-hợp-telegram)
5. [Tạo Notification Rule Telegram](#5-tạo-notification-rule-telegram)
6. [Cài Windows Agent và sửa lỗi kết nối](#6-cài-windows-agent-và-sửa-lỗi-kết-nối)
7. [Service Discovery và cảnh báo Windows](#7-service-discovery-và-cảnh-báo-windows)
8. [Giảm cảnh báo lặp bằng Delay service notifications](#8-giảm-cảnh-báo-lặp-bằng-delay-service-notifications)
9. [Chẩn đoán NIC Proxmox](#9-chẩn-đoán-nic-proxmox)
10. [Bảo mật, kiểm tra và đưa lên GitHub](#10-bảo-mật-kiểm-tra-và-đưa-lên-github)
11. [Phụ lục ảnh](#11-phụ-lục-ảnh)

## 1. Kiến trúc và kết quả

```text
                         CHECKMK 2.4 (Docker)
                Ubuntu Server 192.168.31.128
                     Site cmk / container monitoring
                Web 8080 --> 5000 | Agent Receiver 8000
                                  |
          +-----------------------+------------------+
          |                       |                  |
    Proxmox VE               Ubuntu Server       Windows 11 Pro
    pve                      ubuntu-server        windows-pc01
    172.16.5.178             192.168.31.128        192.168.31.1 (VMnet8)
          +-----------------------+------------------+
                                  |
                       Notification Rule
                     "Telegram HPA Monitoring"
                                  |
                     telegram_alert.py + config
                                  |
                     Telegram: CheckMK HPA Alert
```

| Thành phần | Giá trị đã thực hiện | Kiểm tra |
|---|---|---|
| CheckMK | `checkmk/check-mk-cloud:2.4.0p18` | Container healthy |
| Site | `cmk` | Giao diện hoạt động |
| Web | `http://192.168.31.128:8080/cmk/` | Truy cập được |
| Proxmox | `pve` / `172.16.5.178` | Đã giám sát |
| Ubuntu | `ubuntu-server` | Đã giám sát |
| Windows | `windows-pc01` / `192.168.31.1` | Agent TLS thành công; 17 services |
| Telegram | `@hpa_checkmk_alert_2026_bot` | Đã nhận thông báo Windows DOWN và các service Proxmox |
| Delay rule | `pve` + `^Interface 2$` / 2 phút | Đã Activate Changes thành công |

> **Chú ý:** Các địa chỉ IP trong đây là IP lab riêng. Hãy thay IP phù hợp khi triển khai ở môi trường khác. `192.168.31.1` là VMware VMnet8 trên Windows host trong bài thử nghiệm, không nên sử dụng mặc định cho các Windows khác.

## 2. Kiểm tra CheckMK Docker

Trên Ubuntu:

```bash
sudo docker ps
sudo docker start monitoring             # chỉ khi container đang dừng
sudo docker logs --tail 100 monitoring
```

Ánh xạ cổng quan sát được trong môi trường này: `8080:5000` (web) và `8000:8000` (Agent Receiver). Xác minh lại với `docker ps`, vì ánh xạ thực tế có thể thay đổi.

Vào site trong container:

```bash
sudo docker exec -it -u cmk monitoring bash
whoami
printf '%s\n' "$OMD_ROOT"
```

Kết quả mong muốn là user `cmk`, root site `/omd/sites/cmk`.

## 3. Thêm Proxmox vào CheckMK

Trong giao diện **Setup → Hosts**, tạo `pve`, nhập IP `172.16.5.178`, chọn Checkmk agent và cấu hình Proxmox VE integration nếu có. Trên Proxmox dùng agent/plugin phù hợp; **không mặc định rằng truy cập HTTPS 8006 đồng nghĩa API hoạt động**. Cần kiểm tra credentials, API token và quyền riêng biệt.

Chạy từ Proxmox:

```bash
ip route
ping -c 4 8.8.8.8
chronyc tracking
curl -k -I --connect-timeout 5 https://172.16.5.178:8006
```

Lệnh `curl -I` có thể nhận HTTP `501 Not Implemented` vì API không hỗ trợ HEAD tại đường dẫn đó: kết quả vẫn chứng tỏ TCP/TLS/HTTP phản hồi, không khẳng định API plugin đã xác thực. CheckMK từng báo lỗi `Check_MK Discovery` do kết nối API thất bại; cần phân biệt lỗi plugin với agent Linux.

![Proxmox monitor](images/03-checkmk-proxmox.png)
![Proxmox services](images/04-checkmk-services-pve.png)

## 4. Tạo Bot và tích hợp Telegram

### 4.1. Tạo bot

Mở Telegram → tìm bot chính thức `@BotFather` → `/newbot` → đặt tên và username kết thúc bằng `_bot`. Sau đó vào bot vừa tạo và nhấn **Start**. **Không chia sẻ Bot Token**, kể cả qua ảnh chụp màn hình hoặc trên GitHub.

### 4.2. Xác định Chat ID và kiểm tra API

Trên PowerShell, lấy token bằng cách nhập kín:

```powershell
$secureToken = Read-Host 'Telegram Bot Token' -AsSecureString
$token = [System.Net.NetworkCredential]::new('', $secureToken).Password
Invoke-RestMethod -Uri "https://api.telegram.org/bot${token}/getMe"
```

Nhắn một tin mới tới bot rồi lấy Chat ID:

```powershell
$result = Invoke-RestMethod -Uri "https://api.telegram.org/bot${token}/getUpdates"
$result.result | ForEach-Object { if ($_.message) { $_.message.chat.id } }
```

Test gửi tin (thay `YOUR_CHAT_ID`, **không dán token vào ảnh hay code**):

```powershell
$chatId = 'YOUR_CHAT_ID'
Invoke-RestMethod -Method Post -Uri "https://api.telegram.org/bot${token}/sendMessage" -Body @{ chat_id=$chatId; text='CheckMK Telegram Test OK' }
```

Trong quá trình thực hành đã gặp **404 Not Found** khi dùng biến `$token` kiểu SecureString trực tiếp trong URL. Cần chuyển SecureString thành chuỗi tạm trong bộ nhớ như ví dụ trên. Xóa biến sau khi dùng: `Remove-Variable token,secureToken -ErrorAction SilentlyContinue`.

![Telegram test](images/05-telegram-bot-test.png)

### 4.3. Lưu token trong CheckMK site

Đăng nhập container dưới user `cmk`:

```bash
sudo docker exec -it -u cmk monitoring bash
umask 077
mkdir -p ~/var ~/local/share/check_mk/notifications
read -rsp 'Telegram Bot Token: ' TOKEN; echo
read -rp 'Telegram Chat ID: ' CHAT_ID
printf '%s\n%s\n' "$TOKEN" "$CHAT_ID" > ~/var/telegram_bot.conf
chmod 600 ~/var/telegram_bot.conf
unset TOKEN CHAT_ID
```

**Cực kỳ quan trọng:** File `/omd/sites/cmk/var/telegram_bot.conf` là bí mật; không đưa vào GitHub, không in nội dung bằng `cat`, không commit và chỉ cho user `cmk` đọc. File chứa **2 dòng: token rồi chat ID**. Không đưa literal `read -rp ...` vào trong file.

Kiểm tra mà không lộ nội dung:

```bash
ls -l ~/var/telegram_bot.conf
awk '{print "Line " NR ": " length($0) " characters"}' ~/var/telegram_bot.conf
```

### 4.4. Notification script

Script đã dùng nằm tại [`scripts/telegram_alert.py`](scripts/telegram_alert.py). Từ Ubuntu host copy vào container:

```bash
sudo docker cp scripts/telegram_alert.py monitoring:/omd/sites/cmk/local/share/check_mk/notifications/telegram_alert.py
sudo docker exec -u root monitoring chown cmk:cmk /omd/sites/cmk/local/share/check_mk/notifications/telegram_alert.py
sudo docker exec monitoring chmod 755 /omd/sites/cmk/local/share/check_mk/notifications/telegram_alert.py
sudo docker exec monitoring python3 -m py_compile /omd/sites/cmk/local/share/check_mk/notifications/telegram_alert.py
```

Để dùng lệnh `docker cp`, file `scripts/telegram_alert.py` phải nằm trên Ubuntu host (hoặc điều chỉnh đường dẫn); đường dẫn trong repository không tự xuất hiện trên host.

Script đọc `NOTIFY_*` do CheckMK truyền vào, lấy token/chat ID từ file bí mật và gọi Telegram HTTP API. Test bằng bộ biến mô phỏng:

```bash
sudo docker exec -it -u cmk monitoring bash
NOTIFY_WHAT=SERVICE NOTIFY_HOSTNAME=pve NOTIFY_SERVICEDESC='Interface 2' NOTIFY_SERVICESTATE=CRIT NOTIFY_NOTIFICATIONTYPE=PROBLEM NOTIFY_SERVICEOUTPUT='Manual test' ~/local/share/check_mk/notifications/telegram_alert.py
```

Nếu token đúng và bot đã được Start, bạn sẽ thấy tin nhắn trên Telegram.

## 5. Tạo Notification Rule Telegram

Vào **Setup → Events → Notifications → Add notification rule**. Trong Guided mode nhập:

1. **Triggering events**: Host `DOWN`, `UP`, `UNREACHABLE`; Service `CRIT`, `WARN`, `OK`, `UNKNOWN`.
2. **Filter for hosts/services**: chọn đúng hosts `pve`, `ubuntu-server`, sau đó thêm `windows-pc01` khi Windows đã được tạo.
3. **Notification method**: `Telegram alert notification for Checkmk`.
4. **Select parameters**: Create → Description `Telegram HPA Alert`; **Call with the following parameters** để trống vì script lấy token/chat ID qua file.
5. **Recipient**: `Specific users` → `cmkadmin` (một người nhận để tránh gửi trùng về cùng Chat ID).
6. **Sending conditions**: không giới hạn time period để gửi 24/7; nếu có cấu hình thông báo định kỳ ở nơi khác thì vẫn có thể gửi lại.
7. **General properties**: Description `Telegram HPA Monitoring`; Save/Apply & test notification rule.

![Trigger events](images/06-notification-rule-events.png)
![Host filters](images/07-notification-host-filter.png)
![Method](images/08-notification-method.png)
![Parameters](images/09-notification-parameters.png)
![Recipient](images/10-notification-recipient.png)
![Sending conditions](images/11-notification-conditions.png)
![Review rule](images/12-notification-review.png)

Trong **Test notifications** chọn host `pve` hay `windows-pc01`, mô phỏng `UP → DOWN`. **Khi không bật** `Trigger notification for a specific method`, CheckMK chủ yếu phân tích các quy tắc phù hợp. **Khi bật** và chọn Telegram method + parameters, bài test có thể phát thông báo thực tế. Kiểm tra kết quả **Test results**, **Predicted notifications**, và tin nhắn trong Telegram.

![Test notification](images/13-notification-test.png)

## 6. Cài Windows Agent và sửa lỗi kết nối

### 6.1. Cài CheckMK Agent 2.4 trên Windows 10/11

Vào giao diện CheckMK → **Setup → Agents → Windows** (tên menu có thể hơi khác) → tải `check_mk_agent.msi`. Máy chưa cài Agent trước đó có thể chọn **Clean installation**, nhưng đừng dùng nếu cần giữ cấu hình Agent cũ. Nhấn Next → Install → Finish.

![Windows MSI options](images/14-windows-agent-install-options.png)
![Windows MSI Install](images/15-windows-agent-install.png)

Mở **PowerShell Administrator** trên Windows:

```powershell
Get-Service CheckmkService
& 'C:\Program Files (x86)\checkmk\service\cmk-agent-ctl.exe' status
```

Lúc chưa đăng ký, `No connections` là bình thường.

![Windows Agent status](images/16-windows-agent-status.png)

### 6.2. Xác định IP Windows và tạo host

```powershell
ipconfig
Test-NetConnection 192.168.31.128 -Port 8000
```

Trong lab, VMnet8 Windows host là `192.168.31.1` và Ubuntu guest là `192.168.31.128`. Đây là mạng riêng VMware Workstation; **không phải IP mạng vật lý cho mọi máy Windows**.

Vào **Setup → Hosts → Main → Add host**, tạo host `windows-pc01`, IPv4 `192.168.31.1`, connection mode Pull, SNMP No SNMP. **Save** trước khi đăng ký TLS. Nếu chưa tạo host, Agent báo `404 Not Found: Host windows-pc01 does not exist`.

![Add Windows host](images/17-windows-host-add.png)
![VMnet8 IP](images/18-windows-network-ip.png)

### 6.3. Gỡ lỗi TCP 6556

Kết nối từ Ubuntu đến Windows ban đầu `TimeoutError: timed out`. Trên Windows kiểm tra:

```powershell
Get-NetTCPConnection -LocalPort 6556 -State Listen
Get-Service CheckmkService
Restart-Service CheckmkService
netstat -ano | findstr :6556
```

Trong thực tế, restart `CheckmkService` khiến cổng `0.0.0.0:6556` chuyển sang `LISTENING`. Nếu vẫn timeout, kiểm tra firewall; chỉ khi cần mới thêm rule **giới hạn nguồn**:

```powershell
New-NetFirewallRule -DisplayName 'CheckMK Agent 6556 LAB' -Direction Inbound -Protocol TCP -LocalPort 6556 -RemoteAddress 192.168.31.128 -Action Allow
```

Từ Ubuntu kiểm tra:

```bash
python3 -c "import socket; socket.create_connection(('192.168.31.1',6556),5).close(); print('TCP 6556 OK')"
```

![Timeout](images/19-windows-agent-timeout.png)
![Windows listening](images/20-windows-agent-listening.png)
![Connectivity OK](images/21-windows-agent-connectivity.png)

### 6.4. Đăng ký TLS

Chỉ chạy sau khi host `windows-pc01` đã được **Save** trong CheckMK:

```powershell
& 'C:\Program Files (x86)\checkmk\service\cmk-agent-ctl.exe' register --server 192.168.31.128:8000 --site cmk --hostname windows-pc01 --user cmkadmin
```

Xác minh chứng chỉ được cấp bởi CA site `cmk`, nhập `y`, sau đó mật khẩu CheckMK `cmkadmin`. Không dùng mật khẩu Windows. Kiểm tra:

```powershell
& 'C:\Program Files (x86)\checkmk\service\cmk-agent-ctl.exe' status
```

Kết quả trong lab: `Registration complete`, có `Connection: 192.168.31.128/cmk`, `Remote hostname: windows-pc01`.

![TLS complete](images/22-windows-agent-tls.png)

## 7. Service Discovery và cảnh báo Windows

Vào **Setup → Hosts → windows-pc01 → Service discovery → Accept all → Activate Changes**.

Thực tế ban đầu phát hiện **17 services**, gồm CPU, RAM, C:/ filesystem, Interface, Disk I/O, Log System, Service Summary, Uptime. Có thời điểm Memory `CRIT` (virtual memory ~91%) và Log System `WARN` (lỗi dynamic DNS registration); cần chẩn đoán riêng thay vì chỉ tắt cảnh báo.

![Services discovered](images/23-windows-services-discovered.png)
![Services monitored](images/24-windows-services-monitored.png)

Sửa Notification Rule `Telegram HPA Monitoring`: trong Host filters thêm `windows-pc01`, giữ nguyên Telegram method, `Telegram HPA Alert` và recipient `cmkadmin`.

![Add Windows to rule](images/25-telegram-rule-windows.png)

**Test notifications** → Host `windows-pc01`, `Status change`, `UP → DOWN`. Trong bài thực hành, test phân tích cho thấy **2 rules matching, 1 notification predicted**. Nếu chọn nhầm `Start of downtime`, rule không khớp và 0 thông báo được kích hoạt.

![Matching rules](images/26-windows-test-matching.png)
![Wrong downtime event](images/27-windows-test-nomatch.png)

Khi bật Trigger notification for a specific method và chọn Telegram method, bot nhận **PROBLEM / windows-pc01 / Host availability / DOWN**, chứng minh đường gửi test hoạt động. Test này **không tắt Windows thật**.

![Telegram received Windows alert](images/28-windows-telegram-result.png)

## 8. Giảm cảnh báo lặp bằng Delay service notifications

Do dịch vụ `pve / Interface 2` nhiều lần `WARN → OK → WARN`, tạo rule chỉ trì hoãn thông báo **sự cố của dịch vụ đó**, không trì hoãn host DOWN hay RAM Windows.

1. **Setup → Services → Service monitoring rules** → tìm `Delay service notifications` → **Add rule**.
2. Description: `Delay pve Interface 2 alerts`.
3. Delay: `0 days, 0 hours, 2 mins, 0 secs`.
4. Condition type: `Explicit conditions`; Folder `Main`.
5. Tích **Explicit hosts**: chọn `pve`. Không tích Negate.
6. Tích **Services**: nhập regex chính xác `^Interface 2$`. Không tích Negate.
7. Save → nhấn **1 change** → **Activate on selected sites**.

![Delay form](images/29-delay-rule-input.png)
![Delay conditions](images/30-delay-rule-conditions.png)
![Saved rule](images/31-delay-rule-saved.png)
![Anchored service regex](images/32-delay-rule-anchored.png)
![Activation success](images/33-delay-rule-activated.png)

**Kết quả thực tế đã xác nhận:** trạng thái Activate Changes **Success**, không còn pending changes. **Chưa có phép đo riêng** chứng minh tỷ lệ tin nhắn giảm sau áp dụng. Delay làm các sự cố `Interface 2` được báo muộn khoảng 2 phút nếu vẫn tồn tại; khi hồi phục trong khoảng chờ, thông báo sự cố ngắn hạn có thể bị bỏ qua.

## 9. Chẩn đoán NIC Proxmox

Proxmox đang chạy nested trong VMware Workstation. Các lệnh kiểm tra:

```bash
ethtool nic0
ip -s link show nic0
lspci -nn | grep -i ethernet
ip -br link
cat /etc/network/interfaces
```

Thực tế quan sát: `AMD 79C97x [PCnet32 LANCE]`, driver `pcnet32`, Speed `10Mb/s`, Duplex `Half`; RX errors / dropped / missed có giá trị khác 0. Chưa thể kết luận tốc độ tăng lỗi theo thời gian chỉ từ một ảnh.

![NIC check](images/02-proxmox-driver.png)
![Network config](images/01-proxmox-network.png)

Cấu hình bridge đang dùng:

```ini
auto lo
iface lo inet loopback
iface nic0 inet manual

auto vmbr0
iface vmbr0 inet static
    address 172.16.5.178/24
    gateway 172.16.5.1
    bridge-ports nic0
    bridge-stp off
    bridge-fd 0

source /etc/network/interfaces.d/*
```

Đã sao lưu cấu hình trước thay đổi NIC:

```bash
cp -a /etc/network/interfaces /root/interfaces.backup
```

**Chưa thực hiện chuyển NIC.** Phương án dự kiến: thêm VMXNET3 trong VMware Workstation (cùng mạng VMnet/Bridged của NIC cũ), xác nhận tên NIC mới/driver `vmxnet3`, sau đó mới lập kế hoạch chuyển `bridge-ports`. Không xóa `nic0` hoặc đổi mạng khi chưa có console VMware để khôi phục.

## 10. Bảo mật, kiểm tra và đưa lên GitHub

### Bí mật phải giữ riêng

- **Không commit:** `telegram_bot.conf`, Bot Token, mật khẩu CheckMK, cookies, API token.
- **Cảnh báo:** Bot Token từng xuất hiện trong ảnh hội thoại gốc. **Nên vào `@BotFather` → `/revoke` để tạo token mới** trước khi dùng tiếp. Sau khi thay token, cập nhật file cấu hình trên CheckMK và test lại.
- Các ảnh được chọn cho gói này đã **loại bỏ những màn hình BotFather hiển thị token**, nhưng vẫn chứa thông tin IP private, tên host và chi tiết hạ tầng. Kiểm duyệt lại trước khi đưa repository công khai. Nên ưu tiên repository **Private**.

### Upload bằng giao diện GitHub

1. Đăng nhập [github.com](https://github.com/) → **New repository**.
2. Đặt tên `checkmk-telegram-monitoring-guide` và chọn **Private**.
3. Giải nén ZIP đi kèm tài liệu này.
4. Trên repository, nhấn **Add file → Upload files**.
5. Tải lên **README.md**, thư mục **images/** và **scripts/** (có thể kéo thả toàn bộ nội dung thư mục).
6. Chọn **Commit changes**. GitHub sẽ hiển thị README với ảnh tự động.

### Upload bằng Git trên máy tính

```bash
git init
git add README.md images scripts .gitignore
git commit -m "Document CheckMK 2.4 monitoring and Telegram alerts"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/checkmk-telegram-monitoring-guide.git
git push -u origin main
```

Thay `YOUR_USERNAME` bằng tài khoản GitHub của bạn và tạo repository trên GitHub trước khi push.

### Đối chiếu sau triển khai

- CheckMK `Monitor → All hosts`: đủ 3 host.
- Service Discovery: Windows có 17 monitored services ở thời điểm ghi nhận.
- CheckMK `Test notifications`: test `UP → DOWN` qua Telegram.
- Telegram: nhận thông báo PROBLEM và RECOVERY tương ứng.
- CheckMK `Analyze recent notifications`: kiểm tra rule thực tế và số thông báo.
- `Delay service notifications`: áp đúng `pve` / `^Interface 2$` / `2 minutes`, đã Activate.

## 11. Phụ lục ảnh

Danh sách ảnh đi kèm dưới thư mục `images/`. Mỗi ảnh được đặt tên theo giai đoạn cấu hình để dễ tìm lại.

- [`images/01-proxmox-network.png`](images/01-proxmox-network.png) — Card mang Proxmox PCnet32 va cau hinh vmbr0
- [`images/02-proxmox-driver.png`](images/02-proxmox-driver.png) — Kiem tra ethtool va loi RX tren Proxmox
- [`images/03-checkmk-proxmox.png`](images/03-checkmk-proxmox.png) — Tong quan CheckMK giam sat Proxmox
- [`images/04-checkmk-services-pve.png`](images/04-checkmk-services-pve.png) — Danh sach dich vu Proxmox
- [`images/05-telegram-bot-test.png`](images/05-telegram-bot-test.png) — Telegram bot nhan tin nhan kiem tra
- [`images/06-notification-rule-events.png`](images/06-notification-rule-events.png) — Chon su kien DOWN UP CRIT WARN OK
- [`images/07-notification-host-filter.png`](images/07-notification-host-filter.png) — Loc host pve va ubuntu-server
- [`images/08-notification-method.png`](images/08-notification-method.png) — Chon Telegram alert notification method
- [`images/09-notification-parameters.png`](images/09-notification-parameters.png) — Tao tham so Telegram HPA Alert
- [`images/10-notification-recipient.png`](images/10-notification-recipient.png) — Chon nguoi nhan cmkadmin
- [`images/11-notification-conditions.png`](images/11-notification-conditions.png) — Dieu kien gui canh bao 24 tren 7
- [`images/12-notification-review.png`](images/12-notification-review.png) — Kiem tra va luu notification rule
- [`images/13-notification-test.png`](images/13-notification-test.png) — Man hinh Test notifications
- [`images/14-windows-agent-install-options.png`](images/14-windows-agent-install-options.png) — Lua chon khi cai CheckMK Agent Windows
- [`images/15-windows-agent-install.png`](images/15-windows-agent-install.png) — Chay trinh cai dat CheckMK Agent
- [`images/16-windows-agent-status.png`](images/16-windows-agent-status.png) — Kiem tra CheckmkService va status Agent
- [`images/17-windows-host-add.png`](images/17-windows-host-add.png) — Tao host windows-pc01
- [`images/18-windows-network-ip.png`](images/18-windows-network-ip.png) — Xac dinh dia chi VMnet8 Windows
- [`images/19-windows-agent-timeout.png`](images/19-windows-agent-timeout.png) — Su co timeout TCP 6556
- [`images/20-windows-agent-listening.png`](images/20-windows-agent-listening.png) — Restart Service va TCP 6556 LISTENING
- [`images/21-windows-agent-connectivity.png`](images/21-windows-agent-connectivity.png) — Ubuntu kiem tra TCP 6556 thanh cong
- [`images/22-windows-agent-tls.png`](images/22-windows-agent-tls.png) — Dang ky TLS thanh cong
- [`images/23-windows-services-discovered.png`](images/23-windows-services-discovered.png) — Service Discovery Windows 17 dich vu
- [`images/24-windows-services-monitored.png`](images/24-windows-services-monitored.png) — 17 Windows services monitored
- [`images/25-telegram-rule-windows.png`](images/25-telegram-rule-windows.png) — Them Windows vao quy tac Telegram
- [`images/26-windows-test-matching.png`](images/26-windows-test-matching.png) — Rule matching cho Windows
- [`images/27-windows-test-nomatch.png`](images/27-windows-test-nomatch.png) — Downtime khong khop notification rule
- [`images/28-windows-telegram-result.png`](images/28-windows-telegram-result.png) — Telegram nhan canh bao windows-pc01
- [`images/29-delay-rule-input.png`](images/29-delay-rule-input.png) — Form tao quy tac Delay service notifications
- [`images/30-delay-rule-conditions.png`](images/30-delay-rule-conditions.png) — Loc pve va Interface 2
- [`images/31-delay-rule-saved.png`](images/31-delay-rule-saved.png) — Da luu delay 2 phut
- [`images/32-delay-rule-anchored.png`](images/32-delay-rule-anchored.png) — Dieu kien regex chinh xac
- [`images/33-delay-rule-activated.png`](images/33-delay-rule-activated.png) — Activate Changes thanh cong

---

**Phạm vi tài liệu:** hướng dẫn từ các lần thực hành đã được chụp ảnh; không khẳng định mọi thao tác vận hành lâu dài đã được kiểm chứng. Không có thao tác tải lên GitHub tự động trong gói này.
