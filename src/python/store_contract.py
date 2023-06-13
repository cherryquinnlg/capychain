from web3 import Web3
from ABI import contract_abi
import dotenv
import os
# Load the .env file
dotenv.load_dotenv()
# Get the value of the `SECRET_KEY` environment variable
CONTRACT_ADDRESS = os.getenv("store_contract_address")
CONTRACT_URL = os.getenv(("contract_url"))

def store_contract(users, times, idHashs, reportHashs):
    provider = Web3.HTTPProvider(CONTRACT_URL)
    web3 = Web3(provider)

    # Create a contract instance
    contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

    # Convert the string arrays to bytes arrays
    users_bytes = [web3.toBytes(text=user) for user in users]
    times_bytes = [web3.toBytes(text=time) for time in times]
    idHashs_bytes = [web3.toBytes(text=idHash) for idHash in idHashs]
    reportHashs_bytes = [web3.toBytes(text=reportHash) for reportHash in reportHashs]

    # Call the addDataBatch function
    tx_hash = contract.functions.addDataBatch(users_bytes, times_bytes, idHashs_bytes, reportHashs_bytes).transact()

    # Wait for the transaction to be mined
    web3.eth.waitForTransactionReceipt(tx_hash)

# Check the result by calling other functions, such as getCountByUser or getDataByUser
