from dataclasses import dataclass



@dataclass
class AccountCreate:
    username: str
    email: str
    password: str
    role: str


@dataclass
class AccountLogin:
    username: str
    password: str