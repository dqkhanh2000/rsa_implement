from posixpath import expanduser
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from rsa import generate_keypair, decrypt, encrypt
from md5 import MD5

class chukyso(QWidget):

    def __init__(self):
        super().__init__()
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.height = 300
        self.width = 1000

        sshFile="style.css"
        with open(sshFile,"r") as fh:
            self.setStyleSheet(fh.read())

        self.title = 'Chukyso'
        self.left = 20
        self.top = 40
        self.initUI()
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    ################encrypt##############3
        lbl_encrypt = QLabel("Encrypt",self)
        self.cbb_encrypt_type = QComboBox()
        self.cbb_encrypt_type.addItems(["Text", "File"])
        self.cbb_encrypt_type.currentIndexChanged.connect(self.choose_options_encrypt)

        hbox_encrypt = QHBoxLayout()
        hbox_encrypt.addWidget(lbl_encrypt,7)
        hbox_encrypt.addWidget(self.cbb_encrypt_type,3)

        self.qpte_encrypt = QPlainTextEdit(self)
        self.qpte_encrypt.setObjectName("qpteText")

        self.btn_choose_file_encrypt = QPushButton("Select file",self)
        self.btn_choose_file_encrypt.hide()
        self.btn_choose_file_encrypt.clicked.connect(self.choose_file_encrypt)

        self.qle_file_path_encrypt =QLineEdit(self)
        self.qle_file_path_encrypt.hide()

        hbox_choose_path_encrypt = QHBoxLayout()
        hbox_choose_path_encrypt.addWidget(self.btn_choose_file_encrypt,1)
        hbox_choose_path_encrypt.addWidget(self.qle_file_path_encrypt,9)

        self.btn_sign = QPushButton("Sign",self)
        self.btn_sign.clicked.connect(self.click_sign)
        hbox_btn_sign = QHBoxLayout()
        hbox_btn_sign.addStretch(1)
        hbox_btn_sign.addWidget(self.btn_sign,1)
        hbox_btn_sign.addStretch(1)

        lbl_md5_encrypt = QLabel("Md5", self)
        self.qle_md5_encrypt = QLineEdit(self)
        self.qle_md5_encrypt.setReadOnly(True)
        hbox_md5_encrypt = QHBoxLayout()
        hbox_md5_encrypt.addWidget(lbl_md5_encrypt,1)
        hbox_md5_encrypt.addWidget(self.qle_md5_encrypt,9)

        lbl_hash_encrypt = QLabel("Hash", self)
        self.qpte_hash_encrypt = QPlainTextEdit(self)
        self.qpte_hash_encrypt.setReadOnly(True)
        hbox_hash_encrypt = QHBoxLayout()
        hbox_hash_encrypt.addWidget(lbl_hash_encrypt,1)
        hbox_hash_encrypt.addWidget(self.qpte_hash_encrypt,9)

        line_horizontal_bottom =QLabel(self)
        line_horizontal_bottom.setStyleSheet("border-top : 1px solid #c1c1c1;")

        lbl_private_key = QLabel("Private key", self)
        self.qpte_private_key = QPlainTextEdit(self)
        self.qpte_private_key.setObjectName("qpteKey")
        self.qpte_private_key.setReadOnly(True)
        hbox_private_key = QHBoxLayout()
        hbox_private_key.addWidget(lbl_private_key,1)
        hbox_private_key.addWidget(self.qpte_private_key,9)

        lbl_public_key = QLabel("Public key", self)
        self.qpte_public_key = QPlainTextEdit(self)
        self.qpte_public_key.setObjectName("qpteKey")
        self.qpte_public_key.setReadOnly(True)
        hbox_public_key = QHBoxLayout()
        hbox_public_key.addWidget(lbl_public_key,1)
        hbox_public_key.addWidget(self.qpte_public_key, 9)

        self.btn_generatekey = QPushButton("Generate key", self)
        self.btn_generatekey.clicked.connect(self.click_generatekey)
        hbox_btn_generatekey = QHBoxLayout()
        hbox_btn_generatekey.addStretch(1)
        hbox_btn_generatekey.addWidget(self.btn_generatekey, 1)
        hbox_btn_generatekey.addStretch(1)

        vbox_encrypt = QVBoxLayout()
        vbox_encrypt.addLayout(hbox_encrypt,1)
        vbox_encrypt.addWidget(self.qpte_encrypt, 3)
        vbox_encrypt.addLayout(hbox_choose_path_encrypt,1)
        vbox_encrypt.addLayout(hbox_btn_sign,1)
        vbox_encrypt.addLayout(hbox_md5_encrypt,1)
        vbox_encrypt.addLayout(hbox_hash_encrypt,1)
        vbox_encrypt.addWidget(line_horizontal_bottom,1)
        vbox_encrypt.addLayout(hbox_private_key,1)
        vbox_encrypt.addLayout(hbox_public_key,1)
        vbox_encrypt.addLayout(hbox_btn_generatekey,1)
        vbox_encrypt.addStretch(3)

    ###################### Decrypt#######################

        lbl_decrypt = QLabel("Decrypt", self)
        self.cbb_decrypt_type = QComboBox()
        self.cbb_decrypt_type.addItems(["Text", "File"])
        self.cbb_decrypt_type.currentIndexChanged.connect(self.chage_options_decrypt)

        hbox_decrypt = QHBoxLayout()
        hbox_decrypt.addWidget(lbl_decrypt, 7)
        hbox_decrypt.addWidget(self.cbb_decrypt_type, 3)

        self.qpte_decrypt = QPlainTextEdit(self)
        self.qpte_decrypt.setObjectName("qpteText")

        self.btn_choose_file_decrypt = QPushButton("Select file", self)
        self.btn_choose_file_decrypt.hide()
        self.btn_choose_file_decrypt.clicked.connect(self.choose_file_decrypt)

        self.qle_file_path_decrypt = QLineEdit(self)
        self.qle_file_path_decrypt.hide()

        hbox_choose_path_decrypt = QHBoxLayout()
        hbox_choose_path_decrypt.addWidget(self.btn_choose_file_decrypt, 1)
        hbox_choose_path_decrypt.addWidget(self.qle_file_path_decrypt, 9)

        self.btn_check = QPushButton("Check", self)
        self.btn_check.clicked.connect(self.click_check)
        hbox_btn_check = QHBoxLayout()
        hbox_btn_check.addStretch(1)
        hbox_btn_check.addWidget(self.btn_check, 1)
        hbox_btn_check.addStretch(1)

        lbl_key_decrypt = QLabel("Key", self)
        self.qpte_key_decrypt = QPlainTextEdit(self)
        self.qpte_key_decrypt.setObjectName("qpteKey")

        hbox_key_decrypt = QHBoxLayout()
        hbox_key_decrypt.addWidget(lbl_key_decrypt, 1)
        hbox_key_decrypt.addWidget(self.qpte_key_decrypt, 9)

        lbl_hash_decrypt = QLabel("Hash", self)
        self.qpte_hash_decrypt = QPlainTextEdit(self)
        self.qpte_hash_decrypt.setObjectName("qpteKey")

        hbox_hash_decrypt = QHBoxLayout()
        hbox_hash_decrypt.addWidget(lbl_hash_decrypt, 1)
        hbox_hash_decrypt.addWidget(self.qpte_hash_decrypt, 9)

        lbl_md5_file_decrypt = QLabel("Md5 from text", self)
        self.qpte_md5_file_decrypt = QPlainTextEdit(self)
        self.qpte_md5_file_decrypt.setReadOnly(True)
        self.qpte_md5_file_decrypt.setObjectName("qpteKey")

        hbox_md5_file_decrypt = QHBoxLayout()
        hbox_md5_file_decrypt.addWidget(lbl_md5_file_decrypt, 1)
        hbox_md5_file_decrypt.addWidget(self.qpte_md5_file_decrypt, 9)

        lbl_md5_decrypt = QLabel("Md5 decrypt", self)
        self.qpte_md5_decrypt = QPlainTextEdit(self)
        self.qpte_md5_decrypt.setReadOnly(True)
        self.qpte_md5_decrypt.setObjectName("qpteKey")

        hbox_md5_decrypt = QHBoxLayout()
        hbox_md5_decrypt.addWidget(lbl_md5_decrypt, 1)
        hbox_md5_decrypt.addWidget(self.qpte_md5_decrypt, 9)

        lbl_result_decrypt = QLabel("Result",self)
        self.qle_result_decrypt = QLineEdit(self)
        self.qle_result_decrypt.setReadOnly(True)

        hbox_result_decrypt = QHBoxLayout()
        hbox_result_decrypt.addWidget(lbl_result_decrypt, 1)
        hbox_result_decrypt.addWidget(self.qle_result_decrypt, 9)

        vbox_decrypt= QVBoxLayout()
        vbox_decrypt.addLayout(hbox_decrypt,1)
        vbox_decrypt.addWidget(self.qpte_decrypt,3)
        vbox_decrypt.addLayout(hbox_choose_path_decrypt,1)
        vbox_decrypt.addLayout(hbox_key_decrypt,1)
        vbox_decrypt.addLayout(hbox_hash_decrypt,1)
        vbox_decrypt.addLayout(hbox_btn_check,1)
        vbox_decrypt.addLayout(hbox_md5_file_decrypt,1)
        vbox_decrypt.addLayout(hbox_md5_decrypt,1)
        vbox_decrypt.addLayout(hbox_result_decrypt,1)
        vbox_encrypt.addStretch(3)

        line_vertical =QLabel(self)
        line_vertical.setStyleSheet("border-right : 1px solid #c1c1c1;")

        hbox = QHBoxLayout()
        hbox.addLayout(vbox_encrypt)
        hbox.addWidget(line_vertical)
        hbox.addLayout(vbox_decrypt)


        self.setLayout(hbox)
        self.show()
    
    def choose_options_encrypt(self,value):
        value = self.cbb_encrypt_type.currentText()
        if value == "File" :
            self.btn_choose_file_encrypt.show()
            self.qle_file_path_encrypt.show()
            self.qpte_encrypt.hide()
        else:
            self.btn_choose_file_encrypt.hide()
            self.qle_file_path_encrypt.hide()
            self.qpte_encrypt.show()

    def chage_options_decrypt(self,value):
        value = self.cbb_decrypt_type.currentText()
        if value == "File" :
            self.btn_choose_file_decrypt.show()
            self.qle_file_path_decrypt.show()
            self.qpte_decrypt.hide()
        else:
            self.btn_choose_file_decrypt.hide()
            self.qle_file_path_decrypt.hide()
            self.qpte_decrypt.show()
    
    def choose_file_encrypt(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', expanduser("~"), "Select files (*.*)")
        if len(fname[0]) == 0:
            return
        self.qle_file_path_encrypt.setText(fname[0])

    def choose_file_decrypt(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', expanduser("~"), "Select files (*.*)")
        if len(fname[0]) == 0:
            return
        self.qle_file_path_decrypt.setText(fname[0])

    def click_generatekey(self):
        public_key, self.private_key = generate_keypair()
        self.qpte_public_key.setPlainText(str(public_key))
        self.qpte_private_key.setPlainText(str(self.private_key))
    
    def click_sign(self):
        md5 = MD5()
        md5_text = None
        if not hasattr(self, "private_key"):
                self.click_generatekey()
        if self.cbb_encrypt_type.currentIndex() == 0:
            plain_text = self.qpte_encrypt.toPlainText()
            if len(plain_text) == 0:
                plain_text = ''
            md5.hash(plain_text)
            
        else:
            if self.qle_file_path_encrypt.text() == '':
                self.choose_file_encrypt()
            md5.hash(self.qle_file_path_encrypt.text(), 'file')
        md5_text = md5.hexdigest()
        encrypt_signature = encrypt(self.private_key, md5_text)

        self.qle_md5_encrypt.setText(md5_text)
        self.qpte_hash_encrypt.setPlainText(encrypt_signature)
        
    def click_check(self):
        
        encrypt_text = self.qpte_hash_decrypt.toPlainText()
        public_key = self.qpte_key_decrypt.toPlainText()
        if public_key == '' or encrypt_text == '':
            return

        md5 = MD5()
        md5_text = None
        
        if self.cbb_decrypt_type.currentIndex() == 0:
            plain_input_text = self.qpte_decrypt.toPlainText()
            md5.hash(plain_input_text)
            
        else:
            if self.qle_file_path_decrypt.text() == '':
                self.choose_file_decrypt()
            md5.hash(self.qle_file_path_decrypt.text(), 'file')
        md5_text = md5.hexdigest()
        md5_decrypt = decrypt(eval(public_key), encrypt_text)

        self.qpte_md5_file_decrypt.setPlainText(md5_text)
        self.qpte_md5_decrypt.setPlainText(md5_decrypt)
        if md5_decrypt == md5_text:
            self.qle_result_decrypt.setText('Matched')
        else:
            self.qle_result_decrypt.setText('Mismatched')
