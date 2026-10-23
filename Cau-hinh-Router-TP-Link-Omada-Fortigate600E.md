# Cấu hình Router TP-Link Omada và FortiGate 600E

## Giới thiệu

Tài liệu này ghi lại quy trình cấu hình **Router TP-Link Omada** kết hợp với **FortiGate 600E**, theo đúng thứ tự các ảnh đã có trong file gốc.

> **Lưu ý quan trọng:** Các ảnh trong file gốc là link GitHub Attachment. Phần lời hướng dẫn dưới đây được bổ sung theo **quy trình cấu hình chuẩn Omada/FortiGate** và không tự suy đoán các địa chỉ IP, tài khoản PPPoE hoặc VLAN không đọc được trực tiếp từ ảnh. Khi thực hành, hãy ưu tiên **thông số đang hiển thị trong ảnh và thông số thực tế của hệ thống**.

---

## Sơ đồ nguyên lý

```text
Internet
   |
   v
FortiGate 600E
   |
   |  Interface/LAN/Transit
   v
WAN - TP-Link Omada Router
   |
   |  LAN + DHCP
   v
PC / Laptop / Switch / Access Point
```

### Luồng hoạt động

1. **FortiGate** có đường Internet, Default Route và Firewall Policy/NAT phù hợp.
2. **WAN Omada** nhận IP từ mạng phía FortiGate hoặc được đặt IP tĩnh.
3. **LAN Omada** tạo một mạng riêng cho client.
4. **DHCP Server** trên Omada cấp IP, Gateway và DNS cho máy tính.
5. Máy tính gửi lưu lượng: **PC → Omada → FortiGate → Internet**.

---

## Trình tự cấu hình theo ảnh

### Bước 1: Chuẩn bị kết nối và truy cập Router Omada

Kết nối máy tính vào một cổng **LAN** của Router TP-Link Omada bằng dây mạng. Tạm thời ngắt các kết nối mạng khác nếu chúng có thể làm máy tính đi sai gateway.

Mở trình duyệt và truy cập địa chỉ quản trị của Router Omada. Nếu chưa biết địa chỉ quản trị, có thể kiểm tra **Default Gateway** trên máy tính bằng lệnh `ipconfig`.

**Mục tiêu:** vào được giao diện quản trị của Router trước khi cấu hình WAN/LAN.

**Ảnh minh họa bước 1:**

<img width="1910" height="997" alt="Screenshot 2026-10-22 151356" src="https://github.com/user-attachments/assets/e4ce7206-1096-4912-823d-09af4e03abac" />

---

### Bước 2: Đăng nhập vào giao diện quản trị

Đăng nhập bằng tài khoản quản trị của Router Omada. Với thiết bị mới, hệ thống có thể yêu cầu tạo tài khoản quản trị lần đầu.

Sau khi đăng nhập, kiểm tra nhanh model thiết bị, firmware và trạng thái các cổng để chắc chắn dây **WAN/LAN** đang cắm đúng vị trí.

> Không nên thay đổi nhiều mục cùng lúc. Cấu hình xong từng phần rồi kiểm tra trước khi chuyển bước.

**Ảnh minh họa bước 2:**

<img width="1915" height="994" alt="Screenshot 2026-10-22 151430" src="https://github.com/user-attachments/assets/32ec1191-372f-4694-ae8b-41df952043a0" />

---

### Bước 3: Mở phần cấu hình WAN

Trong giao diện Omada, vào phần cấu hình **Network / WAN** hoặc mục tương đương theo firmware. Chọn đúng cổng đang nối lên mạng phía trên, modem hoặc FortiGate.

**WAN** là phía Router dùng để đi ra mạng bên ngoài. Nếu chọn nhầm cổng, Router có thể lưu cấu hình nhưng máy trong LAN vẫn không truy cập Internet được.

**Ảnh minh họa bước 3:**

<img width="1912" height="998" alt="Screenshot 2026-10-22 151524" src="https://github.com/user-attachments/assets/825fab97-2bed-473a-9055-4241f903a872" />

---

### Bước 4: Chọn kiểu kết nối WAN

Chọn loại kết nối WAN phù hợp với hệ thống thực tế:

- **Dynamic IP (DHCP):** thiết bị phía trên tự cấp IP cho Omada.
- **Static IP:** nhập IP, Subnet Mask, Gateway và DNS cố định.
- **PPPoE:** dùng khi đường Internet yêu cầu tài khoản PPPoE của nhà mạng.

Nếu Omada đặt **sau FortiGate**, thường WAN Omada sẽ dùng DHCP hoặc Static IP trong mạng do FortiGate cung cấp. Không nhập thông số ngẫu nhiên; dùng đúng thông số của hệ thống.

