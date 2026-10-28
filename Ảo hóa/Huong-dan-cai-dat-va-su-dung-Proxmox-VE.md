# Hướng dẫn cài đặt và sử dụng Proxmox VE

## 1. Giới thiệu

**Proxmox VE (Proxmox Virtual Environment)** là nền tảng ảo hóa mã nguồn mở dùng để triển khai và quản lý máy ảo (Virtual Machine - VM) và Linux Container (LXC) trên máy chủ vật lý.

Proxmox VE hỗ trợ:

- Máy ảo KVM.
- Linux Container (LXC).
- Quản lý qua giao diện Web.
- Quản lý Storage.
- Snapshot và Backup.
- Cluster nhiều máy chủ.
- VLAN và Bridge mạng.
- High Availability khi triển khai nhiều node.

---

# 2. Chuẩn bị trước khi cài đặt

Trước khi cài Proxmox VE cần chuẩn bị:

- Một máy chủ hoặc máy tính hỗ trợ ảo hóa.
- CPU hỗ trợ Intel VT-x/VT-d hoặc AMD-V/AMD-Vi.
- RAM tối thiểu khoảng 4 GB, nên sử dụng từ 8 GB trở lên.
- Ổ SSD/HDD để cài hệ điều hành Proxmox.
- USB boot chứa bộ cài Proxmox VE.
- Một cổng mạng LAN.
- Một máy tính khác cùng mạng để truy cập giao diện Web Proxmox.

> **Lưu ý:** Nên đặt IP tĩnh cho Proxmox để địa chỉ quản trị không bị thay đổi sau khi khởi động lại.

---

# 3. Các bước cài đặt Proxmox VE

## Bước 1: Khởi động máy chủ từ USB cài Proxmox

Cắm USB đã tạo bộ cài Proxmox VE vào máy chủ, sau đó khởi động máy.

Vào **Boot Menu** hoặc BIOS/UEFI và chọn USB làm thiết bị khởi động.

<img width="800" alt="Bước 1 - Khởi động bộ cài Proxmox" src="https://github.com/user-attachments/assets/af4e2dbe-c4f8-4ea3-b853-1198028ea752" />

---

## Bước 2: Chọn chế độ cài đặt Proxmox VE

Khi menu cài đặt Proxmox xuất hiện, chọn mục cài đặt **Proxmox VE**.

Thông thường chỉ cần sử dụng chế độ cài đặt đồ họa mặc định.

<img width="800" alt="Bước 2 - Chọn Install Proxmox VE" src="https://github.com/user-attachments/assets/6dc53fee-8e9f-480d-8949-e4adfdd16aa8" />

---

## Bước 3: Khởi động trình cài đặt

Chờ hệ thống nạp các thành phần cần thiết của Proxmox.

Không tắt máy hoặc rút USB trong quá trình này.

<img width="800" alt="Bước 3 - Khởi động trình cài đặt" src="https://github.com/user-attachments/assets/c82edb65-d10d-4a14-b986-992b549ea910" />

---

## Bước 4: Đồng ý điều khoản sử dụng

Đọc điều khoản sử dụng của Proxmox VE.

Chọn **I Agree** để tiếp tục.

<img width="800" alt="Bước 4 - Đồng ý điều khoản" src="https://github.com/user-attachments/assets/aa00e93e-bdf7-4603-b723-f0766a3f6454" />

---

## Bước 5: Chọn ổ đĩa cài đặt

Tại mục **Target Harddisk**, chọn SSD hoặc HDD muốn dùng để cài Proxmox VE.

> **Cảnh báo:** Dữ liệu trên ổ đĩa được chọn có thể bị xóa trong quá trình cài đặt.

Nếu không có yêu cầu đặc biệt, có thể giữ các tùy chọn mặc định.

<img width="800" alt="Bước 5 - Chọn ổ đĩa" src="https://github.com/user-attachments/assets/ca257e50-3d95-4199-ba36-7d066f5711d6" />

---

## Bước 6: Cấu hình quốc gia, múi giờ và bàn phím

Thiết lập các thông tin:

- **Country:** quốc gia.
- **Time zone:** múi giờ.
- **Keyboard Layout:** kiểu bàn phím.

Nếu triển khai tại Việt Nam có thể chọn múi giờ tương ứng với **Asia/Ho_Chi_Minh**.

<img width="800" alt="Bước 6 - Cấu hình quốc gia và múi giờ" src="https://github.com/user-attachments/assets/5665406e-e83a-4b80-bf7a-8f2731af7377" />

---

## Bước 7: Đặt mật khẩu quản trị

Thiết lập mật khẩu cho tài khoản quản trị:

```text
root
```

Nhập thêm địa chỉ Email quản trị để Proxmox sử dụng cho các thông báo hệ thống.

Nên sử dụng mật khẩu mạnh gồm chữ hoa, chữ thường, số và ký tự đặc biệt.

<img width="800" alt="Bước 7 - Đặt mật khẩu root" src="https://github.com/user-attachments/assets/3334e47a-38bc-490f-abdd-6ddbb1905596" />

