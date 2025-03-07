from tkinter import *
from mydb import Database
from myapi import api
from tkinter import messagebox #to desplay print on screen like alert
class NLPApp:
    def __init__(self):
        #create api object
        self.apio = api()
        #create database object
        self.dbo = Database()
        #load gui login
        self.root = Tk()
        self.root.title('NLPApp')
        self.root.iconbitmap('rescoures/favicon.ico')
        self.root.geometry('350x600')
        self.root.configure(bg='#34495E')
        self.login_gui()

        self.root.mainloop()

    def login_gui(self):
        #label class take two parameter -> self.root,text
        self.clear()
        heading = Label(self.root,text='NLPApp',bg='#34495E',fg='white')
        heading.pack(pady=(30,30))
        heading.configure(font=('verdana',24,'bold'))

        label1 = Label(self.root,text='Enter Email')
        label1.pack(pady=(10,10))

        self.email_input = Entry(self.root, width=50)
        self.email_input.pack(pady=(5, 10), ipady=4)

        label2 = Label(self.root,text="Enter Password")
        label2.pack(pady=(10,10))

        self.password_input = Entry(self.root,width=50,show='*')
        self.password_input.pack(pady=(5,10),ipady=4) #ipady = internal padding

        login_btn = Button(self.root,text='Login',command=self.perform_login)
        login_btn.pack(pady=(10,10))

        label3 = Label(self.root,text='Not a member ?')
        label3.pack(pady=(20,10))

        redirect_btn = Button(self.root,text='Register Now',command=self.register_gui)
        redirect_btn.pack(pady=(10,10))

    def clear(self):
        for i in self.root.pack_slaves():
            i.destroy()

    def register_gui(self):
        self.clear()
        heading = Label(self.root, text='NLPApp', bg='#34495E', fg='white')
        heading.pack(pady=(30, 30))
        heading.configure(font=('verdana', 24, 'bold'))

        label0 = Label(self.root, text='Enter Name')
        label0.pack(pady=(10, 10))

        self.name_input = Entry(self.root, width=50)
        self.name_input.pack(pady=(5, 10), ipady=4)

        label1 = Label(self.root, text='Enter Email')
        label1.pack(pady=(10, 10))

        self.email_input = Entry(self.root, width=50)
        self.email_input.pack(pady=(5, 10), ipady=4)

        label2 = Label(self.root, text='Enter Password')
        label2.pack(pady=(10, 10))

        self.password_input = Entry(self.root, width=50,show='*')
        self.password_input.pack(pady=(5, 10), ipady=4)

        register_btn = Button(self.root,text="Register",width='25',command=self.perform_registration)
        register_btn.pack(pady=(10,10),ipady=4)

        label3 = Label(self.root, text='Already a member?')
        label3.pack(pady=(20, 10))

        redirect_btn = Button(self.root,text='Login Now',command=self.login_gui)
        redirect_btn.pack(pady=(5, 10), ipady=4)

    def perform_registration(self):
        name = self.name_input.get()
        email = self.email_input.get()
        password = self.password_input.get()
        response = self.dbo.add_data(name,email,password)

        if response:
            messagebox.showinfo('success','Registration successful! you can login now')
        else:
            messagebox.showerror('Error','Email already exists')

    def perform_login(self):

        email = self.email_input.get()
        password = self.password_input.get()

        response = self.dbo.search(email,password)
        if response:
            messagebox.showinfo('success','Login successful')
            self.home_gui()
        else:
            messagebox.showerror('Error','Incorrect email/password')

    def home_gui(self):
        self.clear()

        heading = Label(self.root, text='NLPApp', bg='#34495E', fg='white')
        heading.pack(pady=(30, 30))
        heading.configure(font=('verdana', 24, 'bold'))

        sentiment_btn = Button(self.root, text="Sentiment Analysis", width='30',height=4, command=self.sentiment_gui)
        sentiment_btn.pack(pady=(10, 10), ipady=4)

        entity_btn = Button(self.root, text="Entity Analysis", width='30', height=4,
                               command=self.entity_gui)
        entity_btn.pack(pady=(10, 10), ipady=4)

        relationship_btn = Button(self.root, text="Relationship Analysis", width='30', height=4,
                               command=self.relationship_gui)
        relationship_btn.pack(pady=(10, 10), ipady=4)

    def sentiment_gui(self):
        self.clear()
        heading = Label(self.root, text='NLPApp', bg='#34495E', fg='white')
        heading.pack(pady=(30, 30))
        heading.configure(font=('verdana', 24, 'bold'))

        heading2 = Label(self.root, text='Sentiment Analysis', bg='#34495E', fg='white')
        heading2.pack(pady=(10, 20))
        heading2.configure(font=('verdana', 24))

        label1 = Label(self.root, text='Enter the text')
        label1.pack(pady=(10, 10))

        self.sentiment_input = Entry(self.root, width=50)
        self.sentiment_input.pack(pady=(5, 10), ipady=4)

        sentiment_btn = Button(self.root, text="Analysis Sentiment", width='25', command=self.do_sentiment_analys)
        sentiment_btn.pack(pady=(10, 10), ipady=4)

        self.sentiment_result = Label(self.root, text='',bg='#34495E', fg='white')
        self.sentiment_result.pack(pady=(10, 10))
        self.sentiment_result.configure(font=('verdana', 16))

        go_back_btn =Button(self.root, text="Go Back", width='10', command=self.home_gui)
        go_back_btn.pack(pady=(10, 10), ipady=4)

    def do_sentiment_analys(self):
        # Get text from input
        text = self.sentiment_input.get()

        # Check if input is empty
        if not text.strip():
            self.sentiment_result.config(text="Please enter some text!", fg='red')
            return

        # Call API
        if self.apio.analyze_text(text):
            # Get sentiment result
            sentiment = self.apio.get_sentiment()

            # Set appropriate color based on sentiment
            color = '#2ECC71'  # Green for positive
            if sentiment.lower() == 'negative':
                color = '#E74C3C'  # Red for negative
            elif sentiment.lower() == 'neutral':
                color = '#F1C40F'  # Yellow for neutral

            # Update result label
            self.sentiment_result.config(
                text=f"Sentiment: {sentiment.capitalize()}",
                fg=color
            )
        else:
            self.sentiment_result.config(
                text="Error analyzing sentiment!",
                fg='red'
            )



    # Entity-----------------------------------

    def entity_gui(self):
        self.clear()
        heading = Label(self.root, text='NLPApp', bg='#34495E', fg='white')
        heading.pack(pady=(30, 30))
        heading.configure(font=('verdana', 24, 'bold'))

        heading2 = Label(self.root, text='Entity Analysis', bg='#34495E', fg='white')
        heading2.pack(pady=(10, 20))
        heading2.configure(font=('verdana', 24))

        label1 = Label(self.root, text='Enter the text')
        label1.pack(pady=(10, 10))

        self.entity_input = Entry(self.root, width=50)
        self.entity_input.pack(pady=(5, 10), ipady=4)

        entity_btn = Button(self.root, text="Analysis Sentiment", width='25', command=self.do_entity_analysis)
        entity_btn.pack(pady=(10, 10), ipady=4)

        self.entity_result = Label(self.root, text='',bg='#34495E', fg='white')
        self.entity_result.pack(pady=(10, 10))
        self.entity_result.configure(font=('verdana', 11))

        go_back_btn =Button(self.root, text="Go Back", width='10', command=self.home_gui)
        go_back_btn.pack(pady=(10, 10), ipady=4)

    def do_entity_analysis(self):
        text = self.entity_input.get()

        if not text.strip():
            self.entity_result.config(text="Please enter some text!", fg='red')
            return

        if self.apio.analyze_text(text):
            entities = self.apio.get_entities()

            if entities:
                # Proper tuple unpacking
                entity_list = "\n".join([f"{name} ({etype})" for name, etype in entities])
                self.entity_result.config(
                    text=f"Entities:\n{entity_list}",
                    fg='white'
                )
            else:
                self.entity_result.config(
                    text="No entities found",
                    fg='#F1C40F'  # Yellow
                )
        else:
            self.entity_result.config(
                text="Error analyzing entities!",
                fg='red'
            )

