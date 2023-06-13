import os

from web3 import Web3
from solcx import compile_source
import dotenv

CONTRACT_URL = os.getenv(("contract_url"))
def read_solidity_file(filename):
    with open(filename, 'r') as file:
        solidity_code = file.read()
    return solidity_code

def deploy_contract():
    # Connect to the Ethereum network
    w3 = Web3(Web3.HTTPProvider(CONTRACT_URL))

    # Compile the Solidity contract
    filename = "/src/solidity/Storage.sol"
    contract_source_code = read_solidity_file
    compiled_contract = compile_source(contract_source_code)
    contract_interface = compiled_contract['<contract_name>:<contract_name>']

    # Create an instance of the contract
    contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

    # Estimate the gas required for deployment
    gas_estimate = contract.constructor().estimateGas()

    # Deploy the contract
    tx_hash = contract.constructor().transact({'from': w3.eth.accounts[0], 'gas': gas_estimate})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    # Retrieve the contract address
    contract_address = tx_receipt['contractAddress']

    # Return the contract address
    return contract_address

# Deploy the contract
contract_address = deploy_contract()
print("Contract deployed at address:", contract_address)
