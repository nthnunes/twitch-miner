# Twitch Miner

O Twitch Miner é uma aplicação desktop desenvolvida em Python para automatizar a coleta de pontos do canal em streams da Twitch e streamelements. Com uma interface gráfica moderna e intuitiva, o aplicativo oferece diversas funcionalidades para melhorar a experiência de coleta de pontos.

## 🚀 Funcionalidades

- **Interface Gráfica Moderna**

  - Tema escuro/claro configurável
  - Design responsivo usando CustomTkinter
  - Execução em segundo plano na bandeja do sistema
  - Painel de controle intuitivo

- **Notificações e Alertas**

  - Notificações na área de trabalho
  - Alertas para menções e respostas nos chats conectados
  - Integração com serviços como Telegram, Discord e Webhook
  - Sistema de notificações personalizável

- **Gerenciamento de Streams**

  - Interface gráfica para edição de streams favoritas
  - Troca de conta Twitch
  - Priorização inteligente de streams
  - Acompanhamento de sequências de visualização

## Build/Compilação

Para compilar o projeto em um executável único, use o seguinte comando:

```bash
pyinstaller -F --collect-all dateutil --collect-all win10toast run.py --onefile --name="TwitchMiner" --icon="icons/tray.png" --noconfirm --noconsole
```

Este comando irá:
- Criar um executável único (`-F --onefile`)
- Incluir todas as dependências do `dateutil` e `win10toast` (`--collect-all`)
- Nomear o arquivo final como "TwitchMiner" (`--name="TwitchMiner"`)
- Não mostrar confirmações (`--noconfirm`)
- Executar sem janela de console (`--noconsole`)

## Utilização

  - Coleta automática de drops e recompensas
  - Gerenciamento de participação em chats
  - Sistema de apostas e previsões
  - Acompanhamento de raids

- **Análise de Dados**

  - Painel de estatísticas via web (localhost)
  - Acompanhamento do histórico de pontos ganhos
  - Análise de desempenho por streamer
  - Relatórios personalizados

- **Segurança e Desempenho**
  - Execução em segundo plano estável
  - Verificação SSL configurável

## 💻 Tecnologias Utilizadas

- **Python 3**: Linguagem principal do projeto
- **CustomTkinter**: Framework para a interface gráfica moderna
- **Pystray**: Gerenciamento de ícone na bandeja do sistema
- **Requests/WebSockets**: Comunicação com a API da Twitch
- **Flask**: Servidor web para o painel de estatísticas
- **Pandas**: Processamento de dados estatísticos
- **PIL/Pillow**: Processamento de imagens
- **Pyinstaller**: Empacotamento da aplicação

## 📦 Instalação

1. Baixe o instalador
2. Execute o arquivo de instalação
3. Siga as instruções do assistente de instalação
4. O aplicativo será instalado e configurado automaticamente
5. Você pode optar por iniciar automaticamente com o Windows

## 🔄 Atualização

O Twitch Miner possui um sistema de atualização automática que notifica o usuário quando novas versões estão disponíveis. As atualizações podem ser instaladas com um único clique.
