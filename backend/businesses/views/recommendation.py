from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Employee
from hr.models import Order
from ..serializers.recommendation import RecommendationSerializer
from ..services.recommendation import RecommendationService

@api_view(['GET'])
def get_recommendations(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        employees = Employee.objects.filter(status='active')
        
        recommendations = []
        
        for employee in employees:
            score = RecommendationService.calculate_match_score(employee, order)
            if score > 0:
                recommendations.append({
                    'employee': employee,
                    'score': score,
                    'reasons': RecommendationService.get_match_reasons(employee, order)
                })
        
        # Sắp xếp theo điểm số từ cao xuống thấp
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        
        serializer = RecommendationSerializer(recommendations, many=True)
        return Response(serializer.data)
        
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)