# Changelog - TwitchMiner

## [2.1.3] - 2025-11-18

### 🐛 Correções

- **Correção de Duplicação de Streamers nos Slots de Watch**
  - Corrigido bug onde o mesmo streamer poderia preencher ambos os slots de watch simultaneamente
  - Substituição de lista por `set()` para evitar duplicatas automaticamente
  - Adicionada função auxiliar `remaining_watch_amount()` para calcular slots disponíveis de forma mais precisa
  - Melhorias nas verificações de limite para parar o processamento quando os 2 slots estiverem preenchidos
  - Refatoração da lógica de seleção de streamers para garantir que apenas 2 streamers únicos sejam selecionados

- **Atualização de Operações GraphQL**
  - Atualizados os hashes SHA256 das operações `Inventory` e `ViewerDropsDashboard` para versões mais recentes da API da Twitch
  - Migração de `UserByLogin` para `GetIDFromLogin` usando persisted queries (sha256Hash) em vez de queries explícitas
  - Atualização das chamadas em `Twitch.py` e `TwitchLogin.py` para usar a nova operação `GetIDFromLogin`
  - Melhoria na compatibilidade com as mudanças recentes da API GraphQL da Twitch

### 🔧 Melhorias

- **Otimização da Seleção de Streamers**
  - Uso de `set()` em vez de lista para garantir unicidade dos streamers selecionados
  - Verificações mais eficientes com `remaining_watch_amount() <= 0` para evitar processamento desnecessário
  - Código mais limpo e manutenível com constante `max_watch_amount = 2`

- **Atualização da API GraphQL**
  - Migração para persisted queries (sha256Hash) para operações de obtenção de ID de usuário
  - Redução do tamanho das requisições GraphQL usando hashes em vez de queries completas
  - Melhor compatibilidade com as atualizações da API da Twitch


## [2.1.2] - 2025-11-11

### 🐛 Correções

- Correção das chamadas GraphQL que passaram a usar `UserByLogin` em vez do payload `ReportMenuItem`, restabelecendo a obtenção de IDs de usuários.
- Ajuste no fluxo de sincronização de campanhas para tratar respostas inesperadas e limpar o estado após falhas, evitando travamentos.


## [2.1.1] - 2025-10-04

### ✨ Novas Funcionalidades

- **Interface de Configuração de Usuário**
  - Nova janela moderna para configurar username e email
  - Validação de email com regex para garantir formato correto
  - Salvamento automático em `config.json` com estrutura `userData`
  - Compatibilidade mantida com sistema antigo (`username.txt`)

- **Suporte a Ícones de Janela**
  - Ícones personalizados nas janelas principais
  - Uso do arquivo `window.ico` nativo do Windows
  - Aplicado na janela de configuração e painel principal

### 🔧 Melhorias

- **Sistema de Configuração Aprimorado**
  - Fallback automático entre `config.json` e `username.txt`
  - API atualizada para incluir email do usuário no registro
  - Estrutura de dados mais robusta e organizada

- **Interface do Usuário**
  - Janela de configuração desenvolvida com CustomTkinter
  - Tema automático baseado nas preferências salvas
  - Validação em tempo real de campos obrigatórios
  - Mensagens de erro mais claras e específicas

- **Refatorações Técnicas**
  - Atualização do `twitch_viewer` para Playwright síncrono
  - Simplificação da lógica de monitoramento de canais
  - Substituição de ícones remotos por assets locais

### 📝 Documentação

- **Instruções de Build**
  - Comandos PyInstaller atualizados com ícone personalizado
  - Guias de criação de executável standalone
  - Documentação melhorada para desenvolvimento

### 🐛 Correções

- **Correções Menores**
  - Atualização do canal monitorado padrão
  - Melhorias na estabilidade geral do sistema
  - Tratamento de erros aprimorado

### 🏗️ Arquitetura

- **Estrutura de Dados**
  - Migração para `config.json` como fonte principal de configuração
  - Manutenção de compatibilidade com sistema legado
  - Validação robusta de dados do usuário
  - Sistema de fallback inteligente
