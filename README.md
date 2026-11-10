# Conversor MP3

Interface gráfica simples para Windows que permite baixar e converter vídeos em MP3 utilizando [yt-dlp](https://github.com/yt-dlp/yt-dlp) e [FFmpeg](https://ffmpeg.org/).

O aplicativo possui um campo para colar o link do vídeo, seleção da pasta de destino e acompanhamento do progresso do download.

## Como instalar e usar (Windows)

**Não é necessário instalar Python.**

### 1. Baixe o aplicativo

Baixe o arquivo `ConversorMP3.exe`, disponível na pasta `dist` deste repositório.

### 2. Baixe o yt-dlp

Baixe o executável diretamente do projeto oficial:

[Download yt-dlp.exe](https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe)

Coloque o arquivo `yt-dlp.exe` na mesma pasta do `ConversorMP3.exe`.

### 3. Baixe o FFmpeg

Utilize a versão LGPL estática para Windows 64 bits:

[Download FFmpeg LGPL (Windows 64 bits)](https://github.com/FFmpeg-Builds/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-lgpl.zip)

1. Extraia o arquivo ZIP.
2. Abra a pasta extraída e localize a subpasta `bin`.
3. Copie os arquivos `ffmpeg.exe` e `ffprobe.exe`.
4. Crie uma pasta chamada `bin` ao lado do `ConversorMP3.exe`.
5. Cole os dois executáveis dentro dela.

A estrutura final deve ficar assim:

```text
ConversorMP3/
├── ConversorMP3.exe
├── yt-dlp.exe
└── bin/
    ├── ffmpeg.exe
    └── ffprobe.exe
```

**Observação:** essa versão do FFmpeg é estática e normalmente não exige DLLs adicionais. Se utilizar uma versão compartilhada (`shared`), pode ser necessário copiar toda a pasta `bin`.

### 4. Execute o aplicativo

1. Abra `ConversorMP3.exe`.
2. Cole o link do vídeo.
3. Escolha a pasta onde deseja salvar o arquivo.
4. Clique em **Converter para MP3**.
5. Aguarde a conclusão do download e da conversão.

O arquivo MP3 será salvo na pasta selecionada.

## Executar pelo código-fonte

Para executar sem utilizar o binário compilado:

1. Instale [Python 3.10 ou superior](https://www.python.org/downloads/).
2. Baixe o código-fonte deste repositório.
3. Coloque `yt-dlp.exe` e os arquivos do FFmpeg nas pastas indicadas anteriormente.
4. Execute `abrir.bat` ou utilize:

```powershell
python app.py
```

### Gerar o executável

Execute:

```powershell
.\gerar-exe.bat
```

O executável será gerado em:

```text
dist/ConversorMP3.exe
```

## Observações

- O aplicativo converte um vídeo por vez, sem baixar playlists completas.
- A conversão para MP3 utiliza a melhor qualidade VBR configurada no yt-dlp (`--audio-quality 0`).
- A qualidade final depende do áudio original.
- Alguns sites podem exigir atualizações do yt-dlp ou dependências adicionais.
- Baixe apenas conteúdos que você tenha autorização para baixar.

## Tecnologias

- Python e Tkinter: interface gráfica.
- [yt-dlp](https://github.com/yt-dlp/yt-dlp): download de mídia.
- [FFmpeg](https://ffmpeg.org/): conversão de áudio para MP3.
- PyInstaller: geração do executável Windows.

## Desenvolvedor

**Davi Mafra**

Desenvolvedor Full Stack e estudante de Engenharia de Software.

Projeto desenvolvido para simplificar o download e a conversão de vídeos em arquivos MP3 no Windows, por meio de uma interface gráfica acessível.

## Créditos e licenças

O Conversor MP3 foi desenvolvido por **Davi Mafra**, utilizando Python e Tkinter para a interface gráfica.

O aplicativo utiliza as seguintes ferramentas de código aberto:

- [yt-dlp](https://github.com/yt-dlp/yt-dlp): responsável pelo download de mídia.
- [FFmpeg](https://ffmpeg.org/): responsável pela conversão de áudio.
- [FFmpeg-Builds](https://github.com/FFmpeg-Builds/FFmpeg-Builds): fornece a build estática LGPL utilizada no projeto.

Essas ferramentas pertencem aos seus respectivos autores e são distribuídas sob suas próprias licenças.

O Conversor MP3 é um projeto independente e não possui vínculo oficial com os desenvolvedores do yt-dlp ou do FFmpeg.

---

Desenvolvido por **Davi Mafra**.
