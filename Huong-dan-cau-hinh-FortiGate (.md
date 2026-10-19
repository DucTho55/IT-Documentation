# Hướng dẫn cấu hình FortiGate cơ bản
<a id="mo-hinh"></a>
## 1. Mô hình và thông số ví dụ

![Sơ đồ kết nối mạng nội bộ qua FortiGate ra Internet](https://uploads-us-west-2.insided.com/fortinet-en/attachment/kb_19934_1.png)

*Hình 1. Mô hình LAN → FortiGate → Internet. 

Ví dụ trong bài giả định modem/router phía trước **đã có Internet và đang cấp DHCP**. Đây không phải hướng dẫn quay PPPoE trực tiếp.

| Thành phần | Giá trị dùng trong ví dụ |
| --- | --- |
| Cổng ra modem/router | `port1`, dùng làm WAN |
| Cổng xuống switch/máy tính | `port2`, dùng làm LAN |
| IP WAN | Nhận tự động từ modem/router |
| IP LAN của FortiGate | `192.168.50.1/24` |
| Dải DHCP cấp cho máy tính | `192.168.50.100` đến `192.168.50.200` |
| Gateway của máy tính LAN | `192.168.50.1` |
| DNS ví dụ cho máy tính thử nghiệm | `1.1.1.1`, `8.8.8.8` |

**Đây là thông số giả định để học.** Chỉ sử dụng khi dải LAN không trùng với mạng WAN, VPN hoặc các mạng hiện có. Tên cổng thay đổi theo model; đối chiếu cổng thực tế trước khi chọn. [Tham khảo về khác biệt giữa các model][nguon-model].

---

<a id="truy-cap"></a>
## 2. Truy cập thiết bị

Kết nối máy tính vào mạng quản trị, mở địa chỉ HTTPS đã được cấu hình và đăng nhập bằng tài khoản được cấp. Không lấy một mật khẩu trong tài liệu mẫu để thử trên thiết bị.

![Trang đăng nhập Web GUI FortiGate trong bài mẫu](https://raw.githubusercontent.com/hiiamtu16/InternReport/043bdcd189c99fe0b11615a7d470e4fc421be96e/Picture%20/Network%20/C%E1%BA%A5u%20h%C3%ACnh%20Firewall%20Fortinet%20FortiGate-300E/login_web.png)

*Hình 2. Ô Username, Password và nút Login. Thông báo "Your session has expired" thuộc ảnh nguồn, không phải lỗi trên thiết bị của bạn.

**Không mặc định Default Gateway của máy tính luôn là IP quản trị FortiGate.** Khi chưa biết địa chỉ quản trị, kiểm tra hồ sơ bàn giao hoặc dùng kết nối console được cho phép.

Giữ nguyên cổng quản trị đang dùng trong quá trình cấu hình hai cổng thử nghiệm. Chỉ mở HTTPS/SSH quản trị ở mạng tin cậy; không bật toàn bộ dịch vụ quản trị trên WAN chỉ để giống một ảnh mẫu.

---

<a id="wan"></a>
## 3. Cấu hình WAN nhận IP tự động

Vào **Network → Interfaces**, chỉnh sửa cổng nối modem/router, trong ví dụ là `port1`.

![Network Interfaces và vị trí chọn cổng được khoanh đỏ](https://raw.githubusercontent.com/hiiamtu16/InternReport/265780e8ccbfa4c8fe45a07d777526fa013accef/Picture%20/Network%20/C%E1%BA%A5u%20h%C3%ACnh%20Firewall%20Fortinet%20FortiGate-300E/choosePort.png)

*Hình 3. Mở Network → Interfaces rồi chọn cổng nối modem/router. Khung đỏ là chú thích có sẵn trong ảnh mẫu. Không sao chép IP, Loopback hoặc danh sách dịch vụ quản trị trong ảnh. 

| Mục | Thiết lập |
| --- | --- |
| Alias | `WAN` |
| Role | `WAN` |
| Addressing mode | `DHCP` |
| Retrieve default gateway from server | Bật |
| Override internal DNS | Chỉ bật khi muốn dùng DNS do phía trên cấp |

Nhấn **OK**, kiểm tra trạng thái kết nối và IP đã nhận. Không ghi đè DNS nội bộ khi hệ thống đang phụ thuộc DNS của công ty. [Hướng dẫn DHCP client của Fortinet][nguon-wan].

![Giao diện cấu hình DHCP client và tự nhận default gateway trên FortiGate](https://uploads-us-west-2.insided.com/fortinet-en/attachment/50103i162E67AB8363BCC4.png)

*Hình 4. Các trường DHCP và default gateway trên cổng WAN. IP trong ảnh thuộc ví dụ của Fortinet, không phải IP cần nhập. 

---

<a id="lan-dhcp"></a>
## 4. Cấu hình LAN và DHCP

Vào **Network → Interfaces**, chỉnh sửa cổng LAN thử nghiệm `port2`.

| Mục | Giá trị ví dụ |
| --- | --- |
| Role | `LAN` |
| Addressing mode | `Manual` |
| IP/Netmask | `192.168.50.1/255.255.255.0` |
| DHCP Server | Bật |
| Address range | `192.168.50.100` – `192.168.50.200` |
| Netmask | `255.255.255.0` |
| Default gateway | Same as Interface IP |
| DNS server | Specify: `1.1.1.1`, `8.8.8.8` |

Chỉ bật DHCP trên mạng thử nghiệm chưa có máy chủ DHCP khác. Đặt máy tính thử nghiệm ở chế độ nhận IP tự động. [Hướng dẫn DHCP server của Fortinet][nguon-dhcp].

![Cấu hình địa chỉ LAN và DHCP Server trên FortiGate](https://uploads-us-west-2.insided.com/fortinet-en/attachment/67499iD572F94ABD10AF3B.png)

*Hình 5. Vị trí các trường IP, DHCP Server, gateway và DNS. Ảnh dùng một mạng khác; nhập thông số theo bảng ví dụ hoặc kế hoạch mạng của bạn. 

---

<a id="default-route"></a>
## 5. Kiểm tra đường ra Internet

Với WAN DHCP và **Retrieve default gateway from server** đã bật, FortiGate có thể nhận default route từ máy chủ DHCP. Không tạo thêm một default route thủ công nếu đường hiện có đã đúng. [Tham khảo][nguon-wan].

**Trường hợp khác: WAN dùng IP tĩnh.** Vào **Network → Static Routes → Create New**, đặt đích `0.0.0.0/0`, gateway do nhà mạng hoặc quản trị mạng cung cấp và cổng WAN tương ứng. [Tham khảo cấu hình route][nguon-co-ban].

![Ví dụ tạo default route trên FortiGate với đích 0.0.0.0/0](https://uploads-us-west-2.insided.com/fortinet-en/attachment/kb_19934_4.png)

*Hình 6. Ví dụ default route cho WAN IP tĩnh. Không sao chép gateway `172.25.176.1` trong ảnh vào hệ thống của bạn. 

DNS của chính FortiGate được cấu hình tại **Network → DNS**. Phân biệt phần này với DNS cấp cho máy tính qua DHCP. [Tham khảo][nguon-tong-quan].

---

<a id="policy"></a>
## 6. Tạo policy LAN ra Internet

Tạo address object kiểu subnet tên `LAN_NET`, chứa mạng ví dụ `192.168.50.0/24`. Sau đó vào **Policy & Objects → Firewall Policy → Create New**.

| Mục | Thiết lập minh họa |
| --- | --- |
| Name | `LAN-to-Internet` |
| Incoming Interface | `port2` |
| Outgoing Interface | `port1` |
| Source | `LAN_NET` |
| Destination | `all`, cho ví dụ truy cập Internet |
| Schedule | `always` |
| Service | `DNS`, `HTTP`, `HTTPS`, `PING` |
| Action | `ACCEPT` |
| NAT | Bật, dùng địa chỉ cổng ra |
| Log Allowed Traffic | Bật để kiểm tra |

Đối chiếu policy đang có, thứ tự xử lý và nhu cầu dịch vụ trước khi lưu. Không thay thế toàn bộ chính sách bảo mật hiện tại bằng policy ví dụ này. [Tham khảo policy][nguon-policy] · [Tham khảo NAT][nguon-nat].

> Phần này giả định dùng NAT ngay trong policy. Khi Central SNAT hoặc chế độ policy khác đang được sử dụng, cần điều chỉnh cách cấu hình; không tự ý tắt các tính năng đang hoạt động.

![Các mục NAT Use Outgoing Interface Address và Log Allowed Traffic trong firewall policy](https://uploads-us-west-2.insided.com/fortinet-en/attachment/79856i3CCE1F41FC768FD6.png)

*Hình 7. Vị trí NAT → Use Outgoing Interface Address và Log Allowed Traffic → All Sessions. Ảnh chỉ minh họa hai nhóm tùy chọn này; các giá trị policy và Security Profiles khác trong ảnh không thay thế bảng cấu hình phía trên.

---

<a id="kiem-tra"></a>
## 7. Kiểm tra kết nối

Trên máy tính Windows trong LAN, chạy từng lệnh:

```cmd
ipconfig
ping 192.168.50.1
ping 1.1.1.1
nslookup example.com
```

![Kết quả ipconfig với IPv4 Subnet Mask và Default Gateway được khoanh đỏ](https://raw.githubusercontent.com/hiiamtu16/InternReport/3c10797db448de5b8658e702e81872fe4fd88dbf/Picture%20/Network%20/C%E1%BA%A5u%20h%C3%ACnh%20Firewall%20Fortinet%20FortiGate-300E/CheckIP.png)

*Hình 8. Vị trí IPv4 Address, Subnet Mask và Default Gateway trong kết quả ipconfig. Ảnh dùng mạng quản trị của tác giả nguồn; với ví dụ trong bài, gateway LAN là 192.168.50.1.


![Ví dụ kiểm tra IP và ping với khung đỏ chỉ lệnh](https://raw.githubusercontent.com/hiiamtu16/InternReport/0c6f287b84b49d833d5d3903f2c52117110ef991/Picture%20/Network%20/C%E1%BA%A5u%20h%C3%ACnh%20Firewall%20Fortinet%20FortiGate-300E/ping.png)

*Hình 9. Cách đọc dòng Reply from và thống kê mất gói. Đây là kết quả trong bài nguồn, không phải kết quả kiểm tra mạng của bạn. Dùng các lệnh trong khối lệnh phía trên; phần tracert -d bị thiếu đích ở cuối ảnh không phải bước cần làm. 

Đồng thời mở thử một trang HTTPS. Không kết luận mất Internet chỉ dựa vào ping thất bại, vì ICMP có thể bị chặn.

Trên CLI của FortiGate có thể kiểm tra:

```text
execute ping 1.1.1.1
execute ping example.com
```

Các lệnh từ FortiGate kiểm tra kết nối của chính thiết bị, không thay thế kiểm tra từ máy tính LAN. [Tham khảo công cụ kiểm tra][nguon-ping].

Xem **Log & Report → Forward Traffic** để đối chiếu lưu lượng với policy. [Tham khảo logging][nguon-tong-quan].

### Danh sách hoàn tất

- [ ] Máy tính nhận đúng IP, gateway và DNS.
- [ ] Truy cập được địa chỉ LAN của FortiGate theo quyền cho phép.
- [ ] Máy tính truy cập được trang HTTPS.
- [ ] Lưu lượng được xử lý bởi policy dự kiến.
- [ ] Cấu hình được sao lưu sau khi kiểm tra.
- [ ] Ảnh và tài liệu đăng công khai không chứa bí mật.

<a id="hinh-anh"></a>

---

