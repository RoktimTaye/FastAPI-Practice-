from fastapi import FastAPI,HTTPException,Query  # ty:ignore[unresolved-import]
from service.product import get_all_products

app = FastAPI()

@app.get("/")
def root():
    return {"Message" : "Welcome to FastAPI"}

# dynamic routing 
@app.get("/products")
def List_products(
    name:str = Query(default=None,min_length=1,max_lenght=50,description="Search by product name"),
    sort_by_price:bool = Query(default=False,description="Sort products by price"),
    order: str = Query(default="asc",description="Sort order : asc, desc"),
    limit: int = Query(default=10,ge=1,le=100,description="Number of items to return"),
    offset: int = Query(default=0, description="Pagination offset")
):
    products = get_all_products()
    
    if name:
        needle = name.strip().lower()
        products = [p for p in products if needle in p.get("name","").lower()]
        if not products:
            raise HTTPException(status_code=404,detail=f"No product found matching name {name} ")
        
    if sort_by_price:
        reverse = True if order == "desc" else False
        products = sorted(products,key=lambda p: p.get("price",0),reverse=reverse)
        
    paginated_product = products[offset : offset + limit]
    return {
        "total": len(products),
        "items":paginated_product
    }
    