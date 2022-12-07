'''
Program for sorting CSV files through a discord bot (by first column, numerical) - Final Project (2) for UNO CSCI-1620

Requires a valid `token.key` file in project directory containing a valid discord bot token.

Uses discord.py library.

Author: Ethan Harvey
'''

import os
import discord
from csv_helper import read_csv, sort_csv, write_csv

def main():
    '''
    Main script for initalizing and running bot.
    '''

    # Create the client
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)


    # Print to the console when the CSV bot connects successfuly
    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')

    # Handle a new discord message
    @client.event
    async def on_message(message: discord.Message):
        if message.author == client.user:
            return

        # If the message starts with $csv_sort and has an attachment, attempt to sort.
        if message.content.startswith('$csv_sort') and not len(message.attachments) == 0:
            # Save file (temporary - will be deleted when process completes)
            filepath = f"./files/{message.id}.csv"
            await message.attachments[0].save(fp=filepath)

            # Read file
            try:
                rows_in = read_csv(filepath)
            except:
                await message.channel.send('Unable to parse file.')
                cleanup(message.id) # Delete temp file
                return

            # Sort data
            try:
                sorted_rows = sort_csv(rows_in)
            except ValueError:
                await message.channel.send('Unable to sort data, first column is not numeric.')
                cleanup(message.id) # Delete temp file
                return

            # Write file
            write_csv(filepath, sorted_rows)

            # Respond with sorted file
            await message.channel.send(file=discord.File(filepath))

            # Delete the temporary file
            cleanup(message.id)
            return

    with open('token.key', 'r', encoding='utf-8') as tokenfile:
        tkn = tokenfile.readline()
    client.run(tkn)

def cleanup(message_id: int) -> None:
    '''
    Removes associated files after sorting is complete (or fails).

    :param id: Associated message id to cleanup
    '''
    filepath = f"./files/{message_id}.csv"
    # cleanup
    if os.path.isfile(filepath):
        os.remove(filepath)

# Project best run as script.
if __name__ == "__main__":
    main()
