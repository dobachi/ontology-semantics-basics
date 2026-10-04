CREATE TABLE supplier (
  supplier_id TEXT PRIMARY KEY,
  name        TEXT NOT NULL
);
CREATE TABLE part (
  part_id     TEXT PRIMARY KEY,
  name        TEXT NOT NULL,
  weight_g    REAL,
  supplier_id TEXT NOT NULL REFERENCES supplier(supplier_id)
);
INSERT INTO supplier VALUES ('S-01', '東和精工');
INSERT INTO part VALUES ('P-100', '六角ボルト M8', 12, 'S-01');

SELECT part.name, supplier.name
FROM part JOIN supplier ON part.supplier_id = supplier.supplier_id;
