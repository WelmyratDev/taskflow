from dataclasses import dataclass


@dataclass
class AccountLoginOutput:
    session_id: str
    msg: str