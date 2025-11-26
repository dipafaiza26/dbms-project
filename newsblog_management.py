import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector
from mysql.connector import Error


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "@ftd1218@",    
    "database": "newsblog_management"
}

def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        messagebox.showerror("DB Error", f"Could not connect:\n{e}")
        raise


def fetch_all_users():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users ORDER BY user_id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def fetch_user_by_id(user_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row

def add_user_to_db(username, email, age, contact, address):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username,email,age,contact_number,address) VALUES (%s,%s,%s,%s,%s)",
                (username,email,age,contact,address))
    conn.commit()
    cur.close()
    conn.close()

def update_user_in_db(user_id, username, email, age, contact, address):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET username=%s,email=%s,age=%s,contact_number=%s,address=%s WHERE user_id=%s",
                (username,email,age,contact,address,user_id))
    conn.commit()
    cur.close()
    conn.close()

def delete_user_from_db(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE user_id=%s", (user_id,))
    cur.execute("DELETE FROM news WHERE user_id=%s", (user_id,))
    conn.commit()
    cur.close()
    conn.close()

def fetch_news_by_user(user_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM news WHERE user_id=%s ORDER BY created_at DESC", (user_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def fetch_all_news():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM news ORDER BY created_at DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def add_news_to_db(title, body, user_id, username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO news (title,body,created_at,user_id,username) VALUES (%s,%s,NOW(),%s,%s)",
                (title,body,user_id,username))
    conn.commit()
    cur.close()
    conn.close()

def update_news_in_db(news_id, title, body):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE news SET title=%s,body=%s WHERE news_id=%s",(title,body,news_id))
    conn.commit()
    cur.close()
    conn.close()

def delete_news_from_db(news_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM news WHERE news_id=%s",(news_id,))
    conn.commit()
    cur.close()
    conn.close()

def search_news_db(keyword):
    kw = f"%{keyword}%"
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM news WHERE username LIKE %s OR title LIKE %s OR body LIKE %s ORDER BY created_at DESC",
                (kw,kw,kw))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


class UserDialog(simpledialog.Dialog):
    def __init__(self,parent,title,initial=None):
        self.initial=initial
        super().__init__(parent,title)
    def body(self,master):
        tk.Label(master,text="Username:").grid(row=0,column=0,sticky="e",padx=6,pady=6)
        tk.Label(master,text="Email:").grid(row=1,column=0,sticky="e",padx=6,pady=6)
        tk.Label(master,text="Age:").grid(row=2,column=0,sticky="e",padx=6,pady=6)
        tk.Label(master,text="Contact:").grid(row=3,column=0,sticky="e",padx=6,pady=6)
        tk.Label(master,text="Address:").grid(row=4,column=0,sticky="e",padx=6,pady=6)

        self.e_username=tk.Entry(master,width=35)
        self.e_email=tk.Entry(master,width=35)
        self.e_age=tk.Entry(master,width=35)
        self.e_contact=tk.Entry(master,width=35)
        self.e_address=tk.Entry(master,width=35)
        self.e_username.grid(row=0,column=1,padx=6,pady=6)
        self.e_email.grid(row=1,column=1,padx=6,pady=6)
        self.e_age.grid(row=2,column=1,padx=6,pady=6)
        self.e_contact.grid(row=3,column=1,padx=6,pady=6)
        self.e_address.grid(row=4,column=1,padx=6,pady=6)

        if self.initial:
            self.e_username.insert(0,self.initial.get("username",""))
            self.e_email.insert(0,self.initial.get("email",""))
            self.e_age.insert(0,self.initial.get("age",""))
            self.e_contact.insert(0,self.initial.get("contact_number",""))
            self.e_address.insert(0,self.initial.get("address",""))
        return self.e_username
    def apply(self):
        username=self.e_username.get().strip()
        email=self.e_email.get().strip()
        age=self.e_age.get().strip()
        contact=self.e_contact.get().strip()
        address=self.e_address.get().strip()
        self.result=(username,email,age,contact,address)

class NewsDialog(simpledialog.Dialog):
    def __init__(self,parent,title,initial=None):
        self.initial=initial
        super().__init__(parent,title)
    def body(self,master):
        tk.Label(master,text="Title:").grid(row=0,column=0,sticky="e",padx=6,pady=6)
        tk.Label(master,text="Body:").grid(row=1,column=0,sticky="ne",padx=6,pady=6)
        self.e_title=tk.Entry(master,width=50)
        self.e_body=tk.Text(master,width=50,height=10)
        self.e_title.grid(row=0,column=1,padx=6,pady=6)
        self.e_body.grid(row=1,column=1,padx=6,pady=6)
        if self.initial:
            self.e_title.insert(0,self.initial.get("title",""))
            self.e_body.insert("1.0",self.initial.get("body",""))
        return self.e_title
    def apply(self):
        title=self.e_title.get().strip()
        body=self.e_body.get("1.0","end").strip()
        self.result=(title,body)


class NewsApp:
    def __init__(self, root):
        self.root = root
        root.title("News Blog Management System")
        root.geometry("1100x650")
        root.configure(bg="white")
        self.selected_user_id = None

        # Left frame (Users)
        left_frame = tk.Frame(root, bg="white", padx=10, pady=10)
        left_frame.pack(side="left", fill="y")
        tk.Label(left_frame, text="Users", font=("Arial",14,"bold"), bg="white").pack(pady=(0,6))
        self.user_tree = ttk.Treeview(left_frame, columns=("id","username","email"), show="headings", height=25)
        self.user_tree.heading("id", text="ID")
        self.user_tree.heading("username", text="Username")
        self.user_tree.heading("email", text="Email")
        self.user_tree.column("id", width=40, anchor="center")
        self.user_tree.column("username", width=120)
        self.user_tree.column("email", width=140)
        self.user_tree.pack()
        self.user_tree.bind("<<TreeviewSelect>>", self.on_user_select)
        ubtns = tk.Frame(left_frame, bg="white")
        ubtns.pack(pady=8)
        tk.Button(ubtns,text="Add User", width=12,bg="gray",fg="white",command=self.open_add_user).grid(row=0,column=0,padx=4)
        tk.Button(ubtns,text="Edit User", width=12,bg="gray",fg="white",command=self.open_edit_user).grid(row=0,column=1,padx=4)
        tk.Button(ubtns,text="Delete User", width=12,bg="gray",fg="white",command=self.delete_selected_user).grid(row=0,column=2,padx=4)

        # Top frame (Search)
        center_frame = tk.Frame(root, bg="white", pady=6)
        center_frame.pack(side="top", fill="x")
        tk.Label(center_frame, text="Search (Username/Title/Body):", bg="white").pack(side="left")
        self.search_entry = tk.Entry(center_frame,width=50)
        self.search_entry.pack(side="left", padx=6)
        tk.Button(center_frame,text="Search",bg="gray",fg="white",command=self.do_search).pack(side="left", padx=4)
        tk.Button(center_frame,text="Clear Search",bg="gray",fg="white",command=self.load_users_and_news).pack(side="left", padx=4)
        tk.Button(center_frame,text="Show All News",bg="gray",fg="white",command=self.load_all_news).pack(side="left", padx=6)

        # Right frame (News)
        right_frame = tk.Frame(root,bg="white",padx=10,pady=10)
        right_frame.pack(side="right", fill="both", expand=True)
        tk.Label(right_frame,text="News",font=("Arial",14,"bold"),bg="white").pack(anchor="w")
        self.news_text = tk.Text(right_frame,wrap="word",state="normal",font=("Arial",11),bg="white")
        self.news_text.pack(fill="both", expand=True)
        self.news_text.tag_configure("title", font=("Arial",12,"bold"))
        self.news_text.tag_configure("meta", font=("Arial",9,"italic"), foreground="black")
        self.news_text.tag_configure("sep", foreground="gray")
        nbtns = tk.Frame(right_frame,bg="white")
        nbtns.pack(pady=6, anchor="e")
        tk.Button(nbtns,text="Add News",bg="gray",fg="white",width=12,command=self.open_add_news).grid(row=0,column=0,padx=4)
        tk.Button(nbtns,text="Update News",bg="gray",fg="white",width=12,command=self.update_news).grid(row=0,column=1,padx=4)
        tk.Button(nbtns,text="Delete News",bg="gray",fg="white",width=12,command=self.delete_news).grid(row=0,column=2,padx=4)

        # Status bar
        self.status = tk.Label(root,text="",anchor="w",bg="white")
        self.status.pack(side="bottom",fill="x")
        self.load_users_and_news()

    # --- User & News Loading ---
    def load_users(self):
        self.user_tree.delete(*self.user_tree.get_children())
        users = fetch_all_users()
        for u in users:
            self.user_tree.insert("", "end", values=(u["user_id"],u["username"],u["email"]))
        self.status.config(text=f"{len(users)} users loaded")

    def load_news_for_user(self,user_id):
        self.news_text.config(state="normal")
        self.news_text.delete("1.0","end")
        rows = fetch_news_by_user(user_id)
        if not rows:
            self.news_text.insert("end","No news for this user.\n")
            self.news_text.config(state="disabled")
            return
        for r in rows:
            self.news_text.insert("end",f"{r['title']}\n","title")
            meta=f"By: {r.get('username','')}   ID:{r['news_id']}   At:{r['created_at']}\n"
            self.news_text.insert("end",meta,"meta")
            self.news_text.insert("end",f"{r['body']}\n")
            self.news_text.insert("end","-"*80+"\n","sep")
        self.news_text.config(state="disabled")
        self.status.config(text=f"{len(rows)} news shown for user {user_id}")

    def load_all_news(self):
        self.news_text.config(state="normal")
        self.news_text.delete("1.0","end")
        rows = fetch_all_news()
        if not rows:
            self.news_text.insert("end","No news found.\n")
            self.news_text.config(state="disabled")
            return
        for r in rows:
            self.news_text.insert("end",f"{r['title']}\n","title")
            meta=f"By: {r.get('username','')}   ID:{r['news_id']}   At:{r['created_at']}\n"
            self.news_text.insert("end",meta,"meta")
            self.news_text.insert("end",f"{r['body']}\n")
            self.news_text.insert("end","-"*80+"\n","sep")
        self.news_text.config(state="disabled")
        self.status.config(text=f"{len(rows)} total news shown")

    def load_users_and_news(self):
        self.load_users()
        self.news_text.config(state="normal")
        self.news_text.delete("1.0","end")
        self.news_text.insert("end","Select a user from left or click 'Show All News'.\n")
        self.news_text.config(state="disabled")
        self.selected_user_id = None

    # --- User Selection ---
    def on_user_select(self,event):
        sel = self.user_tree.selection()
        if not sel: return
        item = self.user_tree.item(sel[0])["values"]
        self.selected_user_id = item[0]
        self.load_news_for_user(self.selected_user_id)

    # --- User Actions ---
    def open_add_user(self):
        d = UserDialog(self.root,"Add User")
        if d.result:
            username,email,age,contact,address = d.result
            try:
                add_user_to_db(username,email,age,contact,address)
                messagebox.showinfo("Success","User added.")
                self.load_users()
            except Error as e:
                messagebox.showerror("Error",f"Could not add user:\n{e}")

    def open_edit_user(self):
        if not self.selected_user_id:
            messagebox.showwarning("Select user","Select a user to edit.")
            return
        user = fetch_user_by_id(self.selected_user_id)
        if not user:
            messagebox.showerror("Error","User not found.")
            return
        d = UserDialog(self.root,"Edit User",initial=user)
        if d.result:
            username,email,age,contact,address = d.result
            try:
                update_user_in_db(self.selected_user_id,username,email,age,contact,address)
                messagebox.showinfo("Success","User updated.")
                self.load_users()
            except Error as e:
                messagebox.showerror("Error",f"Could not update user:\n{e}")

    def delete_selected_user(self):
        if not self.selected_user_id:
            messagebox.showwarning("Select user","Select a user to delete.")
            return
        if not messagebox.askyesno("Confirm","Delete selected user and all their news?"):
            return
        try:
            delete_user_from_db(self.selected_user_id)
            messagebox.showinfo("Success","User deleted.")
            self.load_users_and_news()
        except Error as e:
            messagebox.showerror("Error",f"Deletion failed:\n{e}")

    # --- News Actions ---
    def open_add_news(self):
        if not self.selected_user_id:
            messagebox.showwarning("Select user","Select a user first.")
            return
        user = fetch_user_by_id(self.selected_user_id)
        if not user: return
        username=user["username"]
        d = NewsDialog(self.root,"Add News")
        if d.result:
            title,body = d.result
            try:
                add_news_to_db(title,body,self.selected_user_id,username)
                messagebox.showinfo("Success","News added.")
                self.load_news_for_user(self.selected_user_id)
            except Error as e:
                messagebox.showerror("Error",f"Could not add news:\n{e}")

    def delete_news(self):
        nid = simpledialog.askinteger("Delete News", "Enter news_id to delete:")
        if not nid: return
        if not messagebox.askyesno("Confirm", "Delete this news?"): return
        try:
            delete_news_from_db(nid)
            messagebox.showinfo("Success", "News deleted.")
            if self.selected_user_id:
                self.load_news_for_user(self.selected_user_id)
            else:
                self.load_all_news()
        except Error as e:
            messagebox.showerror("Error", f"Could not delete news:\n{e}")

    def update_news(self):
        # Get news_id from cursor line
        try:
            index = self.news_text.index("insert")
            line = self.news_text.get(f"{index} linestart", f"{index} lineend").strip()
            if "ID:" not in line:
                messagebox.showwarning("Select News", "Place cursor on the news ID line to update.")
                return
            nid = int(line.split("ID:")[1].split()[0])
        except Exception:
            messagebox.showwarning("Select News", "Could not detect news ID. Place cursor on the ID line.")
            return

        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM news WHERE news_id=%s",(nid,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if not row:
            messagebox.showerror("Error","News not found")
            return

        d = NewsDialog(self.root,"Update News",initial=row)
        if d.result:
            title, body = d.result
            try:
                update_news_in_db(nid, title, body)
                messagebox.showinfo("Success","News updated.")
                if self.selected_user_id:
                    self.load_news_for_user(self.selected_user_id)
                else:
                    self.load_all_news()
            except Error as e:
                messagebox.showerror("Error", f"Could not update news:\n{e}")

    # --- Search ---
    def do_search(self):
        keyword=self.search_entry.get().strip()
        if not keyword:
            messagebox.showwarning("Enter keyword","Enter search keyword")
            return
        rows=search_news_db(keyword)
        self.news_text.config(state="normal")
        self.news_text.delete("1.0","end")
        if not rows:
            self.news_text.insert("end","No results found.\n")
            self.news_text.config(state="disabled")
            return
        for r in rows:
            self.news_text.insert("end",f"{r['title']}\n","title")
            meta=f"By: {r.get('username','')}   ID:{r['news_id']}   At:{r['created_at']}\n"
            self.news_text.insert("end",meta,"meta")
            self.news_text.insert("end",f"{r['body']}\n")
            self.news_text.insert("end","-"*80+"\n","sep")
        self.news_text.config(state="disabled")
        self.status.config(text=f"{len(rows)} search results")


if __name__=="__main__":
    root = tk.Tk()
    app = NewsApp(root)
    root.mainloop()
