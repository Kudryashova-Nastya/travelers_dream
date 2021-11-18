from travelers_dream.models import Employee


def employee_now(request):
    if request.user.is_superuser:
        return {}

    if request.user.is_staff:
        employee = Employee.objects.get(user=request.user.id)
        return {'employee_now': employee}

    return {}