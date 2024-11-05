CREATE KEYSPACE IF NOT EXISTS ecommerce WITH replication = { 'class': 'NetworkTopologyStrategy', 'replication_factor': '3' };

CREATE TABLE ecommerce.product (
    id UUID,
    name TEXT,
    price FLOAT,
    img TEXT,
    PRIMARY KEY (id)
);

CREATE TABLE ecommerce.cart (
    user_id TEXT,
    cart_id UUID,
    is_active BOOLEAN,
    PRIMARY KEY (user_id, cart_id)
);
CREATE INDEX cart_is_active ON ecommerce.cart ((user_id), is_active);

CREATE TABLE ecommerce.cart_items (
    user_id TEXT,
    cart_id UUID,
    product_id UUID,
    product_quantity INT,
    PRIMARY KEY (user_id, cart_id, product_id)
) WITH cdc = {'enabled': true, 'preimage': true, 'postimage': true};
