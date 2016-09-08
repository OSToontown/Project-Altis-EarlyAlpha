DefaultDbName = 'tt_code_redemption'
RedeemErrors = Enum('Success, CodeDoesntExist, CodeIsInactive, CodeAlreadyRedeemed, AwardCouldntBeGiven, TooManyAttempts, SystemUnavailable, ')
RedeemErrorStrings = {RedeemErrors.Success: 'Success, your reward is on its way!',
 RedeemErrors.CodeDoesntExist: 'Invalid code',
 RedeemErrors.CodeIsInactive: 'Sorry! This code has expired!',
 RedeemErrors.CodeAlreadyRedeemed: 'Code has already been redeemed',
 RedeemErrors.AwardCouldntBeGiven: 'Award could not be given',
 RedeemErrors.TooManyAttempts: 'Too many attempts, code ignored',
 RedeemErrors.SystemUnavailable: 'Code redemption is currently unavailable'}
MaxCustomCodeLen = config.GetInt('tt-max-custom-code-len', 16)
MaxCodeAttempts = 5
CodeWaitTime = 2
