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

## Recursos

- Baseado no template [python-flask-restful-mongodb-template](https://github.com/fsjunior/python-flask-restful-mongodb-template).
- Fornece detecção de tipos de máscaras por meio de NER (Named Entity Recognition) usando a biblioteca [Spacy](https://spacy.io/).

## FAQ

### Achei um defeito, um problema ou uma sugestão na sua API. O que faço?

Sinta-se a vontade para abrir uma issue e me informar do problema! Toda contribuição é bem-vinda.

### Testei em alguns sites e a análise não funcionou. O que ocorreu?

Essa API ainda está em fase experimental. Ela não funciona em alguns sites como Americanas ou Shopee.

[MIT License](https://github.com/fsjunior/respirator-recommend-api/blob/main/LICENSE).
