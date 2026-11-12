# Superstore Sales & Profit Analysis — Giới thiệu tiếng Việt

Đây là dự án portfolio thuộc lĩnh vực **Data Analytics & Business Intelligence**, sử dụng **Python, pandas, Matplotlib và Power BI** để phân tích hiệu quả kinh doanh bán lẻ. Mục tiêu là đi từ dữ liệu giao dịch đến phát hiện có bằng chứng và đề xuất hành động có thể kiểm chứng.

Xem [README chính](../README.md) để cài đặt và chạy dự án. Tài liệu này giới thiệu ngắn gọn bài toán, quy trình và các sản phẩm phân tích.

## Bài toán kinh doanh

Doanh thu lớn có đi cùng lợi nhuận tốt? Khu vực và nhóm sản phẩm nào cần ưu tiên rà soát? Mức giảm giá có liên hệ như thế nào với biên lợi nhuận? Cần theo dõi KPI nào trước khi thay đổi chính sách kinh doanh?

Nguồn dữ liệu là **Tableau Sample – Superstore**, bộ dữ liệu bán lẻ mẫu phục vụ học tập, gồm **9.994 dòng mặt hàng**, **5.009 đơn hàng**, từ **03/01/2014 đến 30/12/2017**. Một dòng là một mặt hàng trong đơn; số dòng không phải số đơn hàng. Nguồn gốc và định nghĩa trường được trình bày trong [từ điển dữ liệu](data_dictionary.md).

## Quy trình phân tích

| Giai đoạn | Công việc và sản phẩm |
|---|---|
| **Data Cleaning** | Kiểm tra trường bắt buộc, dữ liệu thiếu và trùng; chuẩn hóa ngày và số; giữ lại lợi nhuận âm hợp lệ. Xem [kết quả chất lượng dữ liệu](../reports/data_quality/data_quality.json). |
| **EDA** | Tính KPI và phân tích theo thời gian, khu vực, danh mục, nhóm hàng, mức giảm giá. Xem [notebook](../notebooks/01_superstore_analysis.ipynb) và [bảng tổng hợp](../reports/tables/). |
| **Data Visualization** | Biểu đồ Python và báo cáo Power BI để khám phá xu hướng và các phân khúc có hiệu quả thấp. Xem [biểu đồ](../reports/figures/) và [hướng dẫn Power BI](../powerbi/README.md). |
| **Business Insights** | Kết nối số liệu với vấn đề kinh doanh, đồng thời nêu giới hạn của kết luận. Xem [phân tích phát hiện](business_insights.md). |
| **Business Recommendations** | Ưu tiên rà soát nhóm hàng lỗ, thử nghiệm chính sách giảm giá và theo dõi lợi nhuận bằng KPI; không tự khẳng định mức cải thiện chưa đo lường. Xem [đề xuất và cách đánh giá](business_insights.md#prioritized-recommendations). |

## Các kết quả đáng chú ý

- Tổng doanh thu **2.297.200,86 USD**, lợi nhuận **286.397,02 USD**, biên lợi nhuận **12,47%** — [KPI](../reports/tables/kpi.json).
- **Tables** lỗ **17.725,48 USD**, biên lợi nhuận **−8,56%** — [kết quả theo nhóm hàng](../reports/tables/summary_subcategory.csv).
- **Central** có biên lợi nhuận thấp nhất, **7,92%**; riêng **Central × Furniture** lỗ **2.871,05 USD** — [kết quả vùng × danh mục](../reports/tables/summary_region_category.csv).
- Nhóm giảm giá **trên 40%** có **933 dòng mặt hàng**, đều ghi nhận lợi nhuận âm, tổng lỗ **99.558,59 USD** — [kết quả theo mức giảm giá](../reports/tables/summary_discount_group.csv).

Biên lợi nhuận được tính bằng **tổng Profit / tổng Sales**, không lấy trung bình tỷ lệ từng dòng. Mối liên hệ giữa giảm giá và lợi nhuận là quan sát trong dữ liệu, **không chứng minh quan hệ nhân quả**. Việc điều chỉnh giá cần xem thêm sản phẩm, khu vực, thời gian và có thử nghiệm phù hợp.

## Sản phẩm portfolio

- [Mã phân tích Python](../src/analyze.py) và [notebook trình bày quy trình](../notebooks/01_superstore_analysis.ipynb).
- [Dữ liệu đã chuẩn hóa](../data/processed/superstore_clean.csv), [bảng kết quả](../reports/tables/) và [biểu đồ](../reports/figures/).
- [Dashboard Power BI](../powerbi/Superstore_Dashboard.pbix) và [công thức DAX](../powerbi/measures.dax). Sau khi tải về, cần cập nhật đường dẫn nguồn dữ liệu và kiểm tra refresh trong Power BI Desktop.
- [Báo cáo PDF](../reports/Superstore_Project_Report.pdf) và [phát hiện kèm đề xuất kinh doanh](business_insights.md).

Dữ liệu lịch sử này phục vụ học tập và giới thiệu năng lực phân tích; không đại diện cho tình hình hiện tại của một doanh nghiệp thật. Nguồn tham khảo: [Tableau Sample Data](https://public.tableau.com/app/learn/sample-data) và [bản CSV sử dụng](https://gist.github.com/SharmaAshwini/8bd642f6c46792a9c40c8ccad60391e9).
