# Relatório de Qualidade de Dados (Northwind)

Este documento apresenta uma análise básica da qualidade dos dados extraídos dos arquivos CSV.

## categories.csv
- **Total de Linhas:** 8
- **Total de Colunas:** 4

### Colunas e Valores Nulos
| Coluna | Tipo | Valores Nulos | % Nulos |
|--------|------|---------------|----------|
| category_id | int64 | 0 | 0.00% |
| category_name | object | 0 | 0.00% |
| description | object | 0 | 0.00% |
| picture | object | 0 | 0.00% |

---

## customers.csv
- **Total de Linhas:** 91
- **Total de Colunas:** 11

### Colunas e Valores Nulos
| Coluna | Tipo | Valores Nulos | % Nulos |
|--------|------|---------------|----------|
| customer_id | object | 0 | 0.00% |
| company_name | object | 0 | 0.00% |
| contact_name | object | 0 | 0.00% |
| contact_title | object | 0 | 0.00% |
| address | object | 0 | 0.00% |
| city | object | 0 | 0.00% |
| region | object | 60 | 65.93% |
| postal_code | object | 1 | 1.10% |
| country | object | 0 | 0.00% |
| phone | object | 0 | 0.00% |
| fax | object | 22 | 24.18% |

---

## customer_customer_demo.csv
- **Total de Linhas:** 0
- **Total de Colunas:** 2

### Colunas e Valores Nulos
| Coluna | Tipo | Valores Nulos | % Nulos |
|--------|------|---------------|----------|
| customer_id | object | 0 | 0.00% |
| customer_type_id | object | 0 | 0.00% |

---

## customer_demographics.csv
- **Total de Linhas:** 0
- **Total de Colunas:** 2

### Colunas e Valores Nulos
| Coluna | Tipo | Valores Nulos | % Nulos |
|--------|------|---------------|----------|
| customer_type_id | object | 0 | 0.00% |
| customer_desc | object | 0 | 0.00% |

---

## employees.csv
- **Total de Linhas:** 9
- **Total de Colunas:** 18

### Colunas e Valores Nulos
| Coluna | Tipo | Valores Nulos | % Nulos |
|--------|------|---------------|----------|
| employee_id | int64 | 0 | 0.00% |
| last_name | object | 0 | 0.00% |
| first_name | object | 0 | 0.00% |
| title | object | 0 | 0.00% |
| title_of_courtesy | object | 0 | 0.00% |
| birth_date | object | 0 | 0.00% |
| hire_date | object | 0 | 0.00% |
| address | object | 0 | 0.00% |
| city | object | 0 | 0.00% |
| region | object | 4 | 44.44% |
| postal_code | object | 0 | 0.00% |
| country | object | 0 | 0.00% |
| home_phone | object | 0 | 0.00% |
| extension | int64 | 0 | 0.00% |
| photo | object | 0 | 0.00% |
| notes | object | 0 | 0.00% |
| reports_to | float64 | 1 | 11.11% |
| photo_path | object | 0 | 0.00% |

---

## employee_territories.csv
- **Total de Linhas:** 49
- **Total de Colunas:** 2

### Colunas e Valores Nulos
| Coluna | Tipo | Valores Nulos | % Nulos |
|--------|------|---------------|----------|
| employee_id | int64 | 0 | 0.00% |
| territory_id | int64 | 0 | 0.00% |

---

## orders.csv
- **Total de Linhas:** 830
- **Total de Colunas:** 14

### Colunas e Valores Nulos
| Coluna | Tipo | Valores Nulos | % Nulos |
|--------|------|---------------|----------|
| order_id | int64 | 0 | 0.00% |
| customer_id | object | 0 | 0.00% |
| employee_id | int64 | 0 | 0.00% |
| order_date | object | 0 | 0.00% |
| required_date | object | 0 | 0.00% |
| shipped_date | object | 21 | 2.53% |
| ship_via | int64 | 0 | 0.00% |
| freight | float64 | 0 | 0.00% |
| ship_name | object | 0 | 0.00% |
| ship_address | object | 0 | 0.00% |
| ship_city | object | 0 | 0.00% |
| ship_region | object | 507 | 61.08% |
| ship_postal_code | object | 19 | 2.29% |
| ship_country | object | 0 | 0.00% |

