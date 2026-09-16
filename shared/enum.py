from enum import Enum



class StrEnum(str, Enum):

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()
    
    def _generate_value(self):
        return self.name.lower()
    
    @property
    def value(self):
        return self._generate_value()
    

# class UserRole(str, Enum):
#     ADMIN = 'admin'
#     REGULAR_USER = 'regular_user'

