import requests

def get_product_name(barcode):
    """
    Obtém o nome, a quantidade e a imagem de um produto a partir do seu código de barras
    usando a API Open Food Facts de Portugal.

    @param barcode O código de barras do produto para consulta.
    
    @return Um tuplo com o nome , a quantidade e a URL da imagem 
            Retorna None para cada campo caso o produto não seja encontrado.

    @details Esta função faz uma requisição [GET] à API Open Food Facts de Portugal utilizando
             o código de barras fornecido.
    
    @exception Se ocorrer uma exceção durante a requisição à API, uma mensagem de erro é impressa
               indicando o problema encontrado.
    """
    product_name = None
    product_quantity = None
    produtct_image = None
    base_url = "https://pt.openfoodfacts.org/api/v0/product/" # URL base da API de Portugal
    url = f"{base_url}{barcode}.json"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if "product" in data:
            product_info = data["product"]
            product_name = product_info.get("product_name", "Nome do produto não encontrado")
            product_quantity = product_info.get("quantity", "Quantidade do produto não encontrada")
            produtct_image = product_info.get("image_url", "Imagem do produto não encontrada")

            
            print(f"Produto: {product_name}")
            print(f"Quantidade: {product_quantity}")
        else:
            print("Produto não encontrado na base de dados.")
    except requests.RequestException as e:
        print(f"Erro ao fazer a consulta: {e}")
    return product_name, product_quantity, produtct_image



   
