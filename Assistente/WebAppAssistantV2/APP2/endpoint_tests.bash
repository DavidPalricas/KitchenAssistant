# TESTING ENDPOINTS

# -------------------------------------------------------------- [TEST GET ALL RECIPES]
curl -X GET http://127.0.0.1:5000/recipes


# -------------------------------------------------------------- [TEST INSERT STOCK FROM PANTRY]
curl -X POST http://127.0.0.1:5000/pantry/insert-stock \
-H "Content-Type: application/json" \
-d '{
    "name": "Azeite",
    "quantity": "1",
    "unit": "l",
    "expiration_date": "2024-04-23"
}'

# -------------------------------------------------------------- [TEST REMOVE STOCK FROM PANTRY]
curl -X POST http://127.0.0.1:5000/pantry/remove-stock \
-H "Content-Type: application/json" \
-d '{
    "name": "Azeite",
    "quantity": "50",
    "unit": "ml"
}'

# -------------------------------------------------------------- [TEST GET COMPLETE PANTRY]
curl -X GET http://127.0.0.1:5000/pantry/stock

# -------------------------------------------------------------- [TEST INSERT PRODUCT INTO SHOPPING LIST]
curl -X POST http://127.0.0.1:5000/pantry/insert-grocery \
-H "Content-Type: application/json" \
-d '{"name": "azeite"}'

# -------------------------------------------------------------- [TEST REMOVE PRODUCT FROM SHOPPING LIST]
curl -X DELETE http://127.0.0.1:5000/pantry/remove-grocery \
-H "Content-Type: application/json" \
-d '{"name": "azeite"}'

# -------------------------------------------------------------- [TEST GET COMPLETE SHOPPING LIST]
curl -X GET http://127.0.0.1:5000/pantry/shopping-list


# -------------------------------------------------------------- [TEST SEND EMAIL]
curl -X POST http://127.0.0.1:5000/send-email \
-H "Content-Type: application/json" \
-d '{
    "from_addr": "kitchen_assistant@outlook.com",
    "to_addr": "inesaguia@ua.pt",
    "subject": "Aviso de Produtos Próximos da Data de Expiração",
    "body": <html><body style=\"font-family: Arial, sans-serif; line-height: 1.6; color: #333;\">
            <h1>Alerta de Produtos!</h1>
            <p>Caro cliente, queremos informar que os seguintes produtos estão próximos da sua data de expiração:</p>
            <ul><li>Maçãs</li><li>Bananas</li><li>Iogurte</li></ul>
            <p>Por favor, verifique estes produtos e aproveite-os enquanto estão frescos!</p>
        <p>Este email foi enviado automaticamente pelo <strong>Kitchen Assistant</strong>. Não é necessário responder a este email.</p>
        <footer><p>Com os melhores cumprimentos,</p><p><strong>Equipa Kitchen Assistant</strong></p></footer>
        </body></html>,
    "smtp_server": "smtp-mail.outlook.com",
    "smtp_port": 587,
    "password": "kitchen123."
}'

