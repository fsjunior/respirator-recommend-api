# respirator-recommend-api
![python 3.9](https://img.shields.io/badge/python-3.9-blue)
[![build](https://img.shields.io/github/workflow/status/fsjunior/respirator-recommend-api/build)](https://github.com/fsjunior/respirator-recommend-api/actions?query=workflow%3Abuild)
[![Codecov](https://img.shields.io/codecov/c/gh/fsjunior/respirator-recommend-api)](https://codecov.io/gh/fsjunior/python-flask-restful-mongodb-template)
[![maintainability](https://img.shields.io/codeclimate/maintainability/fsjunior/respirator-recommend-api)](https://codeclimate.com/github/fsjunior/respirator-recommend-api)
[![quality gate](https://img.shields.io/sonar/quality_gate/fsjunior_respirator-recommend-api?server=https%3A%2F%2Fsonarcloud.io)](https://sonarcloud.io/dashboard?id=fsjunior_respirator-recommend-api)
![GitHub last commit](https://img.shields.io/github/last-commit/fsjunior/respirator-recommend-api)

🇺🇸: A respirator recommendation API for Brazillian respirators.

🇧🇷: Uma API de recomendação de respiradores (máscaras) brasileiros.  

Minha motivação ao criar essa API foi incentivar o uso de máscaras de qualidade durante esse
momento de pandemia. Saber diferenciar uma máscara de qualidade e um com menos qualidade não
é uma tarefa exatamente simples: é muito comum vermos pessoas utilizando máscaras duvidosas 
KN95 mesmo com máscaras PFF2 (que são mais seguras) disponíveis. 

Muitos ainda utilizam máscaras com elastano em sua composição, o que pode aumentar [mais perigoso](https://www.businessinsider.com/what-is-best-face-mask-coronavirus-protection-2020-7) 
a geração de aerossóis pelo usuário.

A ideia dessa API é que ela seja capaz de analisar um site de um fornecedor de máscaras e extraia
informações relevantes da máscara fornecida, como se ela é do tipo PFF2 (e se tem Certificado de
Aprovação válido), se possue elastano em sua composição etc.

É possível acessar a API diretamente [aqui](https://respirator-recommend-api.chico.codes/doc/swagger). Para isso, 
chame o método `POST` do endpoint `/api/v1/respirator com` o parametro url com a URL de 
um fornecedor de máscaras. Por exemplo: 
`https://www.superepi.com.br/mascara-bls-pff2-sem-valvula-bls-tipo-concha-128-b-1835-p1052423`

Quer saber mais sobre proteção efetiva contra a COVID-19? 
Leia [meu texto sobre o assunto](https://chico.codes/blog/guia-prote%C3%A7%C3%A3o-contra-covid-19).

## Recursos

- Baseado no template [python-flask-restful-mongodb-template](https://github.com/fsjunior/python-flask-restful-mongodb-template).
- Fornece detecção de tipos de máscaras por meio de NER (Named Entity Recognition) usando a biblioteca [Spacy](https://spacy.io/).

## Estrutura

A Estrutura do projeto segue a mesma do [template](https://github.com/fsjunior/python-flask-restful-mongodb-template) no 
qual ele foi baseado, com algumas coisas adicionadas:

- Há um diretório `utils` com utilitários úteis para o projeto (que no caso é apenas uma ferramenta)
para geração de exemplos de validação para o modelo de NLP.
- O diretório `validation` possui alguns testes com intuito de validar o **modelo** para extração
das entidades.
- O diretório `nlp` possui o modelo criado e utilizado pela API.

Nota: o código da aplicação ainda está um pouco desorganizado, principalmente na parte da lógica de negócios 
(inclusive com alguns avisos no code climate). 
  
## Como funciona a extração de dados?

A ideia desse projeto, pelo que se sabe de [proteção efetiva contra a COVID-19](https://chico.codes/blog/guia-prote%C3%A7%C3%A3o-contra-covid-19),
é recomendar máscaras do tipo PFF2 e PFF3 sem válvula e com CA válido. Ao mesmo tempo, alertar o 
usuário quando essas informações não são encontradas no site ou quando ele utiliza máscaras que 
possuem [elastano](https://www.businessinsider.com/what-is-best-face-mask-coronavirus-protection-2020-7) 
ou são do tipo KN95.

Em um segundo momento (ainda não funcional), o objetivo é alertar para casos de preços abusivos de 
máscaras, como tem acontecido de forma bastante frequente (algumas são vendidas por R$30!).

Para extrair esses dados dos sites, eu utilizei [NER](https://en.wikipedia.org/wiki/Named-entity_recognition) 
(Named Entity Recognition) por meio da biblioteca [spacy](https://spacy.io/). 

Para isso, eu treinei um novo modelo baseado no modelo brasileiro que a biblioteca já disponibiliza. 
Como esse é um caso de uso muito particular, precisei gerar o dataset para treiná-lo. 
Para gerar ele, eu extrai informações de sites manualmente e etiquetei essas informações. As 
etiquetas utilizadas foram:
 
- CA (Certificado de Aprovação)
- CV (Com Válvula)
- SV (Sem Válvula)
- PFF1 (Respirador PFF Classe 1)
- PFF2 (Respirador PFF Classe 2)
- PFF3 (Respirador PFF Classe 3)
- KN95 (Respirador padrão chinês)
- EL (Elastano)

O modelo treinado está disponível no diretório `nlp`. A partir desse modelo, a API extrai os dados
dos sites apresentados e retorna em um JSON.


## FAQ

### Por que usar spacy/NER e não regex?

A vantagem de usar um modelo estatísticos para extrair as entidades é que o próprio modelo aprende
as características das entidades, sem necessidade analítica para que eu formasse regras para isso. 
Além disso, os modelos não consideram apenas as palavras que estou procurando e sim também o 
contexto no qual elas estão inseridas (ex: nem todo número é um Certificado de Aprovação, mas um 
número com a palavra "CA" próxima deve ser).  

### Achei um defeito, um problema ou uma sugestão na sua API. O que faço?

Sinta-se a vontade para abrir uma issue e me informar do problema! Toda contribuição é bem-vinda.

### Testei em alguns sites e a análise não funcionou. O que ocorreu?

Essa API ainda está em fase experimental. Ela não funciona em alguns sites como Americanas ou Shopee.

Disponível sob a [MIT License](https://github.com/fsjunior/respirator-recommend-api/blob/main/LICENSE).
