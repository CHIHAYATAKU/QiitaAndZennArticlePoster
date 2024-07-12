import os
import webbrowser
import threading
from datetime import date
import tkinter as tk
from tkinter import Tk, Label, Entry, Text, Button, END, Frame, filedialog
import requests
from urllib.parse import urlencode
from modules.HandLingGit import (
    git_add,
    git_commit,
    git_push,
    git_switch,
    git_new_switch,
    git_switch_main,
)


class PostingArticlesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Article Poster")
        self.root.geometry("700x600")

        self.repo_path = os.getenv("REPO_PATH", "")

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
        self.h2_button = Button(self.frame_body, text="章", command=self.insert_h2)
        self.h2_button.pack(side=tk.LEFT)
        self.h3_button = Button(self.frame_body, text="節", command=self.insert_h3)
        self.h3_button.pack(side=tk.LEFT)
        self.h4_button = Button(self.frame_body, text="項", command=self.insert_h4)
        self.h4_button.pack(side=tk.LEFT)

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

        self.post_button = Button(
            root,
            text="Post Article",
            command=self.post_article,
        )
        self.post_button.pack()

    def insert_h2(self):
        current_cursor_pos = self.body_input.index(tk.INSERT)
        self.body_input.insert(current_cursor_pos, "## ")

    def insert_h3(self):
        current_cursor_pos = self.body_input.index(tk.INSERT)
        self.body_input.insert(current_cursor_pos, "### ")

    def insert_h4(self):
        current_cursor_pos = self.body_input.index(tk.INSERT)
        self.body_input.insert(current_cursor_pos, "#### ")

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
        if git_switch(cwd=self.repo_path, branch="qiita") != False:
            print("qiitaへのブランチ切り替えが成功しました\n")
        else:
            git_new_switch(cwd=self.repo_path, branch="qiita")
            print("qiitaブランチを作成しました\n")

        # フォルダを指定
        folder_path_qiita = os.path.join(self.repo_path, "Qiita")
        os.makedirs(folder_path_qiita, exist_ok=True)

        # ファイル名とパスを作成
        file_name = f"{date.today().isoformat()}.md"
        file_path = os.path.join(folder_path_qiita, file_name)

        # ファイルを保存
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(f"# {title}\n\n")
            file.write(f"{body}\n\n")
            file.write(f"**Tags:** {tags}\n")

        try:
            git_add(cwd=self.repo_path)
            git_commit("add: articles", cwd=self.repo_path)
            print("ローカルでのGit操作が成功しました\n")
        except Exception as e:
            print(f"qiita:Git操作に失敗しました: {e}\n")
        if git_switch_main(cwd=self.repo_path) != False:
            print("mainへのブランチ切り替えが成功しました\n")
        else:
            git_new_switch(cwd=self.repo_path, branch="main")
            print("mainブランチを作成しました\n")

        print(f"Article saved to {file_path}\n")

        if git_switch(cwd=self.repo_path, branch="zenn") != False:
            print("zennへのブランチ切り替えが成功しました\n")
        else:
            git_new_switch(cwd=self.repo_path, branch="zenn")
            print("zennブランチを作成しました\n")

        # フォルダを指定
        folder_path_zenn = os.path.join(self.repo_path, "Zenn")
        os.makedirs(folder_path_zenn, exist_ok=True)

        # ファイル名とパスを作成
        file_name = f"{date.today().isoformat()}.md"
        file_path = os.path.join(folder_path_zenn, file_name)

        # ファイルを保存
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(f"# {title}\n\n")
            file.write(f"{body}\n\n")
            file.write(f"**Tags:** {tags}\n")

        try:
            git_add(cwd=self.repo_path)
            git_commit("add: articles", cwd=self.repo_path)
            print("ローカルでのGit操作が成功しました\n")
        except Exception as e:
            print(f"qiita:Git操作に失敗しました: {e}\n")
        if git_switch_main(cwd=self.repo_path) != False:
            print("mainへのブランチ切り替えが成功しました\n")
        else:
            git_new_switch(cwd=self.repo_path, branch="main")
            print("mainブランチを作成しました\n")
        print(f"Article saved to {file_path}\n")

    def post_article(self):
        self.save_article()
        # 記事を投稿する処理
        title = self.title_input.get()
        body = self.body_input.get("1.0", END)
        tags = self.tags_input.get().split(",")

        git_switch(cwd=self.repo_path, branch="qiita")
        try:
            git_push(cwd=self.repo_path, branch="qiita")
            print("リモートリポジトリへのpush操作が成功しました\n")
        except Exception as e:
            print(f"リモートリポジトリへのpush操作に失敗しました: {e}\n")
        print(f"Title: {title}")
        print(f"Body: {body}")
        print(f"Tags: {tags}")
        if git_switch_main(cwd=self.repo_path) != False:
            print("mainへのブランチ切り替えが成功しました\n")
        else:
            git_new_switch(cwd=self.repo_path, branch="main")
            print("mainブランチを作成しました\n")

        git_switch(cwd=self.repo_path, branch="zenn")
        try:
            git_push(cwd=self.repo_path, branch="zenn")
            print("リモートリポジトリへのpush操作が成功しました\n")
        except Exception as e:
            print(f"リモートリポジトリへのpush操作に失敗しました: {e}\n")
        print(f"Title: {title}")
        print(f"Body: {body}")
        print(f"Tags: {tags}")
        if git_switch_main(cwd=self.repo_path) != False:
            print("mainへのブランチ切り替えが成功しました\n")
        else:
            git_new_switch(cwd=self.repo_path, branch="main")
            print("mainブランチを作成しました\n")


if __name__ == "__main__":
    root = Tk()
    app = PostingArticlesApp(root)
    root.mainloop()
