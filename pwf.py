from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
import re
from datetime import datetime
from decimal import Decimal
from urllib.parse import urlparse

@dataclass
class ValidationResult:
    is_valid: bool = True
    errors: List[str] = field(default_factory=list)
    field_errors: Dict[str, List[str]] = field(default_factory=dict)

    def add_field_error(self, field_name: str, error: str) -> None:
        """Add a field-specific error message."""
        if field_name not in self.field_errors:
            self.field_errors[field_name] = []
        self.field_errors[field_name].append(error)
        self.errors.append(f"{field_name}: {error}")
        self.is_valid = False

    def merge(self, other: 'ValidationResult') -> 'ValidationResult':
        """Merge this validation result with another one."""
        result = ValidationResult()
        result.is_valid = self.is_valid and other.is_valid
        result.errors = self.errors + other.errors
        
        for field_name, errors in self.field_errors.items():
            result.field_errors[field_name] = errors.copy()
            
        for field_name, errors in other.field_errors.items():
            if field_name not in result.field_errors:
                result.field_errors[field_name] = []
            result.field_errors[field_name].extend(errors)
            
        return result

class ValidationRule:
    def __init__(self, rule: Callable[[Any], bool], error_message: str):
        self.rule = rule
        self.error_message = error_message
    
    def validate(self, value: Any) -> Tuple[bool, str]:
        """Execute the validation rule and return result with error message."""
        return self.rule(value), self.error_message

class Validator:
    def __init__(self, field_name: Optional[str] = None):
        self.rules: List[ValidationRule] = []
        self.field_name = field_name
    
    def add_rule(self, rule: Callable[[Any], bool], error_message: str) -> 'Validator':
        """Add a validation rule with its error message."""
        self.rules.append(ValidationRule(rule, error_message))
        return self
    
    def validate(self, value: Any) -> ValidationResult:
        """Validate the value against all rules."""
        result = ValidationResult()
        
        for rule in self.rules:
            is_valid, error = rule.validate(value)
            if not is_valid:
                if self.field_name:
                    result.add_field_error(self.field_name, error)
                else:
                    result.errors.append(error)
                    result.is_valid = False
                
        return result

class CommonValidators:
    @staticmethod
    def email_validator(field_name: str = "Email") -> Validator:
        """Create an email validator."""
        return Validator(field_name).add_rule(
            lambda email: bool(email), "Email is required"
        ).add_rule(
            lambda email: isinstance(email, str) and bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email)),
            "Invalid email format"
        )
    
    @staticmethod
    def name_validator(min_length: int = 2, max_length: int = 50, field_name: str = "Name") -> Validator:
        """Create a name validator."""
        return Validator(field_name).add_rule(
            lambda name: bool(name), "Name is required"
        ).add_rule(
            lambda name: len(name) >= min_length,
            f"Name must be at least {min_length} characters long"
        ).add_rule(
            lambda name: len(name) <= max_length,
            f"Name cannot exceed {max_length} characters"
        ).add_rule(
            lambda name: bool(re.match(r"^[a-zA-Z\s-']+$", name)),
            "Name can only contain letters, spaces, hyphens, and apostrophes"
        )
    
    @staticmethod
    def phone_validator(required_length: int = 10, field_name: str = "Phone") -> Validator:
        """Create a phone number validator."""
        return Validator(field_name).add_rule(
            lambda phone: bool(phone), "Phone number is required"
        ).add_rule(
            lambda phone: phone.isdigit(), "Phone number can only contain digits"
        ).add_rule(
            lambda phone: len(phone) == required_length,
            f"Phone number must be exactly {required_length} digits"
        )
    
    @staticmethod
    def password_validator(field_name: str = "Password") -> Validator:
        """Create a password validator with complexity requirements."""
        return Validator(field_name).add_rule(
            lambda pwd: bool(pwd), "Password is required"
        ).add_rule(
            lambda pwd: len(pwd) >= 8, "Password must be at least 8 characters long"
        ).add_rule(
            lambda pwd: bool(re.search(r"[A-Z]", pwd)),
            "Password must contain at least one uppercase letter"
        ).add_rule(
            lambda pwd: bool(re.search(r"[a-z]", pwd)),
            "Password must contain at least one lowercase letter"
        ).add_rule(
            lambda pwd: bool(re.search(r"\d", pwd)),
            "Password must contain at least one number"
        ).add_rule(
            lambda pwd: bool(re.search(r"[^a-zA-Z0-9]", pwd)),
            "Password must contain at least one special character"
        )
    
    @staticmethod
    def url_validator(field_name: str = "URL") -> Validator:
        """Create a URL validator."""
        def is_valid_url(url: str) -> bool:
            try:
                result = urlparse(url)
                return all([result.scheme, result.netloc])
            except:
                return False
        
        return Validator(field_name).add_rule(
            lambda url: bool(url), "URL is required"
        ).add_rule(
            is_valid_url, "Invalid URL format"
        )
    
    @staticmethod
    def date_validator(
        min_date: Optional[datetime] = None,
        max_date: Optional[datetime] = None,
        field_name: str = "Date"
    ) -> Validator:
        """Create a date validator."""
        validator = Validator(field_name)
        
        if min_date:
            validator.add_rule(
                lambda date: date >= min_date,
                f"Date must be on or after {min_date.strftime('%Y-%m-%d')}"
            )
        
        if max_date:
            validator.add_rule(
                lambda date: date <= max_date,
                f"Date must be on or before {max_date.strftime('%Y-%m-%d')}"
            )
        
        return validator
    
    @staticmethod
    def currency_validator(
        min_value: Optional[Decimal] = None,
        max_value: Optional[Decimal] = None,
        field_name: str = "Amount"
    ) -> Validator:
        """Create a currency validator."""
        validator = Validator(field_name).add_rule(
            lambda amount: amount >= 0, "Amount cannot be negative"
        ).add_rule(
            lambda amount: Decimal(str(amount)).as_tuple().exponent >= -2,
            "Amount cannot have more than 2 decimal places"
        )
        
        if min_value is not None:
            validator.add_rule(
                lambda amount: amount >= min_value,
                f"Amount must be at least {min_value}"
            )
        
        if max_value is not None:
            validator.add_rule(
                lambda amount: amount <= max_value,
                f"Amount cannot exceed {max_value}"
            )
        
        return validator

