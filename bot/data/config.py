from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")

IP = env.str("IP")

DB_PASS = env.str("DB_PASS")
DB_USER = env.str("DB_USER")
DB_NAME = env.str("DB_NAME")
