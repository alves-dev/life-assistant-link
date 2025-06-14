<!--
template_name=head
template_version=v1
-->

<h1 align="center">Assistant Link</h1>

<p align="center">
  O projeto é uma API python cujo objetivo é receber eventos via http e replicar os mesmo para o RabbitMQ.<br>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-Finalizado-blue.svg" alt="status">
</p>

<p align="center">
<img src="https://img.shields.io/badge/topics:-grey"> 
<img src="https://img.shields.io/badge/python-lightgrey">
<img src="https://img.shields.io/badge/rabbitmq-lightgrey">
</p>

<hr>



O projeto é uma API python cujo objetivo é receber eventos via http e replicar os mesmo para o RabbitMQ,
com algumas alterações e regras:

Exemplo `POST /api/v1/zone-event`:
```json
{
  "zone": "HOME",
  "person": "joao",
  "action": "enter"
}
```

Esse evento é registrado em memória e enviado para o RabbitMQ, quando um evento do tipo `action = leave` 
é recebido ele calcula o tempo em que a pessoa ficou na `zone` e envia um novo evento para o RabbitMQ.

Exemplos de eventos enviados [aqui](https://github.com/alves-dev/life/tree/main/events#person_tracking-routing_key---person_tracking)

#### Caso de uso
No meu caso essa API é chamada a partir do [Home Assistant](https://www.home-assistant.io/) onde o mesmo monitora minha localização e quando entro
em uma zona monitorada o mesmo dispara a requisição.

-----
### Tecnologias Utilizadas
__[Python](https://www.python.org/):__ É Python, da para fazer de tudo com ela.

__[FastAPI](https://fastapi.tiangolo.com/):__ Framework.

__[RabbitMQ](https://rabbitmq-website.pages.dev/):__ A solução de mensageria para comunicação assíncrona.

__[Testcontainers](https://testcontainers.com/):__ Utilizado para fazer testes de integração.

__[Poetry](https://python-poetry.org/):__ Um ótimo gerenciador de ambientes virtuais.

-----
### Siga esses passos para começar a usar o Assistant Link em sua máquina:

##### Clone o Repositório:
```bash
git clone https://github.com/alves-dev/life-assistant-link.git
cd life-assistant-link
poetry shell # para iniciar o ambiente
poetry install # para instalar as dependências
uvicorn app.main:app # para iniciar a API no ambiente de DEV
```

### Ou acesse [aqui](https://github.com/alves-dev/posts/tree/main/2024/stack-life-python-kotlin) para ver o projeto funcionando juntamente com outros componentes

<!--
template_name=footer
template_version=v1
-->

---
<p align="center">
   <img src="https://img.shields.io/badge/licença-GPL%203-blue.svg" alt="license">
</p>

**Atualizado em:** 2025-06-14 15:18