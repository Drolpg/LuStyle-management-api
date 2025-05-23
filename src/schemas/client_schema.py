from pydantic import BaseModel, AwareDatetime


class Clients(BaseModel):
    id: int
    name: str
    email: str
    number_fone: str
    date_register: AwareDatetime | None = None
