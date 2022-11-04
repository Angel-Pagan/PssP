#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Import Packages """
import sqlalchemy
from sqlalchemy import create_engine
import dotenv
from dotenv import load_dotenv
import os
import pandas as pd


### drop the old tables that do not start with production_
def droppingFunction_limited(dbList, db_source):
    for table in dbList:
        if table.startswith('production_') == False:
            db_source.execute(f'drop table {table}')
            print(f'dropped table {table}')
        else:
            print(f'kept table {table}')

def droppingFunction_all(dbList, db_source):
    for table in dbList:
        db_source.execute(f'drop table {table}')
        print(f'dropped table {table} succesfully!')
    else:
        print(f'kept table {table}')


load_dotenv()

MYSQL_HOSTNAME = os.getenv("HOSTNAME")
MYSQL_USER = os.getenv("USERNAME")
MYSQL_PASSWORD = os.getenv("PASSWORD")
MYSQL_DATABASE = os.getenv("DATABASE") 



########


connection_string_gcp = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOSTNAME}/{MYSQL_DATABASE}'
db_gcp = create_engine(connection_string_gcp)


#### note to self, need to ensure server_paremters => require_secure_transport is OFF in Azure 

### show tables from databases

#tableNames_gcp = db_gcp.table_names()


# reoder tables: production_patient_conditions, production_patient_medications, production_medications, production_patients, production_conditions
tableNames_gcp = ['production_patient_conditions', 'production_patient_medications', 'production_medications', 'production_patients', 'production_conditions']

# ### delete everything 
droppingFunction_all(tableNames_gcp, db_gcp)


#### first step below is just creating a basic version of each of the tables,
#### along with the primary keys and default values 


### 
table_prod_patients = """
create table if not exists production_patients (
    id int auto_increment,
    mrn varchar(255) default null unique,
    first_name varchar(255) default null,
    last_name varchar(255) default null,
    zip_code varchar(255) default null,
    dob varchar(255) default null,
    gender varchar(255) default null,
    contact_mobile varchar(255) default null,
    contact_home varchar(255) default null,
    PRIMARY KEY (id) 
); 
"""


table_prod_medications = """
create table if not exists production_medications (
    id int auto_increment,
    med_ndc varchar(255) default null unique,
    med_human_name varchar(255) default null,
    med_is_dangerous varchar(255) default null,
    PRIMARY KEY (id)
); 
"""

table_prod_conditions = """
create table if not exists production_conditions (
    id int auto_increment,
    icd10_code varchar(255) default null unique,
    icd10_description varchar(255) default null,
    PRIMARY KEY (id) 
); 
"""
table_prod_patients_medications = """
create table if not exists production_patient_medications (
    id int auto_increment,
    mrn varchar(255) default null,
    med_ndc varchar(255) default null,
    PRIMARY KEY (id),
    FOREIGN KEY (mrn) REFERENCES production_patients(mrn) ON DELETE CASCADE,
    FOREIGN KEY (med_ndc) REFERENCES production_medications(med_ndc) ON DELETE CASCADE
); 
"""
table_prod_patient_conditions = """
create table if not exists production_patient_conditions (
    id int auto_increment,
    mrn varchar(255) default null,
    icd10_code varchar(255) default null,
    PRIMARY KEY (id),
    FOREIGN KEY (mrn) REFERENCES production_patients(mrn) ON DELETE CASCADE,
    FOREIGN KEY (icd10_code) REFERENCES production_conditions(icd10_code) ON DELETE CASCADE
); 
"""

db_gcp.execute(table_prod_patients)
db_gcp.execute(table_prod_medications)
db_gcp.execute(table_prod_conditions)
db_gcp.execute(table_prod_patients_medications)
db_gcp.execute(table_prod_patient_conditions)



# get tables from db_gcp
gcp_tables = db_gcp.table_names()


#droppingFunction_limited(gcp_tables, db_gcp)


### confirm that it worked 

# get tables from db_gcp
gcp_tables = db_gcp.table_names()
