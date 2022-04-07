from typing import Optional

from db.postgres.models import User, TgUserAccount
from db.postgres.users import get_users_with_accounts

from .methods import start_client


DEFAULT = 'default'
CLIENTS = 'clients'


class TgClientRepository:
    _clients: dict[int, dict]

    # {
    #     "user_id": {
    #         DEFAULT: "client_id",
    #         CLIENTS: {
    #             "client_id": "client"
    #         }
    #     }
    # }


    def __init__(self, clients: dict[int, dict]):
        self._clients = clients


    @classmethod
    async def create(cls):
        clients = {}

        for user in await get_users_with_accounts():
            accounts = {}
            default = None
            for account in user.accounts:
                if account.activated is True:
                    if account.default is True and default is None:
                        default = account.id

                    client = await start_client(
                        account.api_id, account.api_hash, account.session
                    )
                    accounts[account.id] = client

                    if account.session is None:
                        await account.update(session=client.session.save()) 

            clients[user.id] = {
                DEFAULT: default,
                CLIENTS: accounts
            }

        return cls(clients)


    def get_client(self, user_id: int, account_id: int) -> Optional['client']:
        user = self._clients.get(user_id, {})
        return user.get(CLIENTS, {}).get(account_id)
    

    def get_default(self, user_id: int) -> Optional['client']:
        user = self._clients.get(user_id, {})
        default = user.get(DEFAULT, 0)
        return self.get_client(user_id, default)

    
    def set_default(self, user_id: int, account_id: int):
        user = self._clients.get(user_id, {})
        user[DEFAULT] = account_id
        self._clients[user_id] = user


    async def delete_account(self, user_id: int, account_id: int):
        user = self._clients.get(user_id, {})
        if user.get(DEFAULT) == account_id:
            user[DEFAULT] = None
        client = user.get(CLIENTS, {}).pop(account_id, None)
        if client is not None:
            await client.disconnect()
        self._clients[user_id] = user


    async def create_account(self, account: TgUserAccount, phone: Optional[str] = None):
        user_id = account.user.id
        user = self._clients.get(user_id, {})
        clients = user.get(CLIENTS, {})
        clients[account.id] = await start_client(
            account.api_id, account.api_hash, account.session, phone
        )
        user[CLIENTS] = clients
        self._clients[account.user.id] = user
        return clients[account.id]
