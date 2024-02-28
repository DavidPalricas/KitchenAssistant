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

1. Ativar o ambiente virtual do Rasa:

```bash
conda activate /usr/local/Caskroom/miniconda/base/envs/rasa-env
```

2. Correr o Rasa:

```bash
rasa run --enable-api --cors="*"
```

## Quarto Passo: Correr a APP

```bash
cd WebAppAssistantV2
http-server -p 8082 -S -C cert.pem -K key.pem
```
