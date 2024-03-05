# Instruções de Execução

Este documento descreve os passos necessários para executar os componentes do sistema.

## Primeiro Passo: Correr o FusionEngine

O FusionEngine é um bloco que permite adicionar diferentes módulos.

```bash
cd FusionEngine
java -jar FusionEngine.jar
```

## Segundo Passo: Correr o IM (Interaction Manager)

```bash
cd mmiframeworkV2
java -jar mmiframeworkV2.jar
```

## Terceiro Passo: Correr o Rasa

O Rasa usa para dar reconhecer as entidades e intents.

1. Ativar o ambiente virtual do Rasa:

```bash
conda activate /usr/local/Caskroom/miniconda/base/envs/rasa-env
```

2. Correr o Rasa:

```bash
rasa run --enable-api --cors="*"
```

## Quarto Passo: client-side 

```bash
cd WebAppAssistantV2/APP2
python app.py
```

## Quinto Passo: Correr a APP

```bash
cd WebAppAssistantV2
http-server -p 8082 -S -C cert.pem -K key.pem
```
