from bot import bot
from yaml import load

with open('env.yml', 'r') as f:
    env = load(f)

bot.run(env)
