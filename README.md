# SQL sever data generator

### developed Python version 3.8.10

#### First setting

---

1. Setup virtual env (only once)

```
$ cd [project dir]
$ python3 -m venv [new_env_name]
```

2. Activate venv (windows)

```
$ .\[new_env_name]\Scripts\activate
```

3. Install packages

```
$ pip install -r requirements.txt
```

4. Prepare Schema file (example.csv)

```
table_name,column,type,constraint,length,format
users,id,BIGINT,pk,,
users,user_name,CHAR,,20,
users,created_at,DATE,,,
users,updated_at,DATE,,,
users,department_id,BIGINT,fk.departments.id,,
departments,id,BIGINT,pk,,
...

```

5. Run python script

```
$ python main.py
```

6. Check results folder
