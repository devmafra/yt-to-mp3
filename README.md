# Conversor MP3

Aplicativo com interface gráfica para Windows que baixa o áudio de vídeos e o converte para MP3 usando [yt-dlp](https://github.com/yt-dlp/yt-dlp) e [FFmpeg](https://ffmpeg.org/).

Cole o link, escolha a pasta de destino e acompanhe o progresso. Não é necessário instalar Python para usar o executável.

## Download

**[Baixar ConversorMP3.exe (Windows)](https://github.com/devmafra/yt-to-mp3/releases/latest/download/ConversorMP3.exe)**

Versão publicada: **v1.0.0** | [Ver todas as versões](https://github.com/devmafra/yt-to-mp3/releases)

> O aplicativo não inclui o yt-dlp nem o FFmpeg. É necessário baixá-los separadamente, conforme os passos abaixo.

## Instalação no Windows

### 1. Baixe o aplicativo

Baixe o `ConversorMP3.exe` pelo link acima e coloque-o em uma pasta chamada `ConversorMP3`.

### 2. Baixe o yt-dlp

- [Download oficial do yt-dlp.exe](https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe)
- Coloque `yt-dlp.exe` na mesma pasta de `ConversorMP3.exe`.

### 3. Baixe o FFmpeg

- [Download do FFmpeg LGPL estático para Windows 64 bits](https://github.com/FFmpeg-Builds/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-lgpl.zip)
- Extraia o ZIP e localize a pasta `bin`.
- Crie uma pasta `bin` dentro de `ConversorMP3` e copie para ela os arquivos `ffmpeg.exe` e `ffprobe.exe` do pacote extraído.

A organização final será:

```text
ConversorMP3/
├── ConversorMP3.exe
├── yt-dlp.exe
└── bin/
    ├── ffmpeg.exe
    └── ffprobe.exe
```

**Nota:** o link acima é para a build *estática* LGPL. Se optar por uma build *shared*, mantenha também as DLLs necessárias, normalmente copiando toda a pasta `bin`.

### 4. Converta um vídeo

1. Abra `ConversorMP3.exe`.
2. Cole a URL do vídeo.
3. Escolha onde salvar o arquivo.
4. Clique em **Converter para MP3**.
5. Aguarde o download e a conversão. O MP3 será salvo na pasta escolhida.

## Executar pelo código-fonte

Requisitos: [Python 3.10+](https://www.python.org/downloads/) com Tkinter, além do yt-dlp e FFmpeg nas pastas indicadas acima.

Clone o repositório (ou baixe seu código-fonte) e execute `abrir.bat` ou:

```powershell
python app.py
```

### Gerar um executável

No Windows, execute:

```powershell
.\gerar-exe.bat
```

O script instala o PyInstaller e gera `dist/ConversorMP3.exe`. Para usar esse novo executável, mantenha o yt-dlp e o FFmpeg ao lado dele ou na subpasta `bin`, conforme a estrutura de instalação.

## Dúvidas frequentes

**O aplicativo diz que não encontrou o yt-dlp ou o FFmpeg.** Confira os nomes dos arquivos e as pastas do exemplo acima. Não é necessário colocar os executáveis no `PATH` se estiverem nesses locais.

**A conversão falhou.** Verifique a mensagem na área **Detalhes**. Alguns sites podem alterar seus formatos ou exigir versões mais recentes do yt-dlp e outras dependências.

**O MP3 terá a mesma qualidade do áudio original?** A opção `--audio-quality 0` solicita alta qualidade VBR na conversão. Converter para MP3 não melhora a qualidade da fonte e pode introduzir perdas.

## Limitações

- Processa um vídeo por vez; playlists não são baixadas integralmente.
- Arquivos parciais podem permanecer na pasta de destino após um cancelamento.
- A disponibilidade de vídeos depende dos sites e do suporte oferecido pelo yt-dlp.
- Baixe apenas conteúdos para os quais você tenha autorização.

## Tecnologias e créditos

- **Python e Tkinter:** interface gráfica.
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp):** download de mídia.
- **[FFmpeg](https://ffmpeg.org/):** conversão de áudio.
- **[FFmpeg-Builds](https://github.com/FFmpeg-Builds/FFmpeg-Builds):** disponibilização da build LGPL indicada acima.
- **PyInstaller:** geração do executável Windows.

**Desenvolvido por Davi Mafra**, desenvolvedor Full Stack e estudante de Engenharia de Software.

Este é um projeto independente, sem vínculo oficial com yt-dlp, FFmpeg ou seus mantenedores. As dependências são obtidas separadamente e possuem licenças próprias. Este repositório não apresenta, no momento, uma licença de reutilização para o código do aplicativo.
