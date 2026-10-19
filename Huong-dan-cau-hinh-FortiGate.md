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

**Không mặc định Default Gateway của máy tính luôn là IP quản trị FortiGate.** Khi chưa biết địa chỉ quản trị, kiểm tra hồ sơ bàn giao hoặc dùng kết nối console được cho phép.

Giữ nguyên cổng quản trị đang dùng trong quá trình cấu hình hai cổng thử nghiệm. Chỉ mở HTTPS/SSH quản trị ở mạng tin cậy; không bật toàn bộ dịch vụ quản trị trên WAN chỉ để giống một ảnh mẫu.

---

<a id="wan"></a>
## 3. Cấu hình WAN nhận IP tự động

Vào **Network → Interfaces**, chỉnh sửa cổng nối modem/router, trong ví dụ là `port1`.

| Mục | Thiết lập |
| --- | --- |
| Alias | `WAN` |
| Role | `WAN` |
| Addressing mode | `DHCP` |
| Retrieve default gateway from server | Bật |
| Override internal DNS | Chỉ bật khi muốn dùng DNS do phía trên cấp |

Nhấn **OK**, kiểm tra trạng thái kết nối và IP đã nhận. Không ghi đè DNS nội bộ khi hệ thống đang phụ thuộc DNS của công ty. [Hướng dẫn DHCP client của Fortinet][nguon-wan].

![Giao diện cấu hình DHCP client và tự nhận default gateway trên FortiGate](https://uploads-us-west-2.insided.com/fortinet-en/attachment/50103i162E67AB8363BCC4.png)

*Hình 2. Các trường DHCP và default gateway trên cổng WAN. IP trong ảnh thuộc ví dụ của Fortinet, không phải IP cần nhập. [Nguồn ảnh][nguon-wan].*

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

*Hình 3. Vị trí các trường IP, DHCP Server, gateway và DNS. Ảnh dùng một mạng khác; nhập thông số theo bảng ví dụ hoặc kế hoạch mạng của bạn. [Nguồn ảnh][nguon-dhcp].*

---

<a id="default-route"></a>
## 5. Kiểm tra đường ra Internet

Với WAN DHCP và **Retrieve default gateway from server** đã bật, FortiGate có thể nhận default route từ máy chủ DHCP. Không tạo thêm một default route thủ công nếu đường hiện có đã đúng. [Tham khảo][nguon-wan].

**Trường hợp khác: WAN dùng IP tĩnh.** Vào **Network → Static Routes → Create New**, đặt đích `0.0.0.0/0`, gateway do nhà mạng hoặc quản trị mạng cung cấp và cổng WAN tương ứng. [Tham khảo cấu hình route][nguon-co-ban].

![Ví dụ tạo default route trên FortiGate với đích 0.0.0.0/0](https://uploads-us-west-2.insided.com/fortinet-en/attachment/kb_19934_4.png)

*Hình 4. Ví dụ default route cho WAN IP tĩnh. Không sao chép gateway `172.25.176.1` trong ảnh vào hệ thống của bạn. [Nguồn ảnh][nguon-tong-quan].*

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

---

<a id="hinh-anh"></a>
## 8. Cách quản lý ảnh trong tài liệu

Bản này sử dụng **4 đường dẫn ảnh trực tuyến có thật từ tài liệu Fortinet**, được kiểm tra mở được ngày **19/10/2026**. Bạn không cần tạo thư mục `images` để dùng bản này.

Ảnh chưa được lưu thành file trong repository của bạn. Việc hiển thị cần kết nối Internet và phụ thuộc nơi lưu ảnh của nguồn; nếu nguồn di chuyển hoặc xóa ảnh, đường dẫn có thể ngừng hoạt động.

Khi có ảnh chụp của riêng bạn, nên che thông tin bí mật, tải ảnh lên cùng repository rồi dùng đường dẫn tương đối. Với tài liệu nằm trong `Network`, đường dẫn `images/ten-anh.png` trỏ tới file nằm trong `Network/images`. [Hướng dẫn đường dẫn ảnh của GitHub][nguon-github].

**Ảnh trong bài được giữ nguyên từ nguồn tham khảo; không được trình bày như ảnh chụp hệ thống của tác giả repository.**

---

## Tài liệu tham khảo

- [Fortinet — Kết nối Internet, interfaces, route và policy][nguon-tong-quan].
- [Fortinet — Cấu hình DHCP client trên interface][nguon-wan].
- [Fortinet — Cấu hình DHCP server][nguon-dhcp].
- [Fortinet — Cấu hình cơ bản][nguon-co-ban].
- [Fortinet — Firewall policy][nguon-policy].
- [Fortinet — NAT trong policy][nguon-nat].
- [Fortinet — Ping và traceroute][nguon-ping].
- [GitHub — Đường dẫn tương đối và ảnh trong Markdown][nguon-github].

[nguon-tong-quan]: https://community.fortinet.com/fortigate-3/technical-tip-fortigate-getting-started-configure-interfaces-and-policies-to-access-internet-97554
[nguon-wan]: https://community.fortinet.com/fortigate-3/technical-tip-how-to-configure-a-fortigate-interface-to-use-dhcp-94965
[nguon-dhcp]: https://community.fortinet.com/fortigate-3/technical-tip-how-to-configure-fortigate-as-dhcp-server-99355
[nguon-co-ban]: https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide/777334/basic-configuration
[nguon-model]: https://docs2.fortinet.com/document/fortigate/7.4.0/administration-guide/954635/getting-started
[nguon-policy]: https://docs.fortinet.com/document/fortigate/7.4.1/administration-guide/656084/firewall-policy
[nguon-nat]: https://docs.fortinet.com/document/%20fortigate/6.0.0/cookbook/667291/creating-a-policy
[nguon-ping]: https://docs.fortinet.com/document/fortigate/7.2.10/administration-guide/982816/running-ping-and-traceroute
[nguon-github]: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes
