from yoyo import read_migrations
from yoyo import get_backend as yoyo_get_backend
import os
import argparse

SCRIPT_PATH = os.path.dirname(__file__)
MIGRATIONS_PATH = os.path.join(SCRIPT_PATH, "migrations")

USER = os.environ["POSTGRES_USER"]
PASSWORD = os.environ["POSTGRES_PASSWORD"]
DB = os.environ["POSTGRES_DB"]
HOST = os.environ["POSTGRES_HOST"]

def get_backend():
    print(f"acessing backend postgres://{USER}:XXX@{HOST}/{DB}")
    backend = yoyo_get_backend(f'postgres://{USER}:{PASSWORD}@{HOST}/{DB}')
    return backend


def apply_migrations(backend):
    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))

def re_apply_migrations(backend):
    with backend.lock():
        backend.rollback_migrations(backend.to_rollback(migrations))
        backend.apply_migrations(backend.to_apply(migrations))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--rollback", help="rollback before applying migration", action=argparse.BooleanOptionalAction)
    args = parser.parse_args()

    backend = get_backend()
    migrations = read_migrations(MIGRATIONS_PATH)
    print(migrations)

    if args.rollback:
        print("rolling back")
        re_apply_migrations(backend)
    else:
        apply_migrations(backend)
