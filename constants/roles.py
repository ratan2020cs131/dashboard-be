from enum import Enum

class Roles(Enum):
    SUPERADMIN = "superadmin"
    ADMIN = "admin"
    FACULTY = "faculty"
    STUDENT = "student"

    @classmethod
    def choices(cls):
        return [(key.value, key.value.title()) for key in cls]