from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.product import ProductCreate, ProductOut
from app.models.product import Product
from app.core.deps import get_db, get_current_user, get_current_admin_user
from app.core.exceptions import NotFoundException
from app.models.user import User

router = APIRouter(prefix="/products", tags=["products"])


@router.post(
        "/",
        response_model=ProductOut,
        status_code=status.HTTP_201_CREATED
        )
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    try:
        new_product = Product(**product.model_dump())
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar produto: {str(e)}"
        )


@router.get("/", response_model=list[ProductOut])
def list_products(
    db: Session = Depends(
        get_db), current_user: User = Depends(get_current_user)
):
    try:
        return db.query(Product).all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar produtos: {str(e)}"
        )


@router.get("/{product_id}", response_model=ProductOut)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        product = db.query(Product).get(product_id)
        if not product:
            raise NotFoundException()
        return product
    except NotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar produto: {str(e)}"
        )


@router.put("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    update: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    try:
        product = db.query(Product).get(product_id)
        if not product:
            raise NotFoundException()
        for key, value in update.model_dump().items():
            setattr(product, key, value)
        db.commit()
        db.refresh(product)
        return product
    except NotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar produto: {str(e)}"
        )


@router.delete(
        "/{product_id}",
        status_code=status.HTTP_204_NO_CONTENT
        )
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    try:
        product = db.query(Product).get(product_id)
        if not product:
            raise NotFoundException()
        db.delete(product)
        db.commit()
        return {"message": "Produto excluído com sucesso"}
    except NotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao remover produto: {str(e)}"
        )
