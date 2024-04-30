# Instruções de Execução

Este documento descreve os passos necessários para executar os componentes do sistema.

## Prerequisites

Antes de correr o projeto :

| Dependency | macOS Installation           | Windows Installation                           |
|------------|------------------------------|-----------------------------------------------|
| Doxygen    | `brew install doxygen`       | [Doxygen's Website](https://www.doxygen.nl/index.html) |


## Execução do Assisteste:


## 1º Passo: 

Correr o FusionEngine

```bash
KitchenAssistant/
│
└── Assistente/
  └── FusionEngine/
    └── '1º : Correr o FusionEngine'
      └── java -jar FusionEngine.jar
```

## 2º Passo: 

Correr o IM (Interaction Manager)

```bash
KitchenAssistant/
│
└── Assistente/
  │
  └── mmiframeworkV2/
    └── '2º : Correr o IM'
      └── java -jar mmiframeworkV2.jar
```

## 3º Passo: 

Correr o Rasa

```bash
KitchenAssistant/
│
└── Assistente/
  └── '3º : Correr o RASA'
    ├── 3.1 : Ativar o ambiente virtual
    │ ├── MacOS: 
    │ │ └── conda activate /usr/local/Caskroom/miniconda/base/envs/rasa-env
    │ └── Windows: Abrir o terminal 'miniconda'
    │   └── activate rasa-env
    │
    ├── 3.2 : Treinar o modelo de .nlu
    │ ├── MacOS: 
    │ │ └── rasa train
    │ └── Windows: No terminal 'miniconda'
    │   └── rasa train
    │
    └── 3.3 : 
      ├── MacOS: 
      │ └── rasa run --enable-api --cors="*"
      └── Windows: No terminal 'miniconda'
        └── rasa run --enable-api --cors="*"
```

## 4º Passo: 

Correr o client-side 

```bash
KitchenAssistant/
│   
└── WebAppAssistantV2/
  └── APP2/
    └── '4º : Correr o servidor de todos os endpoints'
      └── python app.py
```

## 5º Passo: 

Correr a APP

```bash
KitchenAssistant/
│   
└── WebAppAssistantV2/
  └── '5º : Correr o Assistente' 
    └── http-server -p 8082 -S -C cert.pem -K key.pem
```

## 6º Passo: 

Abrir Uma janela do Chrome para correr o IM         

```bash
KitchenAssistant/
│  
└── WebAppAssistantV2/
  └── '6º : Abrir o IM'
    └── https://127.0.0.1:8082/index.htm
```

## 7º Passo: 

Abrir Uma janela do Chrome para correr o Assistente 

```bash
KitchenAssistant/
│   
└── WebAppAssistantV2/
  └── '7º : Abrir o Assistente'
    └── https://127.0.0.1:8082/appGui.htm
```