@dataclass
class UserProfile:
    """Example user profile class with various fields."""
    email: str
    first_name: str
    last_name: str
    phone_number: str
    password: str
    website: str
    date_of_birth: datetime
    salary: Decimal

class ValidationBuilder:
    """Builder class for creating complex validators."""
    def __init__(self):
        self.validations: Dict[str, Callable[[Any], ValidationResult]] = {}
    
    def add_validation(self, property_name: str, validation: Callable[[Any], ValidationResult]):
        """Add a validation function for a specific property."""
        self.validations[property_name] = validation
        return self
    
    def validate(self, entity: Any) -> ValidationResult:
        """Validate an entity against all registered validations."""
        result = ValidationResult()
        
        for validation in self.validations.values():
            property_result = validation(entity)
            result = result.merge(property_result)
        
        return result

class UserProfileValidator:
    """Validator for UserProfile objects."""
    def __init__(self):
        self.validator = ValidationBuilder()
        self.validator.add_validation(
            "email",
            lambda p: CommonValidators.email_validator().validate(p.email)
        ).add_validation(
            "first_name",
            lambda p: CommonValidators.name_validator(field_name="FirstName").validate(p.first_name)
        ).add_validation(
            "last_name",
            lambda p: CommonValidators.name_validator(field_name="LastName").validate(p.last_name)
        ).add_validation(
            "phone_number",
            lambda p: CommonValidators.phone_validator().validate(p.phone_number)
        ).add_validation(
            "password",
            lambda p: CommonValidators.password_validator().validate(p.password)
        ).add_validation(
            "website",
            lambda p: CommonValidators.url_validator().validate(p.website)
        ).add_validation(
            "date_of_birth",
            lambda p: CommonValidators.date_validator(
                min_date=datetime.now().replace(year=datetime.now().year - 120),
                max_date=datetime.now().replace(year=datetime.now().year - 18),
                field_name="DateOfBirth"
            ).validate(p.date_of_birth)
        ).add_validation(
            "salary",
            lambda p: CommonValidators.currency_validator(
                min_value=Decimal('0'),
                max_value=Decimal('1000000'),
                field_name="Salary"
            ).validate(p.salary)
        )
    
    def validate_profile(self, profile: UserProfile) -> ValidationResult:
        """Validate a user profile."""
        return self.validator.validate(profile)
