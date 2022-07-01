import snowflake.client as snow_cli

if __name__ == "__main__":
    snow_cli.setup("0.0.0.0", "8910")
    cli = snow_cli.default_client
    print(snow_cli.get_guid())
    print(snow_cli.get_stats())
