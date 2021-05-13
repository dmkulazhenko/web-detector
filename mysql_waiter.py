import os
import time

# noinspection PyUnresolvedReferences,PyPackageRequirements
from mysql.connector import connection


def wait_for_mysql(
    user, password, host, port, database, max_retries, sleep_time
):
    retry = 0
    while retry < max_retries:
        retry += 1
        try:
            connection.MySQLConnection(
                user=user,
                password=password,
                host=host,
                port=port,
                database=database,
            )
        except Exception as exc:
            print(
                "Cannot connect to database {} time".format(retry), flush=True
            )
            if retry >= max_retries:
                raise exc
            time.sleep(sleep_time)
        else:
            break


if __name__ == "__main__":
    host_ = os.getenv("MYSQL_HOST")
    max_retries_, sleep_time_ = os.getenv("MYSQL_WAITER").split(":")
    wait_for_mysql(
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=host_,
        port=3306,
        database=os.getenv("MYSQL_DATABASE"),
        max_retries=int(max_retries_),
        sleep_time=int(sleep_time_),
    )
