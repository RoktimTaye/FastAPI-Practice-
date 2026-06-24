from fastapi import FastAPI,HTTPException,Query,Path  # ty:ignore[unresolved-import]
from service.product import get_all_products
app = FastAPI()

@app.get("/")
def root():
    return {"Message" : "Welcome to FAastAPI"}

@app.get("/products")
def list_products(
    name: str = Query(default=None,min_lenght=50,max_lenght= 50, description="Search product by name"),
    sort_by_price: bool = Query(default=False,description="Sort products by price"),
    order: str = Query(default="asc",description="Sort order : asc, desc"),
    limit: int = Query(default=10,ge=1,le=100,description="Number of items to return"),
    offset: int = Query(default=0,description="Pagination offset")
):
    products = get_all_products()
    
    if name:
        needle = name.strip().lower()
        products = [p for p in products if needle in p.get("name","").lower()]
        if not products:
            raise HTTPException(status_code=404,detail=f"No product found matching the name {name}")

    if sort_by_price:
        reverse = True if order == "desc" else False
        products = sorted(products,key=lambda p:p.get("price",0),reverse = reverse)

    paginated_products = products[offset : offset + limit]
    return {
        "total": len(products),
        "items": paginated_products
    }


@app.get("/products/{product_id}")
def get_product_by_id(
    product_id: str = Path(...,min_lenght=36,max_lenght=36,description="UUID of the product")
):
    products = get_all_products()
    for product in products:
        if product.get("id") == product_id:
            return product
    raise HTTPException(status_code=404,detail="Product not found")

@app.get("/products/{id}")
def get_products(id: int):
    products = ["brush", "laptop", "mouse", "monitor"]
    
    if id < len(products):
        return products[id]
    else:
        raise HTTPException(status_code=404, detail="No product found")
