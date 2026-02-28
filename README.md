# 📊 Boston 311 – Data Lake com Azure

## 📌 Contexto

Entre 2015 e 2020, a cidade de Boston registrou um crescimento significativo nas solicitações de serviços não emergenciais realizadas por meio do canal 311.

Cada registro representa uma demanda da população relacionada a problemas urbanos, infraestrutura e serviços públicos. Organizar esses dados de forma estruturada permite análises futuras e suporte a decisões baseadas em dados.

Este projeto tem como objetivo construir a base de um **Data Lake** para ingestão e armazenamento desses dados na nuvem.

---

## 🎯 Objetivo

Implementar um processo de ingestão dos dados históricos (2015–2020) garantindo:

- Download automatizado
- Organização estruturada por ano
- Armazenamento em nuvem
- Estrutura escalável para evolução futura

O foco principal está na **engenharia de dados e organização da camada de armazenamento (RAW)**.

---

## 🗂 Fonte dos Dados

Dados públicos de solicitações 311 da cidade de Boston referentes aos anos:

- 2015
- 2016
- 2017
- 2018
- 2019
- 2020

Arquivos correspondentes:

- `dados_2015`
- `dados_2016`
- `dados_2017`
- `dados_2018`
- `dados_2019`
- `dados_2020`

---

## 🏗 Arquitetura Utilizada

### 🔹 Linguagem
- Python

### 🔹 Serviços Azure
- Azure Blob Storage
- Azure Data Lake Storage (ADLS Gen2)

---

## 🗂 Estrutura do Data Lake
boston-311-datalake/
│
├── raw/
│ ├── 2015/
│ ├── 2016/
│ ├── 2017/
│ ├── 2018/
│ ├── 2019/
│ └── 2020/


### Camada RAW

- Armazena os dados exatamente como recebidos
- Sem transformação
- Organização por ano
- Mantém rastreabilidade da fonte original

---

## 🔄 Fluxo de Ingestão

1. Download dos arquivos públicos
2. Validação básica do arquivo
3. Upload para Azure Blob Storage
4. Organização hierárquica no Data Lake
5. Separação por ano na camada RAW

---

## 📦 Estrutura do Projeto
data/
get_data.py
main.py
save_Azureblob.py
urls.py

## 🧠 Motivação

Projetos de Data Lake exigem organização, padronização e escalabilidade desde a etapa inicial de ingestão.

Este projeto aplica boas práticas de engenharia de dados para evitar a criação de um “data swamp” e preparar a base para futuras análises.


