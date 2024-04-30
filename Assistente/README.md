# Instruções de Execução

Este documento descreve os passos necessários para executar os componentes do sistema.

## Prerequisites

Antes de correr o projeto :

| Dependency | macOS Installation           | Windows Installation                           |
|------------|------------------------------|-----------------------------------------------|
| Doxygen    | `brew install doxygen`       | [Doxygen's Website](https://www.doxygen.nl/index.html) |


## Como usar o Assisteste:

| Steps | Descrição                  | dir               | Mac Commands                       | Win Commands                       |  
|-------|----------------------------|-------------------|------------------------------------|------------------------------------|
| 1 | Correr o FusionEngine      | ../FusionEngine   | `java -jar FusionEngine.jar`        | `java -jar FusionEngine.jar`       |
| 2 | Correr o IM                | ../mmiframeworkV2 | `java -jar mmiframeworkV2.jar`      | `java -jar mmiframeworkV2.jar`     |
| 3 | Correr o RASA              | ../Assistente     | 
| 3.1 | Ativar o ambiente virtual  | ../Assistente     | `conda activate /usr/local/Caskroom/miniconda/base/envs/rasa-env` | `activate rasa-env` |
| 3.2 | Treinar o modelo de nlu    | ../Assistente     | `rasa train` | `rasa train` |
| 3.3 | Correr o RASA | ../Assistente | `rasa run --enable-api --cors="*"` | `rasa run --enable-api --cors="*"` |
| 4 | Correr o Servidor de endpoints | ../WebAppAssistantV2/APP2 | `python app.py` | `python app.py` |
| 5 | Correr o Assistente | ../Assistente/WebAppAssistantV2 | `http-server -p 8082 -S -C cert.pem -K key.pem` | `http-server -p 8082 -S -C cert.pem -K key.pem` |
| 6 | Abrir o IM | GoogleChrome browser | `https://127.0.0.1:8082/index.htm` | `https://127.0.0.1:8082/index.htm` |
| 7 | Abrir o Assistente | GoogleChrome browser | `https://127.0.0.1:8082/appGui.htm` | `https://127.0.0.1:8082/appGui.htm` |

| Steps | Description | Directory | macOS Commands | Windows Commands |
|-------|-------------|-----------|----------------|------------------|
| 1     | Run FusionEngine | ../FusionEngine | `java -jar FusionEngine.jar` | `java -jar FusionEngine.jar` |
| 2     | Run the IM (Interaction Manager) | ../mmiframeworkV2 | `java -jar mmiframeworkV2.jar` | `java -jar mmiframeworkV2.jar` |
| 3     | Run RASA | ../Assistente | | |
| 3.1   | Activate the virtual environment | ../Assistente | `conda activate /usr/local/Caskroom/miniconda/base/envs/rasa-env` | `activate rasa-env` |
| 3.2   | Train the NLU model | ../Assistente | `rasa train` | `rasa train` |
| 3.3   | Run RASA | ../Assistente | `rasa run --enable-api --cors="*"` | `rasa run --enable-api --cors="*"` |
| 4     | Run the server for endpoints | ../WebAppAssistantV2/APP2 | `python app.py` | `python app.py` |
| 5     | Run the Assistant | ../WebAppAssistantV2 | `http-server -p 8082 -S -C cert.pem -K key.pem` | `http-server -p 8082 -S -C cert.pem -K key.pem` |
| 6     | Open the IM in a browser | Google Chrome | `https://127.0.0.1:8082/index.htm` | `https://127.0.0.1:8082/index.htm` |
| 7     | Open the Assistant in a browser | Google Chrome | `https://127.0.0.1:8082/appGui.htm` | `https://127.0.0.1:8082/appGui.htm` |


## Primeiro Passo: Correr o FusionEngine

O FusionEngine é um bloco que permite adicionar diferentes módulos.

```bash
cd KitchenAssistant/Assistente/FusionEngine
java -jar FusionEngine.jar
```

## Segundo Passo: Correr o IM (Interaction Manager)

```bash
cd KitchenAssistant/Assistente/mmiframeworkV2
java -jar mmiframeworkV2.jar
```

## Terceiro Passo: Correr o Rasa

O Rasa usa para dar reconhecer as entidades e intents.

1. Ativar o ambiente virtual do Rasa:
### - macOs:
Correr no terminal normal

```bash
cd KitchenAssistant/Assistente
conda activate /usr/local/Caskroom/miniconda/base/envs/rasa-env
```

### - windows:
Abrir o terminal do AnacondaPrompt Miniconda

```bash
activate rasa-env
```

2. Caso tenham sido feitas alterações no nlu 

```bash
rasa train
``` 

3. Correr o Rasa:

```bash
rasa run --enable-api --cors="*"
```

## Quarto Passo: client-side 

```bash
cd KitchenAssistant/Assistente/WebAppAssistantV2/APP2
python app.py
```

## Quinto Passo: Correr a APP

```bash
cd KitchenAssistant/Assistente/WebAppAssistantV2
http-server -p 8082 -S -C cert.pem -K key.pem
```

## Sexto Passo: Abrir Uma janela do Chrome para correr o IM         

```bash
https://127.0.0.1:8082/index.htm
```

## Sétimo Passo: Abrir Uma janela do Chrome para correr o Assistente 

```bash
https://127.0.0.1:8082/appGui.htm
```
