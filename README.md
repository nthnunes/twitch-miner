# TwitchMiner

Um bot automatizado para ganhar pontos do canal em streams da Twitch.

## Recursos Principais

- Mineração automática de pontos de canais
- Priorização de streamers favoritos
- Controle através de uma interface gráfica moderna
- Execução em segundo plano

## Nova Interface Modernizada

A interface do aplicativo foi atualizada usando CustomTkinter para proporcionar uma experiência visual mais moderna, com:

- Tema escuro (dark mode) por padrão
- Botões e elementos com cantos arredondados
- Esquema de cores baseado na cor oficial da Twitch (#9147ff)
- Design moderno e consistente
- Melhor experiência visual mantendo todas as funcionalidades originais

## Instalação

1. Certifique-se de ter Python 3.7 ou superior instalado
2. Clone o repositório:
```
git clone https://github.com/yourusername/twitch-miner.git
cd twitch-miner
```
3. Instale as dependências:
```
pip install -r requirements.txt
```

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

Execute o aplicativo principal:
```
python run.py
```

### Configuração de Streamer

1. Vá até a aba "Streams"
2. Adicione os streamers que você deseja acompanhar
3. Organize-os por prioridade arrastando e soltando na lista
4. Clique em "Aplicar alterações" após fazer as alterações

### Configuração de Conta

1. Vá até a aba "Conta"
2. Insira o seu nome de usuário da Twitch
3. Clique em "Alterar conta Twitch"

## Planos Disponíveis

### Plano Free
- Mineração automática de pontos
- Mineração executada no seu computador
- Alto uso de CPU
- Necessário manter o PC ligado

### Plano Pro
- Mineração em nuvem 24/7
- Não precisa manter o PC ligado
- Baixo consumo de CPU
- Suporte prioritário
- Relatórios detalhados de ganhos

## Detalhes Técnicos

O aplicativo usa várias tecnologias:
- Python 3.7+
- CustomTkinter para a interface moderna
- Selenium/Requests para interação com a Twitch
- Pystray para suporte a ícone na bandeja do sistema

## Funcionalidades

- Mineração automática de pontos em transmissões ao vivo no Twitch.
- Execução discreta em segundo plano.
- Configuração fácil e rápida.
- Inicia automaticamente com o sistema operacional.

## Requisitos

- Windows 10 ou superior.
- Roda em qualquer torradeira.
- Conta registrada na Twitch.

## Instalação

Siga os passos abaixo para configurar o TwitchMiner no seu PC:

1. **Download do Arquivo**
   - Faça o download do arquivo [`TwitchMiner.zip`](https://github.com/nthnunes/twitch-miner/releases/tag/releases) e extraia-o para a pasta `Documentos` (Sim, tem que ser nessa pasta, caso contrário a inicialização automática não irá funcionar).

   ![Extração em Documentos](./tutorial-images/image1.jpeg)

2. **Extração**
   - Extraia o conteúdo do arquivo zipado. Dentro da pasta extraída, haverá apenas um arquivo principal para rodar o bot.

3. **Execução**
   - Abra o arquivo extraído e siga os passos de configuração que aparecerão na tela.

4. **Configuração Automática**
   - Após configurar o bot, reinicie o computador.

5. **Execução em Segundo Plano**
   - O bot iniciará automaticamente junto com o sistema e minerará pontos em segundo plano.

## Como funciona

O bot é configurado para monitorar as transmissões ao vivo dos canais que forem adicionados e minerar pontos automaticamente. Ele roda silenciosamente em segundo plano e você pode verificá-lo a qualquer momento.

   ![Verificação no Gerenciador de Tarefas](./tutorial-images/image2.png)

## Aviso Legal

Este projeto foi criado apenas para fins educacionais. O uso deste bot em sua conta da Twitch pode violar os Termos de Serviço da plataforma. Use por sua conta e risco :D.
