# RESTful API products (iphone14-api)

## 構建 image

```
docker compose build
```

## 啟動

1. 啟動服務

    ```
    docker compose up -d
    ```

2. 訪問 openAPI 頁面

    browser: http://localhost:8088/docs


## 測試

```
docker compose exec iphone14-api pytest -sv
```

