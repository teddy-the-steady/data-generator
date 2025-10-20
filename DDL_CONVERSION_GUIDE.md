# DDL to CSV Conversion Guide

This guide explains how to convert PostgreSQL DDL (CREATE TABLE) files to CSV schema format and generate synthetic data.

## Overview

The pg-data-generator can automatically convert SQL DDL files into CSV schema format, making it easy to generate test data from existing database schemas.

## Quick Start

### 1. Prepare Your DDL Files

Place all your `.sql` files containing CREATE TABLE statements in a folder:

```
sql_schemas/
├── customer.sql
├── example.sql
└── orders.sql
```

**Example DDL (`customer.sql`):**
```sql
CREATE TABLE MST_CUSTOMER (
    id INT PRIMARY KEY,
    internal_no INT,
    customer_name VARCHAR(50),
    age INT,
    gender CHAR(1),
    email VARCHAR(50),
    phone_number VARCHAR(50),
    created_at DATETIME,
    FOREIGN KEY (internal_no) REFERENCES MST_EXAMPLE(id)
);
```

### 2. Convert and Generate Data

**Python API:**
```python
from pg_data_generator.main import generate_data_from_ddl_folder

# Convert DDL files and generate data in one step
tables, schema_path = generate_data_from_ddl_folder(
    ddl_folder_path='./sql_schemas',
    output_data_dir='./generated_data',
    row_count=100
)

print(f"Generated {len(tables)} tables")
print(f"Schema saved to: {schema_path}")
```

**Output:**
```
Found 2 SQL file(s):
  - customer.sql
  - example.sql

Parsed 2 table(s)
Successfully created: ./generated_data/schema.csv

Generating 100 rows per table...

Successfully generated 2 table(s):
  - MST_CUSTOMER.csv
  - MST_EXAMPLE.csv

Data generation complete!
```

### 3. Result Files

```
generated_data/
├── schema.csv          # Generated CSV schema
├── MST_CUSTOMER.csv    # 100 rows of customer data
└── MST_EXAMPLE.csv     # 100 rows of example data
```

## Advanced Usage

### Convert DDL to CSV Only

If you only want to convert DDL files without generating data:

```python
from pg_data_generator.main import ddl_folder_to_csv

ddl_folder_to_csv(
    folder_path='./sql_schemas',
    output_csv_path='schema.csv'
)
```

### Convert Single DDL File

```python
from pg_data_generator.main import ddl_to_csv

ddl_to_csv(
    ddl_file_path='customer.sql',
    output_csv_path='customer_schema.csv'
)
```

### Convert DDL String

```python
from pg_data_generator.main import ddl_string_to_csv

ddl = """
CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);
"""

ddl_string_to_csv(ddl, 'users_schema.csv')
```

## Supported DDL Features

### Comments
Both single-line and multi-line comments are automatically removed during parsing:

```sql
-- Single-line comment
CREATE TABLE users (
    id INT PRIMARY KEY,  -- Inline comment
    name VARCHAR(50)
);

/*
 * Multi-line comment
 * Completely ignored
 */
```

**Note:** Comments are fully supported and will not interfere with parsing.

### Column Types
- **Integers**: `INT`, `BIGINT`, `SMALLINT`
- **Strings**: `VARCHAR(n)`, `CHAR(n)`
- **Dates**: `DATE`, `DATETIME`, `TIMESTAMP`
- **Decimals**: `DECIMAL(p,s)` (e.g., `DECIMAL(15,2)`)

### Constraints

#### Primary Keys
```sql
-- Inline PRIMARY KEY
CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(50)
);

-- Table-level PRIMARY KEY
CREATE TABLE users (
    id INT,
    name VARCHAR(50),
    PRIMARY KEY (id)
);

-- Named constraint
CREATE TABLE users (
    id INT,
    CONSTRAINT pk_users PRIMARY KEY (id)
);
```

#### Foreign Keys

**IMPORTANT:** The most common pattern is inline `REFERENCES` (no `FOREIGN KEY` keyword needed):

