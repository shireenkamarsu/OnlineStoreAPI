from dataclasses import dataclass
from datamodels.Name import Name
from datamodels.Address import Address

@dataclass
class User:
    email: str
    username: str
    password: str
    name: Name
    address: Address
    phone: str
