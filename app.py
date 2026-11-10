"""Interface gráfica para baixar e converter áudio em MP3 com yt-dlp + FFmpeg.

Requer Python 3.10+ com Tkinter, e yt-dlp.exe, ffmpeg.exe e ffprobe.exe
na mesma pasta deste arquivo (ou na subpasta bin, ou disponíveis no PATH).
"""

from __future__ import annotations

import os
import queue
import re
import shutil
import subprocess
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from urllib.parse import urlsplit


BASE_DIR = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
PROGRESS_RE = re.compile(r"\[download\]\s+(\d+(?:\.\d+)?)%")


def encontrar_executavel(nome_windows: str, nome_path: str) -> Path | None:
    """Prioriza os binários locais. Usa PATH como alternativa."""
    for candidato in (BASE_DIR / nome_windows, BASE_DIR / "bin" / nome_windows):
        if candidato.is_file():
            return candidato
    encontrado = shutil.which(nome_windows) or shutil.which(nome_path)
    return Path(encontrado).resolve() if encontrado else None


def pasta_padrao() -> Path:
    for nome in ("Music", "Downloads"):
        p = Path.home() / nome
        if p.is_dir():
            return p
    return Path.home()


class ConversorMP3(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Conversor MP3 | yt-dlp | by Davi Mafra")
        self.geometry("730x510")
        self.minsize(650, 550)
        self.configure(bg="#f5f7fb")

        self.url_var = tk.StringVar()
        self.pasta_var = tk.StringVar(value=str(pasta_padrao()))
        self.status_var = tk.StringVar(value="Pronto para converter")
        self.eventos: queue.Queue[tuple[str, object]] = queue.Queue()
        self.processo: subprocess.Popen[str] | None = None
        self.cancelado = False
        self.rodando = False

        estilo = ttk.Style(self)
        if "clam" in estilo.theme_names():
            estilo.theme_use("clam")
        estilo.configure("TFrame", background="#f5f7fb")
        estilo.configure("TLabel", background="#f5f7fb", foreground="#293548", font=("Segoe UI", 10))
        estilo.configure("Titulo.TLabel", font=("Segoe UI Semibold", 21), foreground="#14233f")
        estilo.configure("Subtitulo.TLabel", foreground="#617087")
        estilo.configure("TEntry", padding=8)
        estilo.configure("TButton", padding=(13, 10), font=("Segoe UI", 10))
        estilo.configure("Acao.TButton", background="#1769e0", foreground="#ffffff", font=("Segoe UI Semibold", 10))
        estilo.map("Acao.TButton", background=[("active", "#1154b6"), ("disabled", "#bac9df")])
        estilo.configure("TProgressbar", thickness=14)

        conteudo = ttk.Frame(self, padding=(26, 24))
        conteudo.pack(fill="both", expand=True)

        ttk.Label(conteudo, text="Conversor de áudio MP3", style="Titulo.TLabel").pack(anchor="w")
        ttk.Label(conteudo, text="Cole um link, escolha a pasta e converta com yt-dlp + FFmpeg.", style="Subtitulo.TLabel").pack(anchor="w", pady=(3, 24))

        ttk.Label(conteudo, text="Link do vídeo").pack(anchor="w", pady=(0, 6))
        self.url_entry = ttk.Entry(conteudo, textvariable=self.url_var)
        self.url_entry.pack(fill="x")
        self.url_entry.focus_set()

        ttk.Label(conteudo, text="Salvar em").pack(anchor="w", pady=(17, 6))
        linha_pasta = ttk.Frame(conteudo)
        linha_pasta.pack(fill="x")
        self.pasta_entry = ttk.Entry(linha_pasta, textvariable=self.pasta_var)
        self.pasta_entry.pack(side="left", fill="x", expand=True)
        self.escolher_btn = ttk.Button(linha_pasta, text="Escolher pasta", command=self.escolher_pasta)
        self.escolher_btn.pack(side="left", padx=(8, 0))

        linha_acoes = ttk.Frame(conteudo)
        linha_acoes.pack(fill="x", pady=(20, 14))
        self.converter_btn = ttk.Button(linha_acoes, text="Converter para MP3", style="Acao.TButton", command=self.iniciar)
        self.converter_btn.pack(side="left")
        self.cancelar_btn = ttk.Button(linha_acoes, text="Cancelar", command=self.cancelar, state="disabled")
        self.cancelar_btn.pack(side="left", padx=(8, 0))
        ttk.Button(linha_acoes, text="Abrir pasta", command=self.abrir_pasta).pack(side="right")

        ttk.Label(conteudo, textvariable=self.status_var).pack(anchor="w", pady=(1, 8))
        self.barra = ttk.Progressbar(conteudo, maximum=100, mode="determinate")
        self.barra.pack(fill="x")

        ttk.Label(conteudo, text="Detalhes", style="Subtitulo.TLabel").pack(anchor="w", pady=(18, 7))
        area_log = ttk.Frame(conteudo)
        area_log.pack(fill="both", expand=True)
        self.log = tk.Text(area_log, height=6, wrap="word", state="disabled", bg="#ffffff", fg="#344054", font=("Consolas", 9), relief="flat", padx=10, pady=8)
        barra_rolagem = ttk.Scrollbar(area_log, command=self.log.yview)
        self.log.configure(yscrollcommand=barra_rolagem.set)
        self.log.pack(side="left", fill="both", expand=True)
        barra_rolagem.pack(side="right", fill="y")

        self.bind("<Return>", lambda _evt: self.iniciar() if not self.rodando else None)
        self.protocol("WM_DELETE_WINDOW", self.fechar)
        self.after(100, self.ler_eventos)

    def registrar(self, mensagem: str) -> None:
        self.log.configure(state="normal")
        self.log.insert("end", mensagem.rstrip("\r\n") + "\n")
        if int(self.log.index("end-1c").split(".")[0]) > 450:
            self.log.delete("1.0", "100.0")
        self.log.see("end")
        self.log.configure(state="disabled")

    def escolher_pasta(self) -> None:
        pasta = filedialog.askdirectory(initialdir=self.pasta_var.get() or str(Path.home()))
        if pasta:
            self.pasta_var.set(pasta)

    def abrir_pasta(self) -> None:
        pasta = Path(self.pasta_var.get()).expanduser()
        if not pasta.is_dir():
            messagebox.showwarning("Pasta inválida", "A pasta de destino ainda não existe.")
            return
        try:
            if sys.platform == "win32":
                os.startfile(str(pasta))  # type: ignore[attr-defined]
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(pasta)])
            else:
                subprocess.Popen(["xdg-open", str(pasta)])
        except OSError as exc:
            messagebox.showerror("Erro", f"Não foi possível abrir a pasta:\n{exc}")

    def iniciar(self) -> None:
        if self.rodando:
            return
        url = self.url_var.get().strip()
        try:
            partes = urlsplit(url)
        except ValueError:
            partes = None
        if partes is None or partes.scheme not in ("http", "https") or not partes.netloc or any(c.isspace() for c in url):
            messagebox.showwarning("Link inválido", "Cole uma URL completa começando com https://")
            return

        pasta = Path(self.pasta_var.get().strip()).expanduser()
        try:
            pasta.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            messagebox.showerror("Pasta inválida", f"Não foi possível acessar a pasta:\n{exc}")
            return

        ytdlp = encontrar_executavel("yt-dlp.exe", "yt-dlp")
        ffmpeg = encontrar_executavel("ffmpeg.exe", "ffmpeg")
        ffprobe = encontrar_executavel("ffprobe.exe", "ffprobe")
        faltando = [nome for nome, executavel in (("yt-dlp.exe", ytdlp), ("ffmpeg.exe", ffmpeg), ("ffprobe.exe", ffprobe)) if executavel is None]
        if faltando:
            messagebox.showerror(
                "Programa ausente",
                "Não encontrei: " + ", ".join(faltando) + "\n\n" +
                "Coloque esses executáveis na mesma pasta do app (ou na subpasta bin), " +
                "ou adicione-os ao PATH do Windows. Consulte o LEIA-ME.txt."
            )
            return
        assert ytdlp is not None and ffmpeg is not None and ffprobe is not None

        # ffmpeg e ffprobe podem estar em diretórios distintos quando encontrados no PATH;
        # nesse caso, o próprio PATH é utilizado, sem forçar --ffmpeg-location.
        comando = [
            str(ytdlp), "--no-playlist", "--windows-filenames", "--newline",
            "-f", "bestaudio/best", "-x", "--audio-format", "mp3", "--audio-quality", "0",
            "--paths", str(pasta), "-o", "%(title).180B [%(id)s].%(ext)s", url,
        ]
        if ffmpeg.parent == ffprobe.parent:
            comando[1:1] = ["--ffmpeg-location", str(ffmpeg.parent)]

        self.rodando = True
        self.cancelado = False
        self.processo = None
        self.barra["value"] = 0
        self.status_var.set("Iniciando download...")
        self.converter_btn.configure(state="disabled")
        self.cancelar_btn.configure(state="normal")
        self.escolher_btn.configure(state="disabled")
        self.pasta_entry.configure(state="disabled")
        self.registrar("Iniciando: " + url)
        threading.Thread(target=self.trabalhar, args=(comando,), daemon=True).start()

    def trabalhar(self, comando: list[str]) -> None:
        try:
            configuracao = {"stdout": subprocess.PIPE, "stderr": subprocess.STDOUT,
                           "text": True, "encoding": "utf-8", "errors": "replace", "bufsize": 1}
            if sys.platform == "win32":
                configuracao["creationflags"] = subprocess.CREATE_NO_WINDOW
            processo = subprocess.Popen(comando, **configuracao)
            self.processo = processo
            if self.cancelado and processo.poll() is None:
                processo.terminate()
            assert processo.stdout is not None
            for linha in processo.stdout:
                self.eventos.put(("log", linha))
            codigo = processo.wait()
            self.eventos.put(("fim", codigo))
        except Exception as exc:
            self.eventos.put(("erro", str(exc)))

    def ler_eventos(self) -> None:
        try:
            while True:
                tipo, valor = self.eventos.get_nowait()
                if tipo == "log":
                    linha = str(valor).strip()
                    if not linha:
                        continue
                    self.registrar(linha)
                    progresso = PROGRESS_RE.search(linha)
                    if progresso:
                        percentual = float(progresso.group(1))
                        self.barra["value"] = percentual
                        self.status_var.set(f"Baixando áudio: {percentual:.1f}%")
                    elif "[ExtractAudio]" in linha:
                        self.status_var.set("Convertendo para MP3...")
                elif tipo == "fim":
                    if self.cancelado:
                        self.status_var.set("Operação cancelada")
                        self.registrar("Operação cancelada pelo usuário.")
                    elif valor == 0:
                        self.barra["value"] = 100
                        self.status_var.set("MP3 salvo com sucesso!")
                        self.registrar("Concluído. Clique em 'Abrir pasta' para ver o arquivo.")
                    else:
                        self.status_var.set("Falha na conversão. Consulte os detalhes.")
                        self.registrar(f"O yt-dlp terminou com código de erro {valor}.")
                    self.finalizar()
                elif tipo == "erro":
                    self.status_var.set("Não foi possível executar o programa")
                    self.registrar("Erro: " + str(valor))
                    self.finalizar()
        except queue.Empty:
            pass
        if self.winfo_exists():
            self.after(100, self.ler_eventos)

    def finalizar(self) -> None:
        self.rodando = False
        self.processo = None
        self.converter_btn.configure(state="normal")
        self.cancelar_btn.configure(state="disabled")
        self.escolher_btn.configure(state="normal")
        self.pasta_entry.configure(state="normal")

    def cancelar(self) -> None:
        if not self.rodando:
            return
        self.cancelado = True
        self.status_var.set("Cancelando...")
        processo = self.processo
        if processo is not None and processo.poll() is None:
            try:
                processo.terminate()
            except OSError as exc:
                self.registrar("Não foi possível interromper: " + str(exc))

    def fechar(self) -> None:
        if self.rodando:
            if not messagebox.askyesno("Sair", "Há uma conversão em andamento. Cancelar e sair?"):
                return
            self.cancelar()
        self.destroy()


if __name__ == "__main__":
    ConversorMP3().mainloop()
