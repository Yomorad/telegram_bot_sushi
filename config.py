from dataclasses import dataclass

@dataclass
class Config:
    token: str = 'token'
    admin_ids: int = 'admin_ids'
    pay_token: str = 'pay_token'

    data_base_p: str = 'data_base_p'
    user_p: str = 'user_p'
    host_p: str = 'host_p'
    password_p: str = 'password_p'