**Ảnh minh họa bước 4:**

<img width="1914" height="997" alt="Screenshot 2026-10-22 151553" src="https://github.com/user-attachments/assets/3f6cbfe4-a205-46fb-85fa-d26198899166" />

---

### Bước 5: Nhập thông số WAN

Nhập các thông số WAN theo sơ đồ mạng hoặc theo thông tin đã được cấp. Với Static IP cần kiểm tra đủ:

- **IP Address**
- **Subnet Mask**
- **Default Gateway**
- **DNS Server**

Đặc biệt, **Default Gateway phải là thiết bị nằm phía trên Omada**. Nếu Omada nối trực tiếp đến FortiGate thì gateway thường là IP của cổng FortiGate đang nối với Omada.

**Ảnh minh họa bước 5:**

<img width="1911" height="998" alt="Screenshot 2026-10-22 151640" src="https://github.com/user-attachments/assets/d912fab5-f711-46ed-b340-389e3933e25e" />

---

### Bước 6: Lưu cấu hình WAN

Nhấn **Save / Apply** để lưu cấu hình. Sau đó quay lại trang trạng thái và kiểm tra cổng WAN đã nhận đúng IP hay chưa.

Nếu trạng thái WAN chưa lên, kiểm tra lần lượt: dây mạng, link vật lý, VLAN trên đường uplink, loại kết nối WAN và Default Gateway.

> Chỉ chuyển sang cấu hình LAN khi WAN đã có thông số hợp lệ.

**Ảnh minh họa bước 6:**

<img width="1917" height="993" alt="Screenshot 2026-10-22 151709" src="https://github.com/user-attachments/assets/339e9721-7d0e-40ae-a1c8-2633689ccad4" />

---

### Bước 7: Kiểm tra trạng thái kết nối WAN

Kiểm tra mục **Status** của Router. Cổng WAN cần hiển thị trạng thái kết nối và có đủ IP, Gateway, DNS.

Nếu giao diện hỗ trợ công cụ chẩn đoán, thử ping Default Gateway phía WAN. Ping được gateway nhưng chưa ra Internet thường liên quan đến route, NAT, firewall hoặc DNS ở thiết bị phía trên.

**Ảnh minh họa bước 7:**

<img width="1911" height="995" alt="Screenshot 2026-10-22 151727" src="https://github.com/user-attachments/assets/93e3e413-859f-406c-a9f2-d7b4c63a272b" />

---

### Bước 8: Mở phần cấu hình LAN

Tiếp theo cấu hình mạng **LAN** dành cho máy tính phía sau Omada. Vào **Network / LAN** hoặc mục tương đương.

Đặt địa chỉ LAN của Router làm **Default Gateway** cho các máy client. Mạng LAN không được trùng với mạng WAN; ví dụ nếu WAN thuộc `192.168.1.0/24` thì không nên đặt LAN cũng là `192.168.1.0/24`.

**Ảnh minh họa bước 8:**

<img width="1677" height="867" alt="Screenshot 2026-10-23 093521" src="https://github.com/user-attachments/assets/19e11722-5ed7-4f09-b345-dfd584649036" />

---

### Bước 9: Thiết lập địa chỉ IP cho LAN

Khai báo IP LAN và Subnet Mask. Đây sẽ là địa chỉ quản trị Router từ phía LAN và cũng là Default Gateway của các máy tính trong mạng này.

Sau khi đổi IP LAN, phiên đăng nhập hiện tại có thể bị ngắt. Khi đó hãy truy cập lại Router bằng **địa chỉ LAN mới**.

**Ảnh minh họa bước 9:**

<img width="1677" height="837" alt="Screenshot 2026-10-23 093740" src="https://github.com/user-attachments/assets/94d39206-9dde-403b-8e43-397a693354f2" />

---

### Bước 10: Bật DHCP Server

Trong phần LAN, bật **DHCP Server** để Router tự động cấp cấu hình mạng cho máy tính. DHCP giúp client nhận IP mà không phải nhập tay từng máy.

Khi bật DHCP, cần chắc chắn trong cùng một VLAN/LAN không có hai DHCP Server cấp chồng chéo, trừ khi bạn chủ động thiết kế DHCP redundancy.

**Ảnh minh họa bước 10:**

<img width="1903" height="995" alt="Screenshot 2026-10-23 094325" src="https://github.com/user-attachments/assets/d5892649-dba6-49f1-abd5-22b3783cd1b5" />

---

### Bước 11: Cấu hình dải cấp phát DHCP

