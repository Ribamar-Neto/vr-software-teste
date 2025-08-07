# Sistema de Notificações com Consumidor RabbitMQ

Este projeto implementa um sistema de notificações com processamento assíncrono usando RabbitMQ, incluindo um consumidor integrado que processa mensagens automaticamente.

## 🚀 Funcionalidades

### Endpoint POST `/notifications`
- **Gera um traceId único** (UUID) para cada requisição
- **Persiste a notificação** em memória com status inicial "RECEIVED"
- **Publica na fila RabbitMQ** `fila.notificacao.entrada.ribamarneto`
- **Retorna HTTP 202 Accepted** com `message_id` e `trace_id`

### Consumidor RabbitMQ Integrado
- **Processa automaticamente** mensagens da fila de entrada
- **Simula falhas aleatórias** (12% de chance)
- **Atualiza status** das notificações em memória
- **Roteia mensagens** para filas apropriadas

## 📋 Fluxo de Processamento

1. **POST /notifications** → Cria notificação e publica na fila de entrada
2. **Consumidor processa** a mensagem da fila de entrada
3. **Se falha (12% chance)**:
   - Atualiza status para `INITIAL_PROCESSING_FAILURE`
   - Envia para fila de retry: `fila.notificacao.retry.ribamarneto`
4. **Se sucesso**:
   - Simula processamento (1-1.5 segundos)
   - Atualiza status para `PROCESSING_INTERMEDIATE`
   - Envia para fila de validação: `fila.notificacao.validacao.ribamarneto`

## 🛠️ Configuração

### Variáveis de Ambiente (.env)
```env
BROKER_USERNAME=guest
BROKER_PASSWORD=guest
BROKER_HOST=localhost
BROKER_PORT=5672
ENVIRONMENT=development
```

### Filas RabbitMQ
- **Entrada**: `fila.notificacao.entrada.ribamarneto`
- **Retry**: `fila.notificacao.retry.ribamarneto`
- **Validação**: `fila.notificacao.validacao.ribamarneto`
- **DLQ**: `fila.notificacao.dlq.ribamarneto`

## 🚀 Como Executar

### 1. Instalar dependências
```bash
uv sync
```

### 2. Configurar RabbitMQ
Certifique-se de que o RabbitMQ está rodando na porta 5672.

### 3. Executar a aplicação
```bash
uv run uvicorn src.main:app --reload
```

### 4. Testar o endpoint
```bash
curl -X POST "http://localhost:8000/notifications" \
  -H "Content-Type: application/json" \
  -d '{
    "message_id": "550e8400-e29b-41d4-a716-446655440000",
    "message_content": "Teste de notificação",
    "notification_type": "email"
  }'
```

### 5. Verificar status
```bash
curl "http://localhost:8000/notifications/status/{trace_id}"
```

## 🧪 Teste do Consumidor

Execute o script de teste para verificar o funcionamento:

```bash
uv run python test_consumer.py
```

## 📊 Monitoramento

### Logs da Aplicação
- ✅ Conexão RabbitMQ estabelecida
- 📝 Mensagens processadas com trace_id
- ⚠️ Falhas simuladas
- 🔄 Mensagens enviadas para filas de destino

### Status das Notificações
- `received`: Notificação recebida
- `initial_processing_failure`: Falha no processamento inicial
- `processing_intermediate`: Processamento intermediário concluído

## 🔧 Estrutura do Projeto

```
src/
├── entities/
│   └── notification.py          # Entidade de notificação
├── enums/
│   ├── notification_status_enum.py
│   └── notification_type_enum.py
├── repositories/
│   └── notification_repository_in_memory.py  # Armazenamento em memória
├── services/
│   └── notification_service_rabbitmq.py      # Serviço RabbitMQ + Consumidor
├── use_cases/
│   ├── create_notification_use_case.py       # Caso de uso de criação
│   └── injection.py                          # Injeção de dependências
├── routers/
│   └── notification_router.py                # Rotas da API
└── main.py                                   # Aplicação principal
```

## 🎯 Características Técnicas

- **Framework**: FastAPI
- **Message Broker**: RabbitMQ (aio-pika)
- **Armazenamento**: Memória (dicionário Python)
- **Processamento**: Assíncrono
- **Rastreamento**: UUID único por notificação
- **Resiliência**: Filas de retry e DLQ
- **Monitoramento**: Logs detalhados

## 🔄 Fluxo Completo

1. **Cliente** → POST /notifications
2. **API** → Cria notificação + publica na fila
3. **Consumidor** → Processa mensagem
4. **Resultado** → Atualiza status + roteia para próxima fila
5. **Cliente** → Consulta status via GET /notifications/status/{trace_id}
