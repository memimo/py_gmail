import imaplib
import getpass

class gmail_imap:


    def __init__ (self, username, password):

        self.imap_server = imaplib.IMAP4_SSL("imap.gmail.com",993)
        self.username = username
        self.password = password
        self.loggedIn = False
        self.labels = []

        self.messages = Messages(self)

    def login (self):
        try:
            self.imap_server.login(self.username,self.password)
        except:
            raise Exception, 'Problem loging in'

        self.loggedIn = True


    def logout (self):

        self.imap_server.close()
        self.imap_server.logout()
        self.loggedIn = False

    def get_lables(self):

        if(not self.loggedIn):
            self.login()

        for box in self.imap_server.list()[1]:
            name = box.split(' "/" ')[1][1:-1]
            if( name != "[Gmail]"):  #ignore global [Gmail] mailbox
                self.labels.append(name)

    def get_csv(self, labels, limit = 2):

        out_f = open('out.csv', 'w')
        for label in labels:
            self.messages.get_msg(label, limit)
            for msg in self.messages.messages:
                out_f.write(label + ', ' + msg + '\n')

        out_f.close()

class Messages:
    def __init__(self, server):
        self.server = server
        self.label = None
        self.messages = []


    def get_msg(self, label, limit):
        typ, data = self.server.imap_server.select(label)
        if typ != 'OK':
            raise Exception, typ

        typ, data = self.server.imap_server.search(None, 'ALL')
        msg_lst = data[0].split()[-limit:]
        for msg in msg_lst:
            typ, data = self.server.imap_server.fetch(msg, '(UID BODY[TEXT])')
            self.messages.append(self.__clean_msg(data[0][1]))


    def __clean_msg(self, msg):

        msg = msg.replace('\r', ' ')
        msg = msg.replace('\n', ' ')
        msg = msg.replace('\t', ' ')
        msg = msg.replace(',', ' ')
        return msg

if __name__ == '__main__':

    username = 'memirzamo@gmail.com'
    gmail = gmail_imap(username, getpass.getpass())
    gmail.login()
    gmail.get_csv(['Links', 'IDSS'])
