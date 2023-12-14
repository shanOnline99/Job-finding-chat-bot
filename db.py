import mysql.connector
global cnx

cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="job"
)

def get_company(job_item):
    cursor = cnx.cursor()
    query = ("SELECT Company FROM jobs WHERE JobName = %s")
    cursor.execute(query, (job_item,))
    result = cursor.fetchone()
    cursor.close()
    #cnx.close()

    if result is not None:
        return result[0]
    else:
        return None
    
def get_Qualifications(job_item):
    cursor = cnx.cursor()
    query = ("SELECT Qualifications FROM jobs WHERE JobName = %s")
    cursor.execute(query, (job_item,))
    result = cursor.fetchone()
    cursor.close()
    
    if result is not None:
        return result[0]
    else:
        return None

def get_details(job_item):
    cursor = cnx.cursor()
    query = ("SELECT WorkExp FROM job.jobs WHERE JobName = %s")
    cursor.execute(query, (job_item,))
    result = cursor.fetchone()
    cursor.close()
    
    if result is not None:
        return result[0]
    else:
        return None


def get_contact(job_item):
    cursor = cnx.cursor()
    query = ("SELECT tp FROM job.jobs WHERE JobName = %s")
    cursor.execute(query, (job_item,))
    result = cursor.fetchone()
    cursor.close()
    
    if result is not None:
        return result[0]
    else:
        return None
    
def get_email(job_item):
    cursor = cnx.cursor()
    query = ("SELECT email FROM job.jobs WHERE JobName = %s")
    cursor.execute(query, (job_item,))
    result = cursor.fetchone()
    cursor.close()
    
    if result is not None:
        return result[0]
    else:
        return None

def add_job_details(job_item, qualification, company, work_exp, contact, email):
    cursor = cnx.cursor()
    query = (
        "INSERT INTO job.jobs (JobName, Qualifications, Company, WorkExp, tp, email) "
        "VALUES (%s, %s, %s, %s, %s, %s)"
    )
    data = (job_item, qualification, company, work_exp, contact, email)

    try:
        cursor.execute(query, data)
        cnx.commit()
    except Exception as e:
        print(f"Error adding job details to the database: {e}")
        cnx.rollback()
    finally:
        cursor.close()