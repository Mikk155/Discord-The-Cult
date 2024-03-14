import json

with open('botconfig.json') as bot_config:
    json_config = json.load( bot_config )

jsBot = json_config.get( "BOT", {} )

TOKEN = jsBot.get( "TOKEN", "" )
jsBenefactors = jsBot.get( "BENEFACTORS", {} )
BENEFACTORS_CHANNEL = int( jsBenefactors.get( "CHANNEL", 0 ) )
BENEFACTORS_MAXMEDIA = int( jsBenefactors.get( "MAXMEDIA", 2 ) )
UPLOAD_MB = int( jsBot.get( "MEGABYTES", 2 ) )

if not TOKEN:
    print("Error: No BOT Token set, please config botconfig.json.")
    exit(1)