---

## order_details.csv
- **Total de Linhas:** 2155
- **Total de Colunas:** 5

### Colunas e Valores Nulos
| Coluna | Tipo | Valores Nulos | % Nulos |
|--------|------|---------------|----------|
| order_id | int64 | 0 | 0.00% |
| product_id | int64 | 0 | 0.00% |
| unit_price | float64 | 0 | 0.00% |
| quantity | int64 | 0 | 0.00% |
| discount | float64 | 0 | 0.00% |

---

## products.csv
- **Total de Linhas:** 77
- **Total de Colunas:** 10

### Colunas e Valores Nulos
| Coluna | Tipo | Valores Nulos | % Nulos |
|--------|------|---------------|----------|
| product_id | int64 | 0 | 0.00% |
| product_name | object | 0 | 0.00% |
| supplier_id | int64 | 0 | 0.00% |
| category_id | int64 | 0 | 0.00% |
| quantity_per_unit | object | 0 | 0.00% |
| unit_price | float64 | 0 | 0.00% |
| units_in_stock | int64 | 0 | 0.00% |
| units_on_order | int64 | 0 | 0.00% |
| reorder_level | int64 | 0 | 0.00% |
| discontinued | int64 | 0 | 0.00% |

---

## region.csv
- **Total de Linhas:** 4
- **Total de Colunas:** 2

### Colunas e Valores Nulos
| Coluna | Tipo | Valores Nulos | % Nulos |
|--------|------|---------------|----------|
| region_id | int64 | 0 | 0.00% |
| region_description | object | 0 | 0.00% |

---

## shippers.csv
- **Total de Linhas:** 6
- **Total de Colunas:** 3

### Colunas e Valores Nulos
| Coluna | Tipo | Valores Nulos | % Nulos |
|--------|------|---------------|----------|
| shipper_id | int64 | 0 | 0.00% |
| company_name | object | 0 | 0.00% |
| phone | object | 0 | 0.00% |

---

## suppliers.csv
- **Total de Linhas:** 29
- **Total de Colunas:** 12

### Colunas e Valores Nulos
| Coluna | Tipo | Valores Nulos | % Nulos |
|--------|------|---------------|----------|
| supplier_id | int64 | 0 | 0.00% |
| company_name | object | 0 | 0.00% |
| contact_name | object | 0 | 0.00% |
| contact_title | object | 0 | 0.00% |
| address | object | 0 | 0.00% |
| city | object | 0 | 0.00% |
| region | object | 20 | 68.97% |
| postal_code | object | 0 | 0.00% |
| country | object | 0 | 0.00% |
| phone | object | 0 | 0.00% |
| fax | object | 16 | 55.17% |
| homepage | object | 24 | 82.76% |

---

## territories.csv
- **Total de Linhas:** 53
- **Total de Colunas:** 3

### Colunas e Valores Nulos
| Coluna | Tipo | Valores Nulos | % Nulos |
|--------|------|---------------|----------|
| territory_id | int64 | 0 | 0.00% |
| territory_description | object | 0 | 0.00% |
| region_id | int64 | 0 | 0.00% |

---

## us_states.csv
- **Total de Linhas:** 51
- **Total de Colunas:** 4

### Colunas e Valores Nulos
| Coluna | Tipo | Valores Nulos | % Nulos |
|--------|------|---------------|----------|
| state_id | int64 | 0 | 0.00% |
| state_name | object | 0 | 0.00% |
| state_abbr | object | 0 | 0.00% |
| state_region | object | 0 | 0.00% |

---

