# PG data generator

### developed Python version 3.8.10

#### Steps to run

---

1. Prepare Schema file (example.csv)

```
table_name,column,type,constraint,length,format
MST_CUSTOMER,id,int,,,
MST_CUSTOMER,internal_no,int,fk.MST_EXAMPLE.id,,
MST_CUSTOMER,customer_name,varchar(50),,50,
MST_CUSTOMER,age,int,,,
MST_CUSTOMER,gender,char(1),,1,"[m,f,]"
MST_CUSTOMER,address_code,varchar(4),,4,
MST_CUSTOMER,email,varchar(50),,,
MST_CUSTOMER,phone_number,varchar(50),,,
MST_CUSTOMER,created_at,datetime,,,
MST_EXAMPLE,id,int,,,
MST_EXAMPLE,content,varchar(30),,,
MST_EXAMPLE,trade_start,date,,,
MST_EXAMPLE,trade_end,date,,,
MST_EXAMPLE,price,"DECIMAL(15,2)",,,
MST_EXAMPLE,release_year,int,,,
...

```

2. Run python script

```
$ cd ./src
$ python main.py
```

3. Check results folder