#Relationship-----------------------

    def relationship_gui(self):
        self.clear()
        heading = Label(self.root, text='NLPApp', bg='#34495E', fg='white')
        heading.pack(pady=(30, 30))
        heading.configure(font=('verdana', 24, 'bold'))

        heading2 = Label(self.root, text='Relationship Analysis', bg='#34495E', fg='white')
        heading2.pack(pady=(10, 20))
        heading2.configure(font=('verdana', 24))

        label1 = Label(self.root, text='Enter the text')
        label1.pack(pady=(10, 10))

        self.relationship_input = Entry(self.root, width=50)
        self.relationship_input.pack(pady=(5, 10), ipady=4)

        relationship_btn = Button(self.root, text="Relationship Sentiment", width='25',
                               command=self.do_relationship_analys)
        relationship_btn.pack(pady=(10, 10), ipady=4)

        self.relationship_result = Label(self.root, text='', bg='#34495E', fg='white')
        self.relationship_result.pack(pady=(10, 10))
        self.relationship_result.configure(font=('verdana', 12))

        go_back_btn = Button(self.root, text="Go Back", width='10', command=self.home_gui)
        go_back_btn.pack(pady=(10, 10), ipady=4)

    def do_relationship_analys(self):
        # Get text from input
        text = self.relationship_input.get()

        # Check if input is empty
        if not text.strip():
            self.relationship_result.config(text="Please enter some text!", fg='red')
            return

        # Call API
        if self.apio.analyze_text(text):
            # Get relationship result
            relationships = self.apio.get_relationships()

            if relationships:
                # Format relationships list
                relationship_list = "\n".join(relationships)
                self.relationship_result.config(
                    text=f"Relationships:\n{relationship_list}",
                    fg='white'
                )
            else:
                self.relationship_result.config(
                    text="No relationships found",
                    fg='#F1C40F'  # Yellow for warning
                )
        else:
            self.relationship_result.config(
                text="Error analyzing relationships!",
                fg='red'
            )

npl = NLPApp()