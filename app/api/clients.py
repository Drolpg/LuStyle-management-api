from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.client import ClientCreate, ClientOut
from app.models.client import Client
from app.core.exceptions import AlreadyExistsException, NotFoundException
from app.core.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter(prefix="/clients", tags=["clients"])


@router.post(
        "/", response_model=ClientOut, status_code=status.HTTP_201_CREATED)
def create_client(
    client: ClientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        for field, value in [
            ("email", client.email),
            ("cpf", client.cpf),
            ("phone_number", client.phone_number),
        ]:
            if db.query(Client).filter(
                getattr(Client, field) == value
            ).first():
                raise AlreadyExistsException()

        new_client = Client(**client.model_dump())
        db.add(new_client)
        db.commit()
        db.refresh(new_client)
        return new_client
    except AlreadyExistsException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cliente já existe"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar cliente: {str(e)}"
        )


@router.get("/", response_model=list[ClientOut])
def list_clients(
    db: Session = Depends(get_db), current_user: User = Depends(
        get_current_user)
):
    try:
        return db.query(Client).all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar clientes: {str(e)}"
        )


@router.get("/{client_id}", response_model=ClientOut)
def get_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        client = db.get(Client, client_id)
        if not client:
            raise NotFoundException()
        return client
    except NotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar cliente: {str(e)}"
        )


@router.put("/{client_id}", response_model=ClientOut)
def update_client(
    client_id: int,
    update: ClientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        client = db.get(Client, client_id)
        if not client:
            raise NotFoundException()
        for key, value in update.model_dump().items():
            setattr(client, key, value)
        db.commit()
        db.refresh(client)
        return client
    except NotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar cliente: {str(e)}"
        )


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        client = db.get(Client, client_id)
        if not client:
            raise NotFoundException()
        db.delete(client)
        db.commit()
        return {"message": "Cliente excluído com sucesso"}
    except NotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao remover cliente: {str(e)}"
        )
