import snowflake.client as snow_cli

prev = 0
autoincr = 1


def get_snow_id():
    global prev
    global autoincr
    try:
        snow_cli.get_stats()  # health
        new_id = snow_cli.get_guid()
        prev = new_id
        if autoincr > 1:
            print(f"IN SNOWFLAKE DEAD DURATION:used PREV:{prev}, autoincre:{autoincr} ")
            # rop range key
            while new_id <= prev + autoincr:
                new_id = snow_cli.get_guid()
            autoincr = 1
    except:
        print("ERROR ! SNOW FLAKE SERVER DEAD")
        new_id = prev + autoincr
        autoincr += 1
    return new_id
