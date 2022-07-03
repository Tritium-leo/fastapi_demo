# user
UserRedisInfoCacheKey = "user_info"

# model
UserQueryBatchMax = 200
UserNameMinLen = 7  # [7,20)
UsernameMaxLen = 20

# logic
UserNoUpdateColumn = ['username', 'uuid']  # can't update columns
UserWrongPWDMaxOneDay = 5  # 一天密码错误最大次数（不包括）
UserTokenDuration = 2 * 60 * 60 * 1000  # 2 hour
UserTokenLongDuration = 10 * 24 * 60 * 60 * 100  # 10 day

# Action
ActionCreateUser = "ActionCreateUser"  #
ActionUserLogin = "ActionUserLogin"
ActionUserRegister = "ActionUserRegister"
ActionUserUpdateInfo = "ActioUserUpdateInfo"
ActionUserCancel = "ActionUserCancel"
