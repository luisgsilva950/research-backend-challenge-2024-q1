CREATE UNLOGGED TABLE customer (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(30),
    "limit" INTEGER NOT NULL,
    balance INTEGER NOT NULL DEFAULT 0
);


CREATE UNLOGGED TABLE transactions (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    customer_id INT NOT NULL,
    value INT NOT NULL,
    type CHAR(1) NOT NULL,
    description VARCHAR(10) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_clientes_transacoes_id FOREIGN KEY (customer_id) REFERENCES customer(id)
);

INSERT INTO customer (name, "limit")
  VALUES
    ('o barato sai caro', 1000 * 100),
    ('zan corp ltda', 800 * 100),
    ('les cruders', 10000 * 100),
    ('padaria joia de cocaia', 100000 * 100),
    ('kid mais', 5000 * 100);

CREATE UNIQUE INDEX idx_customer_id ON customer (id) INCLUDE ("limit", balance);
CREATE INDEX idx_transactions_customer_id ON transactions (customer_id) INCLUDE(id, created_at, value, type, description);
CREATE INDEX idx_transactions_customer_id_created_at ON transactions (customer_id, created_at DESC) INCLUDE(id, created_at, value, type, description);
