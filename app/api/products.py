from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.product import ProductCreate, ProductOut
from app.models.product import Product
from app.core.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter(prefix="/products", tags=["products"])


@router.post("/", response_model=ProductOut)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_product = Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.get("/", response_model=list[ProductOut])
def list_products(
    db: Session = Depends(
        get_db), current_user: User = Depends(get_current_user)
):
    return db.query(Product).all()


@router.get("/{product_id}", response_model=ProductOut)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = db.query(Product).get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product


@router.put("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    update: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = db.query(Product).get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    for key, value in update.dict().items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = db.query(Product).get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db.delete(product)
    db.commit()
    return {"message": "Produto excluído com sucesso"}