---

## Bước 8: Chọn card mạng quản trị

Chọn card mạng vật lý sẽ sử dụng để quản trị Proxmox.

Ví dụ card mạng có thể có tên:

```text
eno1
enp1s0
enp2s0
```

Nên chọn cổng mạng đang kết nối với Switch hoặc Router của hệ thống.

<img width="800" alt="Bước 8 - Chọn card mạng" src="https://github.com/user-attachments/assets/1cea45e1-5949-4ef3-821d-f07b55a593b0" />

---

## Bước 9: Cấu hình IP quản trị

Thiết lập địa chỉ mạng cho Proxmox.

Các thông số cần cấu hình gồm:

```text
Hostname
IP Address
Gateway
DNS Server
```

Ví dụ:

```text
Hostname   : pve.local
IP Address : 192.168.1.10/24
Gateway    : 192.168.1.1
DNS Server : 8.8.8.8
```

> IP trên chỉ là ví dụ. Cần sử dụng IP phù hợp với hệ thống mạng thực tế.

<img width="800" alt="Bước 9 - Cấu hình IP Proxmox" src="https://github.com/user-attachments/assets/1f88bea2-d5a0-4c40-830e-138c9883e74c" />

---

## Bước 10: Kiểm tra thông tin trước khi cài đặt

Proxmox sẽ hiển thị lại toàn bộ cấu hình đã thiết lập.

Kiểm tra kỹ:

- Ổ đĩa cài đặt.
- Quốc gia và múi giờ.
- Card mạng.
- Hostname.
- IP Address.
- Gateway.
- DNS.

Nếu thông tin chính xác, tiếp tục quá trình cài đặt.

<img width="800" alt="Bước 10 - Kiểm tra cấu hình" src="https://github.com/user-attachments/assets/62a90d32-181b-4a23-876c-be8ea48da930" />

---

## Bước 11: Tiến hành cài đặt

Proxmox bắt đầu:

- Phân vùng ổ đĩa.
- Cài hệ điều hành.
- Cài kernel.
- Cài các dịch vụ quản lý.
- Cấu hình mạng.
- Cài giao diện Web Management.

Chờ quá trình cài đặt hoàn thành.

<img width="800" alt="Bước 11 - Cài đặt Proxmox" src="https://github.com/user-attachments/assets/5405eac7-d34d-4351-b905-05be3bc75451" />

---

## Bước 12: Hoàn tất quá trình cài đặt

Sau khi quá trình cài đặt hoàn tất, hệ thống sẽ thông báo cài đặt thành công.

Ghi lại địa chỉ IP quản trị được hiển thị trên màn hình.

<img width="800" alt="Bước 12 - Hoàn tất cài đặt" src="https://github.com/user-attachments/assets/9c9df007-ec5a-4d9d-a6e6-0e0f7bc87f92" />

---

## Bước 13: Khởi động lại máy chủ

Chọn **Reboot** để khởi động lại máy.

Nếu hệ thống yêu cầu, hãy tháo USB cài đặt để máy khởi động từ ổ đĩa đã cài Proxmox.

<img width="800" alt="Bước 13 - Khởi động lại máy chủ" src="https://github.com/user-attachments/assets/acc38b62-a430-4612-91dc-f6805de31e89" />

---

## Bước 14: Khởi động Proxmox từ ổ cứng

Sau khi reboot, Proxmox sẽ được nạp từ ổ đĩa của máy chủ.

Chờ hệ thống khởi động hoàn toàn.

<img width="800" alt="Bước 14 - Khởi động Proxmox" src="https://github.com/user-attachments/assets/069567fd-edad-472e-b8e7-667e39723d77" />

---

## Bước 15: Kiểm tra màn hình Console

Khi khởi động thành công, màn hình Console của Proxmox sẽ hiển thị địa chỉ dùng để truy cập giao diện Web.

Thông thường có dạng:

```text
https://IP-PROXMOX:8006
```

Ví dụ:

```text
https://192.168.1.10:8006
```

<img width="800" alt="Bước 15 - Console Proxmox" src="https://github.com/user-attachments/assets/d9cd698d-eb14-4dbe-890b-cf686698b737" />

---

## Bước 16: Kiểm tra kết nối mạng

Từ một máy tính cùng mạng LAN với Proxmox, kiểm tra kết nối bằng lệnh:

### Windows

```powershell
ping 192.168.1.10
```

### Linux

```bash
ping 192.168.1.10
```

Nếu có phản hồi từ Proxmox thì có thể tiếp tục truy cập giao diện Web.

<img width="800" alt="Bước 16 - Kiểm tra kết nối" src="https://github.com/user-attachments/assets/09f99122-9ab9-40b5-be7d-a0c1cc117442" />

---

## Bước 17: Truy cập giao diện Web Proxmox

Trên máy tính quản trị, mở trình duyệt và nhập:

```text
https://<IP-Proxmox>:8006
```

Ví dụ:

```text
https://192.168.1.10:8006
```

