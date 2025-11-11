# Changelog - TwitchMiner

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
