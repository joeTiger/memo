# memo
MEMOrize all your ubuntu command lines and share them with colleagues. a powerful python history tool...

### **Download**
download the **memo_1.0.XX.tar.gz** file
(anywhere you want...people generaly use folder  **~/Download**)

### **UnZip**
`tar -xvf memo_1.0.XX.tar.gz`

### **Installation**
1. `cd  memo_1.0.XX`
2. `. remove_memo.sh `(remove previous version)
3. `. install_memo.sh`

### **Setup**
During installation you will get this question
**Please enter your email or enter for default:**
- if you want to share your command lines with colleagues enter your **cie** email
- if you **don't** want to share your command lines with collegues enter your **private** email
- the default email is generally the **cie** email, if you have a doubt enter your **cie** email

An alias **memo** is created which allow to call it anywhere from any terminal

### **Usage**

- `memo` will display all history from all your console terminals
- `memo [pattern]` will diplsay all your history containing this pattern, for example `memo ls`
- `memo [n]` will execute the index command line - Refer to command line n, for example `memo 5`
- `memo [pattern] [-e email]` will display history of your colleague identified by email, for example `memo ls -e scott.tiger@cisco.com` will display all command lines of **scott**

