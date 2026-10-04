-- 指標: 部品点数（部品の数を数える）
-- ディメンション: 供給者の名称（この単位で分けて数える）
SELECT supplier.name                AS supplier_name,
       COUNT(DISTINCT part.part_id) AS part_count
FROM part JOIN supplier ON part.supplier_id = supplier.supplier_id
GROUP BY supplier.name;
