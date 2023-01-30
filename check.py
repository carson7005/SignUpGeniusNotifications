import schedule
import time

def job(t):
    print("Job done!")
    return


schedule.every().day.at("01:36").do(job, "Job to be done...")

while True:
    schedule.run_pending()
    time.sleep(60)

