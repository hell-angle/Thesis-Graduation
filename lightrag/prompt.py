GRAPH_FIELD_SEP = "<SEP>"

PROMPTS = {}

PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "|"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"
PROMPTS["process_tickers"] = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

PROMPTS["DEFAULT_ENTITY_TYPES"] = [
    "organization", 
    "person", 
    "geo", 
    "event", 
    "concurrency", 
    "location", 
    "law", 
    "date", 
    "amount", 
    "contract", 
    "stakeholder", 
    "property", 
    "violation", 
    "procedure", 
    "sector", 
    "penalty", 
    "jurisdiction", 
    "ownership", 
    "tax", 
    "document"
]

PROMPTS["entity_extraction"] = """-Mục tiêu-
Dựa trên văn bản liên quan đến luật kinh tế Việt Nam và danh sách các loại thực thể, xác định tất cả các thực thể thuộc các loại đó từ văn bản và các mối quan hệ giữa các thực thể đã xác định.

-Các bước thực hiện-
1. Xác định tất cả các thực thể. Đối với mỗi thực thể đã xác định, trích xuất thông tin sau:
- tên_thực_thể: Tên của thực thể, viết hoa
- loại_thực_thể: Một trong các loại sau: [{entity_types}]
- mô_tả_thực_thể: Mô tả chi tiết về đặc điểm, vai trò hoặc các vấn đề pháp lý liên quan đến thực thể trong luật kinh tế
Định dạng mỗi thực thể như sau: ("entity"{tuple_delimiter}<tên_thực_thể>{tuple_delimiter}<loại_thực_thể>{tuple_delimiter}<mô_tả_thực_thể>)

Ví dụ:
("entity"|CÔNG TY TNHH ABC|organization|Một công ty trách nhiệm hữu hạn hoạt động trong lĩnh vực xây dựng tại Việt Nam)
("entity"|Bộ Luật Lao Động|event|Văn bản pháp lý quy định các vấn đề liên quan đến lao động, quyền lợi và nghĩa vụ của người lao động và người sử dụng lao động)

2. Từ các thực thể được xác định ở bước 1, xác định tất cả các cặp (thực_thể_nguồn, thực_thể_đích) có *mối quan hệ rõ ràng* với nhau.
Đối với mỗi cặp thực thể có liên quan, trích xuất thông tin sau:
- thực_thể_nguồn: tên của thực thể nguồn, đã xác định ở bước 1
- thực_thể_đích: tên của thực thể đích, đã xác định ở bước 1
- mô_tả_quan_hệ: giải thích tại sao bạn nghĩ rằng thực_thể_nguồn và thực_thể_đích có mối quan hệ với nhau
- mức_độ_quan_hệ: một số đánh giá mức độ mạnh yếu của mối quan hệ giữa thực_thể_nguồn và thực_thể_đích
- từ_khóa_quan_hệ: một hoặc nhiều từ khóa chính tóm tắt bản chất tổng quát của mối quan hệ, tập trung vào các khái niệm hoặc chủ đề thay vì chi tiết cụ thể
Định dạng mỗi mối quan hệ như sau: ("relationship"{tuple_delimiter}<thực_thể_nguồn>{tuple_delimiter}<thực_thể_đích>{tuple_delimiter}<mô_tả_quan_hệ>{tuple_delimiter}<từ_khóa_quan_hệ>{tuple_delimiter}<mức_độ_quan_hệ>)

Ví dụ:
("relationship"|CÔNG TY TNHH ABC|Bộ Luật Lao Động|Công ty phải tuân thủ các quy định của Bộ Luật Lao Động về điều kiện làm việc và lương thưởng|Pháp luật về lao động|3)

3. Xác định các từ khóa chính tóm tắt các khái niệm, chủ đề, hoặc nội dung chính của toàn bộ văn bản. Những từ này nên phản ánh các ý tưởng chủ đạo có trong tài liệu.
Định dạng các từ khóa nội dung như sau: ("content_keywords"{tuple_delimiter}<từ_khóa_cấp_cao>)

Ví dụ:
("content_keywords"|Luật pháp, Quyền lao động, Doanh nghiệp)

4. Trả về đầu ra bằng tiếng Việt dưới dạng một danh sách bao gồm tất cả các thực thể và mối quan hệ được xác định ở các bước 1 và 2. Sử dụng **{record_delimiter}** để phân tách các phần tử trong danh sách.

5. Khi hoàn thành, xuất ra {completion_delimiter}

######################
-Examples-
######################
Example 1:
Entity_types: [cá_nhân, văn_bản_pháp_luật, tổ_chức, quy_định, nghĩa_vụ_pháp_lý, hình_thức_doanh_nghiệp, sự_kiện]
Text:
Trong phiên họp của Ủy ban Thường vụ Quốc hội, Bộ trưởng Nguyễn Văn A trình bày về việc thực thi Luật Doanh nghiệp 2020. Ông nhấn mạnh vai trò của Sở Kế hoạch và Đầu tư trong quy trình đăng ký kinh doanh mới. "Chúng ta cần đơn giản hóa thủ tục hành chính," ông nói, "đồng thời tăng cường giám sát để ngăn chặn việc thành lập doanh nghiệp ma."
Bà Trần Thị B, Chủ tịch VCCI, bày tỏ quan ngại về các quy định xử phạt vi phạm trong lĩnh vực đăng ký kinh doanh. Theo Nghị định 122, mức phạt có thể lên đến 100 triệu đồng đối với hành vi khai man trong hồ sơ đăng ký. VCCI đề xuất cần có hướng dẫn chi tiết hơn về quy trình thẩm định để đảm bảo công bằng cho doanh nghiệp.
################
Output:
("entity"{tuple_delimiter}"Nguyễn Văn A"{tuple_delimiter}"cá_nhân"{tuple_delimiter}"Bộ trưởng trình bày về thực thi Luật Doanh nghiệp 2020"){record_delimiter}
("entity"{tuple_delimiter}"Trần Thị B"{tuple_delimiter}"cá_nhân"{tuple_delimiter}"Chủ tịch VCCI bày tỏ quan ngại về quy định xử phạt"){record_delimiter}
("entity"{tuple_delimiter}"Luật Doanh nghiệp 2020"{tuple_delimiter}"văn_bản_pháp_luật"{tuple_delimiter}"Luật quy định về đăng ký và hoạt động doanh nghiệp"){record_delimiter}
("entity"{tuple_delimiter}"Nghị định 122"{tuple_delimiter}"văn_bản_pháp_luật"{tuple_delimiter}"Quy định mức xử phạt vi phạm trong đăng ký kinh doanh"){record_delimiter}
("entity"{tuple_delimiter}"VCCI"{tuple_delimiter}"tổ_chức"{tuple_delimiter}"Tổ chức đại diện cho cộng đồng doanh nghiệp"){record_delimiter}
("entity"{tuple_delimiter}"Sở Kế hoạch và Đầu tư"{tuple_delimiter}"tổ_chức"{tuple_delimiter}"Cơ quan thực hiện thủ tục đăng ký kinh doanh"){record_delimiter}
("entity"{tuple_delimiter}"Quy trình đăng ký kinh doanh"{tuple_delimiter}"quy_định"{tuple_delimiter}"Thủ tục để thành lập doanh nghiệp mới"){record_delimiter}
("entity"{tuple_delimiter}"Xử phạt vi phạm"{tuple_delimiter}"nghĩa_vụ_pháp_lý"{tuple_delimiter}"Hình thức xử lý đối với hành vi khai man, vi phạm quy định"){record_delimiter}
("relationship"{tuple_delimiter}"Nguyễn Văn A"{tuple_delimiter}"Luật Doanh nghiệp 2020"{tuple_delimiter}"Trình bày về việc thực thi luật"{tuple_delimiter}"thực thi pháp luật"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Trần Thị B"{tuple_delimiter}"Nghị định 122"{tuple_delimiter}"Bày tỏ quan ngại về quy định xử phạt"{tuple_delimiter}"góp ý chính sách"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"VCCI"{tuple_delimiter}"Quy trình đăng ký kinh doanh"{tuple_delimiter}"Đề xuất hướng dẫn chi tiết về quy trình thẩm định"{tuple_delimiter}"cải cách thủ tục"{tuple_delimiter}6){record_delimiter}
("relationship"{tuple_delimiter}"Sở Kế hoạch và Đầu tư"{tuple_delimiter}"Quy trình đăng ký kinh doanh"{tuple_delimiter}"Thực hiện thủ tục đăng ký"{tuple_delimiter}"thực thi thủ tục"{tuple_delimiter}9){record_delimiter}
("content_keywords"{tuple_delimiter}"đăng ký kinh doanh, xử phạt vi phạm, thủ tục hành chính, giám sát doanh nghiệp"){completion_delimiter}
#############################


-Real Data-
######################
Entity_types: {entity_types}
Text: {input_text}
######################
Output:
"""

