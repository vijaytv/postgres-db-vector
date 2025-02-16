```
- Get Started
- Concepts
- API Documentation
- Internals
- Examples
- Error Messages
- Integrations
- Blog
- Pydantic People
```

```
- Get Started Get Started
    - Welcome to Pydantic
    - Why use Pydantic
    - Help with Pydantic
    - Installation
    - Migration Guide
    - Version Policy
    - Contributing
    - Changelog
```

- Concepts Concepts
    - Models
    - Fields
    - JSON Schema
    - JSON
    - Types
    - Unions
    - Alias
    - Configuration
    - Serialization
    - Validators
    - Dataclasses
    - Forward Annotations
    - Strict Mode
    - Type Adapter
    - Validation Decorator
    - Conversion Table
    - Settings Management
    - Performance
    - Experimental
- API Documentation API Documentation
- Pydantic Pydantic
    - BaseModel
    - RootModel
    - Pydantic Dataclasses
    - TypeAdapter
    - Validate Call
    - Fields
    - Aliases
    - Configuration
    - JSON Schema
    - Errors
    - Functional Validators
    - Functional Serializers
    - Standard Library Types
    - Pydantic Types
    - Network Types
    - Version Information
    - Annotated Handlers
    - Experimental
- Pydantic Core Pydantic Core
- pydantic
- pydantic
- Pydantic Settings
- Pydantic Extra Types Pydantic Extra Types
- Color
- Country
- Payment
- Phone Numbers
- Routing Numbers
- Coordinate
- Mac Address
- ISBN
- Pendulum
- Currency
- Language
- Script Code
- Semantic Version
- Timezone Name
- ULID
- Internals Internals
- Architecture
- Resolving Annotations
- Examples Examples
- Validating File Data Validating File Data Page contents
    - JSON data
    - JSON lines files
    - CSV files
    - TOML files
- Web and API Requests
- Queues
- Databases
- Custom Validators
- Error Messages Error Messages
- Error Handling
- Validation Errors
- Usage Errors
- Integrations Integrations
- Pydantic Logfire
- Dev Tools Dev Tools
    - Mypy
    - PyCharm
    - Hypothesis
    - Visual Studio Code
    - datamodel-code-generator
    - devtools
    - Rich
    - Linting
    - Documentation
- Production Tools Production Tools
- AWS Lambda
- Blog
- Pydantic People
- JSON data
- JSON lines files
- CSV files
- TOML files

# Validating File Data

pydantic is a great tool for validating data coming from various sources. In this section, we will look at how to validate data from different types of files.

!!! Note: If you're using any of the below file formats to parse configuration / settings, you might want to consider using the pydantic-settings library, which offers builtin support for parsing this type of data.

## JSON data¶

.json files are a common way to store key / value data in a human-readable format. Here is an example of a .json file:

```
{
    "name": "John Doe",
    "age": 30,
    "email": "[email protected]"
}
```

To validate this data, we can use a pydantic model:

```
import pathlib

from pydantic import BaseModel, EmailStr, PositiveInt

class Person(BaseModel):
    name: str
    age: PositiveInt
    email: EmailStr

json_string = pathlib.Path('person.json').read_text()
person = Person.model_validate_json(json_string)
print(repr(person))
#> Person(name='John Doe', age=30, email='[email protected]')
```

If the data in the file is not valid, pydantic will raise a ValidationError. Let's say we have the following .json file:

```
{
    "age": -30,
    "email": "not-an-email-address"
}
```

This data is flawed for three reasons:

1. It's missing the name field.
2. The age field is negative.
3. The email field is not a valid email address.

When we try to validate this data, pydantic raises a ValidationError with all of the above issues:

```
import pathlib

from pydantic import BaseModel, EmailStr, PositiveInt, ValidationError

class Person(BaseModel):
    name: str
    age: PositiveInt
    email: EmailStr

json_string = pathlib.Path('person.json').read_text()
try:
    person = Person.model_validate_json(json_string)
except ValidationError as err:
    print(err)
    """
    3 validation errors for Person
    name
    Field required [type=missing, input_value={'age': -30, 'email': 'not-an-email-address'}, input_type=dict]
        For further information visit https://errors.pydantic.dev/2.10/v/missing
    age
    Input should be greater than 0 [type=greater_than, input_value=-30, input_type=int]
        For further information visit https://errors.pydantic.dev/2.10/v/greater_than
    email
    value is not a valid email address: An email address must have an @-sign. [type=value_error, input_value='not-an-email-address', input_type=str]
    """
```

Often, it's the case that you have an abundance of a certain type of data within a .json file. For example, you might have a list of people:

```
[
    {
        "name": "John Doe",
        "age": 30,
        "email": "[email protected]"
    },
    {
        "name": "Jane Doe",
        "age": 25,
        "email": "[email protected]"
    }
]
```

In this case, you can validate the data against a list[Person] model:

```
import pathlib

from pydantic import BaseModel, EmailStr, PositiveInt, TypeAdapter

class Person(BaseModel):
    name: str
    age: PositiveInt
    email: EmailStr

person_list_adapter = TypeAdapter(list[Person])  # (1)!

json_string = pathlib.Path('people.json').read_text()
people = person_list_adapter.validate_json(json_string)
print(people)
#> [Person(name='John Doe', age=30, email='[email protected]'), Person(name='Jane Doe', age=25, email='[email protected]')]
```

1. We use TypeAdapter to validate a list of Person objects.

## JSON lines files¶

Similar to validating a list of objects from a .json file, you can validate a list of objects from a .jsonl file. .jsonl files are a sequence of JSON objects separated by newlines.

Consider the following .jsonl file:

```
{"name": "John Doe", "age": 30, "email": "[email protected]"}
{"name": "Jane Doe", "age": 25, "email": "[email protected]"}
```

We can validate this data with a similar approach to the one we used for .json files:

```
import pathlib

from pydantic import BaseModel, EmailStr, PositiveInt

class Person(BaseModel):
    name: str
    age: PositiveInt
    email: EmailStr

json_lines = pathlib.Path('people.jsonl').read_text().splitlines()
people = [Person.model_validate_json(line) for line in json_lines]
print(people)
#> [Person(name='John Doe', age=30, email='[email protected]'), Person(name='Jane Doe', age=25, email='[email protected]')]
```

## CSV files¶

CSV is one of the most common file formats for storing tabular data. To validate data from a CSV file, you can use the csv module from the Python standard library to load the data and validate it against a Pydantic model.

Consider the following CSV file:

```
name,age,email
John Doe,30,[email protected]
Jane Doe,25,[email protected]
```

Here's how we validate that data:

```
import csv

from pydantic import BaseModel, EmailStr, PositiveInt

class Person(BaseModel):
    name: str
    age: PositiveInt
    email: EmailStr

with open('people.csv') as f:
    reader = csv.DictReader(f)
    people = [Person.model_validate(row) for row in reader]

print(people)
#> [Person(name='John Doe', age=30, email='[email protected]'), Person(name='Jane Doe', age=25, email='[email protected]')]
```

## TOML files¶

TOML files are often used for configuration due to their simplicity and readability.

Consider the following TOML file:

```
name = "John Doe"
age = 30
email = "[email protected]"
```

Here's how we validate that data:

```
import tomllib

from pydantic import BaseModel, EmailStr, PositiveInt

class Person(BaseModel):
    name: str
    age: PositiveInt
    email: EmailStr

with open('person.toml', 'rb') as f:
    data = tomllib.load(f)

person = Person.model_validate(data)
print(repr(person))
#> Person(name='John Doe', age=30, email='[email protected]')
```