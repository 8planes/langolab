from celery.task import task

@task
def update_schedules(user_id, utc_date, num_hours):
    pass
