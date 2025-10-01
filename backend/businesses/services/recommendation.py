from datetime import datetime, timedelta
from hr.models import EmployeeSkill, Skill
from ..models import employee
from hr.models import order
from hr.models import Customer, ServiceType

class RecommendationService:
    @staticmethod
    def calculate_match_score(employee, order):

        print("================================")

        score = 0

        # 1. Kiểm tra thời gian làm việc (40%)
        if RecommendationService.check_time_availability(employee, order):
            score += 40
        
        print(score)

        # 2. Kiểm tra khu vực (30%)
        # Lấy khu vực từ customer thay vì order
        order_area = None
        if hasattr(order, 'customer') and order.customer:
            order_area = getattr(order.customer, 'area', None)
        elif hasattr(order, 'customer_details') and order.customer_details:
            # Nếu lưu dưới dạng customer_details (JSON/dict)
            order_area = order.customer_details.get('area', None)

        if order_area and employee.area == order_area:
            score += 30
        
        print(score)

        # 3. Kiểm tra kỹ năng phù hợp (20%)
        required_skills = []
        if hasattr(order, 'service_type_id') and order.service_type_id:
            try:
                service_type = ServiceType.objects.get(id=order.service_type_id)
                if hasattr(service_type, 'name') and service_type.name:
                    required_skills = [service_type.name]
            except Exception as e:
                print(f"Error getting service type: {e}")
        
        # Lấy kỹ năng của nhân viên từ bảng liên kết
        employee_skills = []
        employee_skill_records = EmployeeSkill.objects.filter(employee=employee)
        if employee_skill_records:
            employee_skills = [es.skill.name for es in employee_skill_records]
        
        if required_skills and employee_skills:
        # Phần còn lại giữ nguyên
            required_skills_set = set(required_skills)
            employee_skills_set = set(employee_skills)
            skill_match = len(required_skills_set.intersection(employee_skills_set))
            if skill_match > 0:
                # score += min(20, skill_match * 10)
                score += 20
        
        print(score)
        
        # 4. Kiểm tra kinh nghiệm/khối lượng công việc (10%)
        # Nhân viên có ít đơn hàng đã hoàn thành sẽ được ưu tiên hơn
        try:
            # Lấy số đơn hàng đã hoàn thành của nhân viên này
            employee_completed_orders = getattr(employee, 'completed_orders_count', 0) or 0
            
            # Lấy ra max completed_orders_count từ tất cả nhân viên
            from ..models.employee import Employee
            max_completed_orders = Employee.objects.all().order_by('-completed_orders_count').first()
            max_value = max_completed_orders.completed_orders_count if max_completed_orders else 0
            
            print("employee_completed_orders", employee_completed_orders)
            print("max_completed_orders", max_value)
            
            # Tính điểm ngược: càng ít đơn thì điểm càng cao
            if max_value > 0:  # Tránh chia cho 0
                # Công thức: 10 * (1 - số đơn của nhân viên / max số đơn)
                normalized_score = 1 - (employee_completed_orders / max_value)
                # Nhân với 10 để có tối đa 10 điểm, làm tròn 2 chữ số thập phân
                experience_score = round(10 * normalized_score, 2)
                score += experience_score
                print("experience_score", experience_score)
            else:
                # Nếu không có dữ liệu, mọi nhân viên có điểm như nhau
                score += 5
                print("experience_score (default)", 5)
        except Exception as e:
            print("Error calculating workload score:", e)
            # Mặc định cộng 5 điểm nếu có lỗi
            score += 5

        print("Final score:", score)
            
        return score

    @staticmethod
    def get_match_reasons(employee, order):
        reasons = []
        
        if RecommendationService.check_time_availability(employee, order):
            reasons.append("Có thể làm việc trong thời gian yêu cầu")
        
        # Lấy khu vực từ customer thay vì order
        order_area = None
        if hasattr(order, 'customer') and order.customer:
            order_area = getattr(order.customer, 'area', None)
        elif hasattr(order, 'customer_details') and order.customer_details:
            # Nếu lưu dưới dạng customer_details (JSON/dict)
            order_area = order.customer_details.get('area', None)
        
        if order_area and employee.area == order_area:
            reasons.append("Làm việc trong cùng khu vực")
        
        # Kiểm tra thuộc tính tồn tại trước khi sử dụng
        required_skills = []
        if hasattr(order, 'ServiceType') and order.ServiceType:
            required_skills = [order.ServiceType.name]
        
        employee_skills = []
        employee_skill_records = EmployeeSkill.objects.filter(employee=employee)
        if employee_skill_records:
            employee_skills = [es.skill.name for es in employee_skill_records]
        
        if required_skills and employee_skills:
            required_skills_set = set(required_skills)
            employee_skills_set = set(employee_skills)
            matching_skills = required_skills_set.intersection(employee_skills_set)
            if matching_skills:
                reasons.append(f"Có {len(matching_skills)} kỹ năng phù hợp")
        
        employee_exp = getattr(employee, 'experience_years', 0) or 0
        min_exp = getattr(order, 'min_experience', 0) or 0
        if employee_exp >= min_exp:
            reasons.append("Đủ kinh nghiệm yêu cầu")
            
        return reasons

    @staticmethod
    def check_time_availability(employee, order):
        try:

            if not employee.working_start_time or not employee.working_end_time:
                return False

            order_start = order.preferred_start_time
            order_end = order.preferred_end_time
            
            emp_start = employee.working_start_time
            emp_end = employee.working_end_time
            
            order_start_time = order_start.time()
            order_end_time = order_end.time()
            
            if emp_start <= emp_end:
                print("1")
                return emp_start <= order_start_time and order_end_time <= emp_end
            else:
                print("2")
                return order_start_time >= emp_start or order_end_time <= emp_end

        except Exception as error:
            print("Error details:", error) 
            return False