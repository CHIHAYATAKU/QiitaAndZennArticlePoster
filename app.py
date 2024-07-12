import os
import webbrowser
import threading
import tkinter as tk
from tkinter import Tk, Label, Entry, Text, Button, END, Frame, filedialog
import requests
from urllib.parse import urlencode
from config.config import REPO_PATH
from modules.HandLingGit import git_add, git_commit, git_push


class PostingArticlesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Article Poster")
        self.root.geometry("700x600")

        # メニューバーを作成
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar, borderwidth=2, relief="groove", pady=50)

        # ファイルメニュー
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_article)
        file_menu.add_command(label="Save", command=self.save_article)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        self.title_label = Label(root, text="Title:")
        self.title_label.pack()
        self.title_input = Entry(root, width=70)
        self.title_input.pack()

        self.frame_body = Frame(root, width=70, height=80)
        self.frame_body.pack(fill=tk.Y, expand=False)
        self.body_label = Label(self.frame_body, text="Body:")
        self.body_label.pack()

        # ツールバーにボタンを追加
        self.bold_button = Button(self.frame_body, text="h1", command=self.insert_h1)
        self.bold_button.pack(side=tk.LEFT)
        self.italic_button = Button(
            self.frame_body, text="Italic", command=self.make_italic
        )
        self.italic_button.pack(side=tk.LEFT)

        self.frame = Frame(root, width=70, height=80)
        self.frame.pack(fill=tk.Y, expand=False)

        self.body_input = Text(self.frame, wrap=tk.WORD)
        self.body_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar_y = tk.Scrollbar(
            self.frame, orient=tk.VERTICAL, command=self.body_input.yview
        )
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.body_input.configure(yscrollcommand=self.scrollbar_y.set)

        self.tags_label = Label(root, text="Tags (comma separated):")
        self.tags_label.pack()
        self.tags_input = Entry(root, width=70)
        self.tags_input.pack()

        self.post_button = Button(root, text="Post Article", command=self.post_article)
        self.post_button.pack()

    def insert_h1(self):
        current_cursor_pos = self.body_input.index(tk.INSERT)
        self.body_input.insert(current_cursor_pos, "##")

    def make_italic(self):
        current_tags = self.body_input.tag_names("sel.first")
        if "italic" not in current_tags:
            self.body_input.tag_add("italic", "sel.first", "sel.last")
            self.body_input.tag_configure("italic", font=("Arial", 12, "italic"))
        else:
            self.body_input.tag_remove("italic", "sel.first", "sel.last")

    def new_article(self):
        # 新しい記事を作成する処理
        self.title_input.delete(0, END)
        self.body_input.delete("1.0", END)
        self.tags_input.delete(0, END)

    def save_article(self):
        title = self.title_input.get()
        body = self.body_input.get("1.0", END)
        tags = self.tags_input.get()

        # ファイルダイアログを表示して保存場所を選択
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"{title}.txt",
            title="Save Article",
        )

        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(f"Title: \n{title}\n\n")
                file.write(f"Body:\n{body}\n\n")
                file.write(f"Tags: \n{tags}\n")

            print(f"Article saved to {file_path}")

    def post_article(self):
        # 記事を投稿する処理
        title = self.title_input.get()
        body = self.body_input.get("1.0", END)
        tags = self.tags_input.get().split(",")
        # 投稿する処理を追加することができます
        # 使用例
        repo_path = REPO_PATH
        try:
            git_add(cwd=repo_path)
            git_commit("add: articles", cwd=repo_path)
            print("ローカルでのGit操作が成功しました")
        except Exception as e:
            print(f"Git操作に失敗しました: {e}")
        try:
            git_push(cwd=repo_path)
            print("リモートリポジトリへのpush操作が成功しました")
        except Exception as e:
            print(f"リモートリポジトリへのpush操作に失敗しました: {e}")
        print(f"Title: {title}")
        print(f"Body: {body}")
        print(f"Tags: {tags}")


if __name__ == "__main__":
    root = Tk()
    app = PostingArticlesApp(root)
    root.mainloop()
