# Instruções de Execução

Este documento descreve os passos necessários para executar os componentes do sistema.

## Prerequisites

Antes de correr o projeto :

| Dependency | macOS Installation           | Windows Installation                           |
|------------|------------------------------|-----------------------------------------------|
| Doxygen    | `brew install doxygen`       | [Doxygen's Website](https://www.doxygen.nl/index.html) |


## Execução do Assisteste:

```
KitchenAssistant/
│
├── Assistente/
│ ├── FusionEngine/
│ │ └── [1º] : Correr o FusionEngine
│ │   └── java -jar FusionEngine.jar
| |
│ └── mmiframeworkV2/
│   └── [2º] : Correr o IM
│     └── java -jar mmiframeworkV2.jar
|
├── Assistente/
│ └── [3º] : Correr o RASA
│   ├── 3.1 : Ativar o ambiente virtual
│   | ├── MacOS: 
|   | | └── conda activate /usr/local/Caskroom/miniconda/base/envs/rasa-env
│   | └── Windows: Abrir o terminal 'miniconda'
|   |   └── activate rasa-env
|   |
│   ├── 3.2 : Treinar o modelo de .nlu
│   | ├── MacOS: 
|   | | └── rasa train
│   | └── Windows: No terminal 'miniconda'
|   |   └── rasa train
|   |
│   └── 3.3 : 
│     ├── MacOS: 
|     | └── rasa run --enable-api --cors="*"
│     └── Windows: No terminal 'miniconda'
|       └── rasa run --enable-api --cors="*"
|   
└── WebAppAssistantV2/
  ├── APP2/
  │ └── [4º] : Correr o servidor de todos os endpoints:
  │   └── python app.py
  |
  ├── [5º] : Correr o Assistente 
  | └── http-server -p 8082 -S -C cert.pem -K key.pem
  |
  ├── [6º] : Abrir o IM
  | └── https://127.0.0.1:8082/index.htm
  |
  └── [7º] : Abrir o Assistente
    └── https://127.0.0.1:8082/appGui.htm

```

## Primeiro Passo: Correr o FusionEngine

O FusionEngine é um bloco que permite adicionar diferentes módulos.

```
KitchenAssistant/
│
└── Assistente/
  ├── FusionEngine/
    └── [1º] : Correr o FusionEngine
      └── java -jar FusionEngine.jar
```

## Segundo Passo: Correr o IM (Interaction Manager)

```bash
KitchenAssistant/
│
└── Assistente/
  |
  └── mmiframeworkV2/
    └── [2º] : Correr o IM
      └── java -jar mmiframeworkV2.jar
```

## Terceiro Passo: Correr o Rasa

O Rasa usa para dar reconhecer as entidades e intents.

```bash
KitchenAssistant/
│
└── Assistente/
  └── [3º] : Correr o RASA
    ├── 3.1 : Ativar o ambiente virtual
    | ├── MacOS: 
    | | └── conda activate /usr/local/Caskroom/miniconda/base/envs/rasa-env
    | └── Windows: Abrir o terminal 'miniconda'
    |   └── activate rasa-env
    |
    ├── 3.2 : Treinar o modelo de .nlu
    | ├── MacOS: 
    | | └── rasa train
    | └── Windows: No terminal 'miniconda'
    |   └── rasa train
    |
    └── 3.3 : 
      ├── MacOS: 
      | └── rasa run --enable-api --cors="*"
      └── Windows: No terminal 'miniconda'
        └── rasa run --enable-api --cors="*"
```

## Quarto Passo: client-side 

```bash
KitchenAssistant/
│   
└── WebAppAssistantV2/
  └── APP2/
    └── [4º] : Correr o servidor de todos os endpoints:
      └── python app.py
```

## Quinto Passo: Correr a APP

```bash
KitchenAssistant/
│   
└── WebAppAssistantV2/
  └── [5º] : Correr o Assistente 
    └── http-server -p 8082 -S -C cert.pem -K key.pem
```

## Sexto Passo: Abrir Uma janela do Chrome para correr o IM         

```bash
KitchenAssistant/
│  
└── WebAppAssistantV2/
  └── [6º] : Abrir o IM
    └── https://127.0.0.1:8082/index.htm
```

## Sétimo Passo: Abrir Uma janela do Chrome para correr o Assistente 

```bash
KitchenAssistant/
│   
└── WebAppAssistantV2/
  └── [7º] : Abrir o Assistente
    └── https://127.0.0.1:8082/appGui.htm
```

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
