# Thông tin chi tiết về mô hình LOS estimator và cách xây dựng tập huấn luyện cho mô hình này

## Sơ lược về cách chia thời điểm trong ngày của BKTraffic

Hệ thống hiện tại đang chia một ngày thành các period (thời điểm) với khoảng thời gian 30 phút, bắt đầu từ period_0_00 đến period_23_30, với period_xx_yy biểu hiện cho thời điểm vào giờ xx và phút yy. 

Ví dụ: 
* period_0_00 là mốc thời gian 0h00
* period_0_30 là mốc thời gian 0h30
* period_18_30 là mốc thời gian 18h30
* period_23_30 là mốc thời gian 23h30

## Dữ liệu để huấn luyện mô hình ước tính LOS

Hiện tại, BKTraffic đang có xxxx segment report được lưu tại collection SegmentReports trong MongoDB. Dữ liệu này chứa thông tin về tình trạng giao thông **thực tế** của các segment vào các period trong ngày thông qua báo cáo trực tiếp từ người dùng từ dd/mm/yyyy đến dd/mm/yyyy. Tuy nhiên, do số lượng người dùng chưa nhiều, kho dữ liệu này chưa bao quát được hết tất cả các segment trong hệ thống vào tất cả các period trong khoảng thời gian nói trên.


Theo lý thuyết, BKTraffic Server sẽ dùng dữ liệu thực tế này cho các tính năng như routing, hiển thị tình trạng giao thông, v.v. Tuy nhiên do thiếu hụt dữ liệu nên thay vào đó hệ thống sẽ sử dụng dữ liệu nền (base data) được lưu ở collection BaseTrafficStatus. Dữ liệu nền đã được các nhóm trước nghiên cứu và cấu hình sẵn, nó cho biết **LOS của một segment tại một thời điểm trong ngày**.

Cũng vì thế, hướng đi hiện tại cho việc xây dựng tập dataset là ta sẽ đắp dữ liệu nền này vào các thời điểm còn thiếu trong khoảng thời gian từ xx đến yy. Kết hợp thêm các thông tin bổ sung như: tọa độ điểm đầu, điểm cuối và độ dài của mỗi segment, thông tin về ngày, tháng, năm của dữ liệu báo cáo, v.v để làm giàu nên dữ liệu huấn luyện.

Code để xây dựng tập huấn luyện có thể tìm thấy ở ```los_dataset/```

## Mô hình ước tính LOS

Sau khi đã xây dựng xong tập dataset, ta cần xác định những feature nào là dữ liệu phân loại (categorial data), feature nào là dữ liệu số (numerical data) để áp dụng các phương pháp mã hóa cho phù hợp (thư viện nổi tiếng hỗ trợ mã hóa dữ liệu là sci-kit learn):

* Categorial features: 
* Numerical features:

Mô hình ước tính LOS hiện tại là một mạng neural network đơn giản có cấu trúc như sau:

(chèn hình)