# 🎨 Seminar Art Generator

Uma aplicação web simples para gerar automaticamente imagens de divulgação de seminários (em formato PNG), com base em dados preenchidos pelo usuário.

## 🖼️ Funcionalidades

- Upload de foto do palestrante com máscara circular
- Escolha de cor de destaque do título
- Inserção de informações como data, hora, local, duração, observações, link de transmissão, etc.
- Layout fixo com imagem de fundo aleatória
- Download imediato da arte gerada
- Totalmente offline e executável localmente

## 📦 Requisitos

- Python 3.8+
- Bibliotecas:

```bash
pip install pillow flask
```

Ou instale com o arquivo de dependências:

```bash
pip install -r requirements.txt
```

## 🚀 Como executar

1. Clone este repositório:
   ```bash
   git clone https://github.com/SEU_USUARIO/seminar-art-generator.git
   cd seminar-art-generator
   ```

2. Execute a aplicação:
   ```bash
   python app.py
   ```

3. Acesse no navegador:
   ```
   http://localhost:5000
   ```

## 📁 Estrutura esperada

```
seminar-art-generator/
│
├── app.py
├── Seminar_Art_Generator.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   └── outputs/
├── uploads/
├── backgrounds/
│   ├── fundo1.png
│   └── fundo2.png
├── fonts/
│   ├── Montserrat-Bold.ttf
│   ├── Montserrat-Regular.ttf
│   └── fontawesome-webfont.ttf
```

## ✍️ Exemplo de uso

Preencha os dados do seminário, envie a foto e clique em "Gerar Arte". A imagem será renderizada com layout padronizado e ficará disponível para download.

## 📝 Licença

Distribuído sob a licença MIT.