Thiết lập **DHCP Pool** nằm cùng subnet với địa chỉ LAN của Omada. Ví dụ nếu gateway LAN là `192.168.10.1/24`, dải DHCP có thể nằm trong `192.168.10.0/24` nhưng không được bao gồm các IP tĩnh đã dành cho router, server hoặc thiết bị quản trị.

Khai báo thêm **Default Gateway** và **DNS** cho client nếu giao diện yêu cầu.

**Ảnh minh họa bước 11:**

<img width="1904" height="945" alt="Screenshot 2026-10-23 102248" src="https://github.com/user-attachments/assets/ec1ec9ef-07f4-4394-b6ae-4f227a54c049" />

---

### Bước 12: Kiểm tra máy tính nhận IP

Cắm máy tính vào cổng LAN của Omada, để card mạng ở chế độ **Obtain an IP address automatically**. Trên Windows chạy:

```powershell
ipconfig /release
ipconfig /renew
ipconfig /all
```

Kiểm tra máy đã nhận đúng **IPv4 Address, Subnet Mask, Default Gateway và DNS** hay chưa.

**Ảnh minh họa bước 12:**

<img width="1528" height="643" alt="Screenshot 2026-10-23 102534" src="https://github.com/user-attachments/assets/f222eb1a-3f2c-4332-92b4-3fb21eb8bd91" />

---

### Bước 13: Kiểm tra cổng FortiGate nối với Omada

Đăng nhập FortiGate 600E và xác định đúng interface đang nối đến WAN của Router Omada. Cổng này phải ở trạng thái **UP** và có IP phù hợp với mạng transit giữa FortiGate và Omada.

Nếu dùng Static IP ở WAN Omada, IP của FortiGate và WAN Omada phải cùng subnet nhưng không được trùng nhau.

**Ảnh minh họa bước 13:**

<img width="1680" height="799" alt="Screenshot 2026-10-23 111105" src="https://github.com/user-attachments/assets/f4d90c1e-dd3f-47a3-9f3f-6c46e62b5365" />

---

### Bước 14: Kiểm tra hoặc tạo route trên FortiGate

Vào phần **Network → Static Routes** để kiểm tra đường đi ra Internet. FortiGate phải có Default Route `0.0.0.0/0` về đúng đường WAN/SD-WAN.

Nếu cần truy cập ngược từ mạng khác vào LAN phía sau Omada, có thể phải bổ sung route tới subnet LAN của Omada. Trường hợp Omada đang NAT thì yêu cầu route ngược sẽ khác với khi chạy routed mode.

**Ảnh minh họa bước 14:**

<img width="1682" height="799" alt="Screenshot 2026-10-23 111118" src="https://github.com/user-attachments/assets/7905f08e-95b8-4a3f-bee6-4d5de9d8dac8" />

---

### Bước 15: Tạo chính sách Firewall cho lưu lượng đi Internet

Vào **Policy & Objects → Firewall Policy** và tạo hoặc kiểm tra policy cho phép lưu lượng từ interface nối Omada đi ra WAN/SD-WAN.

Các trường cơ bản cần kiểm tra:

- **Incoming Interface:** cổng nối Omada
- **Outgoing Interface:** WAN hoặc SD-WAN
- **Source:** mạng Omada hoặc `all` trong giai đoạn lab
- **Destination:** `all`
- **Service:** tùy nhu cầu; khi test có thể dùng `ALL` rồi siết lại sau
- **Action:** `ACCEPT`

**Ảnh minh họa bước 15:**

<img width="1243" height="751" alt="Screenshot 2026-10-23 111710" src="https://github.com/user-attachments/assets/c966610a-4440-476c-b86c-f3fc6166a906" />

---

### Bước 16: Bật NAT khi cho mạng Omada ra Internet

Trong policy đi Internet, bật **NAT** nếu FortiGate là thiết bị thực hiện NAT ra Public IP. Khi NAT bị tắt trong mô hình cần NAT, client có thể đi đến FortiGate nhưng không nhận được gói trả về từ Internet.

Sau khi bật NAT, lưu policy và đảm bảo policy nằm ở vị trí có thể match trước các policy từ chối hoặc policy khác không phù hợp.

**Ảnh minh họa bước 16:**

<img width="1249" height="759" alt="Screenshot 2026-10-23 111719" src="https://github.com/user-attachments/assets/80238516-1e4d-4bce-a5e0-be4fff5fc587" />

---

### Bước 17: Kiểm tra đường đi và kết nối giữa hai thiết bị

Kiểm tra theo từng chặng, không chỉ ping thẳng Internet:

