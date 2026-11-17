# 01 — Samba Active Directory LAB

Tài liệu dựa trên các screenshot triển khai **dc1 / ad.lab.test**, thử nghiệm với `samba-tool`, DNS/Kerberos, quản lý Windows ADUC và xác thực người dùng từ Keycloak.

## 1. Thành phần đã triển khai

| Hạng mục | Dữ liệu xác nhận |
|---|---|
| Domain | `ad.lab.test` |
| DC | `dc1` |
| Samba network namespace | `samba-lab` |
| DNS trong LAB | `10.250.10.2` |
| Cấu hình Samba | `/opt/samba-ad-lab/host-provision/etc/smb.conf` |
| OU thử nghiệm | `OU=LAB-TEST,DC=ad,DC=lab,DC=test` |
| Group thử nghiệm | `GG-LAB-Users` |
| User thử nghiệm | `test.lab01` (CN hiển thị `Test Lab01`) |

## 2. Tạo VM, chuẩn bị công cụ Windows

Dự án sử dụng Proxmox để xây dựng máy `dc1` và một VM Windows Server quản trị. Quy trình bằng ảnh gồm: tạo VM, chuẩn bị ISO/ổ đĩa, cấu hình NIC, cài Windows Server, **Server Manager → Add Roles and Features → Remote Server Administration Tools → AD DS Tools**, và mở **Active Directory Users and Computers**.

![Cấu hình mạng của VM Windows trong Proxmox](../assets/2026-11-12/20261112-033316.png)

*Cấu hình mạng của VM Windows trong Proxmox*

![Thêm RSAT/AD DS Tools trên Windows Server](../assets/2026-11-12/20261112-041709.png)

*Thêm RSAT/AD DS Tools trên Windows Server*



> Các thông số CPU/RAM/ISO ở từng ảnh là trạng thái tại thời điểm chụp, không phải cấu hình bắt buộc. Không thay đổi VM hiện tại chỉ để khớp screenshot.

## 3. Kiểm tra Samba theo namespace và file cấu hình riêng

**Đừng chạy `sudo samba-tool ...` trực tiếp trên host `dc1` nếu bản LAB này đặt Samba trong namespace/provision riêng.** Ví dụ thực tế khi chạy thiếu cấu hình đã báo không tìm thấy `/var/lib/samba/private/sam.ldb`.

```bash
# Xác minh tài khoản trong namespace Samba
sudo ip netns exec samba-lab samba-tool user show test.lab01 \
  --configfile=/opt/samba-ad-lab/host-provision/etc/smb.conf
```

Kiểm tra thông tin cần có: `sAMAccountName: test.lab01`, `userPrincipalName: test.lab01@ad.lab.test`, DN thuộc `OU=LAB-TEST`.

## 4. Kiểm tra DNS và Kerberos

```bash
# Truy vấn DNS AD nội bộ từ network namespace của Samba
sudo ip netns exec samba-lab host auth.ad.lab.test 10.250.10.2
sudo ip netns exec samba-lab host cloud.ad.lab.test 10.250.10.2

# Kiểm tra sau khi dịch vụ được cấu hình
sudo ip netns exec samba-lab ss -lntup
```

Đã ghi nhận `auth.ad.lab.test` và `cloud.ad.lab.test` phân giải về `172.16.120.243`. Việc **thêm bản ghi DNS** phải sử dụng đúng zone, host record và file `smb.conf` của LAB, tránh thêm trùng khi bản ghi đã tồn tại.



## 5. Quản trị OU và người dùng bằng ADUC

Tại VM Windows quản trị: mở **Active Directory Users and Computers**, kết nối domain `ad.lab.test`, vào `OU=LAB-TEST`, kiểm tra/tạo group `GG-LAB-Users` và user `test.lab01`. Các ảnh lịch sử thể hiện cả trường hợp đăng nhập/ủy quyền chưa đúng và thao tác sửa.

![Active Directory Users and Computers](../assets/2026-11-13/20261113-075029.png)

*Active Directory Users and Computers*

![OU LAB-TEST trong Active Directory](../assets/2026-11-13/20261113-075401.png)

*OU LAB-TEST trong Active Directory*



## 6. Đặt lại mật khẩu user thử nghiệm

Sau khi xác minh tài khoản hiện hữu và có quyền quản trị Samba:

```bash
sudo ip netns exec samba-lab samba-tool user setpassword test.lab01 \
  --configfile=/opt/samba-ad-lab/host-provision/etc/smb.conf
```

Nhập mật khẩu mới khi chương trình hỏi `New Password` và `Retype Password`. Kết quả `Changed Password OK` là bằng chứng mật khẩu AD được đổi thành công. Không ghi mật khẩu vào Markdown hay ảnh công khai.

## 7. Tích hợp với Keycloak

Keycloak trong Realm `cloud-lab` có LDAP User Federation trỏ đến Samba AD, tìm người dùng dưới `OU=LAB-TEST,DC=ad,DC=lab,DC=test`. Cấu hình quan sát được ban đầu sử dụng `CN=Test Lab01,...` làm **Bind DN**. Khi người dùng này đổi mật khẩu, **Bind credentials** lưu trong Keycloak cũng phải được cập nhật, nếu không sẽ gặp `LDAP error code 49 (data 52e)`.

**Khuyến nghị cải tiến:** tách tài khoản service bind riêng chỉ đọc (ví dụ `svc_keycloak`) khỏi `test.lab01`, tránh gãy kết nối LDAP mỗi lần đổi mật khẩu người dùng thử nghiệm.

![Màn hình LDAP test authentication thất bại do Bind credentials cũ](../assets/2026-11-16/20261116-094610.png)

*Màn hình LDAP test authentication thất bại do Bind credentials cũ*



## 8. Kiểm thử cuối

- [ ] `samba-tool user show test.lab01` chạy được với `--configfile` đúng.
- [ ] DNS `auth.ad.lab.test` và `cloud.ad.lab.test` trả IP mong đợi.
- [ ] ADUC hiển thị OU/group/user.
- [ ] `Test connection` và `Test authentication` của Keycloak đều thành công.
- [ ] Người dùng đăng nhập Nextcloud bằng tài khoản Samba AD thông qua Keycloak.

Xem thêm: [Các lỗi thực tế](../docs/TROUBLESHOOTING.md) · [Toàn bộ ảnh Samba](SCREENSHOTS.md).
