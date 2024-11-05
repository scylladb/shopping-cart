from scylladb import ScyllaClient
import config
from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
import uuid

app = FastAPI(
    title="ScyllaDB ecommerce sample application",
    contact={"url":"https://scylladb.com"}
)

client = ScyllaClient(config).get_session()

class Product(BaseModel):
    id: str
    name: str
    price: float
    img: str
    

class CartItem(BaseModel):
    product_id: str
    quantity: int = None
    

def fetch_active_cart(user_id):
    return client.execute("SELECT * FROM cart WHERE user_id = %s AND is_active = true;", [user_id]).one()
    

@app.get("/", tags=["home"])
def home():
    return {"Hello World!": "ScyllaDB Ecommerce sample application"}


@app.get("/products", tags=["products"])
def products(limit: int = 10):
    query = f"SELECT * FROM product LIMIT {limit};"
    return client.execute(query).all()


@app.get("/products/{product_id}", tags=["products"])
def product(product_id):
    query = "SELECT * FROM product WHERE id = %s;"
    return client.execute(query, [uuid.UUID(product_id), ]).one()


@app.get("/cart/{user_id}", tags=["cart"])
def cart(user_id):
    active_cart = fetch_active_cart(user_id)
    if active_cart is None:
        raise HTTPException(status_code=404, detail="No items found in cart")
    query = "SELECT * FROM cart_items WHERE user_id = %s AND cart_id = %s;"
    return client.execute(query, [user_id, active_cart["cart_id"]]).all()


@app.post("/cart/{user_id}", tags=["cart"])
def add_to_cart(user_id, cart_item: CartItem):
    active_cart = fetch_active_cart(user_id)
    if active_cart is None: # no active cart, create a new one
        active_cart_id = uuid.uuid4()
        client.execute("INSERT INTO cart(user_id, cart_id, is_active) VALUES (%s, %s, true)", [user_id, active_cart_id])
    else: # use existing cart
        active_cart_id = active_cart["cart_id"]
    
    # add the product to cart  
    query = "INSERT INTO cart_items (user_id, cart_id, product_id, product_quantity) VALUES (%s, %s, %s, %s)"
    values = [user_id, active_cart_id, uuid.UUID(cart_item.product_id), cart_item.quantity]
    return client.execute(query, values)


@app.delete("/cart/{user_id}", tags=["cart"])
def delete_from_cart(user_id, cart_item: CartItem):
    active_cart = fetch_active_cart(user_id)
    if active_cart is None:
        raise HTTPException(status_code=404, detail="No items found in cart")
    query = "DELETE FROM cart_items WHERE user_id = %s AND cart_id = %s AND product_id = %s"
    return client.execute(query,
                          [user_id, active_cart["cart_id"], uuid.UUID(cart_item.product_id)])      


@app.post("/products", tags=["products"])
def upload_product(product: Product):
    query = "INSERT INTO product (id, name, price, img) VALUES (%s, %s, %s, %s)"
    values = list(product.model_dump().values())
    values[0] = uuid.UUID(values[0])
    return client.execute(query, values)


@app.put("/products/{product_id}", tags=["products"])
def update_product(product: Product, product_id):
    values = [product.name, product.price, product.img, uuid.UUID(product_id)]
    query = "UPDATE product SET name=%s, price=%s, img=%s WHERE id = %s"
    return client.execute(query, values)


@app.delete("/products/{product_id}", tags=["products"])
def delete_product(product_id):
    query = "DELETE FROM product WHERE id = %s"
    return client.execute(query, [uuid.UUID(product_id)])


@app.post("/cart/{user_id}/checkout", tags=["cart"])
def checkout(user_id):
    active_cart = fetch_active_cart(user_id)
    if active_cart is None:
        raise HTTPException(status_code=404, detail="User does not have an active cart")
    query = "UPDATE cart SET is_active = false WHERE user_id = %s AND cart_id = %s"
    return client.execute(query, [user_id, active_cart["cart_id"]])
