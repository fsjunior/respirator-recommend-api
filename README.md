# respirator-recommend-api

![python 3.9](https://img.shields.io/badge/python-3.9-blue)
[![build](https://img.shields.io/github/workflow/status/fsjunior/respirator-recommend-api/build)](https://github.com/fsjunior/respirator-recommend-api/actions?query=workflow%3Abuild)
[![Codecov](https://img.shields.io/codecov/c/gh/fsjunior/respirator-recommend-api)](https://codecov.io/gh/fsjunior/python-flask-restful-mongodb-template)
[![maintainability](https://img.shields.io/codeclimate/maintainability/fsjunior/respirator-recommend-api)](https://codeclimate.com/github/fsjunior/respirator-recommend-api)
[![quality gate](https://img.shields.io/sonar/quality_gate/fsjunior_respirator-recommend-api?server=https%3A%2F%2Fsonarcloud.io)](https://sonarcloud.io/dashboard?id=fsjunior_respirator-recommend-api)
![GitHub last commit](https://img.shields.io/github/last-commit/fsjunior/respirator-recommend-api)

🇺🇸: An API for recommending Brazilian respirators.

🇧🇷: Uma API para recomendação de respiradores (máscaras) brasileiros.

## Motivação

A motivação para criar esta API foi incentivar o uso de máscaras de alta qualidade durante a pandemia. Diferenciar uma máscara eficaz de uma menos eficiente não é simples — é comum vermos pessoas usando máscaras KN95 de origem duvidosa, mesmo com opções mais seguras como as PFF2 disponíveis.

Além disso, muitas máscaras ainda contêm elastano em sua composição, o que pode aumentar a geração de aerossóis pelo usuário, tornando-as menos seguras [[fonte](https://www.businessinsider.com/what-is-best-face-mask-coronavirus-protection-2020-7)].

## O que esta API faz?

Esta API é capaz de analisar o site de um fornecedor de máscaras e extrair informações relevantes, como:

- Tipo da máscara (ex.: PFF2)
- Presença de Certificado de Aprovação (CA) válido
- Composição (ex.: presença de elastano)

Você pode acessá-la diretamente [aqui](https://respirator-recommend-api.chico.codes/doc/swagger). Basta enviar um `POST` para o endpoint `/api/v1/respirator` com o parâmetro `url` apontando para o link do produto.

Exemplo de URL:

https://www.superepi.com.br/mascara-bls-pff2-sem-valvula-bls-tipo-concha-128-b-1835-p1052423


Quer saber mais sobre proteção eficaz contra a COVID-19?  
Leia [este guia](https://chico.codes/blog/guia-prote%C3%A7%C3%A3o-contra-covid-19).

## Recursos

- Baseada no template [python-flask-restful-mongodb-template](https://github.com/fsjunior/python-flask-restful-mongodb-template)
- Detecção de tipos de máscaras usando NER (Named Entity Recognition) com [SpaCy](https://spacy.io/)

## Estrutura do Projeto

A estrutura segue a do template mencionado, com algumas adições:

- `utils/`: Ferramentas auxiliares, como geradores de exemplos para validação do modelo.
- `validation/`: Conjunto de testes voltados à validação do modelo de NER.
- `nlp/`: Contém o modelo treinado utilizado pela API.

⚠️ Nota: A lógica de negócios ainda está um pouco desorganizada e pode apresentar alguns avisos no Code Climate.

## Como funciona a extração de dados?

Com base nas recomendações para proteção contra a COVID-19, a API tem como foco:

- Recomendação de máscaras PFF2 ou PFF3 **sem válvula** e **com CA válido**
- Alerta sobre máscaras que contenham **elastano** ou do tipo **KN95**, que podem ser menos eficazes

### Modelo de NER

Utilizei [SpaCy](https://spacy.io/) para treinar um modelo de NER personalizado, baseado no modelo brasileiro da própria biblioteca.

Como se trata de um caso muito específico, criei manualmente um dataset anotado com as seguintes entidades:

- `CA` (Certificado de Aprovação)
- `CV` (Com Válvula)
- `SV` (Sem Válvula)
- `PFF1`, `PFF2`, `PFF3` (Classes de respiradores)
- `KN95` (Modelo chinês)
- `EL` (Elastano)

Esse modelo está no diretório `nlp/` e é utilizado para extrair informações relevantes dos sites e retornar um JSON estruturado.

### Futuro

Em versões futuras, pretendo incluir um mecanismo para identificar **preços abusivos**, já que há casos de máscaras sendo vendidas por até R$30.

## FAQ

### Por que usar SpaCy/NER em vez de regex?

Modelos estatísticos de NER aprendem as características das entidades com base no contexto, dispensando regras manuais. Por exemplo, nem todo número é um CA, mas um número próximo da palavra "CA" provavelmente é.

### Encontrei um problema. O que fazer?

Sinta-se à vontade para abrir uma *issue* no repositório. Feedbacks e sugestões são sempre bem-vindos!

### A análise não funcionou em alguns sites. Por quê?

A API ainda está em fase experimental. Sites como Americanas ou Shopee, por exemplo, não são suportados no momento.

---

Disponível sob a [Licença MIT](https://github.com/fsjunior/respirator-recommend-api/blob/main/LICENSE).
