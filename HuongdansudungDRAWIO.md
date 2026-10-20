# Hướng dẫn sử dụng draw.io (diagrams.net)

> Tài liệu hướng dẫn nhanh cách sử dụng **draw.io / diagrams.net** để vẽ sơ đồ, lưu file và xuất ảnh.

## 1. Giao diện chính

Sau khi mở draw.io, giao diện thường gồm:

- **Menu** ở phía trên: File, Edit, View, Arrange, Extras, Help.
- **Thanh công cụ**: hoàn tác, làm lại, zoom, thêm đường nối, v.v.
- **Shape Libraries** bên trái: nơi chứa các hình khối.
- **Drawing Canvas** ở giữa: vùng dùng để vẽ sơ đồ.
- **Format Panel** bên phải: chỉnh màu sắc, chữ, kích thước và vị trí.

![Giao diện draw.io](https://www.drawio.com/img/blog/interface-introduction.png)

---

## 2. Tạo sơ đồ mới

1. Chọn **Create New Diagram** nếu màn hình hỏi bạn muốn tạo mới hay mở file có sẵn.
2. Nhập tên sơ đồ.
3. Chọn **Blank Diagram** để bắt đầu từ trang trắng.
4. Nhấn **Create**.

![Tạo sơ đồ mới](https://www.drawio.com/img/blog/basic-flow-create-blank-diagram.png)

---

## 3. Thêm hình khối vào sơ đồ

Có thể thêm hình theo một trong các cách sau:

- Kéo hình từ danh sách bên trái vào vùng vẽ.
- Nhấp trực tiếp vào một hình trong thư viện.
- Nhấp đúp vào vùng trống trên canvas rồi chọn hình cần dùng.

Các hình thường dùng:

| Hình | Công dụng thường gặp |
|---|---|
| Rectangle | Một bước hoặc tác vụ |
| Diamond | Điều kiện / quyết định |
| Oval | Bắt đầu / kết thúc |
| Cylinder | Cơ sở dữ liệu / nơi lưu trữ |

![Thêm hình vào canvas](https://www.drawio.com/img/blog/basic-flow-add-shape.gif)

---

## 4. Nối các hình bằng mũi tên

1. Đưa chuột lên hình nguồn.
2. Các mũi tên hướng sẽ xuất hiện quanh hình.
3. Kéo từ một mũi tên sang hình đích.
4. Thả chuột khi hình đích được đánh dấu.

Đường nối sẽ tự bám theo hình khi bạn di chuyển các khối.

![Nối hai hình](https://www.drawio.com/img/blog/basic-flow-floating-connector.gif)

---

## 5. Thêm chữ vào hình và đường nối

### Thêm chữ vào hình

1. Nhấp đúp vào hình.
2. Gõ nội dung.
3. Nhấn **Enter** để hoàn tất.

### Thêm chữ vào đường nối

Nhấp đúp vào đường nối tại vị trí muốn đặt chữ rồi nhập nội dung, ví dụ `Yes`, `No`, `OK`, `Fail`.

![Thêm nhãn](https://www.drawio.com/img/blog/basic-flow-add-labels.gif)

---

## 6. Di chuyển, thay đổi kích thước và xóa hình

- **Di chuyển:** giữ chuột trái và kéo hình.
- **Thay đổi kích thước:** chọn hình rồi kéo các điểm điều khiển ở viền.
- **Xóa:** chọn hình và nhấn **Delete** hoặc **Backspace**.
- **Chọn nhiều hình:** giữ **Shift** rồi nhấp lần lượt các hình.

Mẹo: dùng `Ctrl + Z` để hoàn tác nếu thao tác nhầm.

---

## 7. Đổi màu và kiểu hiển thị

1. Chọn hình hoặc đường nối cần chỉnh.
2. Mở tab **Style** ở bảng bên phải.
3. Chọn màu có sẵn hoặc thay đổi:
   - Fill: màu nền.
   - Line: màu viền hoặc đường nối.
   - Rounded: bo góc.
   - Shadow: bóng đổ.
4. Sang tab **Text** để chỉnh font, cỡ chữ, màu chữ và căn lề.

![Chỉnh style](https://www.drawio.com/img/blog/basic-flow-style-diagram.gif)

Bảng màu nhanh:

![Bảng màu Style](https://www.drawio.com/img/blog/basic-flow-style-palette.png)

---

## 8. Lưu file để chỉnh sửa lại

Để giữ nguyên toàn bộ sơ đồ và có thể sửa về sau:

1. Chọn **File → Save As**.
2. Đặt tên file.
3. Lưu dưới định dạng `.drawio`.

Ví dụ:

```text
So-do-he-thong-mang.drawio
```

Nên giữ file `.drawio` làm file gốc, sau đó xuất thêm PNG/PDF khi cần gửi cho người khác.

---

## 9. Xuất sơ đồ thành ảnh PNG

1. Chọn **File → Export as → PNG**.
2. Chỉnh các lựa chọn nếu cần.
3. Nhấn **Export**.

Một số tùy chọn hữu ích:

- **Zoom:** độ phân giải ảnh.
- **Transparent Background:** nền trong suốt.
- **Selection Only:** chỉ xuất các hình đang chọn.
- **Include a copy of my diagram:** nhúng dữ liệu sơ đồ để có thể mở lại trong draw.io ở một số trường hợp.

![Xuất PNG](https://www.drawio.com/img/blog/basic-flow-export-as-png.png)

---

## 10. Xuất PDF

Chọn:

```text
File → Export as → PDF
```

Sau đó chọn các thiết lập phù hợp và nhấn **Export**.

PDF phù hợp khi cần gửi tài liệu, in ấn hoặc đính kèm vào báo cáo.

---

## 11. Một số phím tắt hữu ích

| Phím tắt | Chức năng |
|---|---|
| `Ctrl + Z` | Hoàn tác |
| `Ctrl + Y` | Làm lại |
| `Ctrl + C` | Sao chép |
| `Ctrl + V` | Dán |
| `Ctrl + D` | Nhân đôi đối tượng |
| `Delete` | Xóa đối tượng |
| `Ctrl + A` | Chọn tất cả |
| `Ctrl + G` | Nhóm các đối tượng |
| `Ctrl + Shift + G` | Bỏ nhóm |
| `Ctrl + S` | Lưu |

---

## 12. Quy trình sử dụng nhanh

```text
Mở draw.io
   ↓
Tạo Blank Diagram
   ↓
Kéo các hình vào canvas
   ↓
Nối các hình bằng connector
   ↓
Nhập nội dung
   ↓
Chỉnh màu và bố cục
   ↓
Lưu file .drawio
   ↓
Xuất PNG hoặc PDF
```

## Ví dụ kết quả

Một sơ đồ đơn giản sau khi hoàn thành có thể trông như sau:

![Ví dụ flowchart](https://www.drawio.com/img/blog/basic-flow.png)

---


