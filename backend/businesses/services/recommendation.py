from datetime import datetime, timedelta
from hr.models import EmployeeSkill, Skill
from ..models import employee
from hr.models import order
from hr.models import Customer

class RecommendationService:
    @staticmethod
    def calculate_match_score(employee, order):
        score = 0
        print("Calculating match score for employee: {}".format(employee.last_name))
        print("Order details: {}".format(order))

        # 1. Kiểm tra thời gian làm việc (40%)
        if RecommendationService.check_time_availability(employee, order):
            score += 40
        
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
        
        # 3. Kiểm tra kỹ năng phù hợp (20%)
        required_skills = []
        if hasattr(order, 'required_skills') and order.required_skills:
            required_skills = order.required_skills
        
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
                score += min(20, skill_match * 10)
        
        # 4. Kiểm tra kinh nghiệm (10%)
        employee_exp = getattr(employee, 'experience_years', 0) or 0
        min_exp = getattr(order, 'min_experience', 0) or 0
        if employee_exp >= min_exp:
            score += 10
            
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
        if hasattr(order, 'required_skills') and order.required_skills:
            required_skills = order.required_skills
        
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
            order_end = order_start + timedelta(hours=2)
            
            emp_start = datetime.strptime(employee.working_start_time, '%H:%M').time()
            emp_end = datetime.strptime(employee.working_end_time, '%H:%M').time()
            
            order_start_time = order_start.time()
            order_end_time = order_end.time()
            
            if emp_start <= emp_end:
                return emp_start <= order_start_time and order_end_time <= emp_end
            else:
                return order_start_time >= emp_start or order_end_time <= emp_end
                
        except Exception:
            return False