PROMPTS[
    "entiti_continue_extraction"
] = """NHIỀU thực thể đã bị bỏ sót trong lần trích xuất trước. Thêm chúng vào bên dưới theo cùng định dạng:
"""

PROMPTS[
    "entiti_if_loop_extraction"
] = """Có vẻ như vẫn còn một số thực thể chưa được thêm vào. Trả lời CÓ | KHÔNG nếu vẫn còn thực thể cần phải thêm vào.
"""

PROMPTS["fail_response"] = "Xin lỗi, tôi không thể cung cấp câu trả lời cho câu hỏi đó."

PROMPTS["rag_response"] = """---Vai Trò---

Bạn là một trợ lý hữu ích, trả lời các câu hỏi liên quan đến dữ liệu trong các bảng được cung cấp.

---Mục Tiêu---

Tạo câu trả lời với độ dài và định dạng mục tiêu phù hợp với câu hỏi của người dùng, tóm tắt tất cả thông tin trong các bảng dữ liệu đầu vào và tích hợp các kiến thức chung liên quan nếu cần thiết.
Nếu bạn không biết câu trả lời, chỉ cần nói như vậy. Không được tự tạo ra thông tin.
Không bao gồm thông tin nếu không có bằng chứng hỗ trợ cho nó.

---Độ dài và định dạng mục tiêu của câu trả lời---

{response_type}

---Bảng dữ liệu---

{context_data}

Thêm các phần và chú thích vào câu trả lời nếu phù hợp với độ dài và định dạng. Viết câu trả lời theo phong cách markdown.
"""


