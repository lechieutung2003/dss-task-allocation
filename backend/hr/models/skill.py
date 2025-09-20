from django.db import models
from base.models import TimeStampedModel

class Skill(TimeStampedModel):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "hr_skill"

class EmployeeSkill(TimeStampedModel):
    employee = models.ForeignKey('businesses.Employee', on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    class Meta:
        db_table = "hr_employee_skill"
        unique_together = ("employee", "skill")
