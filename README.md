# Jaiminho

Um Postman que evita a fadiga

## Requisições

Se localizam na pasta ~/.config/jaiminho. O path a partir dessa pasta define o nome da requisição.
As requisições ficam em arquivos no formato yaml e devem ter esta extensão, `.yml` não irá funcionar.
Qualquer entrada nessa estrutura pode ser usada como variável em uma string.

Após substituir as variáveis nas strings as entradas dentro de `requests` serão passadas para o método `requests.request` no formato chave=valor

