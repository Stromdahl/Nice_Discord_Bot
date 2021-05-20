from mongo_data.Models.guilds import Guild


def main():
    guild = Guild("844253863451951203")
    # guild.post("Kalle", 10)
    # result = guild.get_user_amount("Kalle")
    result = guild.get_total()
    pass


if __name__ == "__main__":
    main()