from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user, get_current_admin_user
from app.core.exceptions import NotFoundException
from app.models.order import Order
from app.models.user import User
from app.schemas.order import OrderCreate, OrderOut

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post(
        "/",
        response_model=OrderOut,
        status_code=status.HTTP_201_CREATED
        )
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    try:
        new_order = Order(**order.model_dump())
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        return new_order
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar pedido: {str(e)}"
        )


@router.get("/", response_model=list[OrderOut])
def list_orders(
    db: Session = Depends(
        get_db), current_user: User = Depends(get_current_user)
):
    try:
        return db.query(Order).all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar pedido: {str(e)}"
        )


@router.get("/{order_id}", response_model=OrderOut)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        order = db.query(Order).get(order_id)
        if not order:
            raise NotFoundException()
        return order
    except NotFoundException:
        raise HTTPException(
                status_code=404,
                detail="Pedido não encontrado"
                )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar pedido: {str(e)}"
        )


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    try:
        order = db.query(Order).get(order_id)
        if not order:
            raise NotFoundException()
        db.delete(order)
        db.commit()
        return {"message": "Pedido excluído com sucesso"}
    except NotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao remover pedido: {str(e)}"
        )
