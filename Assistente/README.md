# Instruções de Execução

Este documento descreve os passos necessários para executar os componentes do sistema.

## Prerequisites

Antes de correr o projeto :

| Dependencias  | macOS                   | Windows                                               |
|-------------|---------------------------|-------------------------------------------------------|
| Java v.21      | [Java's Website](https://learn.microsoft.com/en-us/java/openjdk/download) | [Java's Website](https://learn.microsoft.com/en-us/java/openjdk/download) |
| NodeJs         | [nodeJS's Website](https://nodejs.org/en)                            | [nodeJS's Website](https://nodejs.org/en)                        |
|   └────────────| `npm install -g http-server`                                         | `npm install -g http-server`                                     |
| Miniconda      | [Miniconda's Website](https://docs.conda.io/projects/miniconda/en/latest/) | [Miniconda's Website](https://docs.conda.io/projects/miniconda/en/latest/) |
|   └────────────| `conda create --name /usr/local/Caskroom/miniconda/base/envs/rasa-env python=3.10` | `conda create --name rasa-env python=3.10`                       |
|   └────────────| `conda activate /usr/local/Caskroom/miniconda/base/envs/rasa-env`    | `conda activate rasa-env`                                        |
|   └────────────| `conda install rasa`                                                  | `pip install rasa`                                               |
| Doxygen        | `brew install doxygen`                                                | [Doxygen's Website](https://www.doxygen.nl/index.html)           |
| Flask          | `pip install Flask`                                                   | `pip install Flask`                                               |
| requests       | `pip install requests`                                                | `pip install requests`                                            |
| OpenCV (cv2)   | `pip install opencv-python`                                           | `pip install opencv-python`                                      |
| pyzbar         | `pip install pyzbar`                                                  | `pip install pyzbar`                                             |
| numpy          | `pip install numpy`                                                   | `pip install numpy`                                               |
| email_validator| `pip install email-validator`                                         | `pip install email-validator`                                     |
| spacy          | `pip install spacy`                                                   | `pip install spacy`                                               |
|   └────────────| `python -m spacy download pt_core_news_sm`                           | `python -m spacy download pt_core_news_sm`                       |
| mysql.connector| `pip install mysql-connector-python`                                  | `pip install mysql-connector-python`                             |


## Execução do Assisteste:

### 1º Passo: 

Correr o FusionEngine

```bash
KitchenAssistant/
│
└── Assistente/
  └── FusionEngine/
    └── '1º : Correr o FusionEngine'
      └── java -jar FusionEngine.jar
```

### 2º Passo: 

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

### 3º Passo: 

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

### 4º Passo: 

Correr o client-side 

```bash
KitchenAssistant/
│   
└── WebAppAssistantV2/
  └── APP2/
    └── '4º : Correr o servidor de todos os endpoints'
      └── python app.py
```

### 5º Passo: 

Correr a APP

```bash
KitchenAssistant/
│   
└── WebAppAssistantV2/
  └── '5º : Correr o Assistente' 
    └── http-server -p 8082 -S -C cert.pem -K key.pem
```

### 6º Passo: 

Abrir Uma janela do Chrome para correr o IM         

```bash
KitchenAssistant/
│  
└── WebAppAssistantV2/
  └── '6º : Abrir o IM'
    └── https://127.0.0.1:8082/index.htm
```

### 7º Passo: 

Abrir Uma janela do Chrome para correr o Assistente 

```bash
KitchenAssistant/
│   
└── WebAppAssistantV2/
  └── '7º : Abrir o Assistente'
    └── https://127.0.0.1:8082/appGui.htm
```