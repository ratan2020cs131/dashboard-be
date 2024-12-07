from .models import Institute

def get_institute_by_code(institute_code):
    return Institute.objects.filter(institute_code=institute_code).first()