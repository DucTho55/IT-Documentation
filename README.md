# Hướng dẫn sử dụng draw.io (diagrams.net)

> Tài liệu hướng dẫn cơ bản dành cho người mới, có thể xem trực tiếp trên GitHub.

## 1. draw.io là gì?

**draw.io** (còn gọi là **diagrams.net**) là công cụ vẽ sơ đồ miễn phí, phù hợp để tạo:

- Sơ đồ mạng (Network Diagram)
- Flowchart
- Sơ đồ hệ thống
- UML
- Sơ đồ tổ chức
- Mind map
- Sơ đồ cơ sở dữ liệu
- Sơ đồ quy trình
- Kiến trúc hệ thống / Cloud

Có thể dùng trực tiếp trên trình duyệt hoặc cài bản **draw.io Desktop** để làm việc offline.

---

## 2. Tải draw.io Desktop

Trang phát hành chính thức:

https://github.com/jgraph/drawio-desktop/releases

### Windows

Với máy Windows thông thường 64-bit, ưu tiên tải:

```text
draw.io-<version>-windows-installer.exe
```

Ngoài ra còn có:

```text
draw.io-<version>.msi
draw.io-<version>-windows.zip
```

- **Installer `.exe`**: dễ cài nhất.
- **`.msi`**: phù hợp triển khai trong doanh nghiệp.
- **`.zip`**: bản không cần cài đặt/portable.

> Tại thời điểm tài liệu này được tạo (20/10/2026), bản Desktop mới nhất được ghi nhận là **32.5.5**.

---

## 3. Giao diện chính

![Giao diện draw.io](images/01-editor.png)

Các khu vực quan trọng:

1. **Menu trên cùng**: File, Edit, View, Arrange...
2. **Shapes bên trái**: chứa các hình để kéo vào sơ đồ.
3. **Canvas ở giữa**: khu vực vẽ.
4. **Format bên phải**: chỉnh màu, chữ, đường viền, kích thước...

---

## 4. Tạo sơ đồ mới

Mở draw.io Desktop.

Chọn:

```text
File → New
```

Hoặc khi chương trình hỏi ngay lúc mở, nhập tên file và chọn kiểu sơ đồ.

![Tạo sơ đồ mới](images/02-create-new.png)

Nếu mới làm quen, nên chọn:

```text
Blank Diagram
```

Sau đó bấm **Create**.

---

## 5. Thêm shape vào sơ đồ

Ở cột bên trái, chọn một shape rồi:

```text
Giữ chuột trái → kéo shape → thả vào Canvas
```

Ví dụ có thể dùng:

- Rectangle: thiết bị / bước xử lý
- Ellipse: bắt đầu / kết thúc
- Diamond: điều kiện
- Cloud: Internet / Cloud
- Network: Router, Switch, Server, Firewall...

### Mở thêm thư viện shape

Ở cuối thanh Shapes, chọn:

```text
More Shapes...
```

Sau đó có thể bật:

- Network
- Cisco
- AWS
- Azure
- Google Cloud
- UML
- Entity Relation
- Flowchart

---

## 6. Nối các shape

![Nối connector](images/03-shapes-connectors.png)

Cách nhanh nhất:

1. Rê chuột lên shape.
2. Các **mũi tên màu xanh** xuất hiện.
3. Giữ và kéo mũi tên sang shape khác.
4. Thả chuột.

draw.io sẽ tạo **connector** giữa hai đối tượng.

Connector có thể tự thay đổi đường đi khi bạn di chuyển các shape.

---

## 7. Nhập chữ vào shape

Có thể:

```text
Double-click vào shape
```

Sau đó nhập nội dung.

Ví dụ:

```text
Router
Switch Core
Firewall
Server AD
Internet
```

Bấm ra ngoài để kết thúc nhập.

---

## 8. Đổi màu và định dạng

![Định dạng shape](images/04-format.png)

Chọn shape hoặc connector.

Ở bảng **Format** bên phải có thể chỉnh:

- Fill Color
- Line Color
- Font
- Font Size
- Bold / Italic
- Opacity
- Rounded
- Shadow
- Line Style
- Arrow Type

Nếu không thấy bảng Format:

```text
View → Format Panel
```

---

## 9. Di chuyển nhiều đối tượng cùng lúc

Giữ:

```text
Ctrl
```

rồi click nhiều shape.

Hoặc giữ chuột và kéo một vùng bao quanh các shape.

Sau đó có thể:

- Move
- Copy
- Delete
- Group
- Align

### Group

Chọn nhiều shape rồi:

```text
Ctrl + G
```

### Ungroup

```text
Ctrl + Shift + U
```

---

## 10. Căn thẳng các đối tượng

Chọn nhiều shape.

Vào:

```text
Arrange → Align
```

Có thể chọn:

```text
Left
Center
Right
Top
Middle
Bottom
```

Để chia đều khoảng cách:

```text
Arrange → Distribute
```

---

## 11. Phóng to / thu nhỏ

Có thể dùng:

```text
Ctrl + cuộn con lăn chuột
```

Hoặc dùng mức Zoom ở phía dưới giao diện.

### Fit toàn bộ sơ đồ

Có thể dùng:

```text
View → Zoom → Fit Window
```

---

## 12. Lưu file

![Lưu và xuất file](images/05-save-export.png)

Để tiếp tục sửa sơ đồ sau này, nên lưu file gốc dạng:

