class Config:
    NULL_ADDRESS = "0x0000000000000000000000000000000000000000"
    DEV_ADDRESS = "0x5CCf79Ea2e102249C1949835D50FC3da354A67B1"
    DEPLOYER = "deployer"

class MainnetConfig(Config):
    # 3rd party
    WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    UNISWAP_FACTORY = "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"
    # our own contracts
    STEAK_TOKEN  = ""
    TIMELOCK     = ""
    GOVERNOR     = ""
    V2_FACTORY   = ""
    V2_PAIR_HASH = ""
    V2_ROUTER    = ""
    STEAK_BAR    = ""
    STEAK_MAKER  = ""
    MASTER_CHEF  = ""
    MIGRATOR     = ""
