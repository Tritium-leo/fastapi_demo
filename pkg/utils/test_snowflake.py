import snowflake.client as snow_cli

if __name__ == "__main__":
    snow_cli.setup("0.0.0.0", "8910")
    cli = snow_cli.default_client
    logger.info(snow_cli.get_guid())
    logger.info(snow_cli.get_stats())
