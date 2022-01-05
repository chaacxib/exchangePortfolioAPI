# Create

Used to create a new stock on the database.

**URL** : `/stock/`

**Method** : `POST`

**Auth required** : NO

**Data constraints**

```json
{
  "name": "[Company name (Max 50 characters)]",
  "description": "[Company brief description (Max 100 characters)]",
  "symbol": "[valid New York stock symbol of a company (Max 10 characters)]"
}
```

**Data example**

```json
{
  "name": "Nasdaq, Inc.",
  "description": "Financial services corporation that owns and operates three stock exchanges in the United States",
  "symbol": "nasdaq"
}
```

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "id": "13918333-0a7a-4835-ab76-6685127d7d3b",
    "name": "Nasdaq, Inc.",
    "description": "Financial services corporation that owns and operates three stock exchanges in the United States",
    "symbol": "nasdaq"
    "market_value": [
        0.2,
        ...
    ]
}
```

## Error Response

**Conditions**
* `name` field has more than 50 characters.
* `description` field has more than 100 characters.
* `symbol` field has more than 10 characters.
* `symbol` field is not a valid New York Stock.

**Code** : `422 UNPROCESSABLE ENTITY`

**Content** :

```json
{
  "detail": [
    {
      "loc": [
        "body",
        "name"
      ],
      "msg": "field limited to 50 characters",
      "type": "value_error"
    },
    {
      "loc": [
        "body",
        "description"
      ],
      "msg": "field limited to 100 characters",
      "type": "value_error"
    },
    {
      "loc": [
        "body",
        "symbol"
      ],
      "msg": "field limited to 10 characters",
      "type": "value_error"
    },
    {
      "loc": [
        "body",
        "symbol"
      ],
      "msg": "symbol not listed in the New York stock exchange",
      "type": "value_error"
    }
  ]
}
```

# Read

Used to get a stock from the database using the id.

**URL** : `/stock/{stock_id}`

URL Parameters : stock_id=[string] where stock_id is the ID of the Stock on the server.

**Method** : `GET`

**Auth required** : NO

**Data**: `{}`


## Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "id": "13918333-0a7a-4835-ab76-6685127d7d3b",
    "name": "Nasdaq, Inc.",
    "description": "Financial services corporation that owns and operates three stock exchanges in the United States",
    "symbol": "nasdaq"
    "market_value": [
        0.2,
        ...
    ]
}
```

## Error Response

**Condition**: If the provided ID doesn't exist on the database.

**Code** : `404 NOT FOUND`

**Content** :

```json
{
  "detail": "Stock not found"
}
```

# Read All

Used to get all stocks from the database.

**URL** : `/stocks/`

**Method** : `GET`

**Auth required** : NO

**Data**: `{}`


## Success Response

**Code** : `200 OK`

**Content example**

```json
[
    {
        "id": "13918333-0a7a-4835-ab76-6685127d7d3b",
        "name": "Nasdaq, Inc.",
        "description": "Financial services corporation that owns and operates three stock exchanges in the United States",
        "symbol": "nasdaq"
        "market_value": [
            0.2,
            ...
        ]
    },
    ...
]
```

# Update

Used to update stock data on the database.

**URL** : `/stock/{stock_id}`

URL Parameters : stock_id=[string] where stock_id is the ID of the Stock on the server.

**Method** : `PATCH`

**Auth required** : NO

**Data example**

```json
{
  "name": "S&P 500",
}
```


## Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "id": "13918333-0a7a-4835-ab76-6685127d7d3b",
    "name": "S&P 500",
    "description": "Financial services corporation that owns and operates three stock exchanges in the United States",
    "symbol": "nasdaq"
    "market_value": [
        0.2,
        ...
    ]
}
```

## Error Response

**Condition**: If the provided ID doesn't exist on the database.

**Code** : `404 NOT FOUND`

**Content** :

```json
{
  "detail": "Stock not found"
}
```

# Delete

Used to delete an stock on the database.

**URL** : `/stock/{stock_id}`

URL Parameters : stock_id=[string] where stock_id is the ID of the Stock on the server.

**Method** : `DELETE`

**Auth required** : NO

**Data**: `{}`


## Success Response

**Code** : `200 OK`

**Content example**

```text
Stock successfully deleted
```

## Error Response

**Condition**: If the provided ID doesn't exist on the database.

**Code** : `404 NOT FOUND`

**Content** :

```json
{
  "detail": "Stock not found"
}
```