1. PC → IP LAN của Omada.
2. Omada → Gateway phía WAN.
3. FortiGate → Internet.
4. PC → `8.8.8.8`.

Nếu lỗi ở chặng nào thì tập trung xử lý tại chặng đó. Cách kiểm tra theo từng hop giúp phân biệt lỗi LAN, WAN, routing, firewall và DNS.

**Ảnh minh họa bước 17:**

<img width="1233" height="757" alt="Screenshot 2026-10-23 111752" src="https://github.com/user-attachments/assets/dff1f5f0-6d23-4f90-b1ee-eb526fa7b94d" />

---

### Bước 18: Kiểm tra cấu hình IP trên máy tính

Trên Windows chạy `ipconfig /all` và đối chiếu:

- IPv4 phải thuộc dải DHCP của Omada.
- Subnet Mask phải đúng.
- Default Gateway phải là IP LAN của Omada.
- DNS phải có giá trị hợp lệ.

Sau đó ping gateway. Nếu không ping được gateway thì chưa cần kiểm tra Internet; hãy xử lý kết nối LAN trước.

**Ảnh minh họa bước 18:**

<img width="1345" height="722" alt="Screenshot 2026-10-23 112231" src="https://github.com/user-attachments/assets/d7d2ac00-86c0-4b8b-9ccd-12326d635a6b" />

---

### Bước 19: Kiểm thử Internet và hoàn tất

Thực hiện các bài test cuối:

```powershell
ping <IP-LAN-OMADA>
ping 8.8.8.8
nslookup google.com
tracert 8.8.8.8
```

- Ping gateway thành công → LAN hoạt động.
- Ping `8.8.8.8` thành công → routing/NAT ra Internet cơ bản hoạt động.
- `nslookup` thành công → DNS hoạt động.
- Mở được website → hoàn tất kiểm tra end-to-end.

Sau khi xác nhận hoạt động, nên sao lưu cấu hình Router Omada và FortiGate để có thể khôi phục khi cần.

**Ảnh minh họa bước 19:**

<img width="1918" height="941" alt="Screenshot 2026-10-23 112327" src="https://github.com/user-attachments/assets/2320c791-4460-4349-a23e-8574676d04dd" />

---

## Kiểm tra sau khi cấu hình

Sau khi hoàn thành toàn bộ các bước, kiểm tra theo thứ tự từ gần đến xa:

| Thứ tự | Kiểm tra | Kết quả mong muốn |
|---|---|---|
| 1 | Link vật lý | WAN/LAN đều UP |
| 2 | `ipconfig /all` | Client nhận đúng IP, Gateway, DNS |
| 3 | Ping LAN Omada | Thành công |
| 4 | Ping Gateway WAN của Omada | Thành công |
| 5 | Ping `8.8.8.8` | Thành công |
| 6 | `nslookup google.com` | Phân giải được DNS |
| 7 | Mở website | Truy cập Internet bình thường |

### Lệnh kiểm tra trên Windows

```powershell
ipconfig /all
ping <dia-chi-LAN-cua-Omada>
ping 8.8.8.8
nslookup google.com
tracert 8.8.8.8
```

## Một số lỗi thường gặp

### Máy tính không nhận IP

- Kiểm tra DHCP Server trên Omada đã bật chưa.
- Kiểm tra máy tính đang để DHCP tự động.
- Kiểm tra dây mạng và port LAN.
- Kiểm tra VLAN nếu đường từ Omada đến client đi qua switch.

### Máy tính ping được Omada nhưng không ra Internet

- Kiểm tra WAN Omada có IP/Gateway chưa.
- Kiểm tra Omada có route mặc định hay chưa.
- Kiểm tra interface FortiGate nối Omada.
- Kiểm tra Firewall Policy trên FortiGate.
- Kiểm tra NAT trên policy đi Internet.

### Ping `8.8.8.8` được nhưng không vào website

Khả năng cao là lỗi **DNS**. Kiểm tra DNS client bằng:

```powershell
nslookup google.com
```

Có thể thử DNS công cộng trong quá trình kiểm tra, ví dụ `8.8.8.8` hoặc `1.1.1.1`, nếu chính sách mạng cho phép.

---

## Kết luận

Quy trình tổng quát cần nhớ:

```text
Cấu hình WAN Omada
        ↓
Cấu hình LAN Omada
        ↓
Bật DHCP
        ↓
Kiểm tra FortiGate Route + Policy + NAT
        ↓
Máy tính nhận IP
        ↓
Ping Gateway
        ↓
Ping Internet
        ↓
Kiểm tra DNS
        ↓
Truy cập Internet thành công
```
