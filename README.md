# PG Data Generator

Generate realistic synthetic data for PostgreSQL databases from CSV schemas or DDL files.

**Python 3.8.10+**

## Features

- Generate synthetic data from CSV schema or DDL files
- Enforces foreign key relationships and referential integrity
- Realistic data: names, emails, addresses, phone numbers, dates
- Output as CSV files or SQL INSERT statements
- DDL to INSERT conversion in one step

## Basic Usage

### Generate from CSV Schema

```python
from pg_data_generator.main import generate_data

tables = generate_data(
    schema_csv_path='example.csv',
    row_count=100,
    output_dir='./output'
)
```

### Convert DDL to INSERT Statements

```python
from pg_data_generator.main import generate_dml_from_ddl_folder

result = generate_dml_from_ddl_folder(
    ddl_folder_path='./sql_schemas',
    output_dml_dir='./inserts',
    row_count=100,
    batch_size=50
)
```

### Generate Data with SQL INSERTs

```python
from pg_data_generator.main import generate_data_with_dml

result = generate_data_with_dml(
    schema_csv_path='schema.csv',
    row_count=100,
    output_dir='./data',
    dml_output_dir='./sql',
    batch_size=100
)
```

## CSV Schema Format

```csv
table_name,column,type,constraint,length,format
MST_CUSTOMER,id,int,,,
MST_CUSTOMER,customer_name,varchar(50),,50,
MST_CUSTOMER,gender,char(1),,1,"[m,f,]"
MST_CUSTOMER,internal_no,int,fk.MST_EXAMPLE.id,,
MST_EXAMPLE,id,int,,,
```

**Fields:**
- `constraint`: `pk` (primary key), `fk.TABLE.column` (foreign key), or empty
- `format`: `[option1,option2,...]` for enum-like columns
- `type`: int, varchar, datetime, decimal, etc.

## Supported Data Types

| Type | Detection | Example |
|------|-----------|---------|
| Primary Key | `constraint = "pk"` | 1, 2, 3, ... |
| Foreign Key | `constraint = "fk.TABLE.column"` | Values from referenced table |
| Name | Column name contains "name" | "John Smith" |
| Email | Column name contains "email" | "user@example.com" |
| Address | Column name contains "address" | "123 Main St, NY" |
| Phone | Column name contains "phone" | "(555) 123-4567" |
| DateTime | Type is "date" or "datetime" | "2024-03-15 14:30:00" |
| Integer | Type is "int" | Random integers |
| Decimal | Type is "decimal" | Random decimals |

## Examples

See [test/](test/) directory for working examples:
- [test_main.py](test/test_main.py) - Basic data generation
- [test_ddl_to_dml.py](test/test_ddl_to_dml.py) - DDL to INSERT statements
- [test_dml_generation.py](test/test_dml_generation.py) - Generate SQL INSERTs

## Documentation

- [CLAUDE.md](CLAUDE.md) - Detailed architecture and implementation guide
- [DDL_CONVERSION_GUIDE.md](DDL_CONVERSION_GUIDE.md) - DDL conversion examples

## Use Cases

- Generate test data for QA/dev environments
- Create sample datasets for development
- Generate INSERT scripts for database migrations
- Performance testing with large datasets