Do Proxmox mặc định sử dụng chứng chỉ tự ký nên trình duyệt có thể hiển thị cảnh báo bảo mật.

Chọn tiếp tục truy cập trang Web.

<img width="800" alt="Bước 17 - Truy cập Web Proxmox" src="https://github.com/user-attachments/assets/d78be3c7-006e-4449-85e7-84d3d21db327" />

---

# 4. Đăng nhập và sử dụng Proxmox

## Bước 18: Đăng nhập Proxmox

Tại màn hình đăng nhập nhập:

```text
User name : root
Password  : mật khẩu đã tạo khi cài đặt
Realm     : Linux PAM standard authentication
```

Sau đó chọn **Login**.

<img width="900" alt="Bước 18 - Đăng nhập Proxmox" src="https://github.com/user-attachments/assets/b16e0300-8a8e-464f-98c1-b6145790a34a" />

---

## Bước 19: Kiểm tra Node Proxmox

Sau khi đăng nhập, bên trái giao diện sẽ hiển thị cấu trúc Datacenter.

Thông thường gồm:

```text
Datacenter
└── Node Proxmox
    ├── local
    └── local-lvm
```

Chọn tên **Node** để xem trạng thái máy chủ như:

- CPU.
- RAM.
- Storage.
- Network.
- Uptime.
- Phiên bản Proxmox.

<img width="1000" alt="Bước 19 - Giao diện quản trị Proxmox" src="https://github.com/user-attachments/assets/468214b8-a19f-46c3-b1a4-d41fbe45c1be" />

---

## Bước 20: Kiểm tra trạng thái hệ thống

Trong phần **Summary**, kiểm tra:

- CPU Usage.
- Memory Usage.
- Storage Usage.
- Server Load.
- Kernel Version.
- Uptime.

Nếu các thông số hoạt động bình thường thì quá trình cài đặt Proxmox VE đã hoàn tất.

<img width="1000" alt="Bước 20 - Kiểm tra trạng thái Proxmox" src="https://github.com/user-attachments/assets/9e60f5ba-b3c7-4b2d-bb4a-6b7fa2acddd2" />

---

# 5. Các chức năng cơ bản trên Proxmox

Sau khi cài đặt xong, có thể bắt đầu thực hiện các công việc quản trị.

## 5.1. Upload file ISO

Để cài Windows hoặc Linux cho máy ảo:

```text
Node
→ local
→ ISO Images
→ Upload
```

Chọn file `.iso` từ máy tính và upload lên Proxmox.

---

## 5.2. Tạo máy ảo

Chọn:

```text
Create VM
```

Sau đó cấu hình lần lượt:

1. **General** - đặt tên máy ảo.
2. **OS** - chọn file ISO.
3. **System** - cấu hình BIOS/Machine.
4. **Disks** - cấu hình ổ đĩa.
5. **CPU** - cấp CPU.
6. **Memory** - cấp RAM.
7. **Network** - cấu hình card mạng.
8. **Confirm** - kiểm tra và tạo VM.

---

## 5.3. Khởi động máy ảo

Chọn VM vừa tạo:

```text
VM
→ Start
```

Sau đó mở:

```text
Console
```

để tiến hành cài hệ điều hành.

---

# 6. Một số mục quan trọng trong Proxmox

| Mục | Chức năng |
|---|---|
| **Datacenter** | Quản lý toàn bộ hệ thống Proxmox |
| **Node** | Quản lý máy chủ vật lý |
| **Summary** | Xem trạng thái CPU, RAM, Disk |
| **Shell** | Truy cập Terminal của Proxmox |
| **System** | Quản lý dịch vụ và hệ thống |
| **Network** | Cấu hình Bridge, NIC, VLAN |
| **Disks** | Quản lý ổ đĩa |
| **local** | Lưu ISO, Backup, Template |
| **local-lvm** | Lưu ổ đĩa máy ảo |
| **VM** | Máy ảo KVM |
| **CT** | Linux Container LXC |

---

# 7. Kiểm tra sau khi cài đặt

Sau khi hoàn tất, cần kiểm tra:

- [ ] Proxmox khởi động bình thường.
- [ ] Máy quản trị ping được IP Proxmox.
- [ ] Truy cập được `https://IP:8006`.
- [ ] Đăng nhập được bằng tài khoản `root`.
- [ ] Node hiển thị trạng thái Online.
- [ ] CPU và RAM được nhận đầy đủ.
- [ ] Storage hoạt động bình thường.
- [ ] Card mạng hoạt động bình thường.

---

# 8. Kết luận

Sau khi hoàn thành các bước trên, máy chủ đã được cài đặt **Proxmox VE** và có thể quản lý thông qua trình duyệt Web.

Các bước tiếp theo nên thực hành:

1. Upload ISO.
2. Tạo máy ảo Windows/Linux.
3. Cấu hình Linux Bridge.
4. Cấu hình VLAN.
5. Thêm Storage.
6. Snapshot VM.
7. Backup và Restore VM.
8. Clone VM.
9. Tạo Template.
10. Triển khai Proxmox Cluster.
