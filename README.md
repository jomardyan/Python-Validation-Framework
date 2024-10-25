# Python Validation Framework

A lightweight, flexible, and type-safe validation framework for Python applications. This framework provides an elegant way to validate data with customizable rules and detailed error reporting.

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Table of Contents
- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Examples](#-usage-examples)
- [Built-in Validators](#-built-in-validators)
- [Creating Custom Validators](#-creating-custom-validators)
- [Validation Results](#-validation-results)
- [Advanced Usage](#-advanced-usage)
- [Best Practices](#-best-practices)
- [Contributing](#-contributing)

## ✨ Features

- 🔒 Type-safe validation with Python type hints
- 🎯 Fluent API for building validation rules
- 📝 Detailed error reporting
- 🔧 Easily extensible
- 🏗️ Built-in validators for common scenarios
- 🔄 Chainable validation rules
- 📊 Field-specific error tracking
- 🎨 Clean and maintainable code structure

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/python-validation-framework.git
```

2. Install the package:
```bash
pip install -e .
```

## 🎯 Quick Start

```python
from validation_framework import CommonValidators

# Create an email validator
email_validator = CommonValidators.email_validator()

# Validate an email
result = email_validator.validate("john.doe@example.com")

if result.is_valid:
    print("Email is valid!")
else:
    for error in result.errors:
        print(f"Error: {error}")
```

## 📚 Usage Examples

### Basic Field Validation

```python
# Email validation
email_validator = CommonValidators.email_validator()
email_result = email_validator.validate("john.doe@example.com")

# Name validation
name_validator = CommonValidators.name_validator(min_length=2, max_length=50)
name_result = name_validator.validate("John")

# Phone validation
phone_validator = CommonValidators.phone_validator(required_length=10)
phone_result = phone_validator.validate("1234567890")
```

### Complex Object Validation

```python
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

@dataclass
class UserProfile:
    email: str
    first_name: str
    last_name: str
    phone_number: str
    password: str
    website: str
    date_of_birth: datetime
    salary: Decimal

# Create a profile
profile = UserProfile(
    email="john.doe@example.com",
    first_name="John",
    last_name="Doe",
    phone_number="1234567890",
    password="Secure@123",
    website="https://example.com",
    date_of_birth=datetime(1990, 1, 1),
    salary=Decimal('50000.00')
)

# Validate the profile
validator = UserProfileValidator()
result = validator.validate_profile(profile)
```

## 🛠️ Built-in Validators

### EmailValidator
```python
email_validator = CommonValidators.email_validator()
# Validates:
# - Required field
# - Email format
```

### NameValidator
```python
name_validator = CommonValidators.name_validator(
    min_length=2,
    max_length=50,
    field_name="FirstName"
)
# Validates:
# - Required field
# - Length constraints
# - Valid characters (letters, spaces, hyphens, apostrophes)
```

### PhoneValidator
```python
phone_validator = CommonValidators.phone_validator(
    required_length=10,
    field_name="Phone"
)
# Validates:
# - Required field
# - Numeric characters only
# - Exact length
```

### PasswordValidator
```python
password_validator = CommonValidators.password_validator()
# Validates:
# - Minimum length (8 characters)
# - Contains uppercase letter
# - Contains lowercase letter
# - Contains number
# - Contains special character
```

### UrlValidator
```python
url_validator = CommonValidators.url_validator()
# Validates:
# - Required field
# - Valid URL format
```

### DateValidator
```python
date_validator = CommonValidators.date_validator(
    min_date=datetime.now().replace(year=datetime.now().year - 120),
    max_date=datetime.now().replace(year=datetime.now().year - 18)
)
# Validates:
# - Date range
```

### CurrencyValidator
```python
currency_validator = CommonValidators.currency_validator(
    min_value=Decimal('0'),
    max_value=Decimal('1000000')
)
# Validates:
# - Non-negative amounts
# - Maximum 2 decimal places
# - Value range
```

## 🔧 Creating Custom Validators

Create custom validators by extending the base `Validator` class:

```python
def custom_validator(field_name: str = "CustomField") -> Validator:
    return Validator(field_name).add_rule(
        lambda value: bool(value),
        "Value is required"
    ).add_rule(
        lambda value: # your custom rule,
        "Your error message"
    )
```

## 📊 Validation Results

The `ValidationResult` class provides detailed information about validation results:

```python
@dataclass
class ValidationResult:
    is_valid: bool = True
    errors: List[str] = field(default_factory=list)
    field_errors: Dict[str, List[str]] = field(default_factory=dict)
```

### Handling Validation Results

```python
result = validator.validate_profile(profile)

if not result.is_valid:
    # Access general errors
    for error in result.errors:
        print(f"Error: {error}")

    # Access field-specific errors
    for field_name, errors in result.field_errors.items():
        print(f"Field: {field_name}")
        for error in errors:
            print(f"  - {error}")
```

## 🚀 Advanced Usage

### Using ValidationBuilder

```python
builder = ValidationBuilder()
builder.add_validation(
    "email",
    lambda p: CommonValidators.email_validator().validate(p.email)
).add_validation(
    "first_name",
    lambda p: CommonValidators.name_validator().validate(p.first_name)
)

result = builder.validate(user_profile)
```

### Merging Validation Results

```python
result1 = email_validator.validate(email)
result2 = name_validator.validate(name)
combined_result = result1.merge(result2)
```

## 💡 Best Practices

1. **Type Hints**: Always use type hints for better code clarity
```python
def validate(self, value: str) -> ValidationResult:
```

2. **Field Names**: Provide meaningful field names for better error messages
```python
validator = CommonValidators.email_validator(field_name="Work Email")
```

3. **Custom Rules**: Keep validation rules simple and focused
```python
lambda value: len(value) > 0, "Value is required"
```

4. **Error Messages**: Write clear, actionable error messages
```python
"Password must contain at least one uppercase letter"
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch:
```bash
git checkout -b feature/amazing-feature
```
3. Commit your changes:
```bash
git commit -m 'Add amazing feature'
```
4. Push to the branch:
```bash
git push origin feature/amazing-feature
```
5. Open a Pull Request

### Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by various validation frameworks in the Python ecosystem
- Built with modern Python features and best practices

## 📞 Support

- Create an issue for bug reports
- Start a discussion for feature requests
- Check out the documentation for detailed information

Remember to ⭐ the repository if you find it helpful!