```sql
-- ✅ Inline REFERENCES (RECOMMENDED - Most Common)
CREATE TABLE orders (
    id INT PRIMARY KEY,
    customer_id INT REFERENCES customers(id)  -- Simple and clean
);

-- Also supported: Table-level FOREIGN KEY
CREATE TABLE orders (
    id INT PRIMARY KEY,
    customer_id INT,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- Also supported: Named constraint
CREATE TABLE orders (
    id INT PRIMARY KEY,
    customer_id INT,
    CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES customers(id)
);
```

**All three formats are supported**, but inline `REFERENCES` is the most concise and commonly used in practice.

### Name Quoting
Supports various SQL identifier quoting styles:
```sql
CREATE TABLE "quoted_table" ("col1" INT);  -- Double quotes
CREATE TABLE `quoted_table` (`col1` INT);  -- Backticks
CREATE TABLE [quoted_table] ([col1] INT);  -- Square brackets
```

## CSV Schema Format

The generated CSV schema follows this format:

```csv
table_name,column,type,constraint,length,format
MST_CUSTOMER,id,INT,pk,,
MST_CUSTOMER,internal_no,INT,fk.MST_EXAMPLE.id,,
MST_CUSTOMER,customer_name,VARCHAR(50),,50,
MST_CUSTOMER,gender,CHAR(1),,1,
MST_CUSTOMER,email,VARCHAR(50),,50,
MST_CUSTOMER,created_at,DATETIME,,,
MST_EXAMPLE,id,INT,pk,,
MST_EXAMPLE,content,VARCHAR(30),,30,
```

**Column Definitions:**
- `table_name`: Table name from CREATE TABLE
- `column`: Column name
- `type`: Data type (with length if applicable)
- `constraint`: `pk` for primary key, `fk.TABLE.column` for foreign keys, empty otherwise
- `length`: Extracted length for VARCHAR/CHAR types
- `format`: Optional format for data generation (can be manually added)

## Customizing Generated Data

After conversion, you can manually edit the CSV to customize data generation:

### Add Options for Enum-like Columns

```csv
table_name,column,type,constraint,length,format
MST_CUSTOMER,gender,CHAR(1),,1,"[m,f,]"
MST_CUSTOMER,status,VARCHAR(20),,20,"[active,inactive,pending]"
```

The `format` column with `[option1,option2,...]` tells the generator to randomly choose from these values.

## Complete Workflow Example

```python
from pg_data_generator.main import generate_data_from_ddl_folder

# Step 1: Convert DDL files and generate initial data
tables, schema_path = generate_data_from_ddl_folder(
    ddl_folder_path='./database/schemas',
    output_data_dir='./test_data',
    row_count=1000
)

# Step 2: Optionally edit schema.csv to add custom formats

# Step 3: Re-generate with the customized schema
from pg_data_generator.main import generate_data

tables = generate_data(
    schema_csv_path='./test_data/schema.csv',
    row_count=5000,
    output_dir='./test_data_large'
)
```

## Limitations

- **FK Enforcement**: Foreign key relationships are captured in the CSV but not yet enforced during data generation. FK columns receive independent random data.
- **Unique Constraints**: UNIQUE constraints are parsed but not enforced.
- **Check Constraints**: CHECK constraints are not supported.
- **Default Values**: DEFAULT values are not captured.
- **Complex Types**: Arrays, JSON, and custom types are not supported.

## Troubleshooting

### No .sql files found
**Error:** `No .sql files found in <folder>`

**Solution:** Ensure your folder contains `.sql` files with CREATE TABLE statements.

### Table not found in FK reference
**Error:** `Please provide fk table in your csv file`

**Solution:** Ensure referenced tables are defined in the same DDL files or already in the CSV.

### Unsupported column type
**Error:** `Unsupported columns found: [column_name]`

**Solution:** The column type or name pattern doesn't match any Case generator. Add a custom Case generator or manually edit the CSV to use a supported type.