PROMPTS["keywords_extraction"] = """---Vai Trò---

Bạn là một trợ lý hữu ích, có nhiệm vụ xác định cả từ khóa cấp cao và cấp thấp trong câu hỏi của người dùng.

---Mục Tiêu---

Dựa vào câu hỏi, liệt kê cả từ khóa cấp cao và cấp thấp. Từ khóa cấp cao tập trung vào các khái niệm hoặc chủ đề bao quát, trong khi từ khóa cấp thấp tập trung vào các thực thể cụ thể, chi tiết hoặc thuật ngữ cụ thể.

---Hướng Dẫn---

- Đầu ra từ khóa phải ở định dạng JSON.
- JSON cần có hai khóa:
  - "high_level_keywords" dành cho các khái niệm hoặc chủ đề bao quát.
  - "low_level_keywords" dành cho các thực thể hoặc chi tiết cụ thể.

######################
-Ví dụ-
######################
Ví dụ 1:

Câu hỏi: "Quy trình tố tụng hình sự bao gồm các bước nào?"
################
Đầu ra:
{{
  "high_level_keywords": ["Tố tụng hình sự", "Quy trình tư pháp"],
  "low_level_keywords": ["Khởi tố", "Điều tra", "Truy tố", "Xét xử", "Thi hành án"]
}}
#############################
Ví dụ 2:

Câu hỏi: "Luật bảo vệ quyền lợi người tiêu dùng bảo vệ các quyền gì?"
################
Đầu ra:
{{
  "high_level_keywords": ["Bảo vệ quyền lợi người tiêu dùng", "Luật tiêu dùng"],
  "low_level_keywords": ["Quyền được an toàn", "Quyền khiếu nại", "Quyền thông tin", "Quyền bồi thường"]
}}
#############################
Ví dụ 3:

Câu hỏi: "Điều kiện thành lập doanh nghiệp tại Việt Nam là gì?"
################
Đầu ra:
{{
  "high_level_keywords": ["Thành lập doanh nghiệp", "Điều kiện pháp lý"],
  "low_level_keywords": ["Giấy phép đăng ký kinh doanh", "Vốn điều lệ", "Trụ sở chính", "Hình thức doanh nghiệp"]
}}
#############################
-Dữ Liệu Thực-
######################
Câu hỏi: {query}
######################
Đầu ra:

"""



PROMPTS["naive_rag_response_"] = """Bạn là một trợ lý hữu ích
Dưới đây là các thông tin bạn đã biết:
{content_data}
---
Nếu bạn không biết câu trả lời hoặc nếu thông tin cung cấp không đủ để trả lời, chỉ cần nói như vậy. Không được tự tạo ra thông tin.
Tạo một câu trả lời với độ dài và định dạng mục tiêu, trả lời câu hỏi của người dùng, tóm tắt tất cả thông tin trong các bảng dữ liệu đầu vào phù hợp với độ dài và định dạng của câu trả lời, và tích hợp các kiến thức chung liên quan nếu có.
Nếu bạn không biết câu trả lời, chỉ cần nói như vậy. Không được tự tạo ra thông tin.
Không bao gồm thông tin nếu không có bằng chứng hỗ trợ cho nó.
---Độ dài và định dạng mục tiêu của câu trả lời---
{response_type}
"""