# Como testar o Assistente

## 1. Abrir o terminal Conda neste diretório

## 2. Ativar o ambiente virtual do Rasa
    activate rasa-env
## macOS
    conda activate /usr/local/Caskroom/miniconda/base/envs/rasa-env

## 3. Repetir os passos 1 e 2 noutro terminal

## 4. Passos a Executar no 1º terminal
    Se pretende treinar o assistente :
        rasa train

    Se pretende testar o assistente(executar depois do passo 5):
     rasa shell
     

## 5. Executar o ficheiro de ações personalizadas no 2º terminal:
    rasa run actions

## 6. Repetir os passos 1 e 2 noutro terminal 

## 7. Executar o seguinte comando no 3ºterminal para executar o asssistente na Web:
    rasa run --enable-api --cors="*"

## 8. Executar a app num outro terminal :
    Caso não tenha instalado o flask:
        condsa install flask
        
    cd Site_Assistente/
    python app.py
    
