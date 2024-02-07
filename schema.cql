CREATE KEYSPACE IF NOT EXISTS ecommerce WITH replication = { 'class': 'NetworkTopologyStrategy', 'replication_factor': '3' };

CREATE TABLE ecommerce.product (
    id UUID,
    name TEXT,
    price FLOAT,
    img TEXT,
    PRIMARY KEY (id)
);


CREATE TABLE ecommerce.active_cart (
    user_id TEXT,
    products set<UUID>,
    PRIMARY KEY (user_id)
) WITH cdc = {'enabled': true};


CREATE TABLE ecommerce.orders (
    user_id TEXT,
    created_at TIMESTAMP,
    products set<UUID>,
    PRIMARY KEY (user_id, created_at)
) WITH CLUSTERING ORDER BY (created_at DESC);
