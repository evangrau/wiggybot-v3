import random
from classes.dbconnection import DBConnection
from loguru import logger as log
from settings import MODE

async def get_cracked(ctx):
    try:
    # getting access to the database
        db = DBConnection()
        records = db.get_all_records(f"cracked_table_{MODE}")

        members = []

        if not records.empty:
            for _, r in records.iterrows():
                members.append([r['id'], r['fields.discord_id'], r['fields.username'], r['fields.cracked'], r['fields.bad']])
        else:
            raise ValueError(f"No records found in the 'cracked_table_{MODE}' Airtable table.")

        m = random.choice(members)

        rand = random.randint(0, 99)

        if (rand < 5):
            # bad
            await ctx.send(f"<@{m[1]}>, you're bad.")
            db.update_record(f'cracked_table_{MODE}', m[0], {"bad": m[4] + 1})
            log.info(f"Cracked command ran and {m[2]} was bad: {{'bad': {m[4] + 1}}}")
        else:
            # cracked
            await ctx.send(f"<@{m[1]}>, you're cracked.")
            db.update_record(f'cracked_table_{MODE}', m[0], {"cracked": m[3] + 1})
            log.info(f"Cracked command ran and {m[2]} was cracked: {{'cracked': {m[3] + 1}}}")
    except Exception as e:
        await ctx.send("An error occurred while running the cracked command. Please check the logs for more details.")
        log.error(f"An error occurred while running cracked command: {e}")