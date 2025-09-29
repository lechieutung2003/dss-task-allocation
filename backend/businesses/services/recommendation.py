from datetime import datetime, timedelta
from ..models import employee
from hr.models import Order

class RecommendationService:
    @staticmethod
    def calculate_match_score(employee, order):
        score = 0
        
        # 1. Kiểm tra thời gian làm việc (40%)
        if RecommendationService.check_time_availability(employee, order):
            score += 40
        
        # 2. Kiểm tra khu vực (30%)
        if employee.area == order.area:
            score += 30
        
        # 3. Kiểm tra kỹ năng phù hợp (20%)
        required_skills = set(order.required_skills)
        employee_skills = set(employee.skills)
        skill_match = len(required_skills.intersection(employee_skills))
        if skill_match > 0:
            score += min(20, skill_match * 10)
        
        # 4. Kiểm tra kinh nghiệm (10%)
        if employee.experience_years >= order.min_experience:
            score += 10
            
        return score

    @staticmethod
    def get_match_reasons(employee, order):
        reasons = []
        
        if RecommendationService.check_time_availability(employee, order):
            reasons.append("Có thể làm việc trong thời gian yêu cầu")
        
        if employee.area == order.area:
            reasons.append("Làm việc trong cùng khu vực")
        
        required_skills = set(order.required_skills)
        employee_skills = set(employee.skills)
        matching_skills = required_skills.intersection(employee_skills)
        if matching_skills:
            reasons.append(f"Có {len(matching_skills)} kỹ năng phù hợp")
        
        if employee.experience_years >= order.min_experience:
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