```text
.drawio
```

Ví dụ:

```text
so-do-mang-cong-ty.drawio
```

Thao tác:

```text
File → Save As
```

---

## 13. Xuất ảnh PNG

Vào:

```text
File → Export As → PNG
```

Có thể thiết lập:

- Zoom
- Border Width
- Transparent Background
- Selection Only
- Width / Height
- DPI

Sau đó bấm:

```text
Export
```

PNG phù hợp để chèn vào:

- Word
- PowerPoint
- GitHub README
- Website
- Email

---

## 14. Xuất PDF

Vào:

```text
File → Export As → PDF
```

PDF phù hợp khi:

- Gửi sơ đồ cho người khác
- In tài liệu
- Gửi báo cáo
- Lưu sơ đồ nhiều trang

---

## 15. Xuất SVG

Vào:

```text
File → Export As → SVG
```

SVG là ảnh vector nên khi phóng to thường không bị vỡ hình.

Thích hợp cho:

- Website
- Tài liệu kỹ thuật
- Thiết kế
- Sơ đồ cần độ nét cao

---

## 16. Chèn ảnh vào draw.io

Có thể kéo trực tiếp file ảnh từ Windows Explorer vào Canvas.

Hoặc dùng:

```text
Arrange → Insert → Image
```

Một số định dạng thông dụng:

```text
PNG
JPG
SVG
```

---

## 17. Copy và Paste

Copy:

```text
Ctrl + C
```

Paste:

```text
Ctrl + V
```

Nhân bản nhanh:

```text
Ctrl + D
```

Undo:

```text
Ctrl + Z
```

Redo:

```text
Ctrl + Y
```

---

## 18. Ví dụ sơ đồ mạng

![Ví dụ sơ đồ mạng](images/06-example-network.png)

Một sơ đồ mạng cơ bản có thể gồm:

```text
Internet
   │
 Router
   │
 Switch
 ┌─┼─────────┐
 PC Wi‑Fi AP Server
```

Khi vẽ sơ đồ mạng thực tế, nên ghi thêm:

- IP Address
- VLAN
- Gateway
- Subnet
- Tên thiết bị
- Model
- Port
- Uplink
- Trunk / Access

Ví dụ:

```text
Internet
   │
Firewall
192.168.1.1
   │
Core Switch
   │
   ├── VLAN 10 - Office
   ├── VLAN 20 - Camera
   └── VLAN 30 - WiFi
```

---

## 19. Mẹo dùng draw.io hiệu quả

### Bật Grid

```text
View → Grid
```

Giúp căn thiết bị thẳng hàng.

### Bật Guides

```text
View → Guides
```

Giúp căn shape chính xác hơn.

### Khóa đối tượng

Khi đã bố trí xong:

```text
Right-click → Lock
```

Tránh kéo nhầm.

### Đặt nhiều trang

Ở thanh Page phía dưới:

```text
+ 
```

Ví dụ:

```text
Page 1: Tổng quan
Page 2: Network
Page 3: Server
Page 4: WiFi
```

---

## 20. Một số phím tắt hữu ích

| Chức năng | Phím |
|---|---|
| Copy | `Ctrl + C` |
| Paste | `Ctrl + V` |
| Cut | `Ctrl + X` |
| Undo | `Ctrl + Z` |
| Redo | `Ctrl + Y` |
| Select All | `Ctrl + A` |
| Duplicate | `Ctrl + D` |
| Group | `Ctrl + G` |
| Save | `Ctrl + S` |
| Delete | `Delete` |
| Zoom | `Ctrl + Mouse Wheel` |

---

## 21. File `.drawio` là gì?

File:

```text
*.drawio
```

là file sơ đồ gốc của draw.io.

Ví dụ:

```text
network.drawio
server-room.drawio
flowchart.drawio
```

Không nên chỉ giữ PNG/PDF nếu sau này còn cần chỉnh sửa.

Nên lưu:

```text
network.drawio
```

và xuất thêm:

```text
network.png
network.pdf
```

---

## 22. Nên tổ chức thư mục GitHub như thế nào?

Ví dụ:

```text
drawio-guide/
│
├── README.md
│
├── diagrams/
│   ├── network.drawio
│   └── server.drawio
│
└── images/
    ├── 01-editor.png
    ├── 02-create-new.png
    ├── 03-shapes-connectors.png
    ├── 04-format.png
    ├── 05-save-export.png
    └── 06-example-network.png
```

GitHub sẽ tự hiển thị file `README.md` khi mở repository.

---

## 23. Link chính thức

- Website: https://www.drawio.com/
- Trình vẽ online: https://app.diagrams.net/
- Desktop Releases: https://github.com/jgraph/drawio-desktop/releases
- Tài liệu: https://www.drawio.com/docs/

---

## Tóm tắt quy trình cơ bản

```text
Mở draw.io
    ↓
Tạo Blank Diagram
    ↓
Kéo Shape vào Canvas
    ↓
Nối các Shape
    ↓
Nhập tên / thông tin
    ↓
Chỉnh màu và bố cục
    ↓
Lưu file .drawio
    ↓
Xuất PNG / SVG / PDF
```

---

> **Khuyến nghị:** Luôn lưu file `.drawio` gốc trong GitHub để có thể chỉnh sửa về sau, đồng thời export thêm PNG để người xem có thể xem nhanh ngay trong README.
