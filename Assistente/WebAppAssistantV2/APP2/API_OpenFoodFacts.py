"""
@brief Este módulo contém funções para consultar informações dos produtos 
utilizando o código de barras através da API Open Food Facts de Portugal.

Este módulo permite a obtenção de informações detalhadas de produtos alimentícios, 
como nome, quantidade e imagem, usando seus códigos de barras. 
A interface com a API Open Food Facts facilita a recuperação de 
dados atualizados e relevantes para aplicações focadas em informações nutricionais 
e comerciais de produtos.

@details A função principal deste módulo, `get_product_name`, 
realiza uma requisição HTTP GET para a API Open Food Facts, 
usando o código de barras do produto como input. 
Os resultados são processados para extrair informações essenciais 
que são então retornadas em formato de tuplo.

@note Os erros na requisição são geridos internamente e reportados através de mensagens de erro na consola, 
garantindo que se possa identificar problemas de ( conexão | dados fornecidos) .
"""
import requests

def get_product_name(barcode):
    """
    @brief Obtém o nome, a quantidade e a imagem de um produto a partir do seu código de barras
    usando a API Open Food Facts de Portugal.
    @details Esta função faz uma requisição [GET] à API Open Food Facts de Portugal utilizando o código de barras fornecido.

    @param barcode O código de barras do produto para consulta.
    
    @return Um tuplo com o nome , a quantidade e a URL da imagem 
            Retorna None para cada campo caso o produto não seja encontrado.
    
    @note Se ocorrer uma exceção durante a requisição à API, uma mensagem de erro é impressa
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
