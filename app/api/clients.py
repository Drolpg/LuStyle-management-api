from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.client import ClientCreate, ClientOut
from app.models.client import Client
from app.core.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter(prefix="/clients", tags=["clients"])


@router.post("/", response_model=ClientOut)
def create_client(
    client: ClientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    for field, value in [
        ("email", client.email),
        ("cpf", client.cpf),
        ("phone_number", client.phone_number),
    ]:
        if db.query(Client).filter(getattr(Client, field) == value).first():
            raise HTTPException(
                status_code=400, detail=f"{field} já cadastrado")

    new_client = Client(**client.dict())
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client


@router.get("/", response_model=list[ClientOut])
def list_clients(
    db: Session = Depends(get_db), current_user: User = Depends(
        get_current_user)
):
    return db.query(Client).all()


@router.get("/{client_id}", response_model=ClientOut)
def get_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    client = db.query(Client).get(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return client


@router.put("/{client_id}", response_model=ClientOut)
def update_client(
    client_id: int,
    update: ClientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    client = db.query(Client).get(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    for key, value in update.dict().items():
        setattr(client, key, value)
    db.commit()
    db.refresh(client)
    return client


@router.delete("/{client_id}")
def delete_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    client = db.query(Client).get(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    db.delete(client)
    db.commit()
    return {"message": "Cliente excluído com sucesso"}
